import json


book = {"title": "a man named Ove", 
        "author": "Elif Shafak",
        "year" : 1990,
        "genres": ["romance", "adventure"]}


"""print(book["title"])
print(book['genres'][0])
print(len(book["genres"]))

book["rating"] = 9"""


print("my dictionary")
print(type(book))
print(book)

json_text = json.dumps(book, indent = 4)


with open("book.json", "w", encoding="utf-8") as f:
    json.dump(book, f, indent = 4)
    


with open("book.json", "r", encoding="utf-8") as f :
    loaded_book = json.load(f)


print("dictionary converted to json")
print(type(json_text))
print(json_text)

print("loaded json")
print(type(loaded_book))
print(loaded_book)