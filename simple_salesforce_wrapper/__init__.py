from simple_salesforce import SalesforceResourceNotFound, SalesforceLogin, SFType
from .connection_manager import SalesForceConnection as Salesforce


def quick_regression(salesforce_obj):
    dummy_account = {
        "name": "Biz Name",
        "Phone": "+61000000000",
        "ShippingStreet": "Unit 1234",
        "ShippingCity": "Sydney",
        "ShippingState": "NSW",
        "ShippingPostalCode": "1122",
        "ShippingCountry": "Australia",
        "ShippingLatitude": "23.2",
        "ShippingLongitude": "23.4",
    }

    account_obj = salesforce_obj.Account.create(dummy_account)
    print(repr(account_obj))
    sfid = account_obj.get("id")
    print("Retreiving Object {}", repr(salesforce_obj.Account.get(sfid)))
    updated_account_obj = salesforce_obj.Account.update(sfid, {"ShippingCity": "NewCastle"})
    print(repr(updated_account_obj))
    print("Retreiving Object {}", repr(salesforce_obj.Account.get(sfid)))
    print(repr(salesforce_obj.Account.delete(sfid)))
    try:
        print("Retreiving Object {}", repr(salesforce_obj.Account.get(sfid)))
    except SalesforceResourceNotFound:
        print("Success. The resource is not found")

if __name__ == "__main__":
    SALESFORCE_INSTANCE = {
        "username": 'EMAIL@EXAMPLE.COM',
        "password": 'EXAMPLEPASSWORD',
        "security_token": 'SECURITY_TOKEN',
        "sandbox": True
    }
    sf = Salesforce(username=SALESFORCE_INSTANCE.get("username"),
                    password=SALESFORCE_INSTANCE.get("password"),
                    security_token=SALESFORCE_INSTANCE.get("security_token"),
                    sandbox=SALESFORCE_INSTANCE.get("sandbox"))
    quick_regression(sf)
