#!/usr/bin/python

"""
Universidad de La Laguna
Grado en Ingeniería Informática
Inteligencia Artificial Avanzada - Proyecto
Daniel Hernández de León - alu0101331720
Language Model
"""

import getopt
import json
import sys
import os
import math
import pandas
from vocabulary import Vocabulary
from alive_progress import alive_bar

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
        print('language_model.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for option, argument in options:
        if option in ('-i'):
            input_filename = argument
        elif option in ('-o'):
            output_filename = argument
    return input_filename, output_filename

def search_parameters_json() -> dict:
    """
    Search the parameters file
        :return: dictionary with the parameters
    """
    for filename in os.listdir('./out'):
        if filename == 'parameters.json':
            with open('./out/' + filename, 'r', encoding='utf-8') as file:
                return json.load(file)
    raise Exception('No parameters file found')

def search_vocabulary() -> list[str]:
    """
    Search the vocabulary file
        :return: dictionary with the vocabulary
    """
    for filename in os.listdir('./out'):
        if filename == 'vocabulary.txt':
            with open('./out/' + filename, 'r', encoding='utf-8') as file:
                return file.read().split()
    raise Exception('No vocabulary file found')

def token_probabilities(vocabulary: list[str], tokens: list[str]) -> dict:
    """
    Create the language model
        :param vocabulary: list with the vocabulary
        :param tokens: list of tokens
        :return: dictionary with the probabilities
    """
    auxiliar = {i: 0 for i in vocabulary}
    unknown = '<UNK>'
    auxiliar[unknown] = 0
    for token in tokens:
        if token in auxiliar:
            auxiliar[token] += 1
        else:
            auxiliar[unknown] += 1
    yield 'Words counted.'
    result = auxiliar.copy()
    for token in auxiliar:
        if auxiliar[token] < 2 and token != unknown:
            result[unknown] += 1
            del result[token]
    yield 'Filtered one-aparition words.'
    for token in result:
        probability = (result[token] + 1) / (len(tokens) + len(vocabulary))
        result[token] = {
            'frec': result[token],
            'log_prob': math.log(probability),
        }
    yield 'Words probabilities done.'
    yield result

def write_model(filename: str, number_documents: int, number_words: int, tokens: dict) -> None:
    """
    Write the file
        :param filename: name of the file
        :param data: data to write
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f'Number_of_documents: {number_documents}\n')
        file.write(f'Number_of_words: {number_words}\n')
        for token in tokens:
            prob = tokens[token]
            file.write(f'Word:{token} Frec:{prob["frec"]} LogProb:{prob["log_prob"]}\n')

def main() -> None:
    """
    Main function
        - Parse the arguments
        - Search the parameters file
        - Read the corpus
        - Tokenize the corpus
        - Create the language model
        - Save the language model
    """
    input_filename, output_filename = parse_arguments(sys.argv[1:])
    parameters = search_parameters_json()
    yield 'Parameters file found'
    vocabulary_file = search_vocabulary()[2:]
    yield 'Vocabulary file found'
    vocabulary = Vocabulary('')
    vocabulary.parameters = parameters
    column_names = ['text', 'class_doc']
    train_file = pandas.read_excel(input_filename, header=None, names=column_names)
    positive_tweets = train_file[train_file.class_doc == 'Positive'].iloc[:, 0]
    negative_tweets = train_file[train_file.class_doc == 'Negative'].iloc[:, 0]
    positive = positive_tweets.str.cat(sep=' ').split()
    negative = negative_tweets.str.cat(sep=' ').split()
    for message in vocabulary.tokenize(positive, use_set=False):
        yield message
    positive_tokens = vocabulary.tokens
    for message in vocabulary.tokenize(negative, use_set=False):
        yield message
    negative_tokens = vocabulary.tokens
    count = 0
    iterator_pos = token_probabilities(vocabulary_file, positive_tokens)
    iterator_neg = token_probabilities(vocabulary_file, negative_tokens)
    for message in iterator_pos:
        if (count > 0): break
        count += 1
        yield message
    yield next(iterator_pos)
    positive_probabilities = next(iterator_pos)
    count = 0
    for message in iterator_neg:
        if (count > 0): break
        count += 1
        yield message
    yield next(iterator_neg)
    negative_probabilities = next(iterator_neg)
    write_model(
        output_filename + '_positive.txt',
        len(positive_tweets),
        len(positive_probabilities),
        positive_probabilities,
    )
    yield f'File {output_filename}_positive.txt written.'
    write_model(
        output_filename + '_negative.txt',
        len(negative_tweets),
        len(negative_probabilities),
        negative_probabilities,
    )
    yield f'File {output_filename}_negative.txt written.'

if __name__ == '__main__':
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    RESET = '\033[0m'
    MAX = 28
    print(YELLOW, end='')
    with alive_bar(MAX) as bar:
        count = 1
        for message in main():
            if message == 'NO PRINT': pass
            elif (count < MAX): print(RESET + message + YELLOW)
            else: print(RESET + message + GREEN)
            bar()
            count += 1
    print(RESET)
