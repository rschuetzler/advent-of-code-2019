import re


def check_password(password):
    repeats_two = re.search(r"(\d)\1", str(password))
    repeats_three = re.search(r"(\d)\1\1", str(password))
    digits = [int(char) for char in str(password)]
    increasing = (
        digits[0] <= digits[1] <= digits[2] <= digits[3] <= digits[4] <= digits[5]
    )
    return repeats_two and increasing and not repeats_three


def enumerate_passwords(start, end):
    all_passwords = [x for x in range(start, end + 1) if check_password(x)]
    return all_passwords


if __name__ == "__main__":
    START = 240298
    END = 784956
    matching_passwords = enumerate_passwords(START, END)
    print(matching_passwords)
    print(len(matching_passwords))
    

