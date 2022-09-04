import re

def Parser(rules, target, lines):
    rule_index = 0
    for l in lines:
        if l == '--------':
            rule_index +=1
            continue
        if rule_index < len(rules):
            for r, attr in rules[rule_index]:
                result = re.match(r, l)                
                if result:
                    if len(result.groups()) == 1:
                        setattr(target, attr, result.group(1))
                    else:
                        mod = result.group(1) + '#' + result.group(3) + ', ' + result.group(2)
                        v = getattr(target, attr)
                        if v is None:
                            v = []
                        v.append(mod)
                        setattr(target, attr, v)
                    break