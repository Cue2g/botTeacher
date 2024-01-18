
from mongo import DBConnection

class users:
    def __init__(self, id:int, name:str, lastname:str, username:str, level:str=None, lang:str= None ) -> None:
        self.id = id
        self.name = name
        self.lastname = lastname
        self.username = username
        self.level = level
        self.lang = lang

    def __str__(self):
        return f"Nombre: {self.id}, Tipo: {self.name}, Correo: {self.level}"
    
    @classmethod
    def create_user(cls, id, name, lastname, username, level, lang):
        new_user = cls(id, name, lastname, username, level, lang)
        db = DBConnection().get_db()
        db.users.insert_one({
            'id': new_user.id,
            'name': new_user.name,
            'lastname': new_user.lastname,
            'username': new_user.username,
            'level': new_user.level,
            'lang': new_user.lang
        })
        return new_user

    @classmethod
    def update_user(cls, user_id, new_data):
        db = DBConnection().get_db()
        db.users.update_one({'id': user_id}, {'$set': new_data})

    @classmethod
    def find_user(cls, user_id):
        db = DBConnection().get_db()
        user_data = db.users.find_one({'id': user_id})

        if user_data:
            return user_data
        else:
            return None
    
    @classmethod
    def update_lang(cls, user_id:int, lang:str):
        db = DBConnection().get_db()
        langData = {"lang":lang}
        result = db.users.update_one({'id': user_id}, {'$set': langData})
        if result.modified_count == 0:
            return None
        return True