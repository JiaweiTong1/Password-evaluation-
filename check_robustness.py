"""
Final project: Check Passwords Robustness
===========================================================================
NAME: Jiawei Tong
SEMESTER: 23 Fall

A program that check passwords robustness for prevent account compromise.

Check robustness with the following requirements:
1) at least 10 characters
2) upper case letters
3) lower case letters
4) a number
5) symbols (?!/|}@#)
6) cannot be the same as username
7) not the same as the previous password

If the password cannot meet the requirement, ask to re-create one, and
give suggestions for improving password.
If the password meets the requirement, give a rate of the password, such
as week, average, or strong.
"""
import re
import argparse
from typing import Dict

# program constants show rates of the password
WEAK_PASSWORD = "weak password: **"
AVERAGE_PASSWORD = "average password: ***"
STRONG_PASSWORD = "strong password: *****"


def check_password_minimum_requests(password) -> tuple[bool, str]:
    """
    Check password if it meets the following basic requirements:
    1) Check characters more than 10
    2) Check for at least one uppercase letter
    3) Check for at least one lowercase letter
    4) Check for at least one digit
    5) Check for at least one symbol

    Examples:
        >>> check_password_minimum_requests('carrieT0112!')
        (True, 'Password meets the minimum requirements.')
        >>> check_password_minimum_requests('carrieT0112')
        (False, 'Password should contain at least one symbol (?!/|}@#).')
        >>> check_password_minimum_requests('T0112!')
        (False, 'Password length should be more than 10 characters.')
        >>> check_password_minimum_requests('TTTTT0112!')
        (False, 'Password should contain at least one lowercase letter.')
        >>> check_password_minimum_requests('kijnciwea0112!')
        (False, 'Password should contain at least one uppercase letter.')

    Arg:
        password: New created password
    Return:
        tuple[bool, str]: True password meets the minimum requests; False password
        does not meet a certain requirement.
    """

    if not 10 <= len(password):
        return False, "Password length should be more than 10 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password should contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password should contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password should contain at least one digit."

    if not re.search(r"[?!/|}@#]", password):
        return False, "Password should contain at least one symbol (?!/|}@#)."

    else:
        return True, "Password meets the minimum requirements."


def get_amount_digits(password: str) -> int:
    """
    Check the length of digits.
    Example:
        >>> get_amount_digits('1234567890')
        10
        >>> get_amount_digits('CarrIE@@7890')
        4
    """
    count_digits = 0
    for number in password:
        if number.isdigit():
            count_digits += 1

    return count_digits


def count_upper_case(password: str) -> int:
    """
    Count upper case in the password
    Args:
        password(str): new password
    Examples:
        >>> count_upper_case('TONGJIAWEI01')
        10
        >>> count_upper_case('PYTHONCLASS01')
        11
    """
    count = 0
    for letters in password:
        if letters.isupper():
            count += 1
    return count


def count_lower_case(password: str) -> int:
    """
    Count lower case in the password
    Examples:
        >>> count_lower_case('tongjiawei01')
        10
        >>> count_lower_case('pythonclass01')
        11
    """
    count = 0
    for letters in password:
        if letters.islower():
            count += 1
    return count


def check_symbols(password: str) -> int:
    """
    Count symbols in the password
    Examples:
        >>> check_symbols('tongjiawei0/!')
        2
        >>> check_symbols("Jiaweitong@}")
        2
    """
    symbols = '!@#$%^&*()\\-_=+\\[\\]{};:\'",.<>/?\\\\|`]'

    count = 0
    for digits in password:
        if digits in symbols:
            count += 1

    return count


def password_not_same_username(username: str, password: str) -> tuple[bool, str]:
    """
    Check password not same as username, if 5 consecutive characters overlap with username, return false
    Examples:
        >>> password_not_same_username('carrieT0112', 'carrie8eu')
        (False, 'Password cannot be the same as username.')
        >>> password_not_same_username('carrie', 'carrie8eu')
        (False, 'Password cannot be the same as username.')
        >>> password_not_same_username('carTrie0112', 'carrie8eu')
        (True, 'Password is not the same as username.')
        >>> password_not_same_username('jIIWET0112', 'carrie8eu')
        (True, 'Password is not the same as username.')
        >>> password_not_same_username('njknjno', 'bhj,kjnilioT')
        (True, 'Password is not the same as username.')
    """
    count_overlap = 0
    for char in range(len(password) - 4):
        substring = password[char:char + 5]
        if substring in username:
            count_overlap += 1

    if count_overlap >= 1:
        return False, "Password cannot be the same as username."
    return True, "Password is not the same as username."


def password_level(password: str):
    """
    Examples:
    >>> password_level('carrieTT01!!v')
    'average password: ***'
    >>> password_level('carrieTTT01!!!v')
    'strong password: *****'
    >>> password_level('T!2uuuuuuu')
    'weak password: **'
    >>> password_level('abvcdjlT!mq1')
    'average password: ***'
    """
    symbol_count = check_symbols(password)
    lower_case_count = count_lower_case(password)
    upper_case_count = count_upper_case(password)

    if 10 <= len(password) < 12:
        return WEAK_PASSWORD

    elif 12 <= len(password) <= 14 and symbol_count >= 1 \
            and lower_case_count >= 3 and upper_case_count >= 1:
        return AVERAGE_PASSWORD

    elif len(password) > 14 and symbol_count >= 3 \
            and lower_case_count >= 3 and upper_case_count >= 2:
        return STRONG_PASSWORD

    else:
        return "Password strength unknown"


def load_previous_accounts(filename: str) -> Dict[str, str]:
    """
    Loads the previous username and passwords from given file

    Example:
        >>> load_previous_accounts("previous_passwords.dat")            # doctest: +NORMALIZE_WHITESPACE
        {'carrieTJW01': 'cancjdaTTT8902',
        'carrieTJW02': 'CANFJRE@IO/./n',
        'carrieTJW03': 'XJOCWIOjnj87n9',
        'carrieTJW04': 'jkJK5Nkniu?ni',
        'carrieTJW05': 'carrieT?ni/01'}

    """

    previous_accounts_dict = {}

    try:
        with open(filename, 'r') as file:
            for line in file:
                information = line.strip().split(':', 1)
                if len(information) != 2:
                    print(f'Issue with line:{line.strip()}')
                else:
                    user_name, password = information
                    previous_accounts_dict[user_name] = password.lstrip(':').strip()

    except FileNotFoundError:
        print("file not found")
        return {}

    except Exception as e:
        print(f"an error occurred: {e}")
        return {}

    return previous_accounts_dict


def diff_previous_password(previous_accounts_info: Dict[str, str], password: str) -> int:
    """
    Check new password with previous password.
    Example:
        >>> pa = {'carrieTJW04': 'jkJK5Nkniu?ni','carrieTJW05': 'carrieT?ni/01'}
        >>> diff_previous_password(pa, 'carrieT?ni/01')
        1
    """
    count = 0
    for previous_password in previous_accounts_info.values():
        if password == previous_password:
            count += 1
    return count


def main(filename):
    """
    Ask users to enter username and password until meets all the requirements. Starting with
    checking the basic requirements. Then, checking password cannot be the same as username,
    and can not be the same as previous passwords.
    """
    previous_accounts_info = load_previous_accounts(filename)

    username = input("Please enter username: ")
    while True:
        password = input("Please enter a password: ")
        different_to_username, message_username = password_not_same_username(password, username)
        meets_requirements, message_requirements = check_password_minimum_requests(password)

        if not meets_requirements:
            print(message_requirements)
            continue

        if not different_to_username:
            print(message_username)
            continue

        if diff_previous_password(previous_accounts_info, password) != 0:
            print("password cannot be the same as previous passwords")

        else:
            break
    print(password_level(password))


# use the following command to run the program:
# python3 check_robustness.py -f previous_passwords.dat
# python3 -m doctest -v check_robustness.py

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Password Checker")
    parser.add_argument(
        "-f",
        "--filename",
        help="File containing previous accounts",
        default="previous_passwords.dat",)

    args = parser.parse_args()
    main(args.filename)
