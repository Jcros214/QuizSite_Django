# TODO: Instead of custom HTML tags, convert to <ol>


# from typing import Tuple
import os
import json
from collections import Counter

mat = "matthew"


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
        self.used = 1
        self.used: int

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
        return f"<Word {self.clean()}>"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Word):
            return False

        return self.clean() == __value.clean()

    def __hash__(self) -> int:
        return hash(self.clean())

    def __html__(self, html_class: str | None = None, *args, **kwargs) -> str:
        occur = {1: 'once', 2: 'twice'}.get(self.used, '')

        html_class = f' class="{occur} {html_class if html_class is not None else ""}"'

        return f'{self.punc_before}<word{html_class}>{self.no_case_clean()}</word>{self.punc_after}'


class Verse(HTMLize):
    def __init__(
            self, verse: str, book_name: str, chapter_number: int, verse_number: int, is_quote: bool = False
    ) -> None:
        self.verse = verse
        self.words = [Word(word) for word in verse.split()]
        self.words: list[Word]
        self.book_name = book_name
        self.chapter_number = chapter_number
        self.verse_number = verse_number

        self.is_quote = is_quote

        self.index_at_unique_word = None
        self.index_at_unique_word: int | None

    @property
    def words_with_punctuation(self):
        return "".join([str(word) for word in self.words])

    @property
    def unique_start(self) -> list[Word] | None:
        return (
            self.words[:self.index_at_unique_word]
            if self.index_at_unique_word is not None
            else None
        )

    @property
    def after_unique_start(self):
        return (
            self.words[self.index_at_unique_word:]
            if self.index_at_unique_word is not None
            else None
        )

    # @staticmethod
    # def cleanWord(word: str) -> str:
    #     return ''.join([letter.lower() for letter in word if letter.isalpha()])

    def __repr__(self) -> str:
        return f"<Verse (quote) {self.book_name} {self.chapter_number}:{self.verse_number}>"

    def __str__(self) -> str:
        return " ".join(self.words_with_punctuation)

    def __html__(self, keywords_only: bool = False) -> str:
        if keywords_only:
            return f"<verse> <ref class=\"{'quote' if self.is_quote else 'normal'}\"> {self.verse_number} </ref> {' '.join([html(word) for word in self.words if word.used <= 2])} </verse> "

        if self.index_at_unique_word is None:
            return f"<verse> <ref class=\"{'quote' if self.is_quote else 'normal'}\"> {self.verse_number} </ref> {' '.join([html(word) for word in self.words])} </verse> "
        else:
            return f"<verse> <ref class=\"{'quote' if self.is_quote else 'normal'}\"> {self.verse_number} </ref> <span class='unique_start'>{' '.join([html(word, 'font-weight-bold') for word in self.unique_start])}/ </span> {' '.join([html(word) for word in self.after_unique_start])}</verse> "  # type: ignore


class Chapter(HTMLize):
    def __init__(self, verse_list) -> None:
        verse_list = list(verse_list)
        self.chapter_number = verse_list[0].get("chapter")
        self.book_name = verse_list[0].get("book_name")
        self.verse_list = [
            Verse(verse.get("text"), self.book_name, self.chapter_number, verse_num + 1, verse.get('is_quote'))
            for verse_num, verse in enumerate(verse_list)
        ]
        self.verse_list: list[Verse]

    def __repr__(self) -> str:
        return f"<Chapter {self.book_name} {self.chapter_number}>"

    def __str__(self) -> str:
        return "\n".join([str(_) for _ in self.verse_list])

    @property
    def reference(self):
        return f"{self.book_name} {self.chapter_number}"

    def __html__(self, keywords_only: bool = False) -> str:
        return f"<chapter> {self.book_name} {self.chapter_number} <br> {'<br>'.join([html(verse, keywords_only) for verse in self.verse_list])}</chapter>"


class Book(HTMLize):
    def __init__(self, verse_list) -> None:
        verse_list = list(verse_list)
        self.chapters = []
        self.chapters: list[Chapter]

        self.name = verse_list[0].get('book_name', '')

        # there must be a better way...
        verse_list.append({"chapter": None})

        verses_in_chapter = [verse_list.pop(0)]
        while verse_list:
            verse = verse_list.pop(0)

            if verse.get("chapter") == verses_in_chapter[0].get("chapter"):
                verses_in_chapter.append(verse)
            else:
                self.chapters.append(Chapter(verses_in_chapter))
                verses_in_chapter = [verse]

        # self.chapters.append(Chapter(versesInChapter, f"{versesInChapter[-1].get('book_name')} {versesInChapter[-1].get('chapter')}"))
        # versesInChapter = []

    def __html__(self, keywords_only: bool = False) -> str:
        return f"<book> {self.name.capitalize()} <br><br> {'<br><br>'.join([html(chapter, keywords_only) for chapter in self.chapters])}</book>"


class Material(HTMLize):
    def __init__(self, verse_list):
        self.books = []
        self.onceUsedWords = set()
        self.twiceUsedWords = set()
        self.books: list[Book]

        verses_in_book = [verse_list.pop(0)]
        while verse_list:
            verse = verse_list.pop(0)

            if verse.get("book") == verses_in_book[0].get("book"):
                verses_in_book.append(verse)
            else:
                self.books.append(Book(verses_in_book))
                verses_in_book = []

        self.books.append(Book(verses_in_book))

        for verse in self.verses:
            for verse_starting_phrase in [verse.words[:i] for i in range(1, len(verse.words))]:
                # See if any other verses start with this phrase
                for other_verse in self.verses:
                    if other_verse == verse:
                        continue

                    if other_verse.words[:len(verse_starting_phrase)] == verse_starting_phrase:
                        break
                else:
                    verse.index_at_unique_word = len(verse_starting_phrase)
                    break

        # self.flat_verses_strs = []
        # self.flat_verses_strs: list[str]
        #
        # for verse in self.verses:
        #     self.flat_verses_strs.append(' '.join([word.clean() for word in verse.words]))
        #
        # TODO: What was this for?
        # for verse in self.verses:
        #     for _ in verse.words:
        #         # Create flat string
        #         flat = [word.clean() for word in verse.words]
        #
        #         used = []
        #
        #         for word in flat:
        #             for flat_verse in self.flat_verses_strs:
        #                 if flat_verse.startswith(' '.join(used + [word])):
        #                     # continue somewhere..
        #                     ...
        #
        #     verse.index_at_unique_word = self.word_would_make_verse_unique(verse)

        self.get_words()

    @property
    def chapters(self) -> list[Chapter]:
        return [chapter for book in self.books for chapter in book.chapters]

    @property
    def verses(self) -> list[Verse]:
        return [verse for chapter in self.chapters for verse in chapter.verse_list]

    @property
    def words(self) -> list[Word]:
        return [word for verse in self.verses for word in verse.words]

    def get_words(self):
        counted_words = Counter(self.words)

        for word in self.words:
            word.used = counted_words[word]

    def word_would_make_verse_unique(self, verse: Verse) -> int:
        # def test_num(num):
        #     for other_verse in self.verses:
        #         for ind in range(1, num):
        #             if verse.words[:ind] != other_verse.words[:ind]:
        #                 if num != ind + 1:
        #                     return False
        #     return True

        for other_verse in self.verses:
            for ind in range(1, len(verse.words)):
                if verse.words[:ind] == other_verse.words[:ind]:
                    continue
                else:
                    return ind

        raise ValueError("No unique word found.")

    def __html__(self, keywords_only: bool = False) -> str:
        return "".join([html(book, keywords_only) for book in self.books])


if __name__ == "__main__":
    try:
        os.chdir("./templates/Material/texts")
    except FileNotFoundError:
        print(os.getcwd())
        exit(1)

    # Deserialize txt into Book, Chapter, and Verse objects

    with open(f"{mat}.json", "r") as fr:
        verses = json.load(fr)

    material = Material(verses)

    strHTML = html(material) + '<br><br><br><h2>Keywords by Verse</h2>' + html(material, True)

    # TODO: Create a table of keywords in alphabetical order

    with open(f"{mat}.html", "w") as fw:
        fw.write(strHTML)
