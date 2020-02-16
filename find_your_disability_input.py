from backend import SqliteDB
from data_utils import *
from geopy.geocoders import Nominatim

db = SqliteDB("backend.db")


def User_Build():
    fname = input('What is your first name? \n')
    lname = input('What is your last name? \n')
    dob = input('What is your date of birth? (ddmmyyyy). \n')
    gender = input('What is your gender? (Male / Female / Nonbinary) \n')
    phone = input('What is your preferred telephone number? No special characters, include numbers only and country code \n')
    email = input('What is your email? This will be used in the future to locate your records. \n')
    address = input('Where do you live? Feel free to input to any level of granularity, and to use your clinic or health provider\'s address if you would prefer. \n')
    geolocator = Nominatim(user_agent = 'python')
    location_long = geolocator.geocode(address)
    location = (location.latitude, location.longitude)
    return(fname, lname, dob, gender, phone, email, address)

def Section_Redirect():
    section = input('What information would you like to log? Input the relevant number. \n 1 - Diagnostic \n 2 - Treatment \n')
    return(section)

###################################### ALL DIAGNOSTIC DATA COLLECTION ######################################
def Diagnostic():
    end_var = 'Y'
    while end_var == 'Y':
        dx_type = input('What diagnosis type would you like to input? \n (ICF / Other): ')
        end_var = Diagnostic_Specific(dx_type)
        
dx_sub_dict = {
    '1': ['Mental', 'Sensory and Pain', 'Voice and Speech', 'Cardiovascular, Haematological, Immunological and Respiratory', 'Digestive, Metabolic, Endocrine', 'Genitourinary, Reproductive', 'Neuromusculoskeletal, Movement-related', 'Skin'],
    '2': ['Learning, Applying Knowledge', 'General Tasks, Demands', 'Communication', 'Mobility', 'Self-Care', 'Domestic Life', 'Interpersonal Interactions, Relationships', 'Major Life Areas', 'Community, Social, Civic Life'],
    '3': ['Products and Technology', 'Natural Environment and Human-made Changes', 'Support and Relationships', 'Attitudes', 'Services, Systems, Societies'],
    '4': ['Nervous System', 'Eye, Ear, and Related', 'Voice and Speech', 'Cardiovascular, Immunological, Respiratory', 'Digestive, Metabolic, Endocrine', 'Genitourinary, Reproductive', 'Neuromusculoskeletal, Movement-related', 'Skin']
}

def Diagnostic_Specific(dx_type):
    end_var_branch = 'Y'
    if dx_type == 'ICF':
        while end_var_branch == 'Y':
            dx = input('What ICF code(s) were you diagnosed with? Input one. \n')
            end_var_branch = input('Would you like to input more ICF codes? Y/N: ')
    else: 
        while end_var_branch == 'Y':
            dx_section = input('What section granularity would you like to provide? \n 1 - Body Functions \n 2 - Body Structures \n  3 - Activities and Participation \n 4 - Environmental Factors \n')
            print('Your options are the following')
            for a, b in enumerate(dx_sub_dict
        [dx_section], 1):
                print("{} {}".format (a, b))
            dx_desc_idx = int(input('Please input the number next to the section that most relates to your diagnosis: '))
            dx_desc = dx_sub_dict
        [dx_section][dx_desc_idx - 1]
            end_var_branch = input('Would you like to input any other non-coded diagnostic information? (Y/N): ')
    end_var = input('Would you like to input any other diagnostic information? (Y/N): ')
    return(end_var)

###################################### ALL TREATMENT DATA COLLECTION ######################################
def Treatment():
    end_var = 'Y'
    while end_var == 'Y':
        treatment_type = input('What type of intervention did you receive? \n 1 - Medication \n 2 - Procedure \n 3 - Device \n')
        end_var = Treatment_Specific(treatment_type)

def Treatment_Specific(treatment_type):
    end_var_branch = 'Y'
    # DRUG CONDITION
    if treatment_type == '1':
        while end_var_branch == 'Y':
            drug = input('Please input the name of one drug (limit 1024char): ')
            rx_drug_bool = input('Did you have an adverse reaction to the drug? (Y/N): ')
            if rx_drug_bool == 'Y':
                rx_drug = input('Please input adverse reactions to the drug (limit 1024char): ') 
            end_var_branch = input('Would you like to input another drug? (Y/N): ')
    # PROCEDURE CONDITION
    elif treatment_type == '2':
        while end_var_branch == 'Y':
            prd = input('Please input the name of a procedure (limit 1024char): ')
            rx_prd_bool = input('Did you have an adverse reaction to the procedure? (Y/N): ')
            if rx_prd_bool == 'Y':
                rx_prd = input('Please input adverse reactions to the procedure (limit 1024char): ')
            end_var_branch = input('Would you like to input another procedure? (Y/N): ')
    # DEVICE CONDITION
    elif treatment_type == '3':
        while end_var_branch == 'Y':
            device = input('Please input the name of a device you were given (limit 1024char): ')
            rx_device_bool = input('Did you have an adverse reaction to the device? (Y/N): ')
            if rx_device_bool == 'Y':
                rx_device = input('Please input adverse reactions to the device (limit 1024char): ')
            end_var_branch = input('Would you like to input another device? (Y/N): ')
    end_var = input('Would you like to input any other treatment information? (Y/N): ')
    return(end_var)    

###################################### WRAPPER FUNCTIONS ######################################
def main():
    user_arb = input('Welcome to Find Your Disability. Do you have an account with us? (Y/N): ')
    uid = 0
    if user_arb == 'N':
        [fname, lname, dob, gender, phone, email, address] = User_Build()
        new_user = User(fname, lname, dob, gender, phone, email, address)
        uid = db.add_user(new_user)
        db.commit()
    end_var = 'Y'
    while end_var == 'Y':
        section = Section_Redirect()    
        # Diagnostic Inputs
        if section == '1':
            Diagnostic()
        if section == '2':
            Treatment()
        end_var = input('Would you like to input any other information today? Y/N: ')
    if end_var == 'N':
        print('Thank you. Have a great day!') 

# New to System / Adding to Records

def User_Locate():
    user_email = input('What is the email you used to register with us? \n')
    # Query the data base to get the user_id
    user_id = 'Placebo'
    return(user_id)



