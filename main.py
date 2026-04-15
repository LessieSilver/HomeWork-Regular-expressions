import csv
import re
from collections import defaultdict
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    contacts_list = list(csv.reader(f, delimiter=","))

for contact in contacts_list:
    fio = " ".join(contact[:3]).split()
    contact[:3] = fio + [""] * (3 - len(fio))

def format_phone(phone):
    if not phone or not phone.strip():
        return ""
    ext = re.search(r'доб\.?\s*(\d+)', phone, re.IGNORECASE)
    ext_str = f" доб.{ext.group(1)}" if ext else ""
    digits = re.sub(r'[^\d+]', '', phone)
    if digits.startswith('8') and len(digits) == 11:
        digits = '+7' + digits[1:]
    elif digits.startswith('7') and len(digits) == 11:
        digits = '+7' + digits[1:]
    elif len(digits) == 10:
        digits = '+7' + digits
    if len(digits) == 12 and digits.startswith('+7'):
        return f"+7({digits[2:5]}){digits[5:8]}-{digits[8:10]}-{digits[10:12]}" + ext_str
    return phone

for contact in contacts_list:
    if len(contact) > 5:
        contact[5] = format_phone(contact[5])

contacts_dict = defaultdict(list)
for contact in contacts_list[1:]:
    key = (contact[0].strip().lower(), contact[1].strip().lower())
    contacts_dict[key].append(contact)

result = [contacts_list[0]]
for group in contacts_dict.values():
    merged = [""] * len(result[0])
    for contact in group:
        for i in range(len(merged)):
            if i < len(contact) and not merged[i].strip():
                merged[i] = contact[i].strip()
    result.append(merged)

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows(result)

pprint(result)