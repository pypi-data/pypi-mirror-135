# File: Rest/JSON API + User security. ArangoDB Flavor
# Author: alexsanchezvega
# Company: d20
# Version: 2.0.0

from .Error import MissingConfigurationException
from pyArango.connection import *
from pyArango.collection import *
from pyArango.graph import *
from dtwentyORM import BasicElement, Metadata
from threading import Thread
import datetime
import hashlib
import binascii
import os
import json


class SecurityLayer():
    if os.environ.get('D20_SL_CONF') != None:
        conf = json.loads(os.environ.get('D20_SL_CONF'))
        arangoURL=conf.get('D20_SL_DBURL')
        username=conf.get('D20_SL_DBUSERNAME')
        password=conf.get('D20_SL_DBPASSWORD')        
    else:
        raise MissingConfigurationException

    db_client = Connection(arangoURL=arangoURL, username=username, password=password, verify=True, verbose=True, statsdClient=None, reportFileName=None, loadBalancing='round-robin', use_grequests=False, use_jwt_authentication=False, use_lock_for_reseting_jwt=True, max_retries=10)
    db_name = 'securitylayer'

    def __init__(self):
        if not self.db_client.hasDatabase('securitylayer'):
            self.db = self.db_client.createDatabase('securitylayer')
            self.db.createCollection(className='Collection', name='UserCredentials')
            self.db.createCollection(className='Collection', name='APICredentials')
            self.db.createCollection(className='Collection', name='UserTokens')
            self.db.createCollection(className='Collection', name='APITokens')
            self.db.createCollection(className='Collection', name='OTP')
            self.db.createCollection(className='Collection', name='PasswordRecoveryTokens')
        else:
            self.db = self.db_client['securitylayer']

    class UserCredentials(Collection):
        _fields = {
        }    

    class APICredentials(Collection):
        _fields = {
        }    

    class UserTokens(Collection):
        _fields = {
        }    

    class APITokens(Collection):
        _fields = {
        }    

    class OTP(Collection):
        _fields = {
        }    

    class PasswordRecoveryTokens(Collection):
        _fields = {
        }    
                
    class PasswordRecoveryToken(BasicElement):
        db_name = 'securitylayer'

        @classmethod
        def get_collection(cls):
            return 'PasswordRecoveryTokens'

        def get_class(self):
            return 'PasswordRecoveryToken'

        def make(self):
            self.attributes = ['_key', 'created', 'updated', 'valid_thru', 'active', 'userid', 'username']
            for key in self.attributes:
                setattr(self, key, None)

        def create(self):
            try:
                self.created = datetime.datetime.utcnow()
                self.updated = self.created
                p = Metadata.Parameter('find', {'_key' : 'psswdrec_lifespawn'})
                psswdrec_lifespawn = p.get('value')
                self.valid_thru = self.created + datetime.timedelta(minutes=psswdrec_lifespawn)
                self.active = True
                to_insert = self.to_dict()
                for key in self.attributes:
                    if key in to_insert and to_insert[key] == None:
                        to_insert.pop(key)
                ins_obj = self.db[self.get_collection()].createDocument(to_insert)
                ins_obj.save()
                self._key = ins_obj._key
                self.status = True
            except:
                ins_obj = None
                self.status = False
            return ins_obj != None

        def find(self):
            try:
                foundl = self.db[self.get_collection()].fetchFirstExample({"_key": self._key, "active": True, 'userid': self.userid})
                if len(foundl) <= 0:
                    foundl = self.db[self.get_collection()].fetchFirstExample({"_key": self._key, "active": True, 'username': self.userid})
                found = foundl[0]
                for key in self.attributes:
                    setattr(self, key, found[key] if key in found.getStore() else self.get(key))
                self.valid_thru = datetime.datetime.strptime(self.valid_thru, '%Y-%m-%d %H:%M:%S.%f')
                self.status = (self.valid_thru >= datetime.datetime.utcnow() and self.active)
                delete_thread = Thread(target=found.delete)
                delete_thread.start()
            except:
                self._key = None
                self.status = False
        

    class OneTimeAccess(BasicElement):
        db_name = 'securitylayer'

        @classmethod
        def get_collection(cls):
            return 'OTP'

        def get_class(self):
            return 'OneTimeAccess'

        def make(self):
            self.attributes = ['_key', 'created', 'updated', 'valid_thru', 'active', 'userid', 'username']
            for key in self.attributes:
                setattr(self, key, None)

        def create(self):
            try:
                self.created = datetime.datetime.utcnow()
                self.updated = self.created
                p = Metadata.Parameter('find', {'_key' : 'otp_lifespawn'})
                otp_lifespawn = p.get('value')
                self.valid_thru = self.created + datetime.timedelta(minutes=otp_lifespawn)
                self.active = True
                to_insert = self.to_dict()
                for key in self.attributes:
                    if key in to_insert and to_insert[key] == None:
                        to_insert.pop(key)
                ins_obj = self.db[self.get_collection()].createDocument(to_insert)
                ins_obj.save()
                self._key = ins_obj._key
                self.status = True
            except:
                ins_obj = None
                self.status = False
            return ins_obj != None

        def find(self):
            try:
                foundl = self.db[self.get_collection()].fetchFirstExample({"_key": self._key, "active": True, 'userid': self.userid})
                if len(foundl) <= 0:
                    foundl = self.db[self.get_collection()].fetchFirstExample({"_key": self._key, "active": True, 'username': self.userid})
                found = foundl[0]
                for key in self.attributes:
                    setattr(self, key, found[key] if key in found.getStore() else self.get(key))
                self.valid_thru = datetime.datetime.strptime(self.valid_thru, '%Y-%m-%d %H:%M:%S.%f')
                self.status = (self.valid_thru >= datetime.datetime.utcnow() and self.active)
                delete_thread = Thread(target=found.delete)
                delete_thread.start()
            except:
                self._key = None
                self.status = False
        

    class UserToken(BasicElement):
        db_name = 'securitylayer'
        
        @classmethod
        def get_collection(cls):
            return 'UserTokens'

        def get_class(self):
            return 'UserToken'

        def make(self):
            self.attributes = ['_key', 'created', 'updated', 'valid_thru', 'active', 'userid', 'username', 'password', 'oauth', 'oauth_client', 'scopes', 'delegated', 'can_write', 'isadmin']
            for key in self.attributes:
                setattr(self, key, None)
        
        def auth(self):
            try:
                user = SecurityLayer.UserAccess('auth', {"username" : self.get('userid'), 'password' : self.get('password')})
                if user.get('status'):
                    self.userid = user._key
                    self.password = ''
                    self.status = self.create()
                else:
                    self.status = False
            except:
                self.password = ''
                self._key = None
                self.status = False

        def create(self):
            try:
                self.created = datetime.datetime.utcnow()
                self.updated = self.created
                p = Metadata.Parameter('find', {'_key' : 'user_token_lifespawn'})
                user_token_lifespawn = p.get('value')
                self.valid_thru = self.created + datetime.timedelta(minutes=user_token_lifespawn)
                self.active = True
                to_insert = self.to_dict()
                for key in self.attributes:
                    if key in to_insert and to_insert[key] == None:
                        to_insert.pop(key)
                ins_obj = self.db[self.get_collection()].createDocument(to_insert)
                ins_obj.save()
                self._key = ins_obj._key
                self.status = True
            except:
                ins_obj = None
                self.status = False
            return ins_obj != None

        def find(self):
            try:
                if self.get('oauth') != True:
                    foundl = self.db[self.get_collection()].fetchFirstExample({"_key": self._key, "active": True, 'userid': self.userid})
                    if len(foundl) <= 0:
                        foundl = self.db[self.get_collection()].fetchFirstExample({"_key": self._key, "active": True, 'username': self.userid})
                else:
                    foundl = self.db[self.get_collection()].fetchFirstExample({"_key": self._key, "oauth": True, 'userid': self.userid})
                    if len(foundl) <= 0:
                        foundl = self.db[self.get_collection()].fetchFirstExample({"_key": self._key, "oauth": True, 'username': self.userid})
                found = foundl[0]
                self._key = found['_key']
                for key in self.attributes:
                    setattr(self, key, found[key] if key in found else self.get(key))
                self.valid_thru = datetime.datetime.strptime(self.valid_thru, '%Y-%m-%d %H:%M:%S.%f')
                if self.get('oauth') != True and (self.valid_thru < datetime.datetime.utcnow() or not self.active):
                    self.active = False
                    delete_thread = Thread(target=found.delete)
                    delete_thread.start()
                else:
                    self.active = True
                    p = Metadata.Parameter('find', {'_key' : 'user_token_lifespawn'})
                    user_token_lifespawn = p.get('value')
                    found['valid_thru'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=user_token_lifespawn)
                    update_thread = Thread(target=found.save)
                    update_thread.start()
                self.status = self.active
            except:
                self._key = None
                self.status = False

    class UserAccess(BasicElement):
        db_name = 'securitylayer'
        
        @classmethod
        def get_collection(cls):
            return 'UserCredentials'

        def get_class(self):
            return 'UserAccess'

        def make(self):
            self.attributes = ['_key', 'password', 'username', 'created', 'updated']
            for key in self.attributes:
                setattr(self, key, None)
        
        def auth(self):
            try:
                self.status = self.verify_password()
            except:
                self.password = ''
                self._key = None
                self.status = False

        def create(self):
            try:
                self.created = datetime.datetime.utcnow()
                self.updated = self.created
                self.password = self.hash_password()
                to_insert = self.to_dict()
                for key in self.attributes:
                    if key in to_insert and to_insert[key] == None:
                        to_insert.pop(key)
                ins_obj = self.db[self.get_collection()].createDocument(to_insert)
                ins_obj.save()
                self._key = ins_obj._key
            except:
                ins_obj = None
                self.status = False
            return ins_obj != None
            
        def verify_password(self):
            try:
                chk_data = self.db[self.get_collection()].fetchDocument( self.get('username'))
                stored_password = chk_data["password"]
                self._key = chk_data["_key"]
                self.username = chk_data['username']
            except:
                return False
            salt = stored_password[:64]
            stored_password = stored_password[64:]
            pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                        self.get('password').encode('utf-8'), 
                                        salt.encode('ascii'), 
                                        100000)
            pwdhash = binascii.hexlify(pwdhash).decode('ascii')
            return pwdhash == stored_password

        def hash_password(self):
            salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
            pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), 
                                        salt, 100000)
            pwdhash = binascii.hexlify(pwdhash)
            return (salt + pwdhash).decode('ascii')

        def update(self):
            try:
                self.updated = datetime.datetime.utcnow()
                if self.password != None and self.password != '':
                    self.password = self.hash_password()
                to_update = self.to_dict()
                to_update.pop('_key')
                to_update.pop('created')
                if self.password == None or self.password == '':
                    to_update.pop('password')
                for key in self.attributes:
                    if key in to_update and to_update[key] == None:
                        to_update.pop(key)
                update_obj = self.db[self.get_collection()].fetchDocument(self._key)
                before = update_obj['_rev']
                update_obj.set(to_update)
                update_obj.patch()
                after = update_obj['_rev']
            except:
                return False
            return before != after

    class AccessToken(BasicElement):
        db_name = 'securitylayer'
        
        @classmethod
        def get_collection(cls):
            return 'APITokens'

        def get_class(self):
            return 'AccessToken'

        def make(self):
            self.attributes = ['_key', 'created', 'updated', 'valid_thru', 'active', 'deleted', 'apiuser', 'apisecret', 'origin', 'partners', 'actions', 'allowed_types','permalink', 'oauth', 'oauth_urls', 'oauth_scopes', 'scopes']
            for key in self.attributes:
                setattr(self, key, None)
        
        def add_partner(self, partner_code):
            if self.partners == None:
                self.partners = []
            self.partners.append(partner_code)
            self.update()

        def build_from_access(self, api_access) -> None:
            for key in self.get('attributes'):
                setattr(self, key, api_access.get(key) if key in api_access.to_dict() and api_access.get(key) != None else self.get(key))
            self.apisecret = ''
            self.password = ''

        def auth(self):
            try:
                user = SecurityLayer.APIAccess('auth', {"username" : self.get('apiuser'), 'password' : self.get('apisecret')})
                if user.get('_key') != None:
                    self.build_from_access(user)
                    self._key = None
                    self.status = self.create()
                else:
                    self.status = False
            except:
                self.password = ''
                self._key = None
                self.status = False

        def create(self):
            try:
                self.created = datetime.datetime.utcnow()
                self.updated = self.created
                if self.get('origin') == None or self.get('origin') == '':
                    self.origin = ['NoCors']
                if not isinstance(self.get('origin'), list):
                    self.origin = [self.get('origin')]
                if not isinstance(self.get('oauth_urls'), list):
                    self.oauth_urls = [self.get('oauth_urls')]
                if self.get('permalink') == True:
                    self.valid_thru = self.created + datetime.timedelta(weeks=52000)
                else:
                    p = Metadata.Parameter('find', {'_key' : 'api_token_lifespawn'})
                    api_token_lifespawn = p.get('value')
                    self.valid_thru = self.created + datetime.timedelta(minutes=api_token_lifespawn)
                self.active = True
                self.deleted = False
                to_insert = self.to_dict()
                for key in self.attributes:
                    if key in to_insert and to_insert[key] == None:
                        to_insert.pop(key)
                ins_obj = self.db[self.get_collection()].createDocument(to_insert)
                ins_obj.save()
                self._key = ins_obj._key
                self.status = True
            except:
                ins_obj = None
                self.status = False
            return ins_obj != None

        def find(self):
            # try:
            found = self.db[self.get_collection()].fetchFirstExample({"_key": self._key, "active": True})[0]
            if self.get('origin') == None or self.get('origin') == '':
                self.origin = 'NoCors'
            if max([self.get('origin').find(url) for url in found['origin']]) != 0 and max(['DevToken'.find(url) for url in found['origin']]) != 0:
                found = None
            for key in self.attributes:
                setattr(self, key, found[key] if key in found else self.get(key))
            self.valid_thru = datetime.datetime.strptime(self.valid_thru, '%Y-%m-%d %H:%M:%S.%f')
            if self.valid_thru < datetime.datetime.utcnow() or not self.active:
                self.active = False
                delete_thread = Thread(target=found.delete)
                delete_thread.start()
            else:
                if self.permalink != True:
                    p = Metadata.Parameter('find', {'_key' : 'api_token_lifespawn'})
                    api_token_lifespawn = p.get('value')
                    found['valid_thru'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=api_token_lifespawn)
                    update_thread = Thread(target=found.save)
                    update_thread.start()
            self.status = self.active
            # except:
            #     self._key = None
            #     self.status = False


    class APIAccess(BasicElement):
        db_name = 'securitylayer'
        
        @classmethod
        def get_collection(cls):
            return 'APICredentials'

        def get_class(self):
            return 'APIAccess'

        def make(self):
            self.attributes = ['_key', 'password', 'username', 'created', 'updated', 'partners', 'actions', 'email', 'active', 'oauth_urls', 'oauth_scopes', 'allowed_types', 'deleted']
            for key in self.attributes:
                setattr(self, key, None)

        def update_all_tokens(self):
            tokens_list = SecurityLayer.AccessToken('fetch_exact', {'apiuser': self.get('username')}).found
            for t in tokens_list:
                token = SecurityLayer.AccessToken('find', {'_key':t.get('_key')})
                token.build_from_access(self)
                token.update()
        
        def add_partner(self, partner_code):
            if self.partners == None:
                self.partners = []
            self.partners.append(partner_code)
            self.update()
        
        def auth(self):
            try:
                self.status = self.verify_password()
            except:
                self.password = ''
                self._key = None
                self.status = False
            
        def verify_password(self):
            try:
                chk_data = self.db[self.get_collection()].fetchDocument(self.username)
                stored_password = chk_data["password"]
            except:
                try:
                    chk_data = self.db[self.get_collection()].fetchFirstExample({'username':self.username})[0]
                    stored_password = chk_data["password"]
                except:
                    return False
            self._key = chk_data["_key"]
            self.partners = chk_data["partners"]
            self.actions = chk_data["actions"]
            self.permalink = chk_data["permalink"]
            self.oauth_scopes = chk_data["oauth_scopes"]
            self.allowed_types = chk_data.getStore().get("allowed_types")
            salt = stored_password[:64]
            stored_password = stored_password[64:]
            pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                        self.password.encode('utf-8'), 
                                        salt.encode('ascii'), 
                                        100000)
            pwdhash = binascii.hexlify(pwdhash).decode('ascii')
            return pwdhash == stored_password

        def hash_password(self):
            salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
            pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), 
                                        salt, 100000)
            pwdhash = binascii.hexlify(pwdhash)
            return (salt + pwdhash).decode('ascii')

        def update(self):
            try:
                self.updated = datetime.datetime.utcnow()
                if self.password != None and self.password != '':
                    self.password = self.hash_password()
                else:
                    self.password = None
                to_update = self.to_dict()
                to_update.pop('_key')
                to_update.pop('created')
                for key in self.attributes:
                    if key in to_update and to_update[key] == None:
                        to_update.pop(key)
                update_obj = self.db[self.get_collection()].fetchDocument(self._key)
                before = update_obj['_rev']
                update_obj.set(to_update)
                update_obj.patch()
                after = update_obj['_rev']
            except:
                return False
            return before != after

        def create(self):
            try:
                self.created = datetime.datetime.utcnow()
                self.updated = self.created
                self.active = True
                self.deleted = False
                self.password = self.hash_password()
                to_insert = self.to_dict()
                for key in self.attributes:
                    if key in to_insert and to_insert[key] == None:
                        to_insert.pop(key)
                ins_obj = self.db[self.get_collection()].createDocument(to_insert)
                ins_obj.save()
                self._key = ins_obj._key
            except:
                ins_obj = None
                self.status = False
            return ins_obj != None

