"""SSE byte/content bounds apply before provider-neutral token release."""
import json
import pytest
from llm.bounded_stream import request_stream
from llm.inference import InferenceOutputLimitError, InferenceResponseError


class Response:
    status_code=200
    headers={}
    def __init__(self,events):
        self.raw=(''.join('data: '+json.dumps(e)+'\n\n' for e in events)+'data: [DONE]\n\n').encode()
        self.closed=False
    def iter_content(self,chunk_size):
        for i in range(len(self.raw)):yield self.raw[i:i+1]
    def close(self):self.closed=True


def test_content_cap_checked_before_release():
    r=Response([{'model':'approved','choices':[{'delta':{'content':'too much output'}}]}])
    class HTTP:
        def post(self,*a,**k):return r
    emitted=[]
    with pytest.raises(InferenceOutputLimitError):
        request_stream(HTTP(),'https://offline.invalid/v1',headers={},payload={'model':'approved'},timeout=(1,1),
            total_seconds=2,max_bytes=4096,response_bytes=4,on_chunk=emitted.append,allowed_models=('approved',))
    assert emitted==[] and r.closed


def test_stream_response_model_checked_before_release():
    r=Response([{'model':'unapproved','choices':[{'delta':{'content':'private'}}]}])
    class HTTP:
        def post(self,*a,**k):return r
    emitted=[]
    with pytest.raises(InferenceResponseError):
        request_stream(HTTP(),'https://offline.invalid/v1',headers={},payload={'model':'approved'},timeout=(1,1),
            total_seconds=2,max_bytes=4096,on_chunk=emitted.append,allowed_models=('approved',))
    assert emitted==[] and r.closed
