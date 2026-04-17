import csv
import re
from collections import defaultdict
from pprint import pprint


def normalize_for_comparison(text):
    return text.strip().lower().replace('ё', 'е') if text else ""


def format_phone(phone):
    if not phone or not phone.strip():
        return ""
    phone = phone.strip()

    ext = re.search(r'доб\.?\s*(\d+)', phone, re.IGNORECASE)
    extension = f" доб.{ext.group(1)}" if ext else ""
    main_part = phone[:ext.start()].strip() if ext else phone

    digits = re.sub(r'[^\d+]', '', main_part)
    if digits.startswith('8') and len(digits) == 11:
        digits = '+7' + digits[1:]
    elif digits.startswith('7') and len(digits) == 11:
        digits = '+7' + digits[1:]
    elif len(digits) == 10:
        digits = '+7' + digits

    if len(digits) == 12 and digits.startswith('+7'):
        return f"+7({digits[2:5]}){digits[5:8]}-{digits[8:10]}-{digits[10:12]}" + extension
    return phone


with open("phonebook_raw.csv", encoding="utf-8") as f:
    contacts_list = list(csv.reader(f, delimiter=","))

for contact in contacts_list:
    fio = " ".join(contact[:3]).strip()
    parts = fio.split()
    contact[:3] = parts + [""] * (3 - len(parts))

for contact in contacts_list:
    if len(contact) > 5:
        contact[5] = format_phone(contact[5])

contacts_dict = defaultdict(list)
for contact in contacts_list[1:]:
    key = (normalize_for_comparison(contact[0]), normalize_for_comparison(contact[1]))
    contacts_dict[key].append(contact)

result = [contacts_list[0]]
for group in contacts_dict.values():
    if len(group) == 1:
        result.append(group[0])
    else:
        merged = [""] * len(result[0])
        for contact in group:
            for i in range(min(len(merged), len(contact))):
                if not merged[i] or not merged[i].strip():
                    val = contact[i].strip() if i < len(contact) and contact[i] else ""
                    if val:
                        merged[i] = val
        result.append(merged)

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows(result)

pprint(result, width=120)