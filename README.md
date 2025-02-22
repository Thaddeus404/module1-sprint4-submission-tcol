# Movie Manager Application
Welcome to the Movie Watchlist application! This tool helps users manage their personal movie watchlist by adding, rating, and organizing movies, as well as receiving personalized movie recommendations.

I tried to do this project to showcase my current Python proficiency, including object-oriented programming, API integration, file I/O, and secure user authentication.

This program allows users to manage their movie watchlist by:

1. Searching for movies via the TMDb API.
2. Adding movies to their personal collection.
3. Rating watched movies and marking movies as "to-watch".
4. Receiving personalized recommendations (selection from the current user list).
5. The program saves user data locally, demonstrating file I/O operations using CSV files.

Main Components
1. **main.py** (Main Entry Point): Handles the program flow. It prompts the user for their username and guides them through the main menu options for managing their movie list.
2. **users.py** (User Class): Manages user authentication (login and account creation). Passwords are hashed using SHA-256 and stored securely.
3. **movie.py** (Movie Class): Represents individual movies. Stores attributes like title, release date, TMDb rating, user rating, and watchlist status.
4. **moviemanage.py** (MovieManage Class): Handles the main movie management logic:
   - search_for_movie(): Searches TMDb for a movie by title and release year (optional).
   - print_watchlist() and open_movie_list(): Opens movie list (either "to-watch", or all movies from the collection).
   - recommend_movies(): Fetches recommended movies based on a selected movie.
   - manage_movie_list(): Allows users to update their watchlist and ratings or delete movies.
   - save_csv() and load_csv(): Save and load user movie lists from CSV files.

Run this by simply changing your directory to the folder and write python _main.py_ in the terminal
