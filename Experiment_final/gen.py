import random

def generate_random_code():
    code_list = []
    for a in range(12):
        for b in range(64):
            random_num = random.randint(1, 10000)
            code_list.append(f"{a} {b} {random_num}")
    return code_list

random_code = generate_random_code()

with open("data.txt", "w") as file:
    for code in random_code:
        file.write(code + "\n")
