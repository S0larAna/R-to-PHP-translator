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
PRIORITY10 = ['W14', 'R10', 'R9']


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
    i = 0
    stack = []
    out_seq = ''
    aem_count = proc_num = proc_level = operand_count = 1
    func_count = tag_count = proc_num = if_count = while_count = \
        begin_count = end_count = bracket_count = args_count = 0
    is_if = is_while = is_description_var = is_function = False
    while i < len(t):
        p = get_priority(t[i])
        if p == -1:
            if t[i] != '\n' and t[i] != '\t':
                out_seq += t[i] + ' '
        else:
            if t[i] == 'R6':
                aem_count += 1
                stack.append(str(aem_count) + ' АЭМ')
            elif t[i] == 'R7':
                while not (re.match(r'^\d+ АЭМ$', stack[-1])):
                    out_seq += stack.pop() + ' '
                out_seq += stack.pop() + ' '
                aem_count = 1
            elif t[i] == 'R2':
                if is_identifier(t[i - 1]):
                    if t[i + 1] != 'R3':
                        func_count += 1
                    stack.append(str(func_count) + ' Ф')
                else:
                    stack.append(t[i])
                bracket_count += 1
            elif t[i] == 'R2':
                while stack[-1] != 'R3' and not (re.match(r'^\d+ Ф$', stack[-1])):
                    out_seq += stack.pop() + ' '
                if re.match(r'^\d+ Ф$', stack[-1]):
                    stack.append(str(func_count + 1) + ' Ф')
                    func_count = 0
                stack.pop()
                bracket_count -= 1
                if bracket_count == 0:
                    if is_if:
                        while stack[-1] != 'W3':
                            out_seq += stack.pop() + ' '
                        tag_count += 1
                        stack[-1] += ' М' + str(tag_count)
                        out_seq += 'М' + str(tag_count) + ' УПЛ '
                        is_if = False
                    if is_while:
                        while not (re.match(r'^while М\d+$', stack[-1])):
                            out_seq += stack.pop() + ' '
                        tag_count += 1
                        out_seq += 'М' + str(tag_count) + ' УПЛ '
                        stack[-1] += ' М' + str(tag_count)
                        is_while = False
            elif t[i] == 'R4':
                while not (re.match(r'^\d+ АЭМ$', stack[-1])) and \
                        not (re.match(r'^\d+ Ф$', stack[-1])) and \
                        not (re.match(r'^var', stack[-1])):
                    out_seq += stack.pop() + ' '
                if re.match(r'^\d+ АЭМ$', stack[-1]):
                    aem_count += 1
                    stack.append(str(aem_count) + ' АЭМ')
                if re.match(r'^\d+ Ф$', stack[-1]):
                    func_count += 1
                    stack.append(str(func_count) + ' Ф')
            elif t[i] == 'R3':
                stack.append(t[i])
                if_count += 1
                bracket_count = 0
                is_if = True
            elif t[i] == 'R4':
                while not (re.match(r'^if М\d+$', stack[-1])):
                    out_seq += stack.pop() + ' '
                stack.pop()
                tag_count += 1
                stack.append('if М' + str(tag_count))
                out_seq += 'М' + str(tag_count) + ' БП М' + str(tag_count - 1) + ' : '
            elif t[i] == 'R6':
                tag_count += 1
                stack.append(t[i] + ' М' + str(tag_count))
                out_seq += 'М' + str(tag_count) + ' : '
                while_count += 1
                bracket_count = 0
                is_while = True
            elif t[i] == 'O21':
                j = i + 1
                while t[j] == 'R1':
                    j += 1
                if t[j] == 'W14':
                    proc_num += 1
                    i += (j - i)
                    stack.append('НП ' + str(proc_num) + ' ' + str(proc_level) + ' ')
                    is_function = True
                else:
                    stack.append('O21')
            elif t[i] == 'R7':
                j = i + 2
                bracket_count = 1
                a = []
                while t[j] != ';':
                    a.append(t[j])
                    j += 1
                    if t[j] == '(':
                        bracket_count += 1
                    elif t[j] == ')':
                        bracket_count -= 1
                j += 1
                b = []
                while t[j] != ';':
                    b.append(t[j])
                    j += 1
                    if t[j] == '(':
                        bracket_count += 1
                    elif t[j] == ')':
                        bracket_count -= 1
                j += 1
                c = []
                while bracket_count != 0:
                    c.append(t[j])
                    j += 1
                    if t[j] == '(':
                        bracket_count += 1
                    elif t[j] == ')':
                        bracket_count -= 1
                j += 1
                d = []
                while t[j] != ';' and t[j] != '{':
                    d.append(t[j])
                    j += 1
                if t[j] == '{':
                    j += 1
                    bracket_count = 1
                    d = ['{']
                    while bracket_count != 0:
                        d.append(t[j])
                        j += 1
                        if t[j] == '{':
                            bracket_count += 1
                        elif t[j] == '}':
                            bracket_count -= 1
                    d.append('}')
                j += 1
                t = t[:i] + a + [';', '\n', 'while', '('] + b + [')', '{', '\n'] + d + \
                    ['\n'] + c + [';', '\n', '}'] + t[j:]
                i -= 1
            elif t[i] == 'W14':
                proc_num += 1
                stack.append('PROC ' + str(proc_num) + ' ' + str(proc_level))
            elif t[i] == 'R9':
                if len(stack) > 0 and re.match(r'^PROC', stack[-1]):
                    num = re.findall(r'\d+', stack[-1])
                    stack.pop()
                    out_seq += '0 Ф ' + str(num[0]) + ' ' + str(num[1]) + ' НП '
                    stack.append('PROC ' + str(proc_num) + ' ' + str(proc_level))
                begin_count += 1
                proc_level = begin_count - end_count + 1
                stack.append(t[i])
            elif t[i] == 'R10':
                end_count += 1
                proc_level = begin_count - end_count + 1
                while stack and stack[-1] != 'R9':
                    out_seq += stack.pop() + ' '
                if stack:
                    stack.pop()
                if len(stack) > 0 and stack and re.match(r'^PROC', stack[-1]):
                    stack.pop()
                    out_seq += 'КП '
                if if_count > 0 and stack and re.match(r'^if М\d+$', stack[-1]):
                    tag = re.search('М\d+', stack[-1]).group(0)
                    j = i + 1
                    while j < len(t) and t[j] == '\n':
                        j += 1
                    if j >= len(t) or t[j] != 'R4':
                        stack.pop()
                        out_seq += tag + ' : '
                        if_count -= 1
                if while_count > 0 and re.match(r'^while М\d+ М\d+$', stack[-1]):
                    tag = re.findall('М\d+', stack[-1])
                    stack.pop()
                    out_seq += tag[0] + ' БП ' + tag[1] + ' : '
                    while_count -= 1
            elif t[i] == 'R8':
                if len(stack) > 0 and re.match(r'^PROC', stack[-1]):
                    num = re.findall(r'\d+', stack[-1])
                    stack.pop()
                    out_seq += str(num[0]) + ' ' + str(num[1]) + ' НП '
                elif len(stack) > 0 and stack[-1] == 'end':
                    stack.pop()
                    out_seq += 'КП '
                elif is_description_var:
                    proc_num, proc_level = re.findall('\d+', stack[-1])
                    stack.pop()
                    out_seq += str(operand_count) + ' ' + proc_num + ' ' + proc_level + \
                               ' КО '
                    is_description_var = False
                elif if_count > 0 or while_count > 0:
                    while not (len(stack) > 0 and stack[-1] == 'R9') and \
                            not (if_count > 0 and re.match(r'^if М\d+$', stack[-1])) and \
                            not (while_count > 0 and re.match(r'^while М\d+ М\d+$', stack[-1])):
                        out_seq += stack.pop() + ' '
                    if if_count > 0 and re.match(r'^if М\d+$', stack[-1]):
                        tag = re.search('М\d+', stack[-1]).group(0)
                        j = i + 1
                        while t[j] == '\n':
                            j += 1
                        if t[j] != 'else':
                            stack.pop()
                        out_seq += tag + ' : '
                        if_count -= 1
                    if while_count > 0 and re.match(r'^while М\d+ М\d+$', stack[-1]):
                        tag = re.findall('М\d+', stack[-1])
                        out_seq += tag[0] + ' БП ' + tag[1] + ' : '
                        while_count -= 1
                else:
                    while len(stack) > 0 and stack[-1] != 'R9':
                        out_seq += stack.pop() + ' '
            else:
                while len(stack) > 0 and get_priority(stack[-1]) >= p:
                    out_seq += stack.pop() + ' '
                stack.append(t[i])
        i += 1
        print(out_seq)

    while len(stack) > 0:
        out_seq += stack.pop() + ' '
    print(out_seq)
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

if __name__ == '__main__':
    expressions = test_tokens.split()
    infix_to_postfix(expressions)