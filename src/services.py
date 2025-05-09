import pandas as pd


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

    def add_user_from_csv(self, file):
        df = pd.read_csv(file)

        for _, row in df.iterrows():
            self.userList.append({"name": row['Name'], "age": row['Age']})

    def clear_users(self):
        self.userList.clear()

    def calculate_users_average_age_of_each_group(self):
        df = pd.DataFrame(self.userList)

        if df.empty:
            return {}

        df['firstCharacter'] = df['name'].str[0]

        # for key, group in df.groupby('firstCharacter'):
        #     print(f"Group {key}")
        #     print(group)

        return df.groupby('firstCharacter')['age'].mean().to_dict()