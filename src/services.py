import pandas as pd
from src.models import User


class Services:
    def __init__(self):
        self.userList = [
            {'name': 'Zavier', 'age': 20},
            {'name': 'John', 'age': 21},
            {'name': 'Steve', 'age': 22},
            {'name': 'Charies', 'age': 23}
        ]

    def list_users(self):
        return self.userList

    def add_user(self, user):
        self.userList = [item for item in self.userList if item['name'] != user.name]
        self.userList.append(user.dict())

    def delete_user(self, userName):
        for item in self.userList:
            if item['name'] == userName:
                self.userList.remove(item)
                return True
        return False

    def add_user_from_csv(self, file):
        self.clear_users()
        df = pd.read_csv(file)

        df['Name'] = df['Name'].str.strip()
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        df = df.dropna()

        df['Age'] = df['Age'].astype(int)
        df = df[df['Age'] >= 0]
        df = df[df['Name'].str.len() > 0]

        for _, row in df.iterrows():
            user = User(name=row['Name'], age=row['Age']).dict()
            self.userList.append(user)


    def clear_users(self):
        self.userList.clear()

    def calculate_users_average_age_of_each_group(self):
        df = pd.DataFrame(self.userList)
        if df.empty:
            return {}

        df['firstCharacter'] = df['name'].str.strip().str[0]

        # for key, group in df.groupby('firstCharacter'):
        #     print(f"Group {key}")
        #     print(group)

        return df.groupby('firstCharacter')['age'].mean().to_dict()