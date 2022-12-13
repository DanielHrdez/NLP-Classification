#!/usr/bin/python

"""
Universidad de La Laguna
Grado en Ingeniería Informática
Inteligencia Artificial Avanzada - Proyecto
Daniel Hernández de León - alu0101331720
Vocabulary
"""

import sys
import getopt
import re
import pandas
import emoji
from symspellpy import SymSpell
import pkg_resources
from nltk.stem import PorterStemmer, WordNetLemmatizer
from stop_words import STOP_WORDS

def parse_arguments(argument_list: list[str]) -> dict:
    """
    Parse the arguments
        :param argv: list of arguments
        :return: dictionary with the arguments
    """
    input_filename = ''
    output_filename = ''
    options, arguments = getopt.getopt(argument_list, 'i:o:', ['ifile=', 'ofile='])
    if len(arguments) != 0 or len(options) != 2:
        print('vocabulary.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for option, argument in options:
        if option in ('-i'):
            input_filename = argument
        elif option in ('-o'):
            output_filename = argument
    return input_filename, output_filename

def ask_parameters() -> dict:
    """
    Ask the user for the parameters
        :return: dictionary with the parameters
    """
    parameters = {}
    parameters['lowercase'] = input('Lowercase? (y/n): ').lower()
    parameters['punctuation_marks'] = input('No punctuation marks? (y/n): ').lower()
    parameters['stopwords'] = input('No stopwords? (y/n): ').lower()
    parameters['emojis'] = input('No emojis? (y/n/w): ').lower()
    parameters['url_html_hashtags'] = input('No URLs and HTML hashtags? (y/n): ').lower()
    parameters['spell_check'] = input('Spell check? (y/n): ').lower()
    parameters['stemming'] = input('Stemming? (y/n): ').lower()
    if parameters['stemming'] != 'y':
        parameters['lemmatization'] = input('Lemmatization? (y/n): ').lower()
    return parameters

def lowercase(text: str, option: str) -> str:
    """
    Lowercase the text
        :param text: text to lowercase
        :param lowercase: lowercase? (y/n)
        :return: text lowercased
    """
    return text.lower() if option == 'y' else text

def puntuation_marks(text: str, option: str) -> str:
    """
    Remove punctuation marks
        :param text: text to remove punctuation marks
        :param punctuation_marks: remove punctuation marks? (y/n)
        :return: text without punctuation marks
    """
    return re.sub(r'[:.,;!?]', '', text) if option == 'y' else text

def stopwords(tokens: list[str], option: str) -> list[str]:
    """
    Remove stopwords
        :param tokens: list of tokens
        :param stopwords: remove stopwords? (y/n)
        :return: list of tokens without stopwords
    """
    if option == 'y':
        return [token for token in tokens if token not in STOP_WORDS]
    return tokens

def emojis(text: str, option: str) -> str:
    """
    Remove emojis
        :param text: text to remove emojis
        :param emojis: remove emojis? (y/n/w)
        :return: text without emojis
    """
    if option == 'y':
        return emoji.replace_emoji(text, '')
    if option == 'w':
        return emoji.demojize(text)
    return text

def url_html_hashtags(text: str, option: str) -> str:
    """
    Remove URLs and HTML hashtags
        :param text: text to remove URLs and HTML hashtags
        :param url_html_hashtags: remove URLs and HTML hashtags? (y/n)
        :return: text without URLs and HTML hashtags
    """
    if option == 'y':
        return re.sub(r'http\S+|#\S+|<.*?>', '', text)
    return text

def spell_check(text: str, option: str) -> str:
    """
    Spell check the text
        :param text: text to spell check
        :param spell_check: spell check? (y/n)
        :return: text without spelling errors
    """
    if option == 'y':
        sym_spell = SymSpell(max_dictionary_edit_distance=1, prefix_length=7)
        dictionary_path = pkg_resources.resource_filename("symspellpy",
                                                          "frequency_dictionary_en_82_765.txt")
        bigram_path = pkg_resources.resource_filename("symspellpy",
                                                      "frequency_bigramdictionary_en_243_342.txt")
        sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
        sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)
        return sym_spell.lookup_compound(text,
                                         max_edit_distance=1,
                                         ignore_non_words=True,
                                         split_by_space=True)
    return text

def stemming(tokens: list[str], option: str) -> list[str]:
    """
    Stemming the text
        :param tokens: list of tokens
        :param stemming: stemming? (y/n)
        :return: list of tokens with stemming
    """
    if option == 'y':
        stemmer = PorterStemmer()
        return [stemmer.stem(word) for word in tokens]
    return tokens

def lemmatization(tokens: list[str], option: str) -> list[str]:
    """
    Lemmatization the text
        :param tokens: list of tokens
        :param lemmatization: lemmatization? (y/n)
        :return: list of tokens with lemmatization
    """
    if option == 'y':
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word, pos='v') for word in tokens]
    return tokens

def tokenize(text: str, parameters: dict) -> list[str]:
    """
    Tokenize the text
        :param text: text to tokenize
        :param parameters: dictionary with the parameters
        :return: list of tokens
    """
    text = re.sub(r'\n', ' ', text)
    text = lowercase(text, parameters['lowercase'])
    text = puntuation_marks(text, parameters['punctuation_marks'])
    text = emojis(text, parameters['emojis'])
    text = url_html_hashtags(text, parameters['url_html_hashtags'])
    text = spell_check(text, parameters['spell_check'])
    tokens = text.split()
    tokens = stopwords(tokens, parameters['stopwords'])
    tokens = stemming(tokens, parameters['stemming'])
    return lemmatization(tokens, parameters['lemmatization'])

def write_file(filename: str, tokens: list[str]) -> None:
    """
    Write the tokens in a file
        :param filename: name of the file
        :param tokens: list of tokens
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f'Number_of_words: {len(tokens)}\n')
        for token in tokens:
            file.write(f'{token}\n')

def main() -> None:
    """
    Main function
    - Parse the arguments
    - Ask the user for the parameters
    - Read the input file
    - Tokenize the text
    - Write the tokens in a output file
    """
    input_filename, output_filename = parse_arguments(sys.argv[1:])
    parameters = ask_parameters()
    data_frame = pandas.read_excel(input_filename)
    list_all_text = data_frame.iloc[:, 0].str.cat(sep=' ')
    tokens = tokenize(list_all_text, parameters)
    write_file(output_filename, tokens)

if __name__ == '__main__':
    main()
