import GetDate
import GetCurrencyAndAmount

# look through the receipt to find whether it is an income or expense and the tax_cat and explanation


def get_type_and_categories(file_path):

    if "PaypalIncome" in file_path or "Stripe" in file_path:
        receipt_type = "tulo"
        explanation = "musiikin vuokraus"
        tax_cat = None
        return receipt_type, tax_cat, explanation

    if "PaypalOther" in file_path:
        receipt_type = "meno"
        tax_cat = "pienhankinta"
        explanation = "työkalukulut"
        return receipt_type, tax_cat, explanation
    else:
        receipt_type = "meno"
        explanation = "vuokrakulut"
        tax_cat = None
        return receipt_type, tax_cat, explanation

# look for currency (if there is € sum, use that)



def get_currency_and_amount(receipt, receipt_type):
    return GetCurrencyAndAmount.get_currency_and_amount(receipt, receipt_type)

def get_date(receipt_data, filepath):
    return GetDate.get_date(receipt_data, filepath)