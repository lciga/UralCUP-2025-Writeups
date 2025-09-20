import Pyro4
from Pyro4 import naming
import pickle
import base64
from picklescan import scanner
import io
import uuid
import sqlite3
import hashlib
import random
import string
import json

av_config_check = True
admin_uuid = str(uuid.uuid4())
admin_rand_pass = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15)).encode('utf-8')
admin_pass_hash = hashlib.sha256(admin_rand_pass).hexdigest()
globalIterator = 0

def ChangeAVState():
    global av_config_check
    if (av_config_check == False):
        av_config_check = True
    else:
        av_config_check = False    
    #av_config_check = False
    #av_config_check = !av_config_check

def InitStartup():
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(username UNIQUE, uid PRIMARY KEY, password, rights, pickles)")
    print(f"Admin uuid: {admin_uuid}")
    print(f"Admin password: admin:{admin_pass_hash}:{admin_rand_pass}")
    cur.execute(f"INSERT INTO users (username, uid, password, rights, pickles) VALUES ('admin', '{admin_uuid}', '{admin_pass_hash}' , 'Administrator', '{json.dumps(["gASVIQAAAAAAAACMCGJ1aWx0aW5zlIwFcHJpbnSUk5SMBGFiY2SUhZRSlC4=", "gASVIQAAAAAAAACMCGJ1aWx0aW5zlIwFcHJpbnSUk5SMBGFiY2SUhZRSlC4="])}')")
    con.commit()

def CheckUserPresence(id) -> bool:
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    results = len(cur.execute(f"SELECT uid FROM users where uid = '{id}'").fetchall()) #тоже скуля (необязательная)

    if (results > 0):
        return True
    else:
        return False


@Pyro4.expose
class PublicFunctions(object):
    def PrintInfo(self):
        info = f"Hi, this is the Pyro project object management server. \n"\
                "If you registered at the website, you can manage your serialized objects here.\n"\
                "Please consider, that not all of functional is implemented\n"\
                "The functions are: \n"\
                "PrintInfo() - Returns this message\n"\
                "CreateFreeUser() - Creates free user and returns it's token\n" \
                "PutObject(unique_token:string, object:b64string ) - puts your object into db\n"\
                "GetObjectList(unique_token:string) - returns your objects\n"\
                "LoadObject(unique_token:string, object_name:string) - not implemented\n"\
                "RemoveObject(unique_token:string, object_name:string) - not implemented\n"\
                "StartObjectServer(unique_token:string, object_name:string) - not implemented\n"
        return info
    
    def CreateFreeUser(self):
        con = sqlite3.connect("test.db")
        cur = con.cursor()
        global globalIterator
        free_username = f"FreeUser{globalIterator}"
        globalIterator = globalIterator +1
        free_uuid = str(uuid.uuid4())        
        cur.execute(f"INSERT INTO users (username, uid) VALUES ('{free_username}', '{free_uuid}')")
        con.commit()
        return f"{free_username} : {free_uuid}."
    
    def GetObjectList(self, id): #no auth here)z
        try:
            cur = sqlite3.connect("test.db").cursor()
            results = cur.execute(f"SELECT pickles FROM users where uid = '{id}'") #скуля
            return str(results.fetchall())
        except Exception as e:
            return e

    def PutObject(self,uid, b64encoded):
        if (CheckUserPresence(uid)) == False:
            return "Invalid UID-token"
        try:
            added = False
            decoded_payload = base64.b64decode(b64encoded)
            if av_config_check:
                if (scanner.scan_pickle_bytes(io.BytesIO(decoded_payload),None).infected_files >= 1):
                    raise Exception("Malicious object found!\nAborting!") 
            pickle.loads(decoded_payload) #десер
            # added=True
            # if added == True:
            ChangeAVState()
            return f"Your object {uuid.uuid4()} successfuly added!"
        except Exception as e:
            return e

@Pyro4.expose
class PrivateFunctions(object):
    def PrintInfo(self):
        info = f"Hi pal, i've temporarly disabled authentication here to add some of our objects from vacation\n"\
                "Please don't forget to enable it again\n\n"\
                "Hi, this is the Pyro project object management server administrative interface. \n"\
                "Be aware, that some functions can cause vulnerabilities\n"\
                "Please consider, that not all of functional is implemented here, use configuration file to manage them\n"\
                "The available functions are: \n"\
                "PrintInfo() - Returns this message\n"\
                "DisablePickleCheck() - Disables picklescan checking\n"\
                "ForceRestartObject(object_uuid:uuid4) - Force Restarts object (better use local menu)\n"\
                "ForceRemoveObject(object_uuid:uuid4) - Force remove object (better use local menu)\n"\
                "Chcfg(cfgname:string, cfgvalue:json) - Remotely change configuration, changes may require restart (better use local menu)\n"
        return info

    def DisablePickleCheck(self, uid):
        if (uid != admin_uuid):
            return "You are not authorized to execute this."
        ChangeAVState()
        return "Picklescan disabled, it will be enabled automaticly after successfull upload."
                

if __name__ == "__main__":

    InitStartup()

    daemon = Pyro4.Daemon(host="0.0.0.0",port=5644)                     
    public = daemon.register(PublicFunctions,"PublicFunctions",)     
    private = daemon.register(PrivateFunctions,"PrivateFunctions")

    nameServer = Pyro4.locateNS("localhost",9090)
    nameServer.register("Public",public)
    nameServer.register("Private",private)

    print(f"Ready. Objects uri: \npublic = {public}\nprivate = {private}")      
    daemon.requestLoop()                   
