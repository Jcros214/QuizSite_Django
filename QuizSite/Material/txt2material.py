from typing import Tuple

mat = "matt5-7"


class HTMLize:
    def __html__(self) -> str:
        return f"<h1>{self}</h1>"
    
    def __hash__(self) -> int:
        hash(self.__str__())


def html(obj: HTMLize) -> str:
    try:
        return obj.__html__()
    except AttributeError:
        return ""


class Word(HTMLize):
    def __init__(self, word: str) -> None:
        self.word = word
        # Set to 1 or 2 as used
        self.used = None
        self.used: int | None

    def clean(self) -> str:
        return "".join([letter.lower() for letter in self.word if letter.isalpha()])

    def __str__(self) -> str:
        return self.word

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Word):
            return False

        return str(self) == str(__value)

    def __hash__(self) -> int:
        return super().__hash__()

    def __html__(self) -> str:
        html_class = f' class="{"once" if self.used == 1 else "twice"}"' if self.used else ""
        return f'<word{html_class}>{self.word}</word>'


class Verse(HTMLize):
    def __init__(
        self, verse: str, bookname: str, chapternum: int, versenum: int
    ) -> None:
        self.verse = verse
        # self.wordswpunc = verse.split(" ")
        self.words = [Word(word) for word in verse.split()]
        self.words: list[Word]
        self.bookname = bookname
        self.chapternum = chapternum
        self.versenum = versenum

        self.index_at_unique_word = None
        self.index_at_unique_word: int | None

    @property
    def wordswpunc(self):
        return "".join([str(word) for word in self.words])

    @property
    def unique_start(self) -> list[Word] | None:
        return (
            self.words[: self.index_at_unique_word]
            if self.index_at_unique_word != None
            else None
        )

    @property
    def after_unique_start(self):
        return (
            self.words[self.index_at_unique_word :]
            if self.index_at_unique_word != None
            else None
        )

    # @staticmethod
    # def cleanWord(word: str) -> str:
    #     return ''.join([letter.lower() for letter in word if letter.isalpha()])

    def __repr__(self) -> str:
        return f"<Verse {self.bookname} {self.chapternum}:{self.versenum}>"

    def __str__(self) -> str:
        return " ".join(self.wordswpunc)

    def __html__(self) -> str:
        if self.index_at_unique_word == None:
            return f"<verse>{' '.join([html(word) for word in self.words])}</verse>"
        else:
            return f"<verse>{' '.join([html(word) for word in self.unique_start])}<span class='unique-start'>{' '.join([html(word) for word in self.after_unique_start])}</span></verse>" # type: ignore


class Chapter(HTMLize):
    def __init__(self, verses) -> None:
        verses = list(verses)
        self.chapternum = verses[0].get("chapter")
        self.bookname = verses[0].get("book_name")
        self.verses = [
            Verse(verse.get("text"), self.bookname, self.chapternum, versenum + 1)
            for versenum, verse in enumerate(verses)
        ]
        self.verses: list[Verse]

    def __repr__(self) -> str:
        return f"<Chapter {self.bookname} {self.chapternum}>"

    def __str__(self) -> str:
        return "\n".join([str(_) for _ in self.verses])

    @property
    def referance(self):
        return f"{self.bookname} {self.chapternum}"

    def __html__(self) -> str:
        return f"<chapter>{''.join([html(verse) for verse in self.verses])}</chapter>"

class Book(HTMLize):
    def __init__(self, verses) -> None:
        verses = list(verses)
        self.chapters = []
        self.chapters: list[Chapter]

        # there must be a better way...
        verses.append({"chapter": None})

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

    def __html__(self) -> str:
        return f"<book>{''.join([html(chapter) for chapter in self.chapters])}</book>"

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

        for verse in self.verses:
            verse.index_at_unique_word = self.word_would_make_verse_unique(verse)

        self.getWords()

    @property
    def verses(self):
        return [
            verse
            for book in self.books
            for chapter in book.chapters
            for verse in chapter.verses
        ]

    def getWords(self):
        allwords = {}
        allwords: dict[Word, int]

        for book in self.books:
            for chapter in book.chapters:
                for verse in chapter.verses:
                    for word in verse.words:
                        try:
                            allwords[word] += 1
                        except KeyError:
                            allwords[word] = 1

        for word in allwords:
            # TODO: what's the right way to do this?

            val = allwords[word]

            if val == 1:
                if val in self.onceUsedWords or val in self.twiceUsedWords:
                    raise ValueError("Attempted duplicate once used.")
                self.onceUsedWords.add(word)
                word.used = 2
            elif val == 2:
                if val in self.twiceUsedWords or val in self.onceUsedWords:
                    raise ValueError("Attempted duplicate twice used.")
                self.twiceUsedWords.add(word)
                word.used = 2

    def word_would_make_verse_unique(self, verse: Verse) -> int:
        for other_verse in self.verses:
            for ind in range(len(verse.words)):
                if verse.words[:ind] == other_verse.words[:ind]:
                    continue
                else:
                    return ind

        raise ValueError("No unique word found.")


import os

os.chdir("./QuizSite/Material/templates/Material/texts")

# Deserialize txt into Book, Chapter, and Verse objects
import json

with open(f"{mat}.json", "r") as fr:
    verses = json.load(fr)

material = Material(verses)

# Create HTML from material

strHTML = ""

for book in material.books:
    strHTML += html(book)
    # strHTML += '<div class="book">\n'
    # for chapter in book.chapters:
    #     strHTML += '\t<div class="chapter">\n'
    #     strHTML += f"\t\t<h2>{chapter.referance}</h2\n>"
    #     for verse in chapter.verses:
    #         strHTML += '\t\t<div class="verse">\n\t\t\t'
    #         strHTML += f'<div class="referance">{verse.versenum}</div>\n\t\t\t'
    #         for word in verse.wordswpunc:
    #             if word in material.onceUsedWords:
    #                 strHTML += f"<h3><once>{word}</once></h3> "
    #             elif word in material.twiceUsedWords:
    #                 strHTML += f"<h3><twice>{word}</twice></h3> "
    #             else:
    #                 strHTML += f"<h3>{word} </h3> "

    #         strHTML += "\n\t\t</div>\n"
    #     strHTML += "\t</div>\n"
    # strHTML += "</div>\n"

# strHTML = '''
# {% extends "base.html" %}
# {% block title %}
# Material
# {% endblock title %}
# {% load static %}

# {% block content %}''' + strHTML + '{% endblock content %}'

with open("{mat}.html", "w") as fw:
    fw.write(strHTML)
