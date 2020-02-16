from data_utils import *
import pymongo as pm
import sqlite3
import hashlib

class SqliteDB():
    def __init__(self, fname=""):
        if(fname != ""):
            self.connect(fname)

    def connect(self, fname):
        self.conn = sqlite3.connect(fname)
        self.cursor = self.conn.cursor()
    
    def execute(self, sql, vals=[], commit=False):
        if(len(vals)>0):
            self.cursor.execute(sql, vals)
        else:
            self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if(commit):
            self.commit()
        return res

    def commit(self):
        self.conn.commit()


    # do not expose pkfield to user! SQL injection
    def fetch_userids(self, field, value):
        sql = "select uid from users where {} = ?".format(field)
        return self.execute(sql, [value])

    def fetch_userid(self, field, value):
        sql = "select uid from users where {} = ?".format(field)
        id = self.execute(sql, [value])
        assert(len(id) == 1)
        return id[0][0]
    
    def add_user(self, user_inst):
        assert(type(user_inst) == User)
        ids = self.fetch_userids("email", user_inst.email)
        if(len(ids)>0):
            print("Warning: email already exists")
            return -1
        fields = ""
        vals = []
        if(user_inst.fname):
            fields += 'first_name, '
            vals.append(user_inst.fname)
        if(user_inst.lname):
            fields += 'last_name, '
            vals.append(user_inst.lname)
        if(user_inst.dob):
            fields += 'dob, '
            vals.append(user_inst.dob)
        if(user_inst.gender):
            fields += 'gender, '
            vals.append(user_inst.gender)
        if(user_inst.phone):
            fields += 'phone, '
            vals.append(user_inst.phone)
        if(user_inst.email):
            fields += 'email, '
            vals.append(user_inst.email)
        if(user_inst.address):
            fields += 'address, '
            vals.append(user_inst.address)
        fields = fields[:-2]
        sql = "insert into users ({}) values ({})".format(fields, ("?,"*len(vals))[:-1])
        self.execute(sql, vals)
        id = self.fetch_userids("email", user_inst.email)[0][0]
        return id

    def add_dx(self, uid, dx):
        if(type(dx) == Dx_ICF):
            sql = "insert into dx_icf values (?, ?)"
            self.execute(sql, [uid, dx.icf])
        elif(type(dx) == Dx_Other):
            sql = "insert into dx_other values (?, ?, ?)"
            self.execute(sql, [uid, dx.cat, dx.sub])
        else:
            print("Dx must be an instance of Dx_ICF or Dx_Other")
    
    def add_treatment(self, uid, treat):
        assert(type(treat) == Treatment)
        values = [uid, treat.type, treat.name]
        if(treat.rx != ''):
            sql = "insert into treatments values (?, ?, ?, ?)"
            values.append(treat.rx)
        else:
            sql = "insert into treatments values (?, ?, ?, null)"
        self.execute(sql, values)

    def get_user_icf_codes(self, uid):
        sql = "select icf from dx_icf where uid = ?"
        codes = self.execute(sql, [uid])
        return [c[0] for c in codes]

    def get_user_dx_other(self, uid):
        sql = "select category, subcategory from dx_other where uid = ?"
        dx_other = self.execute(sql, [uid])
        return dx_other

    def get_user_treatment(self, uid):
        sql = "select type, name, reaction from treatments where uid = ?"
        treats = self.execute(sql, [uid])
        return treats

    def get_icf_code_users(self, icf):
        sql = "select uid from dx_icf where icf = ?"
        uids = self.execute(sql, [icf])
        return [u[0] for u in uids]

    def get_emails_from_uids(self, uids):
        prep = ("?,"*len(uids))[:-1]
        sql = "select email from users where uid in ({})".format(prep)
        ems = self.execute(sql, uids)
        return [e[0] for e in ems]

class MongoDB():
    def __init__(self, user, pwd):
        self.pw = pwd
        self.user = user
    def connect(self):
        conStr = "mongodb+srv://{}:{}@findyourdisability-ukh99.gcp.mongodb.net/finder?retryWrites=true&w=majority"
        conStr = conStr.format(self.user, self.pw)
        self.client = pm.MongoClient(conStr)
        self.db = self.client['finder']
    def getRelation(self, name):
        return self.db[name]


db = SqliteDB("backend.db")
u1 = User(fname="Andrew", lname="Wells", email="ajwells@uchicago.edu")


# returns ([icf users], [other users]) 
def find_similar_users(db, uid):
    icfids = find_similar_icf(db, uid)
    otherids = find_similar_other(db, uid)
    return (icfids, otherids)

def find_similar_icf(db, uid):
    codes = db.get_user_icf_codes(uid)
    usrs = []
    for code in codes:
        usrs += db.get_icf_code_users(code)
    return usrs

def find_similar_other(db, uid):
    return []

def get_anon_email(db, uids):
    emails = db.get_emails_from_uids(uids)
    return [hashlib.sha256(email.encode("utf-8")).hexdigest() for email in emails]

def get_anon_email_from_user_sim(db, uid):
    icfids, otherids = find_similar_users(db, uid)
    anonmail = get_anon_email(db, icfids)
    print("The following people have the same ICF codes as you:")
    for anon in anonmail:
        print("{}@find_your_disability.net".format(anon), end="\n")
    print("")
    anonmail = get_anon_email(db, otherids)
    print("The following people have the similar general disabilities as you:")
    for anon in anonmail:
        print("{}@find_your_disability.net".format(anon), end="\n")
    print("")

def show_records(db, uid):
    dxother = db.get_user_dx_other(uid)
    dxicf = db.get_user_icf_codes(uid)
    treats = db.get_user_treatment(uid)
    print("ICFs:")
    for icf in dxicf:
        print("\t{}".format(icf))
    print("Other disabilities:")
    for icf in dxother:
        print("\t{}: {}".format(icf[0], icf[1]))
    print("Treatments:")
    for icf in treats:
        print("\t{}: {}".format(icf[0], icf[1]))
        if(icf[2] is not None):
            print("\t\tReaction: {}".format(icf[2]))
