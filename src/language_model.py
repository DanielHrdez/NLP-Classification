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
    auxiliar = {i: 1 for i in vocabulary}
    unknown = '<UNK>'
    auxiliar[unknown] = 1
    for token in tokens:
        if token in auxiliar:
            auxiliar[token] += 1
        else:
            auxiliar[unknown] += 1
    result = auxiliar.copy()
    for token in auxiliar:
        if auxiliar[token] < 2 and token != unknown:
            result[unknown] += 1
            del result[token]
    for token in result:
        probability = result[token] / (len(tokens) + len(vocabulary))
        result[token] = {
            'frec': result[token],
            'log_prob': round(math.log(probability), 2),
        }
    return result

def write_model(filename: str, number_documents: int, number_words: int, tokens: dict) -> None:
    """
    Write the file
        :param filename: name of the file
        :param data: data to write
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f'Number of documents of the corpus: {number_documents}\n')
        file.write(f'Number of words of the corpus: {number_words}\n')
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
    # input_filename, output_filename = parse_arguments(sys.argv[1:])
    input_filename, output_filename = './data/COV_train.xlsx', './out/language_model'
    parameters = search_parameters_json()
    vocabulary_file = search_vocabulary()[2:]
    vocabulary = Vocabulary('')
    vocabulary.parameters = parameters
    train_file = pandas.read_excel(input_filename)
    positive_tweets = train_file[train_file.Negative == 'Positive'].iloc[:, 0]
    negative_tweets = train_file[train_file.Negative == 'Negative'].iloc[:, 0]
    positive = positive_tweets.str.cat(sep=' ').split()
    negative = negative_tweets.str.cat(sep=' ').split()
    positive_tokens = vocabulary.tokenize(positive, return_set=False)
    negative_tokens = vocabulary.tokenize(negative, return_set=False)
    positive_probabilities = token_probabilities(vocabulary_file, positive_tokens)
    negative_probabilities = token_probabilities(vocabulary_file, negative_tokens)
    write_model(
        output_filename + '_positive.txt',
        len(positive_tweets),
        len(positive_probabilities),
        positive_probabilities,
    )
    write_model(
        output_filename + '_negative.txt',
        len(negative_tweets),
        len(negative_probabilities),
        negative_probabilities,
    )

if __name__ == '__main__':
    main()
