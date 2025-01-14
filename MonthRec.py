import Receipt

class MonthRec:

    def __init__(self, month):
        self.month = month
        self.receipts = []

    def add_to_receipts(self, receipt):
        self.receipts.append(receipt)