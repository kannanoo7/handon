
class Context:
    def __init__(self,path):
        self.path=path
        self.headers={}
        self.params={}

        # response like data
        self.status_code=200
        self.body=None

        #shared storage
        self.storage={}