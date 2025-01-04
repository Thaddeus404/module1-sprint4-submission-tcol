from pathlib import Path
from movie import Movie

class User:
    users_file = "users.txt"
    
    def __init__(self, username):
        self.username = username

    def get_user(self):
        """If a user with a typed name doesn't exist, a new user will be created
        List of users will be stores in a file called users.txt"""
        self.users_file = Path("profiles") / "users.txt"
        if not self.users_file.exists():
            self.users_file.touch()

        with self.users_file.open("r") as f:
            users = f.read().splitlines()

        if self.username in users:
            return self

        else:
            with self.users_file.open("a") as f:
                f.write(f"{self.username}\n")
                print(f"User named '{self.username}' has been created.")
        return self

    # this will check if the user(name) is accessed correctly
    def __repr__(self):
        return f"User(username='{self.username}')"