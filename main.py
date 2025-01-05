from moviemanage import MovieManage as movman
from users import User as usr


def main():
    username = check_username()
    check_files(username)
    choices(username)
    return



def check_username():
    print("Hello!\nWelcome to your movie list manager!")
    while True:
        username = str(input("Please provide your username: ")).strip().lower()
        if not username:
            return False
        if len(username) < 3:
            print("Username should be at least 3 characters long.")
            continue
        return username

def check_files(username):
    movie_manager = movman(username)
    movie_manager.check_reqs()

def message():
    print("\nPlease select (1-5) whether you'd like to.")
    print("1. Open your movie (watch)list.")
    """Opening movie list will allow you to see your movie list and potentially read a synopsis of a movie."""
    print("2. Manage your movie (watch)list.")
    """Managing movie list will allow you to remove or update movies (watchlist status, user rating) in your movie list."""
    print("3. Search for a movie to potentially add to your collection.")
    """Searching for a movie will allow you to add a movie to your movie list."""
    print("4. Get movie recommendations based on your watched movies!")
    print("5. Exit the program.")

def choices(username):
    while True:
        try:
            message()
            user_input = int(input("\nEnter your choice number(1-5): "))
            if user_input < 1 or user_input > 5:
                print("Enter a valid choice number (1-5).")
                continue

        except ValueError:
            print("Enter a valid number!(1-999)")
            continue
        if user_input == 1:
            see_movie_list = movman(username)
            see_movie_list.open_movie_list()
            continue
        elif user_input == 2:
            manage_movie_list = movman(username)
            manage_movie_list.manage_movie_list()
            continue
        elif user_input == 3:
            search_tmdb_movie_name = input("Please enter a movie title to search for: ")
            search_tmdb_year_opt = input("If you would like to specify the year of movie release, please enter it now (or press Enter to continue without): ")
            search_movies = movman(username)
            search_movies.search_for_movie(search_tmdb_movie_name, search_tmdb_year_opt) 
            continue
        elif user_input == 4:
            pass
        elif user_input == 5 or user_input in ["exit", "quit", "q"]:
            print("Thanks for using the tool, until next time!")
            break

def add_movie():
    movie = str(input("Enter t"))


if __name__ == "__main__":
    main()