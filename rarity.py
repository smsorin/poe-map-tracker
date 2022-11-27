NORMAL = ''
MAGIC = 'Magic'
RARE = 'Rare'

def getColor(r:str) -> str:
    if r == MAGIC:
        return 'blue'
    if r == RARE:
        return '#880'
    return 'black'
