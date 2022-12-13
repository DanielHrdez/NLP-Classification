#!/usr/bin/python

"""
Universidad de La Laguna
Grado en Ingeniería Informática
Inteligencia Artificial Avanzada - Proyecto
Daniel Hernández de León - alu0101331720
Clasificator
"""

import getopt
import sys
import json
import pandas
import math
import os
from alive_progress import alive_bar

from vocabulary.vocabulary import Vocabulary

def parse_arguments(argument_list: list[str]) -> dict:
    """
    Parse the arguments
        :param argv: list of arguments
        :return: dictionary with the arguments
    """
    test_filename = ''
    output_folder = ''
    options, arguments = getopt.getopt(argument_list, 'i:o:', ['ifile=', 'ofile='])
    if len(arguments) != 0 or len(options) != 2:
        print('clasificator.py -i <testfile> -o <outputfolder>')
        sys.exit(2)
    for option, argument in options:
        if option in ('-i'):
            test_filename = argument
        elif option in ('-o'):
            output_folder = argument
    return test_filename, output_folder

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

def search_language_model() -> list:
    """
    Search the language model files
        :return: list with the language model files
    """
    files = []
    with open('./out/language_model_positive.txt', 'r', encoding='utf-8') as file:
        files.append(file.readlines())
    with open('./out/language_model_negative.txt', 'r', encoding='utf-8') as file:
        files.append(file.readlines())
    if len(files) != 2:
        raise Exception('No language model files found')
    return files

def process_language_models(files: list) -> list:
    """
    Process the language model files
        :param files: list with the language model files
        :return: dictionary with the language model
    """
    positive_model = {}
    negative_model = {}
    positive_documents = int(files[0][0].split(' ')[1])
    negative_documents = int(files[1][0].split(' ')[1])
    total_documents = positive_documents + negative_documents
    positive_model['probability'] = math.log(positive_documents / total_documents)
    negative_model['probability'] = math.log(negative_documents / total_documents)
    positive_model['words'] = {}
    negative_model['words'] = {}
    positive_lines = files[0][2:]
    negative_lines = files[1][2:]
    for line in positive_lines:
        [[_, word], _, [_, prob]] = list(map(lambda x : x.split(':', 1), line.split(' ')))
        positive_model['words'][word] = float(prob)
    for line in negative_lines:
        [[_, word], _, [_, prob]] = list(map(lambda x : x.split(':', 1), line.split(' ')))
        negative_model['words'][word] = float(prob)
    return [positive_model, negative_model]

def process_documents(dataframe: pandas.DataFrame, language_models: list, output_folder: str) -> None:
    results = []
    parameters = search_parameters_json()
    yield 'Parameters found.'
    vocabulary = Vocabulary('')
    vocabulary.parameters = parameters
    size = len(dataframe)
    for i in range(size):
        text = dataframe.values[i, 0]
        try: current_result = {'text': text[:10]}
        except: continue
        for _ in vocabulary.tokenize(text.split(), use_set=False):
            pass
        count = 0
        for model in language_models:
            probability = model['probability']
            for word in vocabulary.tokens:
                if word in model['words']:
                    probability += model['words'][word]
                else:
                    probability += model['words']['<UNK>']
            current_result[f'prob_model_{count}'] = probability
            count += 1
        current_result['class'] = 'positive' if current_result['prob_model_0'] > current_result['prob_model_1'] else 'negative'
        results.append(current_result)
        yield 'NO PRINT'
    yield 'Documents processed.'
    export_files(results, output_folder)
    yield 'Files exported.'

def export_files(results: list, output_folder: str) -> None:
    """
    Export the files
        :param results: list with the results
        :param output_folder: folder to export the files
    """
    with open(output_folder + '/clasification_alu0101331720.txt', 'w', encoding='utf-8') as file:
        for result in results:
            file.write(
                f"{result['text']}, {round(result['prob_model_0'], 2)}, " +
                f"{round(result['prob_model_1'], 2)}, {result['class']}\n"
            )
    with open(output_folder + '/resumen_alu0101331720.txt', 'w', encoding='utf-8') as file:
        for result in results:
            file.write(result['class'] + '\n')
    
def main():
    """
    Main function
    """
    test_filename, output_folder = parse_arguments(sys.argv[1:])
    yield 'Arguments parsed.'
    language_models = search_language_model()
    yield 'Language models found.'
    models = process_language_models(language_models)
    yield 'Language models processed.'
    test_data = pandas.read_excel(test_filename, header=None)
    yield 'Test data loaded.'
    for message in process_documents(test_data, models, output_folder):
        yield message

if __name__ == '__main__':
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    RESET = '\033[0m'
    MAX = 6 + 33444
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