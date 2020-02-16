from data_utils import *
import pymongo as pm
import sqlite3

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
        uids = self.execute(sql, [uid])
        return [u[0] for u in uids]

    def get_user_treatment(self, uid):
        sql = "select type, name, reaction from treatments where uid = ?"
        uids = self.execute(sql, [uid])
        return [u[0] for u in uids]

    def get_icf_code_users(self, icf):
        sql = "select uid from dx_icf where icf = ?"
        uids = self.execute(sql, [uid])
        return [u[0] for u in uids]

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


def find_similar_users(db, uid):
    icfids = find_similar_icf(db, uid)


def find_similar_icf(db, uid):
    codes = db.get_user_icf_codes(uid)
    usrs = []
    for code in codes:
        usrs += db.get_icf_code_users(code)
    return usrs

def find_similar_other(db, uid):
    return []
