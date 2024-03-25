from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from lexicalAnalyzer import *
from PyQt5 import uic


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

        input = self.inputProgram.toPlainText()
        output, constants, identificators = analyze(input)
        self.tokensOutput.insertPlainText(output)
        self.populate_tables(identificators, constants)

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




