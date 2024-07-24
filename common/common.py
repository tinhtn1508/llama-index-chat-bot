import re

pattern01 = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b'
pattern02 = r'\b\d{4}-\d{2}-\d{2}\b'

month_map = {
    "January": "Jan",
    "February": "Feb",
    "March": "Mar",
    "April": "Apr",
    "May": "May",
    "June": "Jun",
    "July": "Jul",
    "August": "Aug",
    "September": "Sep",
    "October": "Oct",
    "November": "Nov",
    "December": "Dec",
}

convert_month = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec"
}

def extract_dates(raw_string: str) -> list:
    for key, value in month_map.items():
        raw_string = raw_string.replace(key, value)
    raw_string = raw_string.replace(" 0", " ")
    matches = re.findall(pattern01, raw_string)
    date = []
    for match in matches:
        if "," in match:
            date.append(match)
        else:
            token = match.split(" ")
            date.append(f"{token[0]} {token[1]}, {token[2]}")
    if len(date) > 0:
        return date
    matches = re.findall(pattern02, raw_string)
    for match in matches:
        token = match.split("-")
        date.append(f"{convert_month[token[1]]} {token[2]}, {token[0]}")
    return date

def extract_urls(raw_string: str) -> str:
    urls = re.findall(r'(https?://[^\s]+)', raw_string)
    return urls