import re

PRIORITY0 = ['W3', 'R2', 'R6']
PRIORITY1 = ['R4', 'R3', 'R7']
PRIORITY2 = ['O21']
PRIORITY3 = ['O18', 'O19', 'O15']
PRIORITY4 = ['O16', 'O17']
PRIORITY5 = ['O20']
PRIORITY6 = ['O9', 'O10', 'O11', 'O12', 'O13', 'O14']
PRIORITY7 = ['O1', 'O2']
PRIORITY8 = ['O3', 'O4']
PRIORITY9 = ['O5']
PRIORITY10 = ['W14']


def get_priority(operation):
    if operation in PRIORITY0:
        return 0
    elif operation in PRIORITY1:
        return 1
    elif operation in PRIORITY2:
        return 2
    elif operation in PRIORITY3:
        return 3
    elif operation in PRIORITY4:
        return 4
    elif operation in PRIORITY5:
        return 5
    elif operation in PRIORITY6:
        return 6
    elif operation in PRIORITY7:
        return 7
    elif operation in PRIORITY8:
        return 8
    elif operation in PRIORITY9:
        return 9
    elif operation in PRIORITY10:
        return 10
    else:
        return -1

def is_constant(token):
    if token[0] == 'C':
        return True
    else:
        return False

def is_identifier(token):
    if token[0] == 'I':
        return True
    else:
        return False

def is_operator(token):
    if token[0] == 'O':
        return True
    else:
        return False

test_tokens = '''I1 R1 O21 R1 W14 R2 I2 R3 R1 R9 R8
R1 R1 R1 R1 W3 R2 I2 R1 O9 R1 C1 R1 O18 R1 I2 R1 O9 R1 C2 R3 R1 R9 R8
R1 R1 R1 R1 W13 R2 C2 R3 R8
R1 R1 R10 R1 W4 R1 R9 R8
R1 R1 R1 R1 R1 R1 R1 R1 W13 R2 I2 R1 O3 R1 I1 R2 I2 R5 C2 R3 R3 R8 
R1 R1 R10 R8
R10 R8
R8
I3 R1 O21 R1 C3 R1 R8
R8 
R8 
I4 R1 O21 R1 I1 R2 I3 R3 R8 
R8 
W5 R2 W11 R2 '''


def infix_to_postfix(tokens):
    i = 0
    stack = []
    out_seq = ''
    aem_count = proc_num = proc_level = operand_count = 1
    func_count = tag_count = proc_num = if_count = while_count = \
        begin_count = end_count = bracket_count = args_count = 0
    is_if = is_while = is_description_var = is_function = False
    while i < len(tokens):
        p = get_priority(tokens[i])
        if p == -1:
            if tokens[i] not in ['R8', 'R1']:
                out_seq += tokens[i] + ' '
            if is_function:
                args_count+=1
        elif tokens[i] == 'R2':
            if is_function:
                out_seq += stack.pop()
            elif is_identifier(tokens[i - 1]):
                if tokens[i + 1] != 'R3':
                    func_count += 1
                stack.append(str(func_count) + ' Ф')
            bracket_count+=1
        elif tokens[i] == 'R3':
            if is_function:
                out_seq += f'{str(args_count)} '
        elif tokens[i] == 'O21':
            j = i + 1
            while tokens[j] == 'R1':
                j += 1
            if tokens[j] == 'W14':
                proc_num += 1
                i += (j-i)
                stack.append('НП ' + str(proc_num) + ' ' + str(proc_level) + ' ')
                is_function = True
            else:
                stack.append('O21')
        i += 1
        print(out_seq)
    while len(stack) > 0:
        out_seq += stack.pop() + ' '

    print(out_seq)

if __name__ == '__main__':
    expressions = test_tokens.split()
    infix_to_postfix(expressions)