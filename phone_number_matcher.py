import re

with open("phone_numbers.txt", "r") as input_file_handle:
        lines = input_file_handle.readlines()

for line in lines:
    matches = re.findall(r"(\(?0?1?\)?\s?1?-?[0-9]{3}[0-9]?-?\s?[0-9]{3}[0-9]?-?[0-9]{0,4})|(\+32\s4[0-9]{2}\s[0-9]{2}\s[0-9]{2}\s[0-9]{2})|(0?[0-9]{0,1}\s?[0-9]{2}\s[0-9]{2}\s[0-9]{2}\s[0-9]{2})", line)  # noqa
    #  for match in matches:
    for match in matches:
        if match != "":
            for m in match:
                if m != "":
                    print(m)
