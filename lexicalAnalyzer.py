def read_file_contents(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        content = ''.join(lines)
    return content

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
    '}': 10
}

CONSTANTS = {
    'NA': 1,
    'Null': 2,
    'NaN': 3,
    'Inf': 4
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

IDENTIFIERS = {}

CONSTANTS = {}

def analyze(input_program):
    CONSTANTS = {}
    IDENTIFIERS = {}
    state = 'S'
    output_sequence = buffer = ''
    i=0
    identificator_id = const_id = 0
    while i < len(input_program):
        symbol = input_program[i]
        if state == 'S':
            buffer = ''
            if symbol.isalpha():
                buffer+=symbol
                state = 'q1'
            elif symbol.isalnum():
                buffer+=symbol
                state = 'q3'
            elif symbol == "#":
                state = 'q5'
            elif symbol in DELIMITERS:
                output_sequence+='R' + str(DELIMITERS[symbol]) + ' '
                if symbol == '\n':
                    output_sequence+='\n'
            elif symbol in OPERATIONS:
                curr_and_next = symbol + input_program[i+1]
                if curr_and_next in OPERATIONS:
                    output_sequence+='O' + str(OPERATIONS[curr_and_next]) + ' '
                    i+=1
                else:
                    output_sequence+='O'+str(OPERATIONS[symbol]) + ' '
            else:
                state = 'F'
        elif state == 'q1':
            if symbol.isalpha():
                buffer+=symbol
            elif symbol.isalnum():
                buffer+=symbol
                state = 'q2'
            elif symbol in DELIMITERS or OPERATIONS:
                if buffer in KEYWORDS:
                    output_sequence += 'W' + str(KEYWORDS[buffer]) + ' '
                elif buffer in IDENTIFIERS:
                    output_sequence += 'I' + str(IDENTIFIERS[buffer]) + ' '
                else:
                    identificator_id+=1
                    IDENTIFIERS[buffer] = identificator_id
                    output_sequence += 'I' + str(IDENTIFIERS[buffer]) + ' '
                state = 'S'
                i -= 1
        elif state == 'q2':
            if symbol.isalpha() or symbol.isalnum():
                buffer+=symbol
            elif symbol in DELIMITERS or OPERATIONS:
                if buffer in KEYWORDS:
                    output_sequence += 'W' + str(KEYWORDS[buffer]) + ' '
                elif buffer in IDENTIFIERS:
                    output_sequence += 'I' + str(IDENTIFIERS[buffer]) + ' '
                else:
                    identificator_id+=1
                    IDENTIFIERS[buffer] = identificator_id
                    output_sequence += 'I' + str(IDENTIFIERS[buffer]) + ' '
                state = 'S'
                i -= 1
        elif state == 'q3':
            if symbol.isalnum():
                buffer+=symbol
            elif symbol == '.':
                state = 'q4'
                buffer+=symbol
            elif symbol in DELIMITERS or OPERATIONS:
                if buffer in CONSTANTS:
                    output_sequence += 'C' + str(CONSTANTS[buffer]) + ' '
                else:
                    const_id += 1
                    CONSTANTS[buffer] = const_id
                    output_sequence += 'C' + str(CONSTANTS[buffer]) + ' '
                state = 'S'
                i -= 1
        elif state == 'q4':
            if symbol.isalnum():
                buffer+=symbol
            elif symbol in DELIMITERS or OPERATIONS:
                if buffer in CONSTANTS:
                    output_sequence += 'C' + str(CONSTANTS[buffer]) + ' '
                else:
                    const_id += 1
                    CONSTANTS[buffer] = const_id
                    output_sequence += 'C' + str(CONSTANTS[buffer]) + ' '
                state = 'S'
                i -= 1
        elif state == 'q5':
            buffer+=symbol
            if symbol == '\n':
                state = 'S'
        i += 1
    if not(buffer == ''):
        if state == 'q3':
            if buffer in CONSTANTS:
                output_sequence += 'C' + str(CONSTANTS[buffer]) + ' '
            else:
                const_id += 1
                CONSTANTS[buffer] = const_id
                output_sequence += 'C' + str(CONSTANTS[buffer]) + ' '
    return output_sequence, CONSTANTS, IDENTIFIERS


if __name__ == '__main__':
    input_program = read_file_contents("./input.txt")
    analyze(input_program)

