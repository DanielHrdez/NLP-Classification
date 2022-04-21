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

def parse_args(argv: list[str]) -> dict:
    """
    Parse the arguments
        :param argv: list of arguments
        :return: dictionary with the arguments
    """
    input_filename = ''
    output_filename = ''
    opts, args = getopt.getopt(argv, 'i:o:', ['ifile=', 'ofile='])
    if len(args) != 0 or len(opts) != 2:
        print('vocabulary.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-i'):
            input_filename = arg
        elif opt in ('-o'):
            output_filename = arg
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

def tokenize(text: str, parameters: dict) -> list[str]:
    """
    Tokenize the text
        :param text: text to tokenize
        :param parameters: dictionary with the parameters
        :return: list of tokens
    """
    text = re.sub(r'\n', ' ', text)
    if parameters['lowercase'] == 'y':
        text = text.lower()
    if parameters['punctuation_marks'] == 'y':
        text = re.sub(r'[:.,;!?]', '', text)
    if parameters['stopwords'] == 'y':
        text = re.sub(rf'\b({"|".join(STOP_WORDS)})\b', '', text)
        text = re.sub(r'\s+', ' ', text)
    if parameters['emojis'] == 'y':
        text = emoji.replace_emoji(text, '')
    elif parameters['emojis'] == 'w':
        text = emoji.demojize(text)
    if parameters['url_html_hashtags'] == 'y':
        text = re.sub(r'http\S+|#\S+|<.*?>', '', text)
    if parameters['spell_check'] == 'y':
        sym_spell = SymSpell(max_dictionary_edit_distance=1, prefix_length=7)
        dictionary_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_dictionary_en_82_765.txt"
        )
        bigram_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_bigramdictionary_en_243_342.txt"
        )
        sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
        sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)
        text = sym_spell.lookup_compound(
            text,
            max_edit_distance=1,
            ignore_non_words=True,
            split_by_space=True,
        )
    tokens = text.split()
    if parameters['stemming'] == 'y':
        porter = PorterStemmer()
        tokens = [porter.stem(word) for word in tokens]
    elif parameters['lemmatization'] == 'y':
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word, pos="v") for word in tokens]
    return tokens

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

def main():
    """Main function"""
    input_filename, output_filename = parse_args(sys.argv[1:])
    parameters = ask_parameters()
    data_frame = pandas.read_excel(input_filename)
    list_all_text = data_frame.iloc[:, 0].str.cat(sep=' ')
    tokens = tokenize(list_all_text, parameters)
    write_file(output_filename, tokens)

if __name__ == '__main__':
    main()
