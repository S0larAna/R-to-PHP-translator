import re
import sys

PRIORITY0 = ['W3', 'R2', 'R6', 'АЭМ', 'Ф']
PRIORITY1 = ['R4', 'R3', 'R7', 'W4', 'R8']
PRIORITY2 = ['O21']
PRIORITY3 = ['O18', 'O19', 'O15']
PRIORITY4 = ['O16', 'O17']
PRIORITY5 = ['O20']
PRIORITY6 = ['O9', 'O10', 'O11', 'O12', 'O13', 'O14']
PRIORITY7 = ['O1', 'O2']
PRIORITY8 = ['O3', 'O4']
PRIORITY9 = ['O5']
PRIORITY10 = ['W14', 'R10', 'R9', 'W13', 'W5', 'W11']

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

def infix_to_postfix(t):
    try:
        i = 0
        stack = []
        array_index_mode = False
        if_mode = False
        function_mode = False
        procedure_mode = False
        return_mode = False
        procedure_count = 0
        procedure_level = 0
        label_count = 0
        operand_count = 0
        out_seq = ''
        while i < len(t):
            token = t[i]
            p = get_priority(token)
            if p == -1 and token!='R1':
                if i+1 < len(t) and t[i+1] == 'R2':
                    function_mode = True
                out_seq += token + ' '
            elif token == 'R2': # (
                if function_mode:
                    stack.append('Ф')
                    operand_count = 1
                elif if_mode:
                    stack.append(token)
                elif not return_mode:
                    procedure_count += 1
                    stack.append(token)
                    stack.append((procedure_count, procedure_level, 1))
            elif token == 'R3': # )
                if function_mode:
                    while stack and stack[-1] != 'Ф':
                        out_seq += stack.pop() + ' '
                    if stack:
                        out_seq += str(operand_count) + stack.pop() + ' '  # Добавление 'Ф'
                        operand_count = 0
                    function_mode = False
                elif if_mode:
                    while stack and stack[-1] != 'W3':
                        out_seq += stack.pop() + ' '
                    if stack:
                        label_count = 0
                        #out_seq+=f"M{label_count} "
                    # if_mode = False
                elif not return_mode:
                    while stack and stack[-1]!='R2':
                        out_seq +=  ' '.join(map(str, stack.pop())) + ' НП '
            elif token == 'R6': # [
                stack.append('АЭМ')
                operand_count = 1
                array_index_mode = True
            elif token == 'R7': # ]
                while stack and stack[-1] != 'АЭМ':
                    out_seq += stack.pop() + ' '
                if stack:
                    out_seq += str(operand_count) + stack.pop() + ' '
                operand_count = 0
                array_index_mode = False
            elif token == 'R4': # ,
                if function_mode:
                    while stack and stack[-1] != 'Ф':
                        out_seq += stack.pop() + ' '
                    operand_count += 1
                elif stack and isinstance(stack[-1], tuple) and stack[-2] == 'R2':
                    stack[-1] = (stack[-1][0], stack[-1][1], stack[-1][2] + 1)
                else:
                    while stack and stack[-1] != 'АЭМ':
                        out_seq += stack.pop() + ' '
                    operand_count += 1
            elif token == 'W3':
                stack.append(token)
                if_mode = True
            elif token == 'R9': # {
                if if_mode:
                    while stack and stack[-1] != 'W3':
                        out_seq += stack.pop() + ' '
                    if stack:
                        label_count += 1
                        stack.append(f"M{label_count}")
                        out_seq += f"M{label_count} УПЛ "
            elif token == 'W4':
                while stack and stack[-1] != 'W3':
                    out_seq += stack.pop() + ' '
                #if stack:
                label_count += 2
                out_seq+=f"M{label_count} БП M{label_count}: "
                # if_mode = False
                    # stack.append(f"M{label_count}")
            # elif token == 'R10':
            #     stack.append(token)
            elif token == 'W13':
                procedure_mode = False
                return_mode = True
            elif token == 'R10':
                stack.append(token)
                if stack and isinstance(stack[-1], tuple) and stack[-1][0] == 'R2':
                    proc_num, proc_level, operand_count = stack.pop()[1], stack.pop()[2], stack.pop()[3]
                    out_seq+=f"КО {proc_num} {proc_level}"
                elif stack and stack[-1] == 'R10':
                    stack.pop()
                    while stack and stack[-1] != 'W14':
                        out_seq += stack.pop() + ' '
                    if stack:
                        stack.pop()
                    procedure_level -= 1
                    if procedure_level <0:
                        procedure_level = 0
                    if return_mode == True:
                        out_seq+=f"КП {procedure_count} {procedure_level} КО "
                        return_mode = False
                elif if_mode == True:
                    if_mode = False
                else:
                    out_seq+='\n'
            elif token == 'W14':
                stack.append(token)
                procedure_mode = True
            elif token!='R1':
                while stack and stack[-1] != 'R2' and (p <= get_priority(stack[-1]) or get_priority(stack[-1]) == -1):
                    if not isinstance(stack[-1], tuple):
                        out_seq += stack.pop() + ' '
                    else:
                        stack.pop()
                stack.append(token)
            i+=1
        while stack:
            if not isinstance(stack[-1], tuple):
                out_seq += stack.pop() + ' '
            else:
                stack.pop()
    except:
        error_type, error_instance, traceback = sys.exc_info()
        print(f"Error: {error_type.__name__}, {error_instance}")
    return out_seq




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

test_tokens_2 = '''I1 R1 O21 R1 W14 R2 I2 R4 R1 I3 R3 R1 R9 W13 R2 I2 R1 O1 R1 I3 R3 R8 R10 '''

if __name__ == '__main__':
    expressions = test_tokens.split()
    infix_to_postfix(expressions)
    print(infix_to_postfix(expressions))