
def is_alpha(x):
    return x in 'qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM'


def split(txt):
    dx = []
    tmp = []
    compound = 0
    variable = []
    vtmp = []
    in_expression = False
    before_specifier = True
    for ch in txt + '%':
        if ch == '%':
            if compound > 0:
                tmp.append(ch)
            elif len(tmp) > 0:
                if tmp[-1] != ':':
                    if len(tmp) > 0:
                        dx.append(''.join(tmp))
                    tmp = [ch]
                else:
                    tmp.append(ch)
            else:
                tmp.append(ch)

            before_specifier = False

        elif ch == ';':
            if compound > 0:
                tmp.append(ch)
            else:
                if len(tmp) > 0:
                    dx.append(''.join(tmp))
                dx.append(ch)
                tmp = []
        
        elif ch == '(':
            before_specifier = True
            compound += 1
            tmp.append(ch)
        
        elif ch == ')':
            before_specifier = True

            compound -= 1
            tmp.append(ch)

        elif is_alpha(ch) and before_specifier:
            vtmp.append(ch)
            tmp.append(ch)

        elif ch == ':' and before_specifier:
            variable.append(''.join(vtmp))
            vtmp.clear()
            tmp.append(ch)

        elif ch in ['{', '[']:
            tmp.append(ch)
            in_expression = True

        elif ch in ['}', ']']:
            tmp.append(ch)
            in_expression = False
        
        elif ch == '$':
            if compound > 0 or in_expression:
                tmp.append(ch)
            else:
                if len(tmp) > 0:
                    dx.append(''.join(tmp))
                tmp = [ch]              
    
        elif ch == ' ':
            pass
            
        else:
            tmp.append(ch)

    return [dx, variable]


if __name__ == '__main__':
    # print(split('%d %d %d %d;%d'))
    # print(split('%d[:50]'))
    # print(split('%d[-30:]{4}'))
    # print(split('a:%d;%d[-30:]{$a}'))
    # print(split('%d[2:7]'))
    # print(split('%d{2}'))
    # print(split('%(%d[0:5] %d[5:10]);%d'))
    # print(split('a:%d %d $a %d;%d'))
    # print(split('a:%d[:50]'))
    # print(split('%d[-30:]{4}'))
    # print(split('v:%d[2:7]'))
    # print(split('n:%d{2}'))
    # print(split('%(%d[0:5] %d[5:10]);%d'))
    print(split('a:%d;$a;$a'))
    


        
    

