class Output:
    def __init__(self):
        self.variables = dict()
        self.output = []

    def parse_val(self, value, d_type=int):
        if value[0] == '$':
            return d_type(self.get_variable(value[1:]))
        else:
            return d_type(value)

    def get_variable(self, variable_name):
        return self.variables.get(variable_name)

    def parse_request(self, txt):
        if txt[0] != '%':
            # Must be a named variable
            var_name = txt.split(':')[0]
            txt = ':'.join(txt.split(':')[1:])
            print(var_name, txt)
        kw = dict()
        types = {'d': 'integer', 'f': 'float', 'c':'character', 's': 'string', 'c': 'compund'}
        
        kw['type'] = types[txt[1]]
        tmp = []

        if kw['type'] == 'integer':
            for ch in txt[2:]:
                if ch == '[' and kw.get('range', False) == False:
                    pass
                elif ch == '{' and kw.get('repeat', False) == False:
                    pass
                elif ch == ']' and kw.get('range', '') == '':
                    tmp = ''.join(tmp)
                    # No lower Limit
                    if (tmp[0] == ':'):
                        kw['range'] = True
                        kw['range_end'] = self.parse_val(tmp[1:], int)
                    elif (tmp[-1] == ':'):
                        kw['range'] = True
                        kw['range_start'] = self.parse_val(tmp[:-1], int)
                    else:
                        tmp = tmp.split(':')
                        kw['range'] = True
                        kw['range_start'] = self.parse_val(tmp[0], int)
                        kw['range_end'] = self.parse_val(tmp[1], int)
                    tmp = []
                
                elif ch == '}' and kw.get('repeat', '') == '':
                    tmp = ''.join(tmp)
                    kw['repeat'] = True
                    kw['repeat_count'] = self.parse_val(tmp, int)

                else:
                    tmp.append(ch)
        
        return kw



def generate(txt, **kwargs):
    pass

def generate_number(txt, **kwargs):
    
    pass


def generate_character(txt, **kwargs):
    pass


def generate_float(txt, **kwargs):
    pass


def generate_string(txt, **kwargs):
    pass

    
def generate_numbers(txt, **kwargs):
    pass

