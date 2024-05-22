import re

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from lexicalAnalyzer import *
from reversePolishNotation import *
from PyQt5 import uic
from translator import *
from syntaxAnalyser import Tokenizer, Parser

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

def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

def replace_identifiers(tokens, identificators):
    for ident in identificators.values():
        tokens = re.sub(f"I{ident}", get_key_by_value(identificators, ident), tokens)
    return tokens

def replace_constants(tokens, constants):
    for const in constants.values():
        tokens = re.sub(f"C{const}", get_key_by_value(constants, const), tokens)
    return tokens


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file
        uic.loadUi('main-window.ui', self)
        self.runButton.clicked.connect(lambda: self.lexicalAnalyzis())

    def lexicalAnalyzis(self):

        self.idTable.clearContents()
        self.constTable.clearContents()
        self.tokensOutput.setPlainText('')
        self.rpnOutput.setPlainText('')
        self.phpOutput.setPlainText('')
        self.syntaxAnalyser.setPlainText('')

        input = self.inputProgram.toPlainText()
        output, constants, identificators = analyze(input)
        output = re.sub(r'\n', r'', output)
        self.tokensOutput.insertPlainText(output)
        self.populate_tables(identificators, constants)
        tokenizer = Tokenizer(output)
        parser = Parser(tokenizer)
        errors = parser.program()
        if errors:
            errors = '\n'.join(errors)
            self.syntaxAnalyser.insertPlainText(errors)
        else:
            self.syntaxAnalyser.insertPlainText('Parsing finished successfully')
            postfix = infix_to_postfix(output.split())
            self.rpnOutput.insertPlainText(postfix)
            rpn_tokens = postfix.split()
            mp_automaton = MPAutomaton()
            output = mp_automaton.translate(rpn_tokens)
            output = ' '.join(output)
            output = replace_identifiers(output, identificators)
            output = replace_constants(output, constants)
            self.phpOutput.insertPlainText(output)



    def populate_tables(self, identificators, constants):
        self.idTable.setRowCount(len(identificators))

        for row, (ident, value) in enumerate(identificators.items()):
            self.idTable.setItem(row, 0, QTableWidgetItem(ident))
            self.idTable.setItem(row, 1, QTableWidgetItem(str(value)))

        self.idTable.resizeColumnsToContents()

        self.constTable.setRowCount(len(constants))

        for row, (constant, value) in enumerate(constants.items()):
            self.constTable.setItem(row, 0, QTableWidgetItem(constant))
            self.constTable.setItem(row, 1, QTableWidgetItem(str(value)))

        self.constTable.resizeColumnsToContents()




