import cv2
import pytesseract
import os
import pdfplumber


def read_receipts(folder_location):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    files_to_read = []
    for root, dirs, files in os.walk(folder_location):
        for name in files:
            files_to_read.append(os.path.join(root, name))
            print((os.path.join(root, name)))

    # Go through all the folders and store them in text form if they are valid files
    receipt_texts = []
    for file in files_to_read:
        # Check if valid file
        if os.path.isfile(file) and (file.split(".")[-1].lower() == 'jpg' or file.split(".")[-1].lower() == 'png'):
            img = cv2.imread(file)
            text = pytesseract.image_to_string(img)
            text = text.lower()
            receipt_texts.append((file, text))

        elif os.path.isfile(file) and file.split(".")[-1].lower() == 'pdf':
            text = []
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text.append(page.extract_text())

            text = " ".join(text)
            text = text.lower()
            receipt_texts.append((file, text))
        else:
            print("ERROR: FILE COULD NOT BE READ!")

    return receipt_texts


