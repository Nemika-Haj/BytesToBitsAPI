from ._database import get_col

accounts = get_col("accounts")

class Account:

    def validate(email):
        return email.find("@") != -1
        

    def get(**kwargs):
        return accounts.find_one(kwargs)
    
    def create(**kwargs):
        return accounts.insert_one(kwargs)

    def delete(**kwargs):
        return accounts.delete_one(kwargs)
    
    def update(_id, **kwargs):
        return accounts.update_one({
            "_id": _id
        }, {
            "$set": kwargs
        })