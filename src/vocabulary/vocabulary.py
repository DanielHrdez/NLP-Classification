#!/usr/bin/python

"""
Universidad de La Laguna
Grado en Ingeniería Informática
Inteligencia Artificial Avanzada - Proyecto
Daniel Hernández de León - alu0101331720
Vocabulary
"""

import sys
import os
import getopt
import re
import json
import pandas
import emoji
from symspellpy import SymSpell
import pkg_resources
from nltk.stem import PorterStemmer, WordNetLemmatizer
from .constants import PUNTUATION_MARKS, STOP_WORDS
from alive_progress import alive_bar

class Vocabulary:
    """
    class Vocabulary:
    """
    parameters = {}
    output_filename = ''
    tokens = []

    def __init__(self, output_filename: str, ask_for_parameters: bool = False):
        """
        Constructor
            :param output_filename: output file
        """
        self.output_filename = output_filename
        if ask_for_parameters:
            self.parameters = self.ask_parameters()

    @staticmethod
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
        else:
            parameters['lemmatization'] = 'n'
        return parameters

    @staticmethod
    def lowercase(tokens: set[str], option: str, return_set: bool = True) -> set[str]:
        """
        Lowercase the tokens
            :param tokens: set to lowercase
            :param lowercase: lowercase? (y/n)
            :return: set lowercased
        """
        if return_set:
            return {token.lower() for token in tokens if token} if option == 'y' else tokens
        return [token.lower() for token in tokens if token] if option == 'y' else tokens

    @staticmethod
    def puntuation_marks(tokens: set[str], option: str, return_set: bool = True) -> set[str]:
        """
        Remove punctuation marks
            :param tokens: set to remove punctuation marks
            :param punctuation_marks: remove punctuation marks? (y/n)
            :return: set without punctuation marks
        """
        if option == 'y':
            if return_set:
                return {re.sub(rf"[{'|'.join(PUNTUATION_MARKS)}]", '', token) for token in tokens if token}
            return [re.sub(rf"[{'|'.join(PUNTUATION_MARKS)}]", '', token) for token in tokens if token]
        return tokens

    @staticmethod
    def stopwords(tokens: set[str], option: str, return_set: bool = True) -> set[str]:
        """
        Remove stopwords
            :param tokens: set of tokens
            :param stopwords: remove stopwords? (y/n)
            :return: set of tokens without stopwords
        """
        if return_set:
            return {token for token in tokens if token not in STOP_WORDS} if option == 'y' else tokens
        return [token for token in tokens if token not in STOP_WORDS] if option == 'y' else tokens

    @staticmethod
    def emojis(tokens: set[str], option: str, return_set: bool = True) -> set[str]:
        """
        Remove emojis
            :param tokens: set to remove emojis
            :param emojis: remove emojis? (y/n/w)
            :return: set without emojis
        """
        if option == 'y':
            if return_set:
                return {emoji.replace_emoji(token, '') for token in tokens if token}
            return [emoji.replace_emoji(token, '') for token in tokens if token]
        if option == 'w':
            if return_set:
                return {emoji.demojize(token) for token in tokens if token}
            return [emoji.demojize(token) for token in tokens if token]
        return tokens

    @staticmethod
    def url_html_hashtags(tokens: set[str], option: str, return_set: bool = True) -> set[str]:
        """
        Remove URLs and HTML hashtags
            :param tokens: set to remove URLs and HTML hashtags
            :param url_html_hashtags: remove URLs and HTML hashtags? (y/n)
            :return: set without URLs and HTML hashtags
        """
        if option == 'y':
            if return_set:
                return {re.sub(r'http.*|#.*|<.*>|@.*', '', token) for token in tokens if token}
            return [re.sub(r'http.*|#.*|<.*>|@.*', '', token) for token in tokens if token]
        return tokens

    @staticmethod
    def spell_check(tokens: set[str], option: str, return_set: bool = True) -> set[str]:
        """
        Spell check the tokens
            :param tokens: set to spell check
            :param spell_check: spell check? (y/n)
            :return: set without spelling errors
        """
        if option == 'y':
            sym_spell = SymSpell(max_dictionary_edit_distance=1, prefix_length=7)
            dictionary_path = pkg_resources.resource_filename(
                "symspellpy",
                "frequency_dictionary_en_82_765.txt")
            bigram_path = pkg_resources.resource_filename(
                "symspellpy",
                "frequency_bigramdictionary_en_243_342.txt")
            sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
            sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)
            result = set()
            if not return_set:
                result = []
            for token in tokens:
                if token:
                    suggestions = sym_spell.lookup_compound(token, max_edit_distance=1)
                    if suggestions:
                        term = suggestions[0].term
                        splitted = term.split(' ')
                        if return_set:
                            if len(splitted) > 1:
                                result.add(splitted[0])
                                result.add(splitted[1])
                            else:
                                result.add(term)
                        else:
                            if len(splitted) > 1:
                                result.append(splitted[0])
                                result.append(splitted[1])
                            else:
                                result.append(term)
            return result
        return tokens

    @staticmethod
    def stemming(tokens: set[str], option: str, return_set: bool = True) -> set[str]:
        """
        Stemming the tokens
            :param tokens: set of tokens
            :param stemming: stemming? (y/n)
            :return: set of tokens with stemming
        """
        if option == 'y':
            stemmer = PorterStemmer()
            if return_set:
                return {stemmer.stem(word) for word in tokens if word}
            return [stemmer.stem(word) for word in tokens if word]
        return tokens

    @staticmethod
    def lemmatization(tokens: set[str], option: str, return_set: bool = True) -> list[str]:
        """
        Lemmatization the tokens
            :param tokens: set of tokens
            :param lemmatization: lemmatization? (y/n)
            :return: list of tokens with lemmatization in alphabetic order
        """
        if option == 'y':
            lemmatizer = WordNetLemmatizer()
            if return_set:
                return sorted({lemmatizer.lemmatize(word, pos='v') for word in tokens if word})
            return sorted([lemmatizer.lemmatize(word, pos='v') for word in tokens if word])
        return sorted(tokens)

    @staticmethod
    def filter_numbers(tokens: set(), return_set: bool = True) -> set():
        """
        Filter the numbers
            :param tokens: set of tokens
            :return: set without numbers
        """
        if return_set:
            return {token for token in tokens if re.match(r'.*\d.*', token) is None}
        return [token for token in tokens if re.match(r'.*\d.*', token) is None]

    @staticmethod
    def filter_long_words(tokens: set[str], return_set: bool = True) -> set[str]:
        """
        Filter the long words
            :param tokens: set of tokens
            :return: set without long words
        """
        if return_set:
            return {token for token in tokens if len(token) < 20}
        return [token for token in tokens if len(token) < 20]

    def tokenize(self, tokens: list[str], return_set: bool = True) -> list[str]:
        """
        Tokenize the text
            :param tokens: text to tokenize
            :return: list of tokens in alphabetic order
        """
        tokens = self.filter_numbers(tokens, return_set)
        yield 'Numbers filtered.'
        tokens = self.filter_long_words(tokens, return_set)
        yield 'Long words filtered.'
        tokens = self.lowercase(tokens, self.parameters['lowercase'], return_set)
        yield 'Lowercase done.'
        tokens = self.puntuation_marks(tokens, self.parameters['punctuation_marks'], return_set)
        yield 'Puntuation marks done.'
        tokens = self.stopwords(tokens, self.parameters['stopwords'], return_set)
        yield 'Stopwords done.'
        tokens = self.emojis(tokens, self.parameters['emojis'], return_set)
        yield 'Emojis done.'
        tokens = self.url_html_hashtags(tokens, self.parameters['url_html_hashtags'], return_set)
        yield 'URL-HTML-# done.'
        tokens = self.spell_check(tokens, self.parameters['spell_check'], return_set)
        yield 'Spell check done.'
        tokens = self.stemming(tokens, self.parameters['stemming'], return_set)
        yield 'Stemming done.'
        self.tokens = self.lemmatization(tokens, self.parameters['lemmatization'], return_set)
        yield 'Lemmatization done.'

    def write_file(self, filename: str, tokens: list[str]) -> None:
        """
        Write the tokens in a file
            :param filename: name of the file
            :param tokens: list of tokens
        """
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f'Number_of_words: {len(tokens)}\n')
            for token in tokens:
                file.write(f'{token}\n')

    
    def write_json_parameters(self, filename: str) -> None:
        """
        Write the parameters in a json file
        """
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.parameters, file, indent=4)

    
    def write(self) -> None:
        """
        Write the tokens in a file
        """
        self.write_file(self.output_filename, self.tokens)
        path = os.path.dirname(self.output_filename)
        self.write_json_parameters(path + '/parameters.json')

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
    vocabulary = Vocabulary(output_filename, True)
    data_frame = pandas.read_excel(input_filename)
    all_text = data_frame.iloc[:, 0].str.cat(sep=' ')
    vocabulary.tokenize(set(all_text.split()))
    vocabulary.write()

if __name__ == '__main__':
    main()
