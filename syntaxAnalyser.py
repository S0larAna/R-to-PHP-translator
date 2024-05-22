import re

# Лексический анализатор
class Tokenizer:
    def __init__(self, code):
        tokens = list(filter(('R1').__ne__, code.split()))
        self.tokens = list(filter(('R8').__ne__, tokens))
        self.current_token_index = 0

    def next_token(self):
        if self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            self.current_token_index += 1
            return token
        return None

    def peek_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

# Синтаксический анализатор
class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.next_token()
        self.errors = []

    def error(self, message):
        self.errors.append(f"Syntax error: {message} {self.current_token} ")

    def eat(self, token_type):
        if self.current_token is None:
            return
        elif self.current_token == token_type:
            self.current_token = self.tokenizer.next_token()
        else:
            self.error(f"Expected {token_type}, got {self.current_token}")

    def program(self):
        while self.current_token is not None:
            self.statement()
        return self.errors

    def statement(self):
        if self.current_token == 'W3':
            self.if_statement()
        elif self.current_token == 'W6':
            self.while_statement()
        elif self.current_token == 'W7':
            self.for_statement()
        elif self.current_token == 'W14':
            self.function_definition()
        elif self.current_token == 'W13':
            self.return_statement()
        elif self.current_token == 'W5':
            self.print_statement()
        else:
            self.assignment()

    def print_statement(self):
        self.eat('W5')
        self.eat('R2')
        if not self.is_ident(self.current_token) and not self.is_const(self.current_token):
            self.error("Expected identifier or constant")
        self.eat(self.current_token)
        self.eat('R3')

    def if_statement(self):
        self.eat('W3')
        self.eat('R2')
        self.expression()
        self.eat('R3')
        self.block()
        if self.current_token == 'W4':
            self.eat('W4')
            self.block()

    def return_statement(self):
        self.eat('W13')
        self.expression()

    def while_statement(self):
        self.eat('W6')
        self.eat('R2')
        self.expression()
        self.eat('R3')
        self.block()

    def for_statement(self):
        self.eat('W7')
        self.eat('R2')
        self.assignment()
        self.eat('R12')
        self.expression()
        self.eat('R12')
        self.assignment()
        self.eat('R3')
        self.block()

    def function_definition(self):
        self.eat('W14')
        self.eat('R2')
        while self.current_token != 'R3':
            self.eat(self.current_token)
            if self.current_token == 'R4':
                self.eat('R4')
        self.eat('R3')
        self.block()

    def assignment(self):
        if not self.is_ident(self.current_token) and not self.current_token != 'W14' and not self.current_token[0]!='C':
            self.error("Expected identifier")
        self.eat(self.current_token)
        if self.current_token == 'O21':
            self.eat('O21')
        else:
            self.error(f"Expected <- for assignment")
        if self.current_token == 'W14':
            self.function_definition()
        else:
            self.expression()

    def block(self):
        self.eat('R9')
        while self.current_token != 'R10':
            self.statement()
        self.eat('R10')

    def expression(self):
        self.term()
        while self.current_token in ['O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'O11', 'O12', 'O9', 'O10', 'O13', 'O14', 'O16',
                                     'O17', 'O18', 'O19', 'O20', 'O22', 'O23', 'W14']:
            self.eat(self.current_token)
            self.term()

    def term(self):
        self.factor()
        while self.current_token in ['O3', 'O4']:
            self.eat(self.current_token)
            self.factor()

    def factor(self):
        if self.current_token == 'R2':
            self.eat('R2')
            self.expression()
            self.eat('R3')
        elif self.is_const(self.current_token):
            self.eat(self.current_token)
        elif self.is_ident(self.current_token):
            ident = self.current_token
            self.eat(self.current_token)
            if self.current_token == 'R2':
                self.function_call(ident)
            elif self.current_token == 'R6':
                self.array_access(ident)
            elif self.current_token == 'O21':
                self.eat('O21')
                if not self.is_ident(self.current_token) and not self.current_token != 'W14' and not self.current_token[0]!='C':
                    self.error("Expected identifier")
                self.eat(self.current_token)
                self.statement()
            else:
                while self.current_token in ['O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'O11', 'O12', 'O9', 'O10',
                                             'O13', 'O14', 'O16',
                                             'O17', 'O18', 'O19', 'O20', 'O22', 'O23', 'W14']:
                    self.eat(self.current_token)
                    self.term()
        elif self.current_token == 'W14':
            self.eat(self.current_token)
        else:
            self.error("Expected constant or identifier")

    def array_access(self, ident):
        self.eat('R6')
        self.expression()
        self.eat('R7')

    def function_call(self, ident):
        self.eat('R2')
        while self.current_token != 'R3':
            self.expression()
            if self.current_token == 'R4':
                self.eat('R4')
        self.eat('R3')

    def is_ident(self, token):
        if token:
            return token[0] == 'I'

    def is_const(self, token):
        if token:
            return token[0] == 'C'

# Пример использования
# code = """I1 R1 O21 R1 W14 R2 I2 R3 R1 R9 R8 R1 R1 R1 R1 W3 R2 I2 R1 O9 R1 C1 R1 O18 R1 I2 R1 O9 R1 C2 R3 R1 R9 R8 R1 R1 R1 R1 W13 R2 C2 R3 R8 R1 R1 R10 R1 W4 R1 R9 R8 R1 R1 R1 R1 R1 R1 R1 R1 W13 R2 I2 R1 O3 R1 I1 R2 I2 O2 C2 R3 R3 R8 R1 R1 R10 R8 R10 R8 R8 I3 R1 O21 R1 C3 R1 R8 R8 R8 I4 R1 O21 R1 I1 R2 I3 R3 R8 R8 W5 R2 I4 R3 R8 """
#
# tokenizer = Tokenizer(code)
# parser = Parser(tokenizer)
# parser.program()
# print("Parsing completed successfully.")
