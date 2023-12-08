# Final Project Report

* Student Name: Jiawei Tong
* Github Username: JiaweiTong1
* Semester: 23Fall
* Course: 5001 Python

## Description
Nowadays, one person have multiple accounts that need strong passwords to
protect sensitive information and accounts from unauthorized access. Strong
passwords make it significantly harder for malicious actors to guess or crack
them, thus enhancing the security of password is necessary.

This program check password robustness by its length, upper case letters,
lower case letters, digits, symbols, and it cannot be the same as username
and should be significant different from the previous passwords.

## Key Features
The key feature starts with screen check all the basic requirements by
check_password_minimum_requests function. If one of the requirements does
not meet, there is a feedback relates to what is missing in the password.
I include those feedbacks because I struggled to create a password.Some website
has high password requirements. When I register their account, it takes time
to know which part of my password does not meet the requirements. Thus,
feedbacks are useful.

This whole program is for increasing the robustness of passwords. Thus, it
provide feedback as strong, average, or weak even though this password meets
the basic requirements. If the user get a weak password feedback, it might
indicate them to create a stronger password in future.


## Guide
In the terminal, simply copy and paste follow command line to run the program.
The file "previous_passwords.dat" has all the previous username pair with
usernames.
python3 check_robustness.py -f previous_passwords.dat

An example of run the program in action as follow:

'''
carrietong@Jiaweidebijibendiannao python_final_project % python3
check_robustness.py -f previous_passwords.dat


Please enter username:  
'''
This is the time to input username. Then, program shows as follow.


'''
Please enter username: cds
Please enter a password:
'''
This is the time to input password.


'''
Please enter username: cds
Please enter a password: T!2uuuuuuu
weak password: **
'''
This means the password meets the basic requirements, but it is a weak password.


## Installation Instructions
In this project, the "re", "argparse", or "typing" modules are part of the
Python standard library. People can use them without installing any additional
packages or modules.

If people wanted to run this project locally, they would need to check their
Python version. If it is before Python 3.5, they need to install the "typing"
module separately. For Python 3.5 and later versions, "typing" is included in
the standard library.

## Code Review
'''
import re
import argparse
from typing import Dict
'''

The code starts by importing required modules, which are 're', 'argparse' and
defining constants for different password strength levels.
'''

    def check_password_minimum_requests(password) -> tuple[bool, str]:
    
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
'''

Defines a function to verify if a password meets basic requirements such as
length, uppercase, lowercase, digits, and symbols. I use if statement to set
up a true condition, such as length is more than 10 characters. If the length
of password less than 10, user will get a feedback "Password length should be
more than 10 characters."

'''

    def password_not_same_username(password: str, username: str) -> tuple[bool, str]:
    
    count_overlap = 0
       for char in range(len(password)):
           for chars in range(char + 4, len(password) + 4):
               substring = password[char:chars]
               if substring in username:
                   count_overlap += 1
    
        if count_overlap >= 5:
            return False, "Password cannot be the same as username."
        return True, "Password is not the same as username."
'''
Check password not same as username, if 5 characters overlap with username,
return false. I use for loop to iterate over password and user name. I use
if statement to check the amount of overlapped characters. If it is over 5
characters, return false and show feedback "Password cannot be the same as
username.".
'''

    def password_level(password: str):
        """
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
'''

By using if statement, I set up a condition to evaluate password level. For
example, weak password is 10 to 12 characters with meeting the
minimum request. Evaluates the strength of a password based on its length,
symbols, uppercase and lowercase letters, returning a strength rating, such
as weak, average, and strong.

'''

    def load_previous_accounts(filename: str) -> Dict[str, str]:
    
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
'''
To load previous username and password pairs from a given file into a
dictionary.The function returns a dictionary where keys are usernames
and values are passwords.

Initializes an empty dictionary previous_accounts_dict to store the
username-password pairs. Attempts to open the specified file in read mode ('r')
using a with statement for context management. Then, iterates through each
line in the file. Catches potential errors like FileNotFoundError and
general exceptions (Exception) that might occur during file processing,
printing an error message and returning an empty dictionary in case of an error.

'''

    def diff_previous_password(previous_accounts_info: Dict[str, str],
      password: str) -> int:
    
        count = 0
        for previous_password in previous_accounts_info.values():
            if password == previous_password:
                count += 1
        return count
'''
Checks how many times a given password matches any of the previous passwords
stored in the previous_accounts_info dictionary. Initializes a counter count
to zero. Iterates through each value (previous password) in the
previous_accounts_info dictionary using previous_accounts_info.values().If
a match is found (password == previous_password), increments the count by 1.
After checking against all previous passwords, returns the final count.

'''

    def main(filename):
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
            break
        print(password_level(password))
'''
The main program logic handles user input for username and password, validating the password against various criteria (length, not the same as username, not the same as previous passwords).

The code consists of multiple functions that encapsulate specific tasks, making the code modular and easy to maintain. It applies regex (re module) for pattern matching and uses argparse for command-line argument handling. Additionally, the code includes doctests in function docstrings to provide usage examples and expected outputs for different scenarios. The program can be executed from the command line using the argparse module to provide the filename containing previous accounts.

Loads the previous account information from the provided file using load_previous_accounts(filename). Asks the user to input a username.
Enters a while loop that continues until a valid password is obtained.By using 'password_not_same_username' to check if the password is different from the username. By using 'Check_password_minimum_requests' to ensure the password meets basic security requirements. By using 'diff_previous_password' to verifies the new password is different from previously used passwords. Prints error messages if the password doesn’t meet specific criteria. Breaks out of the loop when a valid password is obtained.

### Major Challenges
Facing to challenges is part of my learning process. In this project, I face to
several challenges that help to strength my coding skills. I would believe the
hardest part is to start everything.

In the beginning of this project, I need to break down complex functions into
smaller and more manageable functions, which can improve readability and
maintainability. I utilize regular expressions, which is 're' module. It is a
challenge for me because its syntax and patterns. Also, I write unit tests for
each function. It was hard to think about the edge tests. The last part of
challenge is to call all the functions in the main(). It took me much more
time to figure out how to call those functions and make them turn out to be
what I expected for.

After I finished build this program, those challenges are the precious
opportunities for growth and learning. I gradually improve my codebase step by step.


## Example Runs
By copy and paste the command line "python3 check_robustness.py -f previous_passwords.dat" in 
the terminal, there are three run examples as below. Each example end with three password levels, which are 
weak password,average password, strong password. Examples also show the false conditions for less length, 
no symbol, no uppercase letter, no lowercase letter, no digit, same as username, same as previous passwords.

Run example #1
'''
Username must be 5 to 15 characters
Please enter username: cn
Username must be 5 to 15 characters
Please enter username: njknicwqncuinquic
Username must be 5 to 15 characters
Please enter username: carnjk
Please enter a password: carrieT!!!!
Password should contain at least one digit.
Please enter a password: carrieTTTTTT
Password should contain at least one digit.
Please enter a password: carrie!!!!!000
Password should contain at least one uppercase letter.
Please enter a password: carrieTT!21  
weak password: **
'''

Run example #2
'''
Please enter username: avwcd
Please enter a password: carrie
Password length should be more than 10 characters.
Please enter a password: jkJK5Nkniu?ni 
password cannot be the same as previous passwords
Please enter a password: carrieT
Password length should be more than 10 characters.
Please enter a password: carrieT000
Password should contain at least one symbol (?!/|}@#).
Please enter a password: carrie000000
Password should contain at least one uppercase letter.
Please enter a password: carrieT0112!
average password: ***
'''

Run example #3
'''
Please enter username: carrie
Please enter a password: carrieTTT01!!!v
Password cannot be the same as username.
Please enter a password: njkTTT01!!!/VVV        
strong password: *****
'''


## Testing
In each function, I test the code with doctest. In the terminal, I use
command line python3 -m doctest -v check_robustness.py to make sure my code
is correct.

For the main function, I manually test it to make sure it was correct.

## Missing Features / What's Next
There are few features is missing. I would like to add the feature if the
password cannot meet the requirement, ask to re-create one. Maybe it can be
giving suggestions for a random robust password as we learned from midterm assignment.

Another feature is giving the option of saving a password or inputting a
password every time to log in. I need to learn how to set up the time to
re-enter password once this password is saved for one month.

For comparing password with previous passwords, I created a fake file with
previous account information for this program. However, I would like to learn
how to capture real datas.

## Final Reflection

I definitely see my coding skill is gradually grow in this course. I started
with struggling from homework, gratefully with all the helps from TAs' and
professor's. Now I can build a program with the key concepts that I learned
from this course.

I enjoy the learning patterns of this course. It is flexible, and I can
schedule many TA sections in different time according my schedules. There are
three TAs in this course. Each of them have their own way to tutor. I have the
opportunities to get help from them and learn from their tricks to debug. I
believe it is helpful to learn from different people and understand them
because usually people work on the same project as a team not individual
in the work environment.

In this course, I learned boolean expressions, which I used on my function
'check_password_minimum_requests', while loop, which I used on my main for
user to re-enter password if it does not meet the requirements. String is
really useful because it is used in lots of my code, such as input operations,
reading files, etc. For loop helps me execute a block of code multiple times.
It is used on several functions, such as collecting the same characters of
password and username. Dictionary collects items in a pair of key and value.
It is used for loading the previous username and passwords from given file
and check new password with previous passwords.

The above key takeaways is what I learned in this course. I would like to
learn more about the knowledge to add the feature of saving password in
one month.
