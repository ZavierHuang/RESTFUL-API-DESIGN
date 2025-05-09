class Services:
    def __init__(self):
        self.userList = []

    def list_users(self):
        return self.userList


    def add_user(self, user):
        self.userList.append(user)

