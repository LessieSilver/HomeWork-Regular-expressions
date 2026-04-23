import csv
import re
from collections import defaultdict
from pprint import pprint


def normalize_text(text):
    return text.strip().lower().replace('ё', 'е') if text else ""


def format_phone(phone):
    if not phone or not phone.strip():
        return ""
    phone = phone.strip()

    ext_match = re.search(r'[дД][оО][бБ]\.?\s*(\d+)', phone)
    ext_part = f" доб.{ext_match.group(1)}" if ext_match else ""

    main_part = phone[:ext_match.start()].strip() if ext_match else phone

    digits = re.sub(r'[^\d+]', '', main_part)

    if digits.startswith('8') and len(digits) == 11:
        digits = '+7' + digits[1:]
    elif digits.startswith('7') and len(digits) == 11:
        digits = '+7' + digits[1:]
    elif len(digits) == 10:
        digits = '+7' + digits

    if len(digits) == 12 and digits.startswith('+7'):
        main_formatted = f"+7({digits[2:5]}){digits[5:8]}-{digits[8:10]}-{digits[10:12]}"
        return main_formatted + ext_part

    return phone


with open("phonebook_raw.csv", encoding="utf-8") as f:
    contacts_list = list(csv.reader(f, delimiter=","))

for contact in contacts_list:
    fio_parts = " ".join(contact[:3]).strip().split()
    contact[:3] = fio_parts + [""] * (3 - len(fio_parts))

for contact in contacts_list:
    if len(contact) > 5:
        contact[5] = format_phone(contact[5])

contacts_dict = defaultdict(list)

for contact in contacts_list[1:]:
    key = (normalize_text(contact[0]), normalize_text(contact[1]))
    contacts_dict[key].append(contact)

result = [contacts_list[0]]

for group in contacts_dict.values():
    merged = [""] * len(result[0])

    for contact in group:
        for i in range(len(merged)):
            if i < len(contact) and contact[i] and contact[i].strip():
                if not merged[i] or not merged[i].strip():
                    merged[i] = contact[i].strip()

    result.append(merged)

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows(result)

pprint(result, width=120)