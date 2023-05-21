#lib imports
import random
import nltk
from translate import Translator

from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# local imports
import settings
import random_choise


def synonymize(text : str) -> str:
    translator = Translator(from_lang=settings.LANGUAGE, to_lang="en")
    text = translator.translate(text)

    nltk.download('wordnet')
    nltk.download('punkt')

    tokens = word_tokenize(text)

    new_text_words = []

    NEW_INVITATION_TEXT = ''

    for token in tokens:
        syn = wordnet.synsets(token)
        try:
            new_word = syn[random.randint(0, len(syn) - 1)].lemmas()[0].name()
            new_text_words.append(new_word)
        except:
            new_text_words.append(token)

    for words in new_text_words:
        NEW_INVITATION_TEXT += f"{words} "

    translator = Translator(from_lang="en", to_lang=settings.LANGUAGE)
    NEW_INVITATION_TEXT = translator.translate(NEW_INVITATION_TEXT)
    return NEW_INVITATION_TEXT