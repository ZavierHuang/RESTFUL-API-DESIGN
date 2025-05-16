import pandas as pd
from fastapi import HTTPException

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
        for item in self.userList:
            if item['name'] == user.name:
                return False

        self.userList.append(user.dict())
        return True

    def delete_user(self, userName):
        for item in self.userList:
            if item['name'] == userName:
                self.userList.remove(item)
                return True
        return False

    def add_user_from_csv(self, file):
        df = pd.read_csv(file)
        totalData = len(df)

        df['Name'] = df['Name'].str.strip()
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        df = df.dropna()

        df['Age'] = df['Age'].astype(int)
        df = df[df['Age'] >= 0]
        df = df[df['Name'].str.len() > 0]

        validData = len(df)
        for _, row in df.iterrows():
            user = User(name=row['Name'], age=row['Age']).dict()
            self.userList.append(user)

        return f'({validData}/{totalData})'

    def clear_users(self):
        self.userList.clear()

    def calculate_users_average_age_of_each_group(self):
        df = pd.DataFrame(self.userList)
        if df.empty:
            return {}

        df['firstCharacter'] = df['name'].str.strip().str[0]

        return df.groupby('firstCharacter')['age'].mean().to_dict()

    def update_user_age(self, user):
        for item in self.userList:
            if item['name'] == user.name:
                item['age'] = user.age
                return True
        return False
