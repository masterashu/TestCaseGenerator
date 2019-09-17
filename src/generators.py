from random import randint, random
from sys import maxsize
from .parsers import split as split_request

class Generator:
    def __init__(self):
        self.valid_chars = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.variables = dict()
        self.output = []

    def parse_val(self, value, d_type=int):
        if d_type == int:
            return self.parse_int(value)
        elif d_type == float:
            return self.parse_float(value)
        elif d_type == str:
            return self.parse_str(value)

    def parse_float(self, value):
        if value[0] == '$':
            return float(self.get_variable(value[1:]))
        else:
            if value[0] == '^':
                return float(pow(10, int(value[1:])))
            else:
                return float(value)

    def parse_str(self, value):
        pass

    @staticmethod
    def get_char_in_range(start, end):
        chars = set()
        for i in range(ord(start), ord(end) + 1, 1):
            chars.add(chr(i))
        return chars

    def parse_int(self, value):
        if value[0] == '$':
            return int(self.get_variable(value[1:]))
        else:
            if value[0] == '^':
                return int(pow(10, int(value[1:])))
            else:
                return int(value)

    def get_variable(self, variable_name):
        return self.variables.get(variable_name)

    def parse_request(self, txt):
        kw = dict()
        if txt[0] != '%':
            # Must be a Named variable or a previous variable or a newline
            if txt[0] == ';':
                kw['type'] = 'newline'
                return kw

            if txt[0] == '$':
                # Callback to previous Variable
                kw['type'] = 'variable'
                kw['variable_name'] = txt[1:].strip()
                return kw
            # New Named Variable
            var_name = txt.split(':')[0]
            txt = ':'.join(txt.split(':')[1:])
            kw['var_name'] = var_name
            # print(var_name, txt)
            
        types = {'d': 'integer', 'f': 'float',
                 'c': 'character', 's': 'string', '(': 'compound'}

        kw['type'] = types[txt[1]]
        tmp = []


        if kw['type'] == 'integer':
            for ch in txt[2:]:
                if ch == '[' and kw.get('range', False) is False:
                    pass
                elif ch == '{' and kw.get('repeat', False) is False:
                    pass
                elif ch == ']' and kw.get('range', False) is False:
                    tmp = ''.join(tmp)
                    # No lower Limit
                    if tmp[0] == ':':
                        kw['range'] = True
                        kw['range_end'] = self.parse_val(tmp[1:], int)
                    elif tmp[-1] == ':':
                        # No Upper Limit
                        kw['range'] = True
                        kw['range_start'] = self.parse_val(tmp[:-1], int)
                    else:
                        tmp = tmp.split(':')
                        kw['range'] = True
                        kw['range_start'] = self.parse_val(tmp[0], int)
                        kw['range_end'] = self.parse_val(tmp[1], int)
                    tmp = []

                elif ch == '}' and kw.get('repeat', False) is False:
                    tmp = ''.join(tmp)
                    kw['repeat'] = True
                    kw['repeat_count'] = self.parse_val(tmp, int)

                else:
                    tmp.append(ch)

        elif kw['type'] == 'float':
            for ch in txt[2:]:
                if ch == '[' and kw.get('range', False) is False:
                    pass
                elif ch == '{' and kw.get('repeat', False) is False:
                    pass
                elif ch == ']' and kw.get('range', False) is False:
                    tmp = ''.join(tmp)
                    # No lower Limit
                    if tmp[0] == ':':
                        kw['range'] = True
                        kw['range_end'] = self.parse_val(tmp[1:], int)
                    # No Upper Limit
                    elif tmp[-1] == ':':
                        kw['range'] = True
                        kw['range_start'] = self.parse_val(tmp[:-1], int)
                    else:
                        tmp = tmp.split(':')
                        kw['range'] = True
                        kw['range_start'] = self.parse_val(tmp[0], int)
                        kw['range_end'] = self.parse_val(tmp[1], int)
                    tmp = []

                elif ch == '}' and kw.get('repeat', False) is False:
                    tmp = ''.join(tmp)
                    kw['repeat'] = True
                    kw['repeat_count'] = self.parse_val(tmp, int)

                else:
                    tmp.append(ch)

        elif kw['type'] == 'string' or kw['type'] == 'character':
            choices = set()
            escape = False
            for ch in txt[2:]:
                if ch == '\\':
                    if escape:
                        tmp.append(ch)
                        escape = False
                    else:
                        escape = True
                elif ch == '[' and kw.get('choice', False) is False:
                    if escape:
                        tmp.append(ch)
                        escape = False
                elif ch == '{' and kw.get('repeat', False) is False:
                    if escape:
                        tmp.append(ch)
                        escape = False
                elif ch == ']' and kw.get('choice', False) is False:
                    if escape:
                        tmp.append(ch)
                        escape = False
                    else:
                        tmp = ''.join(tmp)
                        if tmp[0] == '^':
                            kw['choice_invert'] = True
                            tmp = tmp[1:]
                        char = ''
                        active_range = False
                        for chs in tmp:
                            if chs == '-':
                                if char == '':
                                    char = chs
                                else:
                                    active_range = True
                            else:
                                if char == '':
                                    char = chs
                                else:
                                    if active_range:
                                        choices = choices.union(self.get_char_in_range(char, chs))
                                        char = ''
                                        active_range = False
                                    else:
                                        choices.add(char)
                                        char = chs
                        if char != '':
                            choices.add(char)
                        kw['choices'] = choices

                        tmp = []
                elif ch == '}' and kw.get('repeat', False) is False:
                    if escape:
                        tmp.append(ch)
                        escape = False
                    else:
                        tmp = ''.join(tmp)
                        kw['length'] = self.parse_val(tmp, int)

                else:
                    tmp.append(ch)
                
            if kw.get('length', False) is False:
                kw['length'] = 1
        
        elif kw['type'] == 'compound':
            kw['request'] = []
            if txt[-1] == '}':
                kw['repeat'] = True
                kw['repeat_count'] = self.parse_int(txt.split('{')[-1][:-1])
                requests = split_request('{'.join(txt.split('{')[:-1]))[0]
            else:
                requests = split_request(txt[2:-1])[0]
            for request in requests:
                kw['request'].append(self.parse_request(request))
            
        return kw

    def generate(self, **kwargs):
        if kwargs['type'] == 'integer':
            return self.generate_number(**kwargs)
        elif kwargs['type'] == 'float':
            return self.generate_float(**kwargs)
        elif kwargs['type'] == 'string':
            return self.generate_string(**kwargs)
        elif kwargs['type'] == 'character':
            return self.generate_string(**kwargs)
        elif kwargs['type'] == 'variable':
            return self.get_variable(kwargs['variable_name'])
        elif kwargs['type'] == 'compound':
            return self.generate_compounds(**kwargs)


    def generate_number(self, **kwargs):
        if kwargs.get('repeat', False):
            return self.generate_numbers(**kwargs)

        if kwargs.get('range', False):
            if kwargs.get('range_start', False) is not False:
                if kwargs.get('range_end', False) is not False:
                    return randint(kwargs['range_start'], kwargs['range_end'])
                else:
                    return randint(kwargs['range_start'], maxsize)
            else:
                if kwargs.get('range_end', False) is not False:
                    return randint(int(maxsize * random()), kwargs['range_end'])
                else:
                    raise ValueError

        else:
            return int(maxsize * random())

    def generate_float(self, **kwargs):
        pass

    def generate_string(self, **kwargs):
        if kwargs.get('choices', False) is False:
            valid_chars = self.valid_chars
        else:
            if kwargs.get('choice_invert', False) is False:
                valid_chars = set(kwargs['choices'])
            else:
                valid_chars = self.valid_chars - set(kwargs['choices'])
        if kwargs['type'] == 'string':
            output = ''.join([random.choice(valid_chars) for _ in range(kwargs['length'])])
        else:
            output = ' '.join([random.choice(valid_chars) for _ in range(kwargs['length'])])
        return output

    def generate_numbers(self, **kwargs):
        repeat = kwargs.get('repeat_count', 1)
        arr = []
        if kwargs.get('range', False):
            if kwargs.get('range_start', False) is not False:
                if kwargs.get('range_end', False) is not False:
                    for i in range(repeat):
                        arr.append(randint(kwargs['range_start'], kwargs['range_end']))
                else:
                    for i in range(repeat):
                        arr.append(randint(kwargs['range_start'], maxsize))
            else:
                if kwargs.get('range_end', False) is not False:
                    for i in range(repeat):
                        arr.append(randint(maxsize * -1, kwargs['range_end']))
                else:
                    raise ValueError
        else:
            for i in range(repeat):
                arr.append(int(maxsize * random()))
        return arr

    def generate_compounds(self, **kwargs):
        repeat_count = kwargs.get('repeat_count', 1)
        output = []
        for _ in range(repeat_count):
            gens = []
            for reqs in kwargs['request']:
                gens.append(self.generate(**reqs))
            output.append(gens)
        return output


if __name__ == '__main__':
    a = Generator()
    print(a.parse_request('%d[:242]'))
    print(a.parse_request('%d[3:]{2}'))
    print(a.parse_request('%d[1:34]{4}'))
    print(a.parse_request('%s[a-g]'))
    print(a.parse_request('%s[qa-g]'))
    print(a.parse_request('%s[qmark-n]'))
    print(a.parse_request('%s[ABCDa-g]'))
    print(a.parse_request('%s[9583a-g]{2}'))
    print(a.parse_request('%s[-a-g]'))
    print(a.parse_request('%s[^9583a-g]'))
    print(a.parse_request('%s[^-a-g]'))
    print(a.parse_request('%s{34}'))
    print(a.parse_request('%s'))
    print(a.parse_request('%(%d%c)'))
    print(a.parse_request('%(%d %c){4}'))
    print(a.parse_request('%(%d;%c)'))
    print(a.parse_request('%(%d %c %d[2:5]{3})'))

