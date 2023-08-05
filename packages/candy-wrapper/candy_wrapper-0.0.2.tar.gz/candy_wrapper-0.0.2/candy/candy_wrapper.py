from typing import Any 
from pysimplelog import Logger
from yes_or_no.yes_or_no import yes_or_no
from keyword import iskeyword

logger = Logger(__name__)
logger.set_log_file_basename(__name__)
# logger.set_minimum_level(logger.logLevels['debug'])
logger.set_minimum_level(logger.logLevels['info'])

obj_keys = {'', '_obj'}
class Wrapper(dict):
   
    def __init__(self,obj:Any=None):
    
        debug_msg = f"""
                        What is {obj=}?
                        What is {bool(obj)}?
                        What is {type(obj)}?
                        """
        logger.debug(debug_msg)
        self[''] = obj
        if isinstance(obj,dict): super().__init__(self[''])
        else:super().__init__()
    
    def __call__(self,*args, **kwargs) -> Any:
        
        debug_msg = f"""
                        What is {self._obj=}?
                        What is{self['']=}?
                        """
        logger.debug(debug_msg)
        
        obj = self._obj                        
        debug_msg = f"""
                        {yes_or_no(f'Is {obj} callable', callable(obj))}
                        {yes_or_no(f'Is {obj} instance of Wrapper',
                        isinstance(obj,Wrapper))}
                        """
        logger.debug(debug_msg)
        
        return obj if not callable(obj) else obj(*args,**kwargs)
    
    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key:str, value:Any) -> None:
        self[key] = value
    
    def __setitem__(self, key , value) -> None:
        
        
        debug_msg = f"""
                        What is {key=}?
                        What is {value=}?
                        """
        logger.debug(debug_msg)
        
        head, tail = key.split('.', 1) if '.' in key else (key, None)
        debug_msg = f"""
                        {yes_or_no(f'Is . in {key}', '.' in key)}
                        What is {(key.split('.',1) if '.' in key else (key, None))=}
                        What is {head=}?
                        What is {tail=}?
                        """
        logger.debug(debug_msg)
        
        if head and not head.isidentifier() or iskeyword(head):
            raise ValueError(f'{head} is key word' if iskeyword(head) else
                             f'{head} is not identifier')
        
        value = value if head in obj_keys or isinstance(value,Wrapper) else\
                Wrapper(value)
        
        debug_msg = f"""
                        What it {value=}?
                        What is {type(value)}?
                        """
        logger.debug(debug_msg) 
          
        return self[head].__setitem__(tail, value) if tail else\
               super().__setitem__(head, value)
        
    def __getitem__(self, key: str) -> Any:
      
        head, tail = key.split('.', 1) if '.' in key else (key, None)
        if tail: return self[head][tail]
        if head in obj_keys:
            check = [k not in self for k in obj_keys]
            other = (obj_keys - {head}).pop()
            if all(check): self[head] = self[other] = None
            elif head not in self: self[head] = self[other] 
            return super().__getitem__(head)
        if head not in self: self[head] = Wrapper()
        return super().__getitem__(head)

    def __delattr__(self, key):
        if key not in self:
            raise AttributeError(key)
        if key in obj_keys: self[''] = self['_obj'] = None
        else: del self[key]

    def __repr__(self):
        return '<Wrapper ' + dict.__repr__(self) + '>'
