from random import randint, random, randrange
from sys import maxsize

class Generator:
    def __init__(self):
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

    def get_char_in_range(self, start, end):
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
            # Must be a named variable
            var_name = txt.split(':')[0]
            txt = ':'.join(txt.split(':')[1:])
            kw['var_name'] = var_name
            print(var_name, txt)
        types = {'d': 'integer', 'f': 'float',
                 'c': 'string', 's': 'string', '(': 'compund'}

        kw['type'] = types[txt[1]]
        tmp = []

        if kw['type'] == 'integer':
            for ch in txt[2:]:
                if ch == '[' and kw.get('range', False) == False:
                    pass
                elif ch == '{' and kw.get('repeat', False) == False:
                    pass
                elif ch == ']' and kw.get('range', False) == False:
                    tmp = ''.join(tmp)
                    # No lower Limit
                    if (tmp[0] == ':'):
                        kw['range'] = True
                        kw['range_end'] = self.parse_val(tmp[1:], int)
                    elif (tmp[-1] == ':'):
                        # No Upper Limit
                        kw['range'] = True
                        kw['range_start'] = self.parse_val(tmp[:-1], int)
                    else:
                        tmp = tmp.split(':')
                        kw['range'] = True
                        kw['range_start'] = self.parse_val(tmp[0], int)
                        kw['range_end'] = self.parse_val(tmp[1], int)
                    tmp = []

                elif ch == '}' and kw.get('repeat', False) == False:
                    tmp = ''.join(tmp)
                    kw['repeat'] = True
                    kw['repeat_count'] = self.parse_val(tmp, int)

                else:
                    tmp.append(ch)

        elif kw['type'] == 'float':
            for ch in txt[2:]:
                if ch == '[' and kw.get('range', False) == False:
                    pass
                elif ch == '{' and kw.get('repeat', False) == False:
                    pass
                elif ch == ']' and kw.get('range', False) == False:
                    tmp = ''.join(tmp)
                    # No lower Limit
                    if (tmp[0] == ':'):
                        kw['range'] = True
                        kw['range_end'] = self.parse_val(tmp[1:], int)
                    # No Upper Limit
                    elif (tmp[-1] == ':'):
                        kw['range'] = True
                        kw['range_start'] = self.parse_val(tmp[:-1], int)
                    else:
                        tmp = tmp.split(':')
                        kw['range'] = True
                        kw['range_start'] = self.parse_val(tmp[0], int)
                        kw['range_end'] = self.parse_val(tmp[1], int)
                    tmp = []

                elif ch == '}' and kw.get('repeat', False) == False:
                    tmp = ''.join(tmp)
                    kw['repeat'] = True
                    kw['repeat_count'] = self.parse_val(tmp, int)

                else:
                    tmp.append(ch)

        elif kw['type'] == 'string':
            choices = set()
            escape = False
            for ch in txt[2:]:
                if ch == '\\':
                    if escape:
                        tmp.append(ch)
                        escape = False
                    else:
                        escape = True
                elif ch == '[' and kw.get('choice', False) == False:
                    if escape:
                        tmp.append(ch)
                        escape = False
                elif ch == '{' and kw.get('repeat', False) == False:
                    if escape:
                        tmp.append(ch)
                        escape = False
                elif ch == ']' and kw.get('choice', False) == False:
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
                                        choices = choices.union(
                                            self.get_char_in_range(char, chs))
                                        char = ''
                                        active_range = False
                                    else:
                                        choices.add(char)
                                        char = chs
                        if char != '':
                            choices.add(char)
                        kw['choices'] = choices

                        tmp = []
                elif ch == '}' and kw.get('repeat', False) == False:
                    if escape:
                        tmp.append(ch)
                        escape = False
                    else:
                        tmp = ''.join(tmp)
                        kw['repeat'] = True
                        kw['repeat_count'] = self.parse_val(tmp, int)

                else:
                    tmp.append(ch)
        return kw

    def generate(self, **kwargs):
        if kwargs['type'] == 'integer':
            return self.generate_number(**kwargs)
        elif kwargs['type'] == 'float':
            return self.generate_float(**kwargs)
        elif kwargs['type'] == 'string':
            return self.generate_string(**kwargs)

    def generate_number(self, **kwargs):
        if kwargs.get('repeat', False):
            return self.generate_numbers(**kwargs)
        
        if kwargs.get('range', False):
            if kwargs.get('range_start', False):
                if kwargs.get('range_end', False):
                    return randint(kwargs['range_start'], kwargs['range_end'])
                else:
                    return randint(kwargs['range_start'], int(maxsize * random()))
            else:
                if kwargs.get('range_end', False):
                    return randint(int(maxsize * random()), kwargs['range_end'])
                else:
                    raise ValueError
            
        else:
            return int(maxsize * random())

    def generate_character(self, **kwargs):
        pass

    def generate_float(self, **kwargs):
        pass

    def generate_string(self, **kwargs):
        pass

    def generate_numbers(self, **kwargs):
        repeat = kwargs.get('repeat_count', 1)
        arr = []
        if kwargs.get('range', False):
            if kwargs.get('range_start', False):
                if kwargs.get('range_end', False):
                    for i in range(repeat):
                        arr.append(randint(kwargs['range_start'], kwargs['range_end']))
                else:
                    for i in range(repeat):
                        arr.append(randint(kwargs['range_start'], int(maxsize * random())))
            else:
                if kwargs.get('range_end', False):
                    for i in range(repeat):
                        arr.append(randint(int(maxsize * random()), kwargs['range_end']))
                else:
                    raise ValueError
        else:
            for i in range(repeat):
                arr.append(int(maxsize * random()))
        return arr


if __name__ == '__main__':
    a = Output()
    print(a.parse_request('%d[:242]'))
    print(a.parse_request('%d[3:]{2}'))
    print(a.parse_request('%d[1:34]{4}'))
    print(a.parse_request('%s[a-g]'))
    print(a.parse_request('%s[qa-g]'))
    print(a.parse_request('%s[qwtgfa-e]'))
    print(a.parse_request('%s[ABCDa-g]'))
    print(a.parse_request('%s[9583a-g]'))
    print(a.parse_request('%s[-a-g]'))
    print(a.parse_request('%s[^9583a-g]'))
    print(a.parse_request('%s[^-a-g]'))
