from datetime import date
import re


def get_date(receipt, filepath):
    filepath = filepath.split("\\")[-2]
    month_list = [('jan', '01'), ('feb', '02'), ('mar', '03'), ('apr', '04'), ('may', '05'), ('jun', '06'),
                  ('jul', '07'),
                  ('aug', '08'), ('sep', '09'), ('oct', '10'), ('nov', '11'), ('dec', '12')]

    receipt_date_candidates_formatted = []

    if "PaypalIncome" in filepath or "PaypalOther" in filepath:
        print("This is a Paypal receipt!")
        # 1st/2nd/3d/4th monthname (yyyy)
        # eg. 1st jul
        # eg. 1st jul 1991
        possible_date_format = r'\d{1,2}(?:st|nd|rd|th)?\s\w{3,},?(?:,?\s\d{0,4})'
        receipt_date_candidates = re.findall(possible_date_format, receipt)
        # check for results

        if receipt_date_candidates:
            for receipt_date_candidate in receipt_date_candidates:
                # find the possible month words
                if includes_month(receipt_date_candidate):
                    # format to date iso format
                    receipt_date_candidate_formatted = format_date_to_iso(receipt_date_candidate,
                                                                          "alphabets_days_first")
                    receipt_date_candidates_formatted.append(receipt_date_candidate_formatted)

        if len(receipt_date_candidates_formatted) > 0:
            for receipt_date_candidate_formatted in receipt_date_candidates_formatted:
                if receipt_date_candidate_formatted is None:
                    return None
            receipt_date_candidates_formatted.sort()
            return receipt_date_candidates_formatted[0]
        else:
            return None

    if "Beatstars" in filepath or "Dropbox" in filepath or "Splice" in filepath or "Stripe" in filepath or "TubeBuddy" in filepath:

        print("This is a Beatstars/Dropbox/Splice/Stripe receipt!")
        # mmm 1st/2nd/3d/nth/n
        # eg. july 1st
        # eg. july 1 2022
        # eg july 1, 2022
        possible_date_format = r'\w{3,}\s\d{1,2},?(?:st|nd|rd|th)?(?:,?\s\d{0,4})'
        receipt_date_candidates = re.findall(possible_date_format, receipt)

        if receipt_date_candidates:
            for receipt_date_candidate in receipt_date_candidates:
                # find the possible month words
                if includes_month(receipt_date_candidate):
                    # format to date iso format
                    print("included the month!")
                    receipt_date_candidate_formatted = format_date_to_iso(receipt_date_candidate,
                                                                          "alphabets_months_first")
                    receipt_date_candidates_formatted.append(receipt_date_candidate_formatted)

        if len(receipt_date_candidates_formatted) > 0:
            for receipt_date_candidate_formatted in receipt_date_candidates_formatted:
                if receipt_date_candidate_formatted is None:
                    return None
            receipt_date_candidates_formatted.sort()
            return receipt_date_candidates_formatted[0]
        else:
            return None

    if "Adobe" in filepath:
        print("This is an Adobe receipt!")
        # dd-mmm.yyyy
        # eg. 01-JUN-1990
        possible_date_format = r'\d{1,2}[-][a-zA-Z]{3}[-]\d{4}'
        receipt_date_candidates = re.findall(possible_date_format, receipt)

        if receipt_date_candidates:
            for receipt_date_candidate in receipt_date_candidates:
                # find the possible month words
                if includes_month(receipt_date_candidate):
                    # format to date iso format
                    receipt_date_candidate_formatted = format_date_to_iso(receipt_date_candidate, "letters_middle")
                    receipt_date_candidates_formatted.append(receipt_date_candidate_formatted)

    if len(receipt_date_candidates_formatted) > 0:
        for receipt_date_candidate_formatted in receipt_date_candidates_formatted:
            if receipt_date_candidate_formatted is None:
                return None
        receipt_date_candidates_formatted.sort()
        return receipt_date_candidates_formatted[0]
    else:
        return None

    # dd-mm-yyyy OR dd.mm.yyyy
    possible_date_format = r'\d{1,2}\W\d{1,2}\W\d{4}'
    this_format_date_candidates = re.findall(possible_date_format, receipt)
    if this_format_date_candidates:

        for this_format_date_candidate in this_format_date_candidates:
            if 10 >= len(this_format_date_candidate) >= 8:

                # format to date iso format
                date_candidate = format_date_to_iso(this_format_date_candidate, "numbers_only")
                receipt_date_candidates.append(date_candidate)
            else:
                pass


def format_date_to_iso(date_candidate, type):
    month_list = [('jan', '01'), ('feb', '02'), ('mar', '03'), ('apr', '04'), ('may', '05'), ('jun', '06'),
                  ('jul', '07'),
                  ('aug', '08'), ('sep', '09'), ('oct', '10'), ('nov', '11'), ('dec', '12')]
    print("formatting to iso: " + date_candidate)
    print("date candidate type: " + type)

    if type == "numbers_only":
        date_candidate = re.sub('\W', '-', date_candidate)
        date_candidate = date_candidate.split('-')

        if len(date_candidate[1]) < 2:
            date_candidate[1] = "0" + date_candidate[1]

        if len(date_candidate[0]) < 2:
            date_candidate[0] = "0" + date_candidate[0]

        receipt_date = date_candidate[2] + "-" + date_candidate[1] + "-" + date_candidate[0]

        print("receipt date before validation: " + receipt_date)
        if date_is_valid(receipt_date):
            print("turned to iso format succesfully!")
            return date.fromisoformat(receipt_date)
        else:
            return None

    elif type == "letters_middle":

        # transform alphabet form month to numerical form
        for month_alph, month_num in month_list:
            if month_alph in date_candidate.lower():
                date_candidate = re.sub(month_alph + r'\w{0,6}', month_num, date_candidate)
                break
        date_candidate = date_candidate.split('-')

        if len(date_candidate[0]) == 1:
            date_candidate[0] = "0" + date_candidate[0]

        receipt_date = date_candidate[2] + "-" + date_candidate[1] + "-" + date_candidate[0]

        print("receipt date before validation: " + receipt_date)
        if date_is_valid(receipt_date):
            print("turned to iso format succesfully!")
            return date.fromisoformat(receipt_date)
        else:
            return None
    else:
        contains_year = False

        # look for the year
        if date_candidate[-1].isdigit() and date_candidate[-2].isdigit() and date_candidate[-3].isdigit():
            contains_year = True

        # transform alphabet form month to numerical form

        for month_alph, month_num in month_list:
            if month_alph in date_candidate.lower():
                date_candidate = re.sub(month_alph + r'\w{0,6}', month_num, date_candidate)
                break

        # remove possible st, nd, rd, th from date

        date_candidate = re.sub('st|nd|rd|th', '', date_candidate)

        # split to year, month and date

        date_candidate = date_candidate.split()

        # if the date contains a year, use it, otherwise use the current year

        year = None
        if contains_year:
            year = date_candidate[2]
        else:
            year = str(date.today().year)

        # remove non-numerics
        date_candidate[0] = re.sub('\D', '', date_candidate[0])
        date_candidate[1] = re.sub('\D', '', date_candidate[1])

        # if either month or day has only one digit insert a 0 to the beginning

        if len(date_candidate[1]) < 2:
            date_candidate[1] = "0" + date_candidate[1]

        if len(date_candidate[0]) < 2:
            date_candidate[0] = "0" + date_candidate[0]

        if type == "alphabets_days_first":
            receipt_date = year + "-" + date_candidate[1] + "-" + date_candidate[0]
            print("receipt date before validation: " + receipt_date)
            if date_is_valid(receipt_date):
                return date.fromisoformat(receipt_date)
            else:
                return None
        elif type == "alphabets_months_first":
            receipt_date = year + "-" + date_candidate[0] + "-" + date_candidate[1]
            print("receipt date before validation: " + receipt_date)
            if date_is_valid(receipt_date):
                return date.fromisoformat(receipt_date)
            else:
                return None


def includes_month(this_format_date_candidate):
    print("checking the month...")
    print("the month format: " + this_format_date_candidate)
    month_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    if this_format_date_candidate is not None:
        print(this_format_date_candidate)
        letter_month_candidate = re.search(r'\w{3,}', this_format_date_candidate)
        letter_month_candidate = letter_month_candidate.group()
        # check if the dates are acceptable
        for month in month_list:
            # check if there are actual month names
            if month in letter_month_candidate.lower():
                return True

    return False


def date_is_valid(date_to_check):
    date_splitted = date_to_check.split('-')
    date_year = date_splitted[0]
    date_month = date_splitted[1]
    date_day = date_splitted[2]

    date_year_is_correct = False
    date_month_is_correct = False
    date_day_is_correct = False

    if len(date_year) == 4 and 0 < int(date_year) <= int(date.today().strftime("%Y")):
        date_year_is_correct = True
    if len(date_month) == 2 and 12 >= int(date_month) > 0:
        date_month_is_correct = True
    if 31 >= int(date_day) > 0 and len(date_day) == 2:
        date_day_is_correct = True

    if date_year_is_correct and date_month_is_correct and date_day_is_correct:
        return True
    else:
        return False