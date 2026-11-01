"""OpenAI-style, Foundry-style, vLLM and Ollama bounded HTTP contracts."""
from dataclasses import replace
from datetime import datetime, timezone
import json

import pytest
import requests

from llm.bounded_http import retry_after
from llm.inference import (
    InferenceAuthenticationError, InferenceConfigurationError, InferenceConnectionError,
    InferenceModelUnavailableError, InferenceOutputLimitError, InferenceRateLimitError,
    InferenceResponseError, InferenceTimeoutError, InferenceUsage, ModelRole,
)
from llm.openai_compatible import OpenAICompatibleProvider
from llm.ollama_client import OllamaClient
from llm.structured import CapabilityProfile, GenerationRequest


class Response:
    def __init__(self,value=None,*,status=200,headers=None,raw=None):
        self.raw=raw if raw is not None else json.dumps(value).encode()
        self.status_code=status; self.headers=headers or {}; self.closed=False
    def iter_content(self,chunk_size):
        for i in range(0,len(self.raw),chunk_size): yield self.raw[i:i+chunk_size]
    def close(self): self.closed=True


class HTTP:
    def __init__(self,response=None,error=None): self.response=response; self.error=error; self.calls=[]
    def post(self,*args,**kwargs):
        self.calls.append((args,kwargs))
        if self.error: raise self.error
        return self.response


def request(**cap_changes):
    cap=CapabilityProfile(version='explicit/1',context_tokens=16000,max_output_tokens=2000,
                          overhead_tokens=64,safety_tokens=100,**cap_changes)
    return GenerationRequest('Control','Untrusted',ModelRole.SUMMARIZATION,cap,500,1000,{'type':'object'},10)


def client(response=None,*,error=None,kind='vllm',key=None):
    http=HTTP(response,error)
    model_map={r.value:'served-alias' for r in ModelRole}
    if kind=='ollama':
        return OllamaClient(url='http://local.example/api/chat',model_map=model_map,http_client=http)
    base={'vllm':'http://external.example/v1','openai':'https://api.example/v1',
          'foundry':'https://managed.example/openai/v1'}[kind]
    return OpenAICompatibleProvider(base_url=base,model_map=model_map,api_key=key,http_client=http,
                                    generation_parameters={'temperature':1.8,'max_tokens':999999,'tools':[{}]})


def payload(**changes):
    result={'model':'served-alias','choices':[{'message':{'content':'{"value":1}'},'finish_reason':'stop'}],
            'usage':{'prompt_tokens':21,'completion_tokens':7,'total_tokens':28}}
    result.update(changes); return result


@pytest.mark.parametrize('kind',['vllm','openai','foundry'])
@pytest.mark.parametrize('mode',['prompt','json_object','json_schema'])
@pytest.mark.parametrize('usage',[True,False])
def test_protocol_success_roles_bounds_optional_usage(kind,mode,usage):
    value=payload()
    if not usage: value.pop('usage')
    response=Response(value); p=client(response,kind=kind,key='synthetic-credential')
    req=request(structured_output=mode,output_parameter='max_completion_tokens' if kind=='foundry' else 'max_tokens')
    result=p.execute(req)
    assert result.text=='{"value":1}' and result.served_model=='served-alias'
    assert result.usage==(InferenceUsage(21,7,28) if usage else None)
    args,kwargs=p.http_client.calls[0]
    assert args[0].endswith('/chat/completions')
    sent=kwargs['json']
    assert sent['messages']==[{'role':'system','content':'Control'},{'role':'user','content':'Untrusted'}]
    assert sent['model']=='served-alias' and sent['stream'] is False
    assert sent[req.capability.output_parameter]==500
    assert 'tools' not in sent and 'temperature' not in sent
    assert ('response_format' in sent)==(mode!='prompt')
    assert kwargs['headers']['Authorization']=='Bearer synthetic-credential'
    assert response.closed and len(p.http_client.calls)==1
    assert p.generation_parameters['max_tokens']==999999


def test_vllm_optional_auth_and_explicit_temperature():
    p=client(Response(payload()))
    p.execute(request(temperature=0))
    sent=p.http_client.calls[0][1]
    assert 'Authorization' not in sent['headers'] and sent['json']['temperature']==0


@pytest.mark.parametrize('status,error',[(429,InferenceRateLimitError),(401,InferenceAuthenticationError),
    (403,InferenceAuthenticationError),(400,InferenceConfigurationError),(422,InferenceConfigurationError),
    (404,InferenceModelUnavailableError),(500,InferenceConnectionError),(503,InferenceRateLimitError),
    (504,InferenceTimeoutError)])
def test_errors_are_sanitized_closed_and_not_retried(status,error):
    response=Response({'secret':'never expose raw body'},status=status,headers={'Retry-After':'77'})
    p=client(response)
    with pytest.raises(error) as caught: p.execute(request())
    assert 'secret' not in str(caught.value) and 'never expose' not in str(caught.value)
    if status in (429,503): assert caught.value.retry_after==77
    assert response.closed and len(p.http_client.calls)==1


@pytest.mark.parametrize('error,expected',[(requests.Timeout('private'),InferenceTimeoutError),
    (requests.ConnectionError('private'),InferenceConnectionError)])
def test_timeout_and_connection_unknown(error,expected):
    p=client(error=error)
    with pytest.raises(expected) as caught: p.execute(request())
    assert 'private' not in str(caught.value)


@pytest.mark.parametrize('value',[
    {}, {'choices':[]},payload(model='wrong-model'),payload(choices=[{'message':{'content':None}}]),
    payload(choices=[{'message':{'content':'{}'},'finish_reason':'tool_calls'}]),
])
def test_malformed_or_wrong_model(value):
    response=Response(value)
    with pytest.raises(InferenceResponseError): client(response).execute(request())
    assert response.closed


@pytest.mark.parametrize('raw',[b'{',b'{"choices":[],"choices":[]}',b'not-json'])
def test_invalid_transport_json(raw):
    with pytest.raises(InferenceResponseError): client(Response(raw=raw)).execute(request())


def test_returned_model_alias_allowlist():
    p=client(Response(payload(model='versioned-model')))
    assert p.execute(request(response_models=('versioned-model',))).served_model=='versioned-model'


@pytest.mark.parametrize('value',[
    payload(choices=[{'message':{'content':'{}'},'finish_reason':'length'}]),
    payload(choices=[{'message':{'content':'x'*1001},'finish_reason':'stop'}]),
])
def test_output_bounds(value):
    with pytest.raises(InferenceOutputLimitError): client(Response(value)).execute(request())


def test_raw_http_bound():
    response=Response(raw=b'x'*15000)
    with pytest.raises(InferenceOutputLimitError): client(response).execute(request())
    assert response.closed


def test_output_configuration_rejected_before_transport():
    p=client(Response(payload()))
    with pytest.raises(InferenceConfigurationError): p.execute(replace(request(),output_tokens=2001))
    assert not p.http_client.calls


def test_retry_after_date_and_invalid():
    now=datetime(2026,10,7,tzinfo=timezone.utc)
    assert retry_after({'Retry-After':'Wed, 07 Oct 2026 00:00:20 GMT'},now)==20
    for value in ('invalid','nan','inf'):
        assert retry_after({'Retry-After':value},now) is None


@pytest.mark.parametrize('mode',['prompt','json_object','json_schema'])
def test_ollama_additive_generation(mode):
    response=Response({'model':'served-alias','message':{'content':'{}'},'done':True,'done_reason':'stop',
                       'prompt_eval_count':4,'eval_count':2})
    p=client(response,kind='ollama')
    result=p.execute(request(structured_output=mode))
    assert result.text=='{}' and result.usage.prompt_tokens==4
    sent=p.http_client.calls[0][1]['json']
    assert sent['options']['num_predict']==500
    assert ('format' in sent)==(mode!='prompt') and response.closed


def test_length_failure_retains_reported_usage():
    value=payload(choices=[{'message':{'content':'{}'},'finish_reason':'length'}])
    with pytest.raises(InferenceOutputLimitError) as error: client(Response(value)).execute(request())
    assert error.value.usage==InferenceUsage(21,7,28)


def test_read_timeout_wrapped_by_requests_is_normalized():
    from urllib3.exceptions import ReadTimeoutError
    response=Response(payload())
    def broken(chunk_size):
        raise requests.ConnectionError(ReadTimeoutError(None,None,'private-detail'))
        yield b''
    response.iter_content=broken
    with pytest.raises(InferenceTimeoutError) as error: client(response).execute(request())
    assert 'private-detail' not in str(error.value) and response.closed


def test_slow_trickle_hits_deadline(monkeypatch):
    import llm.bounded_http as transport
    now=[0]
    monkeypatch.setattr(transport.time,'monotonic',lambda:now[0])
    response=Response(payload())
    def trickle(chunk_size):
        assert chunk_size==1
        for byte in response.raw:
            now[0]+=1
            yield bytes([byte])
    response.iter_content=trickle
    with pytest.raises(InferenceTimeoutError): client(response).execute(request())
    assert response.closed and now[0]==11


def test_very_long_retry_hint_is_not_discarded():
    assert retry_after({'Retry-After':'999999999'})==604800


def test_explicit_bounded_reasoning_effort_and_inclusive_usage():
    value = payload(model='gpt-5.4-mini-2026-03-17', usage={'prompt_tokens':21,
        'completion_tokens':40, 'total_tokens':61, 'completion_tokens_details':{'reasoning_tokens':35}})
    p = client(Response(value), kind='foundry')
    req = request(reasoning_effort='low', output_parameter='max_completion_tokens',
                  structured_output='json_object', response_models=('gpt-5.4-mini-2026-03-17',))
    result = p.execute(req)
    sent = p.http_client.calls[0][1]['json']
    assert sent['reasoning_effort'] == 'low'
    assert sent['max_completion_tokens'] == req.output_tokens
    assert 'max_tokens' not in sent and 'temperature' not in sent and 'top_p' not in sent
    assert sent['response_format'] == {'type':'json_object'}
    assert result.usage == InferenceUsage(21, 40, 61)  # Reasoning is already included, never added twice.


def test_unset_reasoning_preserves_legacy_serialization_and_fingerprint():
    from documents.jobs.models import fingerprint
    cap = request().capability
    legacy = dict(version='explicit/1', context_tokens=16000, max_output_tokens=2000,
        overhead_tokens=64, safety_tokens=100, structured_output='prompt', output_parameter='max_tokens',
        streaming=True, usage_reporting=False, temperature=None, response_models=[])
    assert cap.model_dump(mode='json') == legacy
    assert fingerprint(cap.model_dump(mode='json')) == fingerprint(legacy)
    assert json.loads(cap.model_dump_json()) == legacy
    changed = request(reasoning_effort='low').capability.model_dump(mode='json')
    assert fingerprint(changed) != fingerprint(legacy)


def test_ollama_rejects_explicit_unsupported_reasoning_before_io():
    p = client(Response({}), kind='ollama')
    with pytest.raises(InferenceConfigurationError):
        p.execute(request(reasoning_effort='low'))
    assert not p.http_client.calls


def test_bounded_redirect_is_rejected_without_retry():
    response=Response(status=307,headers={'Location':'https://unapproved.invalid'})
    p=client(response)
    with pytest.raises(InferenceConfigurationError):p.execute(request())
    assert p.http_client.calls[0][1]['allow_redirects'] is False
    assert len(p.http_client.calls)==1 and response.closed
