class Response:

    def __init__(self,body="",status=200,headers=None):
        self.body =body
        self.status =status
        self.headers = headers or {}

    @classmethod
    def text(cls,body,status=200):
        return cls(body,status,{"content-type":"text/plain"})
    

    @classmethod
    def json(cls,data,status=200):
        import json
        return cls(body=json.dumps(data),status=status, 
                    headers={"content-type":"application/json"})
        