from pydantic import BaseModel
from colorama import Back,Fore, init
init(autoreset=True)


class Movie(BaseModel):
    title: str
    release_year: int
    genres: list[str]
    recommended: bool
    
"""movie = Movie(
    title= "Interestellar",
    release_year= 2014,
    genres= ["Science fiction", "Drama"],
    recommended= True,
)"""
    
movie = Movie(
    title="Interstellar",
    release_year="not a year",
    genres=["Science fiction"],
    recommended=True,
)
    
print(Fore.GREEN + "Movie class")    
print(movie)

print(Fore.YELLOW + "\n \n Movie Title")
print(movie.title)

print(Fore.CYAN + "\n \n Movie Genres")
print(movie.genres)

print(Fore.BLUE + "\n \n Model")
print(movie.model_dump())

print(Fore.GREEN + "\n \n Model Json")
print(movie.model_dump_json(indent=4))