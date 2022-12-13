#!/usr/bin/python

"""
Universidad de La Laguna
Grado en Ingeniería Informática
Inteligencia Artificial Avanzada - Proyecto
Daniel Hernández de León - alu0101331720
Language Model
"""

from ..vocabulary.vocabulary import tokenize
import getopt
import json
import sys
import pandas
import os

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
    for file in os.listdir('./out'):
        if file == 'parameters.json':
            with open(file, 'r') as f:
                return json.load(f)

def search_vocabulary() -> dict:
    """
    Search the vocabulary file
        :return: dictionary with the vocabulary
    """
    for file in os.listdir('./out'):
        if file == 'vocabulary.txt':
            with open(file, 'r') as f:
                return f.read().split()

def token_probabilities(tokens: list[str]) -> dict:
    """
    Create the language model
        :param tokens: list of tokens
        :return: dictionary with the probabilities
    """
    result = {}
    for token in tokens:
        if token in result:
            result[token] += 1
        else:
            result[token] = 2
    result["<UNK>"] = 1
    for token in result:
        if result[token] < 2:
            result["<UNK>"] += 1
            del result[token]
    for token in result:
        result[token] /= len(tokens)
    return result

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
    tweets = pandas.read_excel(input_filename)
    vocabulary = search_vocabulary()
    positive = data_frame.iloc[0, 0].str.cat(sep=' ')
    negative = data_frame.iloc[1, 0].str.cat(sep=' ')
    positive_tokens = tokenize(positive.split(), parameters)
    negative_tokens = tokenize(negative.split(), parameters)
    positive_probabilities = token_probabilities(vocabulary, positive_tokens, data_frame.)
    negative_probabilities = token_probabilities(vocabulary, negative_tokens)
    write_file(output_filename, probabilities)

if __name__ == '__main__':
    main()
