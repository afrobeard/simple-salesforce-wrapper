from simple_salesforce import Salesforce, SalesforceExpiredSession
from .utils import convert_lead


class SalesForceObjectMock(object):
    def __init__(self, sf_instance, objname, manager_instance):
        self.sf_instance = sf_instance
        self.manager_instance = manager_instance
        self.sf_obj = getattr(sf_instance, objname)
        self.objname = objname

    def reconnect(self):
        self.manager_instance.connect(debug=True)  # Reconnect
        self.sf_obj = getattr(self.manager_instance.sf, self.objname)

    def create(self, sf_json):
        try:
            return self.sf_obj.create(sf_json)
        except SalesforceExpiredSession:
            print("Expired Salesforcesession, trying reconnection")
            self.reconnect()
            return self.sf_obj.create(sf_json)

    def update(self, sf_id, sf_json):
        try:
            return self.sf_obj.update(sf_id, sf_json)
        except SalesforceExpiredSession:
            print("Expired Salesforcesession, trying reconnection")
            self.reconnect()
            return self.sf_obj.update(sf_id, sf_json)

    def delete(self, sf_id):
        try:
            return self.sf_obj.delete(sf_id)
        except SalesforceExpiredSession:
            print("Expired Salesforcesession, trying reconnection")
            self.reconnect()
            return self.sf_obj.delete(sf_id)

    def get(self, sf_id):
        try:
            return self.sf_obj.get(sf_id)
        except SalesforceExpiredSession:
            print("Expired Salesforcesession, trying reconnection")
            self.reconnect()
            return self.sf_obj.get(sf_id)


class SalesForceConnection(object):
    def __init__(self, username, password, security_token, sandbox):
        self.sf = None
        (self.username,
         self.password,
         self.security_token,
         self.sandbox) = (username, password, security_token, sandbox)
        self.connect()

    def connect(self, debug=False):
        if debug:
            if self.sf:
                print("SF Object exists session ID {}".format(self.sf.session_id))
            else:
                print("No preexisting SF Object. Will try to create")
        self.sf = Salesforce(username=self.username,
                             password=self.password,
                             security_token=self.security_token,
                             sandbox=self.sandbox)
        if debug:
            print("Reconnect successful. New Session ID {}".format(self.sf.session_id))

    def convert_lead(self, lead_id, account_id):
        try:
            contact_id = convert_lead(self.sf.session, self.sf.session_id,
                                      sandbox=self.sf.sandbox, proxies=self.sf.proxies,
                                      sf_version=self.sf.sf_version, sf_instance=self.sf.sf_instance,
                                      lead_id=lead_id, account_id=account_id)
            return contact_id
        except SalesforceExpiredSession:
            print("Expired Salesforcesession, trying reconnection")
            self.reconnect()
            (status, code_or_id) = convert_lead(self.sf.session, self.sf.session_id,
                                                sandbox=self.sf.sandbox, proxies=self.sf.proxies,
                                                sf_version=self.sf.sf_version, sf_instance=self.sf.sf_instance,
                                                lead_id=lead_id, account_id=account_id)
            return status, code_or_id

    def query(self, query_string):
        """
        Access of the form where there is an underlying object connection
        e.g. 
        
        sf.query        
        :return: 
        """
        try:
            return self.sf.query(query_string)
        except SalesforceExpiredSession:
            print("Expired Salesforcesession, trying reconnection")
            self.connect(debug=True)  # Reconnect
            return self.sf.query(query_string)

    def __getattr__(self, name):
        """
        Access of the form where there is an underlying object connection
        e.g. 
        
        sf.query
        sf.Object.create
        sf.Object.update
        sf.Object.remove
        
        :param name 
        :return: 
        """
        try:
            return SalesForceObjectMock(self.sf, name, self)
        except SalesforceExpiredSession:
            print("Expired Salesforcesession, trying reconnection")
            self.connect(debug=True)  # Reconnect
            return SalesForceObjectMock(self.sf, name, self)
