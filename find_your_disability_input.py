import numpy as np 
import pymongo as pm

def User_Build():
    name = input('What is your name? (Last, First) \n')
    age = input('What is your age? Use numerals please. \n')
    gender = input('What is your gender? (Male / Female / Nonbinary) \n')
    phone = input('What is your preferred telephone number? No special characters, include numbers only and country code \n')
    email = input('What is your email? This will be used in the future to locate your records. \n')
    address = input('Where do you live? Feel free to input to any level of granularity, and to use your clinic or health provider\'s address if you would prefer. \n')
    return(name, age, gender, phone, email, address)

def Section_Redirect():
    section = input('What information would you like to log? Input the relevant number. \n 1 - Diagnostic \n 2 - Treatment')
    return(section)

def Diagnostic():
    end_var = 'N'
    dx_type = input('What diagnosis type would you like to input? \n (ICF / Other)')
    if dx_type == 'ICF':
        while end_var == 'N'
            dx = input('What ICF code(s) were you diagnosed with? Input one. \n')
            end_var = ('Would you like to input more ICF codes? Y/N: ')
    else: 
        

dx_dict = {
    1: ['Mental', 'Sensory and Pain', 'Voice and Speech', 'Cardiovascular, Haematological, Immunological and Respiratory', 'Digestive, Metabolic, Endocrine', 'Genitourinary, Reproductive', 'Neuromusculoskeletal, Movement-related', 'Skin'],
    2: ['Learning, Applying Knowledge', 'General Tasks, Demands', 'Communication', 'Mobility', 'Self-Care', 'Domestic Life', 'Interpersonal Interactions, Relationships', 'Major Life Areas', 'Community, Social, Civic Life']
    3: ['PRoducts and Technology', 'Natural Environment and Human-made Changes', 'Support and Relationships', 'Attitudes', 'Services, Systems, Societies']
    4: ['Nervous System', 'Eye, Ear, and Related', 'Voice and Speech', 'Cardiovascular, Immunological, Respiratory, ']
}

def Diagnostic_General():
    dx_section = input('What section granularity would you like to provide? \n 1 - Body Functions \n 2 - Body Structures \n  3 - Activities and Participation \n 4 - Environmental Factors \n')
    print('Your options are the following')
    for a, b in enumerate(dx_dict[dx_section], 1):
        print("{} {}.format (a, b)")
    dx_desc_idx = input('Please input the number next to the section that most relates to your diagnosis: ')
    dx_desc = dx_dict[dx_section][dx_desc - 1]

def Treatment():
    treatment_type = input('What type of intervention did you receive? \n 1 - Medication \n 2 - Procedure \n 3 -Device) \n')
    # DRUG CONDITION
    end_var = 'N'
    if treatment_type == 1:
        while end_var == 0
            drug = input('Please input the name of one drug: ')
            rx_drug_bool = ('Did you have an adverse reaction to the drug? (Y/N): ')
            if rx_drug_bool == 'Y':
                rx_drug = input('Please input adverse reactions to the drug: ') 
            end_var = input('Would you like to input another drug? (Y/N): ')
    # PROCEDURE CONDITION
    elif treatment_type == 2:
        while end_var == 0
            prd = input('Please input the name of a procedure: ')
            rx_prd_bool = input('Did you have an adverse reaction to the procedure? (Y/N): ')
            if rx_prd_bool == 'Y':
                rx_prd = input('Please input adverse reactions to the procedure: ')
            end_var = input('Would you like to input another procedure? (Y/N): ')
    elif treatment_type == 3:
        while end_var == 0
            device = input('Please input the name of a device you were given: ')
            rx_device_bool = input('Did you have an adverse reaction to the device? (Y/N): ')
            if rx_device_bool == 'Y':
                rx_device = input('Please input adverse reactions to the device: ')
            end_var = input('Would you like to input another device? (Y/N): ')


def main():
    user_arb = input('Welcome to Find Your Disability. Do you have an account with us? (Y/N): ')
    if user_arb == 'N':
        [name, age, gender, phone, email, address] = User_Build()
    section = Section_Redirect()
    # Diagnostic Inputs
    if section == 1:
        Diagnostic()






# New to System / Adding to Records

def User_Locate():
    user_email = input('What is the email you used to register with us? \n')
    # Query the data base to get the user_id

    return(user_id)



