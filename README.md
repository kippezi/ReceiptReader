# Receipt Reader

Receipt Reader is a specialized program developed for personal use, uploaded to GitHub for presentation purposes. Its primary function is to process receipt images or PDFs, extract relevant financial data, and write the data to an Excel file for simple accounting. The program supports both machine vision (for images) and direct PDF content extraction.

## Features

- **Process Receipts**: Reads receipt data from images or PDFs.
- **Excel Integration**: Writes extracted data to an Excel file, organized by date, amount, currency, and category.
- **Automated Calculations**: Leverages a pre-formatted Excel template with built-in formulas for accounting.
- **File Management**: Stores processed receipts in a structured directory with corresponding IDs.

## Project Structure

### Main Components

1. **`excel_handler`**  
   Handles all data inputs to the Excel file.  

2. **`file_handler`**  
   Manages file operations, such as organizing processed receipts into directories with IDs matching those in the Excel file.  

3. **`get_currency_and_amount`**  
   Contains the `get_currency_and_amount` method, which is used by the `receipt_handler` to extract currency and amount information from receipts.  

4. **`get_date`**  
   Includes the `get_date` method and its sub-methods, used by the `receipt_handler` to retrieve date information from receipts.  

5. **`month_rec`**  
   Includes A class that organizes receipts by month for insertion into the appropriate Excel sheet (MonthRec).  

6. **`receipt`**  
   Included a class that represents individual receipt objects (Receipt).  

7. **`receipt_handler`**  
   A module that handles receipt processing, including identifying receipt categories, amounts, and currencies.  

8. **`receipt_reader`**  
   Reads receipt data from image files using machine vision or directly from PDFs.  

9. **`main`**  
   The main entry point of the program, orchestrating the logic and calling functions from other modules.

## How It Works

1. **Input**: Provide receipt files in either image or PDF format.  
2. **Processing**:  
   - Images: Machine vision extracts data such as date, amount, and currency.  
   - PDFs: Direct text extraction is performed.  
3. **Output**: Data is written into a structured Excel file, categorized by month and receipt type.  
4. **File Handling**: Processed receipts are stored in a new directory with unique IDs.

## Requirements (not included in github as it is meant only for presenting)

- Python 3.x
- Libraries: pdfplumber, Tesseract OCR, OpenCV, openpyxl 

