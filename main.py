
import ReceiptReader
import ReceiptHandler
import FileHandler
import ExcelHandler


from Receipt import Receipt
from MonthRec import MonthRec


if __name__ == '__main__':


    receipt_folder = r''
    new_receipt_dir = r''
    excel_file_path = r''


    print("reading receipts\n")
    receipts_data = ReceiptReader.read_receipts(receipt_folder)
    print("read receipts\n")
    receipts = []

    for i, (filepath, receipt_data) in enumerate(receipts_data):

        if "Adobe" in filepath and "_02" in filepath:
            continue
        print (f"reading {i+1}/{len(receipts_data)}\n")

        receipt_type = None
        currency = None
        amount = None
        receipt_date = None
        tax_cat = None
        explanation = None

        receipt_type, tax_cat, explanation = ReceiptHandler.get_type_and_categories(filepath)
        amount, currency = ReceiptHandler.get_currency_and_amount(receipt_data, receipt_type)
        if receipt_type == "meno" and amount is not None:
            amount = -1 * amount
        receipt_date = ReceiptHandler.get_date(receipt_data, filepath)

        if receipt_date is not None:
            receipt = Receipt(receipt_date, currency,  amount, receipt_type, tax_cat, explanation, filepath)
            receipts.append(receipt)
        else:
            print(f"{filepath} needs to be inserted manually")
        print("----------------------------------------------------------------------------------------------------------------------")
    month_recs = []

    receipts.sort(key=lambda receipt: receipt.receipt_date)

    # assign an id and place in a MonthRec object
    month_idx = None
    month_rec = None
    for idx, receipt in enumerate(receipts):
        print("assigning receipt: " + receipt.filepath)
        print(receipt.receipt_date)
        if idx == 0 or receipt.receipt_date.month != receipts[idx - 1].receipt_date.month:
            month_idx = 1
            month_rec = MonthRec(receipt.receipt_date.strftime("%B"))
            month_recs.append(month_rec)
        receipt.create_id(month_idx)
        month_rec.add_to_receipts(receipt)
        month_idx += 1

        # change file name
        new_path = FileHandler.create_new_path(receipt.filepath, new_receipt_dir, receipt.id)
        FileHandler.copy_receipt_imagefiles(receipt.filepath, new_path)


    # insert data to excel

    ExcelHandler.insert_receipts_to_excel(month_recs, excel_file_path)

    for month_rec in month_recs:
        for receipt_idx, receipt in enumerate(month_rec.receipts):
            print("Month : " + str(month_rec.month) + "\nReceipt number: " + str(receipt_idx + 1))
            print(f"Receipt date:  {receipt.receipt_date}")
            print(f"Receipt currency:  {receipt.currency}")
            print(f"Receipt amount:  {receipt.amount}")
            print(f"Receipt type:  {receipt.tax_cat}")
            print(f"Receipt tax category:  {receipt.tax_cat}")
            print(f"Receipt explanation:  {receipt.explanation}")
            print(f"Receipt file path:  {receipt.filepath}")
            print(f"Receipt id:  {receipt.id}")
            print("\n-----------------------------------------------------------------\n")



