from http.client import HTTPException

import pandas as pd
from pydantic.v1 import ValidationError

from src.models import User


class Services:
    def __init__(self):
        self.userList = []

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
        df = pd.read_csv(file)

        for _, row in df.iterrows():
            if pd.isna(row['Name']):
                self.userList.clear()
                raise Exception('Empty name is not valid')
            self.userList.append(User(name=row['Name'], age=row['Age']).dict())

    def clear_users(self):
        self.userList.clear()

    def calculate_users_average_age_of_each_group(self):
        df = pd.DataFrame(self.userList)
        if df.empty:
            return {}

        df['firstCharacter'] = df['name'].str[0]

        for key, group in df.groupby('firstCharacter'):
            print(f"Group {key}")
            print(group)

        return df.groupby('firstCharacter')['age'].mean().to_dict()