
class Receipt:
    def __init__(self, receipt_date, currency,  amount, receipt_type, tax_cat, explanation, filepath):
        self.receipt_date = receipt_date
        self.currency = currency
        self.amount = amount
        self.receipt_type = receipt_type
        self.tax_cat = tax_cat
        self.explanation = explanation
        self.filepath = filepath
        self.id = None

    def create_id(self, index):
        date_part = self.receipt_date.strftime("%m")
        self.id = f'{date_part}_{index}'

    def __str__(self):
        return (
        f"date: {self.receipt_date}, currency: {self.currency}, amount: {self.amount}, receipt_type: {self.receipt_type}, tax_cat: {self.tax_cat},"
        f"explanation: {self.explanation}, id: {self.id}"
        )