
with open('state_codes.txt', 'r') as f:
    file_contents = f.read()

print("".join(file_contents.split()))

with open('state_codes.txt', 'w') as f:
    f.write("state_dict = { " + file_contents + " } ")
