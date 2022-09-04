from dataclasses import dataclass

@dataclass
class Fragment(object):
    name: str = ""
    stack: int = 0
    button = None    
    
    @staticmethod
    def Parse(lines):
        f = Fragment(name=lines[2])
        result = re.match(r'Stack Size: (\d+)', lines[4])
        if result:
            f.stack = int(result.group(1))        
        return f