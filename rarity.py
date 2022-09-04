NORMAL = ''
MAGIC = 'Magic'
RARE = 'Rare'

def getColor(rarity:stri) -> str:
    if rarity == MAGIC:
        return 'blue'
    if rarity == RARE:
        return '#880'
    return 'black'
