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
from alive_progress import alive_bar
if __name__ == '__main__':
    from constants import PUNCTUATION_MARKS, STOP_WORDS
else:
    from .constants import PUNCTUATION_MARKS, STOP_WORDS

class Vocabulary:
    """
    class Vocabulary:
    """
    parameters = {}
    output_filename = ''
    tokens = []
    spell_checker = SymSpell(max_dictionary_edit_distance=1, prefix_length=7)
    spell_check_loaded = False
    use_set = False

    def __init__(self, output_filename: str, ask_for_parameters: bool = False):
        """
        Constructor
            :param output_filename: output file
        """
        self.output_filename = output_filename
        if ask_for_parameters:
            self.ask_parameters()

    def ask_parameters(self) -> dict:
        """
        Ask the user for the parameters
            :return: dictionary with the parameters
        """
        self.parameters = {}
        self.parameters['numbers'] = input('No numbers? (y/n): ').lower()
        self.parameters['long_words'] = input('No long words? (y/n): ').lower()
        self.parameters['lowercase'] = input('Lowercase? (y/n): ').lower()
        self.parameters['punctuation_marks'] = input('No punctuation marks? (y/n): ').lower()
        self.parameters['stopwords'] = input('No stopwords? (y/n): ').lower()
        self.parameters['emojis'] = input('No emojis? (y/n/w): ').lower()
        self.parameters['url_html_hashtags'] = input('No URLs and HTML hashtags? (y/n): ').lower()
        self.parameters['spell_check'] = input('Spell check? (y/n): ').lower()
        self.parameters['stemming'] = input('Stemming? (y/n): ').lower()
        if self.parameters['stemming'] != 'y':
            self.parameters['lemmatization'] = input('Lemmatization? (y/n): ').lower()
        else:
            self.parameters['lemmatization'] = 'n'

    def lowercase(self) -> set[str]:
        """
        Lowercase the tokens
            :param tokens: set to lowercase
            :param lowercase: lowercase? (y/n)
            :return: set lowercased
        """
        option = self.parameters['lowercase']
        if self.use_set:
            self.tokens = {token.lower() for token in self.tokens if token} if option == 'y' else self.tokens
        self.tokens = [token.lower() for token in self.tokens if token] if option == 'y' else self.tokens

    def punctuation_marks(self) -> set[str]:
        """
        Remove punctuation marks
            :param tokens: set to remove punctuation marks
            :param punctuation_marks: remove punctuation marks? (y/n)
            :return: set without punctuation marks
        """
        option = self.parameters['punctuation_marks']
        if option == 'y':
            if self.use_set:
                self.tokens = {re.sub(rf"[{'|'.join(PUNCTUATION_MARKS)}]", '', token) for token in self.tokens if token}
            self.tokens = [re.sub(rf"[{'|'.join(PUNCTUATION_MARKS)}]", '', token) for token in self.tokens if token]

    def stopwords(self) -> set[str]:
        """
        Remove stopwords
            :param tokens: set of tokens
            :param stopwords: remove stopwords? (y/n)
            :return: set of tokens without stopwords
        """
        option = self.parameters['stopwords']
        if self.use_set:
            self.tokens = {token for token in self.tokens if token not in STOP_WORDS} if option == 'y' else self.tokens
        self.tokens = [token for token in self.tokens if token not in STOP_WORDS] if option == 'y' else self.tokens

    def emojis(self) -> set[str]:
        """
        Remove emojis
            :param tokens: set to remove emojis
            :param emojis: remove emojis? (y/n/w)
            :return: set without emojis
        """
        option = self.parameters['emojis']
        if option == 'y':
            if self.use_set:
                self.tokens = {emoji.replace_emoji(token, '') for token in self.tokens if token}
            self.tokens = [emoji.replace_emoji(token, '') for token in self.tokens if token]
        if option == 'w':
            if self.use_set:
                self.tokens = {emoji.demojize(token) for token in self.tokens if token}
            self.tokens = [emoji.demojize(token) for token in self.tokens if token]

    def url_html_hashtags(self) -> set[str]:
        """
        Remove URLs and HTML hashtags
            :param tokens: set to remove URLs and HTML hashtags
            :param url_html_hashtags: remove URLs and HTML hashtags? (y/n)
            :return: set without URLs and HTML hashtags
        """
        option = self.parameters['url_html_hashtags']
        if option == 'y':
            if self.use_set:
                self.tokens = {re.sub(r'http.*|#.*|<.*>|@.*', '', token) for token in self.tokens if token}
            self.tokens = [re.sub(r'http.*|#.*|<.*>|@.*', '', token) for token in self.tokens if token]

    def load_spell_check(self):
        """
        Load the spell checker
        """
        self.spell_checker = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        self.spell_checker.load_dictionary(pkg_resources.resource_filename('symspellpy', 'frequency_dictionary_en_82_765.txt'), term_index=0, count_index=1)
        self.spell_checker.load_bigram_dictionary(pkg_resources.resource_filename('symspellpy', 'frequency_bigramdictionary_en_243_342.txt'), term_index=0, count_index=1)


    def spell_check(self) -> set[str]:
        """
        Spell check the tokens
            :param tokens: set to spell check
            :param spell_check: spell check? (y/n)
            :return: set without spelling errors
        """
        option = self.parameters['spell_check']
        if option == 'y':
            if not self.spell_check_loaded:
                self.load_spell_check()
                self.spell_check_loaded = True
            result = set()
            if not self.use_set:
                result = []
            for token in self.tokens:
                if token:
                    suggestions = self.spell_checker.lookup_compound(token, max_edit_distance=1)
                    if suggestions:
                        term = suggestions[0].term
                        splitted = term.split(' ')
                        if self.use_set:
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
            self.tokens = result

    def stemming(self) -> set[str]:
        """
        Stemming the tokens
            :param tokens: set of tokens
            :param stemming: stemming? (y/n)
            :return: set of tokens with stemming
        """
        option = self.parameters['stemming']
        if option == 'y':
            stemmer = PorterStemmer()
            if self.use_set:
                self.tokens = {stemmer.stem(word) for word in self.tokens if word}
            self.tokens = [stemmer.stem(word) for word in self.tokens if word]

    def lemmatization(self) -> list[str]:
        """
        Lemmatization the tokens
            :param tokens: set of tokens
            :param lemmatization: lemmatization? (y/n)
            :return: list of tokens with lemmatization in alphabetic order
        """
        option = self.parameters['lemmatization']
        if option == 'y':
            lemmatizer = WordNetLemmatizer()
            if self.use_set:
                self.tokens = sorted({lemmatizer.lemmatize(word, pos='v') for word in self.tokens if word})
            self.tokens = sorted([lemmatizer.lemmatize(word, pos='v') for word in self.tokens if word])
        self.tokens = sorted(self.tokens)

    def numbers(self):
        """
        Filter the numbers
            :param tokens: set of tokens
            :return: set without numbers
        """
        if self.parameters['numbers'] == 'y':
            if self.use_set:
                self.tokens = {token for token in self.tokens if re.match(r'.*\d.*', token) is None}
            self.tokens = [token for token in self.tokens if re.match(r'.*\d.*', token) is None]

    def long_words(self) -> set[str]:
        """
        Filter the long words
            :param tokens: set of tokens
            :return: set without long words
        """
        if self.parameters['long_words'] == 'y':
            if self.use_set:
                self.tokens = {token for token in self.tokens if len(token) < 20}
            self.tokens = [token for token in self.tokens if len(token) < 20]

    def tokenize(self, tokens: list[str], use_set: bool = True) -> list[str]:
        """
        Tokenize the text
            :param tokens: text to tokenize
            :return: list of tokens in alphabetic order
        """
        self.tokens = tokens
        self.use_set = use_set
        self.numbers()
        yield 'Numbers filtered.'
        self.long_words()
        yield 'Long words filtered.'
        self.lowercase()
        yield 'Lowercase done.'
        self.punctuation_marks()
        yield 'Punctuation marks done.'
        self.stopwords()
        yield 'Stopwords done.'
        self.emojis()
        yield 'Emojis done.'
        self.url_html_hashtags()
        yield 'URL-HTML-# done.'
        self.spell_check()
        yield 'Spell check done.'
        self.stemming()
        yield 'Stemming done.'
        self.lemmatization()
        yield 'Lemmatization done.'

    def write_file(self, filename: str) -> None:
        """
        Write the tokens in a file
            :param filename: name of the file
            :param tokens: list of tokens
        """
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f'Number_of_words: {len(self.tokens)}\n')
            for token in self.tokens:
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
        self.write_file(self.output_filename)
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
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    RESET = '\033[0m'
    MAX = 10
    input_filename, output_filename = parse_arguments(sys.argv[1:])
    vocabulary = Vocabulary(output_filename, True)
    data_frame = pandas.read_excel(input_filename, header=None)
    all_text = data_frame.iloc[:, 0].str.cat(sep=' ')
    print(YELLOW, end='')
    with alive_bar(MAX) as bar:
        count = 1
        for message in vocabulary.tokenize(set(all_text.split())):
            if message == 'NO PRINT': pass
            elif (count < MAX): print(RESET + message + YELLOW)
            else: print(RESET + message + GREEN)
            bar()
            count += 1
    print(RESET)
    vocabulary.write()

if __name__ == '__main__':
    main()
