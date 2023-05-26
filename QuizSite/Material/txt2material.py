from typing import Tuple

mat = "matt5-7"


class HTMLize:
    def __html__(self, *args, **kwargs) -> str:
        return f"<h1>{self}</h1>"
    
    def __hash__(self) -> int:
        return hash(self.__str__())


def html(obj: HTMLize, *args, **kwargs) -> str:
    try:
        return obj.__html__(*args, **kwargs)
    except AttributeError:
        return ""


class Word(HTMLize):
    def __init__(self, word: str) -> None:
        self.word = word
        # Set to 1 or 2 as used
        self.used = None
        self.used: int | None

    @property
    def punc_before(self) -> str:
        return "".join([letter for letter in self.word[:1] if not letter.isalpha()])
    
    @property
    def punc_after(self) -> str:
        return "".join([letter for letter in self.word[-1:] if not letter.isalpha()])

    def clean(self) -> str:
        return "".join([letter.lower() for letter in self.word if letter.isalpha()])
    
    def no_case_clean(self) -> str:
        return "".join([letter for letter in self.word if letter.isalpha()])

    def __str__(self) -> str:
        return self.word
    
    def __repr__(self) -> str:
        return f"<Word {self.word}>"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Word):
            return False

        return str(self) == str(__value)

    def __hash__(self) -> int:
        return super().__hash__()

    def __html__(self, html_class : str|None = None, *args, **kwargs) -> str:
        if html_class != None:
            occur = "once" if self.used == 1 else "twice" if self.used == 2 else ""
            html_class = f' class="{occur} {html_class}"' if self.used else ""
        else:
            html_class = f' class="{"once" if self.used == 1 else "twice"}"' if self.used else ""
        return f'{self.punc_before}<word{html_class}>{self.no_case_clean()}</word>{self.punc_after}'


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
            self.words[:self.index_at_unique_word]
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
            return f"<verse>{' '.join([html(word) for word in self.words])}</verse> "
        else:
            return f"<verse><ref>{self.versenum} </ref> <span class='unique_start'>{' '.join([html(word, 'font-weight-bold') for word in self.unique_start])}/ </span> {' '.join([html(word) for word in self.after_unique_start])}</verse><br> " # type: ignore


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

        self.flat_verses_strs = []
        self.flat_verses_strs: list[str]

        for verse in self.verses:
            self.flat_verses_strs.append(' '.join([word.clean() for word in verse.words]))


        for verse in self.verses:
            for word in verse.words:
                # Create flat string
                flat = [word.clean() for word in verse.words]

                used = []

                for word in flat:
                    for flat_verse in self.flat_verses_strs:
                        if flat_verse.startswith(' '.join(used + [word])):
                            # continue somewhere..
                            ...



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
        def test_num(num):
            for other_verse in self.verses:
                for ind in range(1,num):
                    if verse.words[:ind] != other_verse.words[:ind]:
                        if num != ind + 1:
                            return False
            return True



        for other_verse in self.verses:
            for ind in range(1,len(verse.words)):
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

with open(f"{mat}.html", "w") as fw:
    fw.write(strHTML)
