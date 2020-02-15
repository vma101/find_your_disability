import numpy as np 
import pandas as pd

def User_Build():
    name = input('What is your name? (Last, First) \n')
    age = input('What is your age? Use numerals please. \n')
    gender = input('What is your gender? (Male / Female / Nonbinary) \n')
    phone = input('What is your preferred telephone number? No special characters, include numbers only and country code \n')
    email = input('What is your email? \n')
    address = input('Where do you live? Feel free to input to any level of granularity, and to use your clinic or health provider\'s address if you would prefer. \n')
    return(name, age, gender, phone, email, address)

def Section_Redirect():
    section = input('What information would you like to log? Input the relevant number. \n 1 - Diagnostic \n 2 - Treatment')
    return(section)

def Diagnostic():
    dx_type = input('What diagnosis type would you like to input? \n (ICF / Other)')
    if dx_type == 'ICF':
        dx = input('What ICF code were you diagnosed with? \n')
    else:
            pass



# New to System / Adding to Records

def User_Locate():
    user_id = input('What is your name? (Last, First) \n')
    return(user_id)


class User:
    User.name 
