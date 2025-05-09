class Services:
    def __init__(self):
        self.userList = []

    def list_users(self):
        return self.userList


    def add_user(self, user):
        self.userList.append(user.dict())

    def delete_user(self, userName):
        for item in self.userList:
            if item['name'] == userName:
                self.userList.remove(item)
                return


