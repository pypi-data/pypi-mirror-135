from .job import Job
from ..utils import request
from .function import Function
import json

__all__ = ['Function', 'Job']


def createJob():
    pass


def currentJob():
    return Job.current()
    pass


def fetch(rid):
    """
        获取函数
    """
    query = """
        query ($rid:ResourceId!) {
                
            function(rid:$rid) {
                rid,
                documentation
                parameters
                implementType
                implement
                configs
                context
                name
                description
                type
                owner
                key
                executor
            }
        }
    """
    payload = {
        'query': query,
        'variables': {
            'rid': rid,
        }
    }
    r = request('POST', 'graphql', data=json.dumps(payload))
    data = json.loads(r.text)
    return Function(data['data']['function'])


def fetchMany(name=None, pageSize=10, pageOffset=0):
    pass
