import pandas as pd
import os

USERS_DB_PATH = os.path.join(os.path.dirname(__file__), 'user_db.csv')


class database:
    
    def __init__(self) -> None:
        if not os.path.isfile(USERS_DB_PATH):
            df = pd.DataFrame([['0', 'none', 'none', 'none', 'none']], columns= ['phone','username', 'password', 'public_key', 'private_key'])
            df.to_csv(USERS_DB_PATH, index = False)

 


    def insert_user(self, phone, username, password):
        df = pd.read_csv(USERS_DB_PATH, index_col= phone)
        
        if int(phone) in df.index:
            print('client already exists')
        else:
            df.loc[len(df)] = [phone, username, password, '', '']
            print(df)
            df.to_csv(USERS_DB_PATH, index_label= 'id')
            print('success')

        

    def get_users_key(self, id):
        df = pd.read_csv(USERS_DB_PATH)
        return {'public_key': df.loc[id, 'public_key'] , 'private_key': df.loc[id, 'private_key']}

    def check_login(self, username, password):
        df = pd.read_csv(USERS_DB_PATH)
        if df.loc[username, password]:
            return{'success': True, 'id': df.loc[username, password, 'id']}

    def add_user_keys(self, id, username, password, public_key, private_key): 
        df = pd.read_csv(USERS_DB_PATH, index_col= 'id')
        if id in df.index:
            df.loc[id] = [id, username, password, public_key, private_key]

    
    
    
if __name__ == '__main__':
    db = database()
    db.insert_user(phone= 10, username= 'null', password= 'null')
    