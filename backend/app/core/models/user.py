from bson.objectid import ObjectId

class User:
    def __init__(self, username, password, _id=None):
        self.id = _id if _id else ObjectId()
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "_id": self.id,
            "username": self.username,
            "password": self.password
        }

    @staticmethod
    def from_dict(data):
        return User(
            username=data.get("username"),
            password=data.get("password"),
            _id=data.get("_id")
        )