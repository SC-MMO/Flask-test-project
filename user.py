class user():
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

    def __eq__(self, other): 
        if not isinstance(other, user):
            return NotImplemented

        return self.username == other.username and self.password and other.password
    
    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }