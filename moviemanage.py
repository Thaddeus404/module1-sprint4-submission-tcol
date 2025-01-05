import csv
import requests
import json
import os
from pathlib import Path
from movie import Movie
from users import User as usr

tmdb_api_key = os.getenv("TMDB_API_KEY")

class MovieManage(Movie):
    def __init__(self, username, title=None, release_date=None, rating=None, overview=None, user_rating=None):
        super().__init__(title, release_date, rating, overview, user_rating)
        self.username = username
        self.file_path = Path("profiles") / f"{self.username}.csv"
        self.movies = []

    def check_for_profiles_dir(self):
        """Profiles directory should always exist, if not – it will be automatically created and users alongside their movie lists will be created"""
        profiles_dir = Path("profiles")
        profiles_dir.mkdir(exist_ok=True)
    
    def check_for_csv(self):
        """If a user's movie list doesn't exist, a new file will be created"""
        if not self.file_path.exists():
            with self.file_path.open(mode="w", newline="") as file:
                writer = csv.DictWriter(
                    file, 
                    fieldnames=["title", "release_date", "rating", "overview", "movie_id", "user_rating", "watchlist"]
                )
                writer.writeheader()
            print(f"A new profile for {self.username} created in profiles folder.")

    def load_csv(self):
        if self.file_path.exists():
            with self.file_path.open(mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    movie = Movie.from_row(row)
                    self.movies.append(movie)
            print(f"{self.username} movie list loaded successfully.")
        else:
            print(f"Profile for {self.username} doesn't exist.")

    def save_csv(self):
        current_movie_list = []
        with self.file_path.open(mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                current_movie_list.append(row)
        
        current_movie_list_to_dict = [Movie.from_row(row).movie_to_dict() for row in current_movie_list]
        movie_dupe_check = {movie["title"] for movie in current_movie_list_to_dict}
        for each_movie in self.movies:
            if each_movie.movie_to_dict()["title"] not in movie_dupe_check:
                current_movie_list_to_dict.append(each_movie.movie_to_dict())
            else:
                print(f"{each_movie.movie_to_dict()["title"]} already exists in your movie list collection. It has not been added.")
                return False

        with self.file_path.open(mode="w", newline="") as file:
            writer = csv.DictWriter(
                file, 
                fieldnames=["title", "release_date", "rating", "overview", "movie_id", "user_rating", "watchlist"]
            )
            writer.writeheader()
            writer.writerows(current_movie_list_to_dict)
        return True

    def access_tmdb(self):
        url = "https://api.themoviedb.org/3/authentication"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {tmdb_api_key}"
        }
        response = requests.get(url, headers=headers).json()
        return response["success"]

    def search_for_movie(self, movie_title, year=None):
        """search_for_movie function searches for a movie using TMDb API and returning movie details (year parameter is optional)."""
        
        if self.access_tmdb():
            url = "https://api.themoviedb.org/3/search/movie"
            params = {
                "query": movie_title,
                "page": 1,
            }
            if year is not None:
                params["primary_release_year"] = str(year)

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {tmdb_api_key}"
            }
            response = requests.get(url, params=params, headers=headers).json()

            if response.get("total_results", 0) == 0:
                print(f"No movie found with the title '{movie_title}'.")
                return None

            movie_info = response["results"][0]
            print("\nMovie found! Details below:")
            print(f"Title: {movie_info["title"]}")
            print(f"Release Date: {movie_info["release_date"][:4]}")
            print(f"TMDb Rating: {movie_info["vote_average"]}")
            print(f"Synopsis: {movie_info["overview"]}")

            prompt_to_add = input("Would you like to add this movie to your Movie Collection? (y/n): ").strip().lower()
            
            if prompt_to_add in ["y", "yes"]:
                prompt_user_rating = input("If you've seen the movie, please rate it (1-10) otherwise, leave this blank: ").strip()
                user_rating = float(prompt_user_rating) if prompt_user_rating.isdigit() and 1 <= float(prompt_user_rating) <= 10 else None
                new_movie = Movie(
                    title=movie_info["title"],
                    release_date=movie_info["release_date"][:4],
                    rating=movie_info["vote_average"],
                    overview=movie_info["overview"],
                    movie_id=movie_info["id"],
                    user_rating=user_rating,
                    watchlist="No" if user_rating else "Yes"
                )
                self.movies.append(new_movie)
                if self.save_csv():
                    print(f"{movie_info["title"]} has been added to your movie list & {self.username} movie list was saved succesfully.")
            else:
                print(f"{movie_info["title"]} was not added to your movie list.")
        else:
            print("Unable to access TMDb. Check if API key is correctly stored in your environment variables and try again.")
            print(self.access_tmdb())
            return None

    def check_reqs(self):
        self.check_for_profiles_dir()
        self.check_for_csv()
        user = usr(self.username)
        user.get_user()
        self.load_csv()

    def print_movie_list(self):
        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                movie_dict = {index: row for index, row in enumerate(reader, 1)}
                if not movie_dict:
                    print("No movies were found in your movie list. Please add some before trying to view them.")
                    return False
                
                print("Your Movie List:")
                for idx, row in movie_dict.items():
                    print(f"{idx}. Movie: {row["title"]} ({row["release_date"].strip()}) - TMDb rating: {row["rating"].strip()} - Your Rating: {row["user_rating"]} - Added to watchlist: {row["watchlist"]}")
        except FileNotFoundError:
            print(f"Filepath {self.file_path} was not found, please check if it exists in your directory.")
            return
        return movie_dict

    def open_movie_list(self):
        movie_dict = self.print_movie_list()
        if not movie_dict:
            return
        
        prompt_more = input("If you'd like to read a synopsis of a movie, please enter its number from the list or type 'q' to quit: ").strip().lower()
        
        while True:
            if prompt_more in ["q", "quit"]:
                break
            if prompt_more.isdigit() and int(prompt_more) in movie_dict:
                chosen_movie = movie_dict[int(prompt_more)]
                print(f"Synopsis for '{chosen_movie["title"]}': {chosen_movie["overview"]}")
                prompt_more = input("For other synopsis, type a movie number. Alternatively, type 'm to see movie list again or type 'q' to quit: ").strip().lower()
            else:
                print("Please enter a number from the list or type 'q' to quit the program.")
                continue

        

    def manage_movie_list(self):
        movie_dict = self.print_movie_list()
        if not movie_dict:
            return
        with open(self.file_path, mode="r", newline="") as file:
            rows = list(csv.DictReader(file))
        while True:        
            watchlist_or_rating = input("\nWould you like to manage your watchlist, ratings, or delete a movie from the list? ('w'/'r'/'d') (type 'q' to quit): ").strip().lower()
            if watchlist_or_rating == "w":
                self.manage_watch_list(rows, movie_dict)
            elif watchlist_or_rating == "r":
                self.manage_user_rating(rows, movie_dict)
            elif watchlist_or_rating == "d":
                self.manage_remove_movie(rows, movie_dict)
            elif watchlist_or_rating in ["q", "quit"]:
                break
            else:
                print("Please enter a valid option: either 'w', 'r', or 'd'. Alternatively, type 'q' to quit the program.")
        print ("Exiting movie manager.")    
            
    def manage_watch_list(self, rows, movie_dict):
        try:
            print("Managing your movie watchlist statuses. Type 'q' to quit.")
            while True:
                select = input("Please select id of the movie that you'd like to add/remove to watchlist or type 'q' to quit: ")
                if select in ["q", "quit"]:
                    break
                if not select.isdigit() or int(select) not in movie_dict:
                    print("Please enter a valid number from the list or type 'q' to quit the program.")
                    continue

                select = int(select)
                selected = movie_dict[select]
                status_current = selected["watchlist"]
                status_new = "No" if status_current == "Yes" else "Yes"

                selected["watchlist"] = status_new
                print(f"{movie_dict[select]["title"]} watchlist status changed to {status_new}.")

            with open(self.file_path, mode="w", newline="") as file:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(movie_dict.values())
                    
        except Exception as e:
            print(f"Error occured: {e}.")

    def manage_user_rating(self, rows, movie_dict):
        try:
            print("Managing your movie ratings. Type 'q' to quit.")
            while True:
                select = input("Please select id of the movie that you'd like to rate or type 'q' to quit: ")
                if select in ["q", "quit"]:
                    break
                if not select.isdigit() or int(select) not in movie_dict:
                    print("Please enter a valid number from the list or type 'q' to quit the program.")
                    continue
                select = int(select)
                selected = movie_dict[select]
                user_rating = input("Please enter a rating (1-10) for the movie: ")
                if not user_rating.isdigit() or not 1 <= int(user_rating) <= 10:
                    print("Please enter a valid rating between 1 and 10.")
                    continue

                selected["user_rating"] = user_rating
                print(f"{movie_dict[select]["title"]} rating changed to {user_rating}.")

            with open(self.file_path, mode="w", newline="") as file:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(movie_dict.values())
                    
        except Exception as e:
            print(f"Error occured: {e}.")

    def manage_remove_movie(self, rows, movie_dict):
        try:
            print("Movie removal activated. Type 'q' to quit.")
            while True:
                select = input("Please select id of the movie that you'd like to remove or type 'q' to quit: ")
                if select in ["q", "quit"]:
                    break
                if not select.isdigit() or int(select) not in movie_dict:
                    print("Please enter a valid number from the list or type 'q' to quit the program.")
                    continue
                select = int(select)
                selected = movie_dict[select]
                confirm_deletion = input(f"Please confirm whether you'd really like to remove {selected["title"]} from your movie list ('y'/'n'): ")
                if confirm_deletion not in ["y", "yes"]:
                    continue
                movie_dict.pop(select)
                print(f"{selected["title"]} removed from your movie list.")

            with open(self.file_path, mode="w", newline="") as file:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(movie_dict.values())
                    
        except Exception as e:
            print(f"Error occured: {e}.")
    
    def recommend_movies(self):
        if not self.access_tmdb():
            print("Unable to access TMDb. Check if API key is correctly stored in your environment variables and try again.")
            return
        
        movie_dict = self.print_movie_list()
        if not movie_dict:
            return
        
        while True:
            select = input("Enter the ID of the movie you'd like to get recommendations based on or type 'q' to quit: ").strip().lower()
            if select in ["q", "quit"]:
                print("Exiting movie recommendations mode.")
                return
            
            if not select.isdigit() or int(select) not in movie_dict:
                print(f"Invalid selection. No movies with ID{select} exist.")
                continue

            selected = movie_dict[int(select)]
            movie_id = selected.get("movie_id")

            if not movie_id:
                print("There is an error with fetching movie ID from your movie list, please check if it has been unchanged.")
                return
            
            print(f"Fetching movie recommendations based on: {selected["title"]}. . .")

            rec_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {tmdb_api_key}"
            }

            rec_response = requests.get(rec_url, headers=headers).json()

            if rec_response.get("total_results", 0) == 0:
                print("No recommendations available for this movie.")
                return

            print("Recommended Movies:")
            rec_movies = rec_response["results"][:5]
            movie_choices = {}

            for index, movie in enumerate(rec_movies, 1):
                print(f"{index}. {movie["title"]} ({movie["release_date"][:4]}) - TMDb Rating: {movie["vote_average"]}")
                movie_choices[index] = movie

            rec_select = input("Enter the number of a recommended movie to add it to your collection or type 'q' to quit: ").strip().lower()

            if rec_select in ["q", "quit"]:
                print("Exiting recommendations.")
                return

            if rec_select.isdigit() and int(rec_select) in movie_choices:
                selected_movie = movie_choices[int(rec_select)]

                new_movie = Movie(
                    title=selected_movie["title"],
                    release_date=selected_movie["release_date"][:4],
                    rating=selected_movie["vote_average"],
                    overview=selected_movie.get("overview", "No synopsis available."),
                    movie_id=selected_movie["id"],
                    user_rating=None,
                    watchlist="Yes"
                )
                self.movies.append(new_movie)

                if self.save_csv():
                    print(f"'{selected_movie["title"]}' has been added to your movie list.")
            else:
                print("Invalid selection. Returning to main menu.")
            


if __name__ == "__main__":
    ...