import fresh_tomatoes
import media

# Movie list including title, storyline, poster image,
# YouTube trailer and release date
blade_runner = media.Movie("Blade Runner",
                           "&Ouml; &auml;u&szlig;erst A dystopian future where a clone hunter "
                           "faces his biggest challenge.",
                           "https://upload.wikimedia.org/wikipedia/en/5/53/Blade_Runner_poster.jpg",  # NOQA
                           "https://www.youtube.com/watch?v=4lW0F1sccqk",
                           "1982")

donnie_darko = media.Movie("Donnie Darko",
                           "After an accident a disturbed teenager "
                           "explores time, reality, and love.",
                           "https://upload.wikimedia.org/wikipedia/en/d/db/Donnie_Darko_poster.jpg",  # NOQA
                           "https://www.youtube.com/watch?v=ZZyBaFYFySk",
                           "2001")

harold_maude = media.Movie("Harold and Maude",
                           "A death obsessed teenager unexpectedly "
                           "falls in love.",
                           "https://upload.wikimedia.org/wikipedia/en/5/5f/Harold_and_Maude_%281971_film%29_poster.jpg",  # NOQA
                           "https://www.youtube.com/watch?v=5mz3TkxJhPc",
                           "1973")

nightmare_christmas = media.Movie("Nightmare Before Christmas",
                                  "Residents of spooky Halloweentown "
                                  "learn about Christmas.",
                                  "https://upload.wikimedia.org/wikipedia/en/9/9a/The_nightmare_before_christmas_poster.jpg",  # NOQA
                                  "https://www.youtube.com/watch?v=8qrB9I3DM80",  # NOQA
                                  "1993")

princess_bride = media.Movie("The Princess Bride",
                             "An adventure story with pirates, a mythical "
                             "kingdom, and true love.",
                             "https://upload.wikimedia.org/wikipedia/en/d/db/Princess_bride.jpg",  # NOQA
                             "https://www.youtube.com/watch?v=VYgcrny2hRs",
                             "1987")

the_hunger = media.Movie("The Hunger",
                         "A story of ancient vampire love set in "
                         "modern times.",
                         "https://upload.wikimedia.org/wikipedia/en/d/d6/The_Hunger_film_poster.jpg",  # NOQA
                         "https://www.youtube.com/watch?v=l9IDoAPC6Ps",
                         "1983")

# Stored list of movies
movies = [blade_runner, donnie_darko, harold_maude,
          nightmare_christmas, princess_bride, the_hunger]

# Converts movies to tiles and loads to page
fresh_tomatoes.open_movies_page(movies)
