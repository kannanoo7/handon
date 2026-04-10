class Hooks:
    def __init__(self):
        self.hooks={}
    
    def register(self,name,func):
        self.hooks.setdefault(name,[]).append(func)
         
    def emit(self,name):
        for hook in self.hooks.get(name,[]):
            hook()  