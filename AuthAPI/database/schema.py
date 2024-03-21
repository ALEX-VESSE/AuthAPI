from pymongo import MongoClient

client = MongoClient('')
db = client['my_database']

users = db['users']

user_schema = {
    'username': str,
    'email': str,
    'password': str,
    'otp': str,
    'otp_expiry': int  
}
