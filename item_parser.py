import re

import map
import fragment


def ParseItem(text):
    lines = re.split(r'[\n\r]+', text)
    if lines[0].startswith('Item Class: Maps'):
        return map.Map.Parse(lines)
    if lines[0].startswith('Item Class: Map Fragments'):
        return fragment.Fragment.Parse(lines)
    
    print('Can\'t parse clipboard text: ', text)
    return None