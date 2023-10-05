import os
import json
from typing import Optional
from abc import ABC, abstractmethod
import logging
from chainlit.types import AppUser
import chainlit as cl


class AbstractLoginHandler(ABC):

    @abstractmethod
    def login(self, username: str, password: str) -> Optional[dict]:
        """
        Abstract method to authenticate a user and return user details if authentication is successful.

        Returns user details (including role) if valid, else None.
        """
        pass


class ChainlitLoginWithJSONCredentials(AbstractLoginHandler):
    """
    Initialize the ChainlitLogin instance by loading user credentials from a specified JSON file.

    The path to the JSON file is read from the USER_CREDENTIALS_FILE environment variable. If not set,
    it defaults to "./data/user_credentials.json".

    Note: This is a naive implementation designed only for development purposes. In a production setting,
    consider using a more secure authentication system with proper hashing and salting of passwords.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.users = {}
        users_credentials_file_path = os.environ.get("USER_CREDENTIALS_FILE", "./data/user_credentials.json")

        try:
            with open(users_credentials_file_path, 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            print("Warning: users.json not found. No users loaded.")
        except json.JSONDecodeError:
            print("Error: users.json contains invalid JSON.")

    def login(self, username: str, password: str) -> Optional[dict]:
        self.logger.info(f"User '{username}' logging in")

        user_data = self.users.get(username)
        if user_data and user_data["password"] == password:
            return {"username": username, "role": user_data["role"]}
        return None

    @staticmethod
    @cl.password_auth_callback
    def auth_callback(username: str, password: str) -> Optional[AppUser]:
        login_instance = ChainlitLoginWithJSONCredentials()
        user_data = login_instance.login(username, password)
        if user_data:
            return AppUser(username=user_data["username"], role=user_data["role"], provider="credentials")
        else:
            return None
