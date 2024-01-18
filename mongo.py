from pymongo import MongoClient

#Singleton pattern
class DBConnection:
   _instance = None
   def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            cls._instance.client = MongoClient('')
            cls._instance.db = cls._instance.client['test']
        return cls._instance
   
   def get_db(cls):
        return cls._instance.db