import json
from utils.errors import UserExeption


class User:
    def __init__(self, region: str, district: str, role: str):
        self.region = region
        self.district = district
        self.role = role
        self.credentials = self.__get_credentials()

    def __get_credentials(self) -> dict:
        response = {"organisation": {}}
        with open("/code/conf/users.json", "r") as f:
            users = json.loads(f.read())
        if self.region not in users.keys():
            raise UserExeption(f"Нет данных для региона {self.region}")
        if self.district not in users[self.region].keys():
            raise UserExeption(f"Нет данных для региона {self.region}: {self.district}")
        if self.role not in users[self.region][self.district].keys():
            raise UserExeption(f"Нет данных для роли {self.role} в регионе {self.region}: {self.district}")
        response["user"] = users[self.region][self.district][self.role]
        if "fullname" in users[self.region][self.district].keys():
            response["organisation"]["fullname"] = users[self.region][self.district]["fullname"]
        if "id" in users[self.region][self.district].keys():
            response["organisation"]["id"] = users[self.region][self.district]["id"]
        return response
        

    def login(self) -> str:
        return self.credentials["user"]["login"]

    def password(self) -> str:
        return self.credentials["user"]["password"]
    
    def username(self) -> str:
        if "username" in self.credentials.keys():
            return self.credentials["user"]["username"]
        raise UserExeption(f"Имя пользователя неизвестно: {self.credentials}")
    
    def department_name(self) -> str:
        if "organisation" in self.credentials.keys():
            return self.credentials["organisation"]["fullname"]
    
    def department_id(self) -> str:
        if "organisation" in self.credentials.keys():
            return self.credentials["organisation"]["id"]


