from data_utils import User
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
        return 0



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

