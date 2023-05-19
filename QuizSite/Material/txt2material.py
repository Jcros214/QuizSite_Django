class Verse:
    def __init__(self, verse: str, bookname: str, chapternum: int, versenum: int) -> None:
        self.verse = verse
        self.wordswpunc = verse.split(" ")
        self.words = []
        self.bookname = bookname
        self.chapternum = chapternum
        self.versenum = versenum

        [self.words.append(self.cleanWord(word)) for word in self.wordswpunc if self.cleanWord(word)]

        pass

    @staticmethod
    def cleanWord(word: str) -> str:
        return ''.join([letter.lower() for letter in word if letter.isalpha()])
    
    def __repr__(self) -> str:
        return f"<Verse {self.bookname} {self.chapternum}:{self.versenum}>"
    
    def __str__(self) -> str:
        return ' '.join(self.wordswpunc)


class Chapter:
    def __init__(self, verses) -> None:
        verses = list(verses)
        self.chapternum = verses[0].get('chapter')
        self.bookname = verses[0].get('book_name')
        self.verses = [Verse(verse.get('text'), self.bookname, self.chapternum, versenum+1) for versenum, verse in enumerate(verses)]
        self.verses: list[Verse]

    def __repr__(self) -> str:
        return f"<Chapter {self.bookname} {self.chapternum}>"
    
    def __str__(self) -> str:
        return '\n'.join([str(_) for _ in self.verses])
    
    @property
    def referance(self):
        return f"{self.bookname} {self.chapternum}"


class Book:
    def __init__(self, verses) -> None:
        verses = list(verses)
        self.chapters = []
        self.chapters: list[Chapter]
        
        # there must be a better way...
        verses.append({'chapter': None})

        versesInChapter = [verses.pop(0)]
        while verses:
            verse = verses.pop(0)

            if verse.get("chapter") == versesInChapter[0].get("chapter"):
                versesInChapter.append(verse)
            else:
                self.chapters.append(Chapter(versesInChapter))
                versesInChapter = [verse]

        # self.chapters.append(Chapter(versesInChapter, f"{versesInChapter[-1].get('book_name')} {versesInChapter[-1].get('chapter')}"))
        # versesInChapter = []


class Material:
    def __init__(self, verses):
        self.books = []
        self.onceUsedWords = set()
        self.twiceUsedWords = set()
        self.books: list[Book]

        versesInBook = [verses.pop(0)]
        while verses:
            verse = verses.pop(0)

            if verse.get("book") == versesInBook[0].get("book"):
                versesInBook.append(verse)
            else:
                self.books.append(Book(versesInBook))
                versesInBook = []

        self.books.append(Book(versesInBook))
        versesInBook = []

        self.getWords()

    def getWords(self) -> list[str]:
        allwords = {}
        
        for book in self.books:
            for chapter in book.chapters:
                for verse in chapter.verses:
                    for word in verse.words:
                        try:
                            allwords[word] += 1
                        except KeyError:
                            allwords[word] = 1

        
        for key in allwords:
            # TODO: what's the right way to do this?
            
            val = allwords[key]
            
            if val == 1:
                if val in self.onceUsedWords or val in self.twiceUsedWords:
                    raise ValueError("Attempted duplicate once used.")
                self.onceUsedWords.add(key)
            elif val == 2:
                if val in self.twiceUsedWords or val in self.onceUsedWords:
                    raise ValueError("Attempted duplicate twice used.")
                self.twiceUsedWords.add(key)


import os

os.chdir("./QuizSite/Material/")

# Deserialize txt into Book, Chapter, and Verse objects
import json

with open("matt5-7.json", "r") as fr:
    verses = json.load(fr)
    
material = Material(verses)

# Create HTML from material

html = ""

for book in material.books:
    html += '<div class="book">\n'
    for chapter in book.chapters:
        html += '\t<div class="chapter">\n'
        html += f'\t\t<h2>{chapter.referance}</h2\n>'
        for verse in chapter.verses:
            html += '\t\t<div class="verse">\n\t\t\t'
            html += f'<div class="referance">{verse.versenum}</div>\n\t\t\t'
            for word in verse.wordswpunc:
                if Verse.cleanWord(word) in material.onceUsedWords:
                    html += f"<dt><once>{word}</once></dt> "
                elif Verse.cleanWord(word) in material.twiceUsedWords:
                    html += f"<dt><twice>{word}</twice></dt> "
                else:
                    html += f"<dt>{word} </dt> "

            html += '\n\t\t</div>\n'
        html += '\t</div>\n'
    html += '</div>\n'

html = '''
{% extends "base.html" %}
{% block title %}
Material
{% endblock title %}
{% load static %}

{% block content %}''' + html + '{% endblock content %}'

with open('templates/Material/material.html', 'w') as fw:
    fw.write(html)