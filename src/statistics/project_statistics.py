#! /usr/bin/env python3

import argparse
import ast
import json
import os
import csv
import collections

from subprocess import PIPE, Popen
from nltk import pos_tag

MAX_FILES_COUNT = 100
TOP_SIZE = 200


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return [item for sub_item in _list for item in sub_item]


def is_verb(_word, word_type='VB'):
    if not _word:
        return False
    pos_info = pos_tag([_word])
    return pos_info[0][1] == word_type


def get_trees(_filenames, with_filenames=False, with_file_content=False):
    """Makes ast nodes from files content.
        filenames         -> List of paths to files in string,
        with_filenames    -> Boolean default False,
        with_file_content -> Boolean default False,
        return            -> List of ast nodes."""

    _trees = []
    for filename in _filenames:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None
        if with_filenames:
            if with_file_content:
                _trees.append((filename, main_file_content, tree))
            else:
                _trees.append((filename, tree))
        else:
            _trees.append(tree)
    return _trees


def get_filenames(_path):
    """Gathers the python file paths down from the given path into the string list."""

    _filenames = []
    for dirname, dirs, files in os.walk(_path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                _filenames.append(os.path.join(dirname, file))
                if len(_filenames) == MAX_FILES_COUNT:
                    return _filenames
    return _filenames


def get_all_words(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name, word_type):
    return [w for w in function_name.split('_') if is_verb(w, word_type)]


def split_snake_case_name_to_words(_name):
    return [n for n in _name.split('_') if n]


def filter_underscores(_list):
    return [f for f in _list if not (f.startswith('__') and f.endswith('__'))]


def get_names(trees):
    node_names = flat([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees])
    return filter_underscores(node_names)


def get_all_words_from_ast_nodes(trees):
    all_words = filter_underscores(flat([get_all_words(t) for t in trees]))
    path_words = flat([split_snake_case_name_to_words(w) for w in all_words])
    print('vars extracted')
    return collections.Counter(path_words).most_common(TOP_SIZE)


def get_top_verbs_from_ast_nodes(_trees, word_type):
    functions = get_names(_trees)
    path_verbs = flat([get_verbs_from_function_name(function_name, word_type) for function_name in functions])
    return collections.Counter(path_verbs).most_common(TOP_SIZE)


def get_top_functions_names_from_ast_nodes(_trees):
    function_names = get_names(_trees)
    print('functions extracted')
    return collections.Counter(function_names).most_common(TOP_SIZE)


class Project:

    def __init__(self, server, project, words, functions, report):
        self.server = server
        self.project = project
        self.word = words
        self.func = functions
        self.report = report
        self.directory = self.project.split("/")[-1].split(".")[0]
        self.project_path = os.path.join(os.getcwd(), self.directory)
        self.verbs = []
        self.names = []

    __commands = {
        "git": "git clone {}"
    }
    @staticmethod
    def _exec(cmd):
        """Executes the received command in shell,
           automatically decodes input to UTF-8
           and removes unnecessary symbols from the end of str.
           :cmd  -> string."""

        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        out = proc.communicate(timeout=60)[0]
        return out.decode(errors="replace").strip(" \n\t")

    def clone(self):
        if os.path.exists(self.project_path):
            self.directory = "_".join(self.project.split("/")[-2:])
        self._exec("mkdir %s" % self.directory)
        self._exec("cd %s" % self.directory)
        command = self.__commands[self.server].format(self.project)
        self._exec(command)

    __word_types = {
        "verb": 'VB',
        "noun": 'NN'
    }

    def _collect(self):
        filenames = get_filenames(self.project_path)
        trees = get_trees(filenames)
        self.verbs += get_top_verbs_from_ast_nodes(trees, self.__word_types[self.word])
        print('%ss extracted' % self.word)
        if self.func == "name":
            self.names += get_top_functions_names_from_ast_nodes(trees)
        else:
            self.names += get_all_words_from_ast_nodes(trees)

    def _to_console(self):
        print('\n Total %s %s, %s unique:' % (len(self.verbs), self.word, len(set(self.verbs))))
        for verb, occurrence in self.verbs:
            print("  %s %s %d" % (verb, "-"*(25 - len(verb)), occurrence))
        print('\n Total %s %s, %s unique:' % (len(self.names), self.func, len(set(self.names))))
        for name, occurrence in self.names:
            print("  %s %s %d" % (name, "-"*(25 - len(name)), occurrence))

    def _to_json(self):
        data = {}
        data[self.word] = {verb: occurrence for verb, occurrence in self.verbs}
        data[self.func] = {name: occurrence for name, occurrence in self.names}
        report_file_path = os.path.join(self.project_path, self.directory + "_json.txt")
        with open(report_file_path, 'w') as outfile:
            json.dump(data, outfile)
        print("The report successfully generated in the file %s" % report_file_path)

    def _to_csv(self):
        report_file_path = os.path.join(self.project_path, self.directory + "_csv.csv")
        with open(report_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quotechar='|')
            writer.writerow([self.word, "occurence"])
            [writer.writerow(v) for v in self.verbs]
            writer.writerow('')
            writer.writerow([self.func, "occurence"])
            [writer.writerow(n) for n in self.names]
        print("The report successfully generated in the file %s" % report_file_path)

    __report_types = {
        "cli": _to_console,
        "json": _to_json,
        "csv": _to_csv,
    }

    def export(self):
        self._collect()
        return self.__report_types[self.report](self)


def main(_args):
    data = vars(_args)
    del data['func']
    p = Project(**data)
    p.clone()
    p.export()


def init_parse():
    p = argparse.ArgumentParser()
    p.add_argument('-s', '--server', default='git', action='store', help='Enter a server')
    p.add_argument('-p', '--project', action='store', help='Enter an url to project')
    p.add_argument('-w', '--words', choices=['verb', 'noun'], help='Select verbs or nouns', required=True)
    p.add_argument('-f', '--functions', choices=['name', 'var'],
                   help='Select function names or thier local variables', required=True)
    p.add_argument('-r', '--report', choices=['cli', 'json', 'csv'], default='cli', help='Select report format')
    p.set_defaults(func=main)
    return p.parse_args()


if __name__ == '__main__':
    try:
        args = init_parse()
        args.func(args)
    except Exception as err:
        print(err)
