from pymongo import MongoClient

client = MongoClient('mongodb+srv://tvkrishsoni:6igYEp1sLrgoTLdH@cluster0.x46sweo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['my_database']

users = db['users']

user_schema = {
    'username': str,
    'email': str,
    'password': str,
    'otp': str,
    'otp_expiry': int  
}