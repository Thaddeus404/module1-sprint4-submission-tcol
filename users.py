import hashlib
from pathlib import Path
from movie import Movie

class User:
    def __init__(self, username):
        self.username = username
        self.users_file = Path("profiles") / "users.txt"
        self.password_file = Path("profiles") / "passwords.txt"

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def get_user(self):
        """If a user with a typed name doesn't exist, a new user will be created - password as well.
        List of users will be stored in a file called users.txt and passwords are hashed stored in passwords.txt"""

        if not self.users_file.exists():
            self.users_file.touch()
        
        if not self.password_file.exists():
            self.password_file.touch()

        with self.users_file.open("r") as f:
            users = f.read().splitlines()

        with self.password_file.open("r") as f:
            passwords = f.read().splitlines()

        user_pass_dict = dict(zip(users, passwords))

        if self.username in users:
            for _ in range(3):
                password = input("Enter your password: ")
                if not password:
                    print("No password entered. Exiting...")
                    return None
                
                if user_pass_dict.get(self.username) == self.hash_password(password):
                    print(f"Welcome back, {self.username}!")
                    return self
                print(f"Incorrect password. Please try again or press Enter to quit.")
            print("Too many failed password enter attempts. Exiting...")
            return None

        else:
            while True:
                password = input("Create a password (minimum 6 characters): ")
                if len(password) < 6:
                    print("Password too short!")
                    continue
                confirm_password = input("Confirm password: ")
                if password != confirm_password:
                    print("Passwords don't match!")
                    continue
                break

            hashed_pass = self.hash_password(password)
            
            with self.users_file.open("a") as f:
                f.write(f"{self.username}\n")
            with self.password_file.open("a") as f:
                f.write(f"{hashed_pass}\n")
                
            print(f"User '{self.username}' has been created.")

        return self

    # this will check if the user(name) is accessed correctly
    def __repr__(self):
        return f"User(username='{self.username}')"