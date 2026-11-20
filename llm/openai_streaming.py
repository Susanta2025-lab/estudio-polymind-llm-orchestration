"""Additive bounded text streaming; the pinned generation adapter stays unchanged."""
from llm.openai_compatible import OpenAICompatibleProvider
from llm.bounded_http import result_text, validate_request
from llm.bounded_stream import request_stream
from llm.inference import InferenceConfigurationError, InferenceResponseError
from llm.structured import GenerationResult, ProviderResultMetadata


class StreamingOpenAICompatibleProvider(OpenAICompatibleProvider):
    def execute(self, request, *, on_chunk=None):
        if on_chunk is None:
            return super().execute(request)
        validate_request(request)
        cap = request.capability
        if not cap.streaming or not cap.usage_reporting or cap.structured_output != 'prompt' or cap.schema_profile:
            raise InferenceConfigurationError('Bounded text-stream capability required.')
        model = self.model_id(request.role)
        payload = {'model':model, 'messages':[{'role':'system','content':request.system},
                   {'role':'user','content':request.data}], cap.output_parameter:request.output_tokens}
        if cap.temperature is not None:
            payload['temperature'] = cap.temperature
        if cap.reasoning_effort is not None:
            payload['reasoning_effort'] = cap.reasoning_effort
        observation = self.metrics.inference(self.name, request.role, model, 'stream')
        error, usage = None, None
        try:
            value = request_stream(self.http_client, self.url, headers=self.headers, payload=payload,
                timeout=self.timeout, total_seconds=request.total_seconds,
                max_bytes=request.max_response_envelope_bytes or request.response_bytes * 6 + 8192,
                response_bytes=request.response_bytes, allowed_models=(model,*cap.response_models), on_chunk=on_chunk)
            raw = value.get('usage')
            reasoning = None
            if raw is not None:
                if not isinstance(raw, dict):
                    raise InferenceResponseError('Invalid inference usage.')
                counts = [raw.get(k) for k in ('prompt_tokens','completion_tokens','total_tokens')]
                if (any(v is not None and (type(v) is not int or v < 0) for v in counts)
                        or all(v is not None for v in counts) and counts[2] != counts[0]+counts[1]):
                    raise InferenceResponseError('Invalid inference usage.')
                if raw.get('completion_tokens_details') is not None:
                    details = raw['completion_tokens_details']
                    if not isinstance(details, dict):
                        raise InferenceResponseError('Invalid inference usage.')
                    reasoning = details.get('reasoning_tokens')
                    if reasoning is not None and (type(reasoning) is not int or reasoning < 0 or counts[1] is None or reasoning > counts[1]):
                        raise InferenceResponseError('Invalid inference usage.')
                usage = self._usage(value)
            observation.observe_usage(usage)
            first = value['choices'][0]
            text = result_text(self._completion_content(value), request, first['finish_reason'], usage=usage, reasoning_tokens=reasoning)
            metadata = ProviderResultMetadata(finish_reason=first['finish_reason'],
                prompt_tokens=getattr(usage,'prompt_tokens',None), completion_tokens=getattr(usage,'completion_tokens',None),
                total_tokens=getattr(usage,'total_tokens',None), reasoning_tokens=reasoning,
                raw_response_byte_count=len(text.encode()), completion_token_limit=request.output_tokens,
                response_byte_limit=request.response_bytes)
            return GenerationResult(text, usage, value['model'], first['finish_reason'], metadata)
        except BaseException as exc:
            error = exc
            if isinstance(exc, InferenceResponseError) or getattr(exc,'category',None) == 'output_limit':
                exc.usage = usage
            raise
        finally:
            observation.finish(error)
