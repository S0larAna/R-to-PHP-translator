OPERATIONS = {
    '+': 1,
    '-': 2,
    '*': 3,
    '/': 4,
    '^': 5,
    '%%': 6,
    '%/%': 7,
    '==': 9,
    '!=': 10,
    '>': 11,
    '<': 12,
    '>=': 13,
    '<=': 14,
    ':': 15,
    '&': 16,
    '&&': 17,
    '|': 18,
    '||': 19,
    '!': 20,
    '<-': 21,
    '->': 22,
    '=' : 23
}

DELIMITERS = {
    ' ': 1,
    '(': 2,
    ')': 3,
    ',': 4,
    '-': 5,
    '[': 6,
    ']': 7,
    '\n': 8,  # Предполагается, что "конец строки" это перевод строки
    '{': 9,
    '}': 10 ,
    ':': 11
}

KEYWORDS = {
    'sqrt': 1,
    'abs': 2,
    'if': 3,
    'else': 4,
    'print': 5,
    'while': 6,
    'for': 7,
    'break': 8,
    'next': 9,
    'in': 10,
    'paste': 11,
    'list': 12,
    'return': 13,
    'function': 14
}

def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

def isidentifier(s):
    if s[0] == 'I':
        return True
    else:
        return False

def isconstant(s):
    if s[0] == 'C':
        return True
    else:
        return False

def get_operation(token):
    if token[0] == 'O' and int(token[1]) in OPERATIONS.values():
        return get_key_by_value(OPERATIONS, int(token[1]))
    else:
        return -1

class MPAutomaton:
    def __init__(self):
        self.stack = []
        self.P = 0
        self.STR = 1
        self.label_table = {}
        self.output = []
        self.procedure_mode = False


    def process_token(self, token):
        if isidentifier(token) or isconstant(token) or (token[0] == 'M'):
            self.stack.append(token)
        elif token.endswith('Ф'):
            self.handle_function_call(token)
        elif token == 'УПЛ':
            self.handle_conditional_jump()
        elif token == 'БП':
            self.handle_unconditional_jump()
        elif token.endswith(':'):
            self.handle_label(token)
        elif token.endswith('АЭМ'):
            self.handle_array_access(token)
        else:
            self.handle_operation(token)

    def handle_function_call(self, token):
        # Извлекаем количество аргументов из токена
        num_args = int(token[0])
        func_name = token[1:]
        args = [self.stack.pop() for _ in range(num_args)]
        args.reverse()  # Порядок аргументов должен быть сохранен
        func_name = self.stack.pop()
        result = f'TEMP{self.P}'
        self.P += 1
        self.output.append(f'{result} = {func_name}({", ".join(args)}) ; \n')
        self.STR += 1
        self.stack.append(result)

    def handle_conditional_jump(self):
        label = self.stack.pop()
        condition = self.stack.pop()
        self.output.append(f'if ({condition}) {{ \n')
        self.STR += 1

    def handle_unconditional_jump(self):
        label = self.stack.pop()
        self.output.append(f'else {{ \n')
        self.STR += 1

    def handle_label(self, token):
        label = token[:-1]
        self.output.append(f'{label}: }}; \n')
        self.STR += 1

    def handle_operation(self, operation):
        if operation == 'O21':
            self.handle_assignment()
        elif operation == 'НП':
            param = self.stack.pop()
            func_name = self.stack.pop()
            self.output.append(f'function {func_name}({param})' + ' {\n')
            self.STR += 1
            self.procedure_mode =True
        elif operation == 'W13':
            self.output.append(f'return\n')
            self.STR += 1
        elif operation == 'КП':
            self.output.append(f'return {self.stack.pop()} ; \n')
            self.STR += 1
        elif operation == 'КО':
            self.output.append(f'' + '}\n')
            self.STR += 1
        elif operation == 'W5':
            self.output.append(f'print {self.stack.pop()}' + ' ;\n')
            self.STR += 1
        elif get_operation(operation)!=-1:
            self.handle_arithmetic(operation)

    def handle_arithmetic(self, operation):
        operation = get_operation(operation)
        operand2 = self.stack.pop()
        operand1 = self.stack.pop()
        result = f'TEMP{self.P}'
        self.P += 1
        self.output.append(f'{result} = {operand1} {operation} {operand2} ; \n')
        self.STR += 1
        self.stack.append(result)

    def handle_assignment(self):
        if self.procedure_mode:
            self.procedure_mode = False
        else:
            value = self.stack.pop()
            variable = self.stack.pop()
            self.output.append(f'${variable} = {value}; \n')
            self.STR += 1

    def handle_array_access(self, token):
        num_operands = int(token[:-3])
        indices = [self.stack.pop() for _ in range(num_operands)]
        array_name = self.stack.pop()
        indices.reverse()
        index_str = ''.join([f'[{index}]' for index in indices])
        result = f'{array_name}{index_str}'
        self.stack.append(result)

    def translate(self, rpn_tokens):
        for token in rpn_tokens:
            self.process_token(token)
        for label in self.label_table.values():
            self.output.insert(label, '}')
        return self.output

# Пример использования
rpn_tokens = "I1 I2 I3 1 0 2 НП I2 I3 O1 R8 R2 КП 1 0 КО O21".split()
mp_automaton = MPAutomaton()
output = mp_automaton.translate(rpn_tokens)

for line in output:
    print(line)