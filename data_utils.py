
class User():
    def __init__(self, fname="", lname="", dob="", gender="", phone="", email="", address=""):
        self.fname = fname
        self.lname = lname
        self.dob = dob
        self.gender = gender
        self.phone = phone
        self.email = email
        self.address = address

class Dx_ICF():
    def __init__(self, dx_icf = '')
        self.icf = dx_icf

class Dx_Other():
    def __init__(self, dx_cat = '', dx_sub = '')
        self.cat = dx_cat
        self.sub = dx_sub

class Treatment():
    def __init__(self, treatment_type = '', treatment_name = '', treatment_rx_bool = '', treatment_rx = '')
        self.type = treatment_type
        self.name = treatment_name
        self.rx_bool = treatment_rx_bool
        self.rx = treatment_rx