import webbrowser


class Movie():
    """List of Movie instance variables and methods
    
    Attributes:
        Movie title
        Storyline
        Poster Image
        YouTube Trailer
        Release Date
    """
    def __init__(self, movie_title, movie_storyline, poster_image,
                 trailer_youtube, release_date):
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube
        self.release_date = release_date

    def show_trailer(self):
        # Plays YouTube trailers
        webbrowser.open(self.trailer_youtube_url)
