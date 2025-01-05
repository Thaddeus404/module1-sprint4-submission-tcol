import csv


class Movie:

    def __init__(self, title, release_date, rating, overview, movie_id, user_rating=None, watchlist=None):
        self.title = title
        self.release_date = release_date
        self.rating = rating
        self.overview = overview
        self.movie_id = movie_id
        self.user_rating = user_rating
        self.watchlist = watchlist
    
    @classmethod
    def from_row(cls, row):
        return cls(
            title=row["title"],
            release_date=row["release_date"],
            rating=float(row["rating"]),
            overview=row.get("overview", ""),
            movie_id=row["movie_id"],
            user_rating=float(row["user_rating"]) if row.get("user_rating") and row["user_rating"].isdigit() else None,
            watchlist=row.get("watchlist")
        )
    
    def movie_to_dict(self):
        return {
            "title": self.title,
            "release_date": self.release_date,
            "rating": self.rating,
            "overview": self.overview,
            "movie_id": self.movie_id,
            "user_rating": str(self.user_rating) if self.user_rating is not None else "",
            "watchlist": self.watchlist,
        }

if __name__ == "__main__":
    ...