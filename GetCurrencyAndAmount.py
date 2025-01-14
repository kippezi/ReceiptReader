import re


def get_currency_and_amount(receipt, receipt_type):

    amount_type = 'net'
    if receipt_type == "tulo":
        if 'fee' in receipt:
            amount_type = 'fee'

    print(f"receipt type: {receipt_type}")
    print(f"amount type: {amount_type}")

    # look for indication for money

    possible_money_format = r'''
    [€$¥]\s?\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d{1,2})?\s?|  # Currency with symbols
    \d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d{1,2})?\s?[€$¥円]|  # Currency with symbols
    \(?euro?\)?\s?\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d{1,2})?|          # Euro amounts (text)
    \(?usd?\)?\s?\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d{1,2})?            # USD amounts (text)
'''

    # Extract possible money values
    possible_money_values = re.findall(possible_money_format, receipt, re.VERBOSE)

    # Initialize lists
    euro_values = []
    dollar_values = []
    yen_values = []


    # Process extracted values
    for value in possible_money_values:
        # Normalize the value (remove whitespace and handle commas/dots)
        value = value.strip()
        value = value.replace(',', '.')  # Ensure decimal point is standardized

        # Process Euros
        if '€' in value or 'eur' in value:
            numeric_value = float(re.sub(r'[^\d.-]', '', value))
            if numeric_value < 500:  # Filter small Euro values
                euro_values.append(numeric_value)

        # Process Dollars
        elif '$' in value or 'usd' in value:
            numeric_value = float(re.sub(r'[^\d.-]', '', value))
            if numeric_value < 500:  # Filter small Dollar values
                dollar_values.append(numeric_value)

        # Process Yen
        elif '¥' in value or '円' in value:
            value = value.replace('.', '')  # Change . of thousands etc to nothing
            numeric_value = float(re.sub(r'[^\d.-]', '', value))
            if numeric_value < 100000:  # Filter large Yen values
                yen_values.append(numeric_value)

    # Determine currency and print results

    if euro_values:
        currency = 'euro'
        values = euro_values
    elif dollar_values:
        currency = 'dollar'
        values = dollar_values
    elif yen_values:
        currency = 'yen'
        values = yen_values
    else:
        print("THERE WERE NO MONEY VALUES IN THE RECEIPT")
        currency = None
        values = []

    if any(values):
        values.sort()

        # Find out which of the values is the final value
        if receipt_type == 'tulo':
            if amount_type == 'net':
                amount = values[-1]
            elif amount_type == 'fee':
                amount = values[-2]
            else:
                amount = None
        else:
            amount = values[-1]
    else:
        amount = None
    print(f"amount: {amount}, currency: {currency}")
    return amount, currency
