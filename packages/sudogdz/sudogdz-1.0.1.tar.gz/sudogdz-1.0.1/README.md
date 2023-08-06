<p align='center'><img src='https://github.com/aye20054925/SudoGDZ/blob/main/png/Logo.png?raw=true'></p>
<h1 align='center'>SudoGDZ</h1>
<p align='center'>
	<img src="https://img.shields.io/badge/version-1.0.1-orange">
	<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/sudogdz">
	<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/aye20054925/sudogdz">
</p>
<p align='center'>Parser of everything from the Russian reshebnik GDZ.RU</p>

## Install
To start, execute this command in command line
```bash
pip install sudogdz
```

## Using and examples
### Get books and copybooks from GDZ.ru
To start using you have to import `sudogdz` into your project
```python
import sudogdz
```
Lets get a list of algebra textbooks for 7 Class and print textbook name and authors?
##### script.py
```python
import sudogdz as gdz

schoolitems = (
    gdz.getSchoolItems()
)  # ["matematika", "english", "russkii_yazik", "algebra", ...]

for i in gdz.getBooks("books", schoolclass=7, schoolitem=schoolitems[3]):
    print(f'{i["name"]}\n{i["class"]}')
```

### Get information about book / copybook
To get information about the textbook, we need to call the `getBooks` function and select the desired item. 
<br/>
We can get information about the textbook such as name, url, authors, publish house, class and cover.
##### script.py
```python
import sudogdz as gdz

schoolitems = (
    gdz.getSchoolItems()
)  # ["matematika", "english", "russkii_yazik", "algebra", ...]

booklist = gdz.getBooks("books", schoolclass=7, schoolitem=schoolitems[3])

book = booklist[3]  # can be any number as you want.

print(
    f"""
Имя: {book["name"]}
Ссылка: {book["url"]["with_domain"]}
Авторы: {",".join(book["authors"])}
Издательство: {book["pubhouse"]}
Обложка: {book["cover"]}
"""
)
```
### Get task list for book / copybook
To get a list of tasks for a specific book, you need to take the URL of the book and call the `getTasksForBook` function
##### script.py
```python
import sudogdz as gdz

books = gdz.getBooks("popularBooks")

book = books[6]

print(
    gdz.getTasksForBook(book["url"]["without_domain"])
)  # you could replace "without_domain" on "with_domain".
```

### Get answers for book / copybook
To get a list of answers, you also need to take the book's URL and call the `getAnswerForBook` function. You can parse the response image.
##### script.py
```python
import sudogdz as gdz

for answer in gdz.getAnswerForBook(
    "https://gdz.ru/class-6/matematika/a-g-merzlyak/3-18/"
):
    print(answer["png"])  # answer image.
```

## Build from source
In order to build a library from source, you need to install some dependencies
```bash
pip install -r requirements.txt
```
Since the library uses flit to easily build the library, you need to enter the following command
```bash
flit build
```
