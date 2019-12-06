import re


def check_password(password):
    repeats = re.findall(r"((\d)\2+)", str(password))
    repeats_two = False
    for repeat in repeats:
        # print(repeat)
        if len(repeat[0]) == 2:
            repeats_two = True

    digits = [int(char) for char in str(password)]
    increasing = (
        digits[0] <= digits[1] <= digits[2] <= digits[3] <= digits[4] <= digits[5]
    )
    return repeats_two and increasing


def enumerate_passwords(start, end):
    all_passwords = [x for x in range(start, end + 1) if check_password(x)]
    return all_passwords


if __name__ == "__main__":
    START = 240298
    END = 784956
    # START = 123456
    # END = 223344
    matching_passwords = enumerate_passwords(START, END)
    print(matching_passwords)
    print(len(matching_passwords))

