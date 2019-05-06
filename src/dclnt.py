import ast
import os
import collections

from nltk import pos_tag


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return [item for sub_item in _list for item in sub_item]


def is_verb(_word):
    if not _word:
        return False
    pos_info = pos_tag([_word])
    return pos_info[0][1] == 'VB'


def read_files(filenames, with_filenames, with_file_content):
    _trees = []
    for filename in filenames:
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


def get_trees(_path, with_filenames=False, with_file_content=False):
    filenames = []
    for dirname, dirs, files in os.walk(_path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                filenames.append(os.path.join(dirname, file))
                if len(filenames) == 100:
                    break
    print('total %s files' % len(filenames))
    _trees = read_files(filenames, with_filenames, with_file_content)
    print('trees generated')
    return _trees


def get_all_words(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    return [w for w in function_name.split('_') if is_verb(w)]


def split_snake_case_name_to_words(_name):
    return [n for n in _name.split('_') if n]


def filter_underscores(_list):
    return [f for f in _list if not (f.startswith('__') and f.endswith('__'))]


def get_names(_trees):
    node_names = flat([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees])
    return filter_underscores(node_names)


def get_all_words_in_path(_trees, _top_size=10):
    all_words = filter_underscores(flat([get_all_words(t) for t in _trees]))
    path_words = flat([split_snake_case_name_to_words(w) for w in all_words])
    print('all words extracted')
    return collections.Counter(path_words).most_common(_top_size)


def get_top_verbs_in_path(_trees, _top_size=10):
    functions = get_names(_trees)
    path_verbs = flat([get_verbs_from_function_name(function_name) for function_name in functions])
    print('verbs extracted')
    return collections.Counter(path_verbs).most_common(_top_size)


def get_top_functions_names_in_path(_trees, _top_size=10):
    function_names = get_names(_trees)
    print('functions extracted')
    return collections.Counter(function_names).most_common(_top_size)


words = []
verbs = []
names = []
projects = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
    'C:\\Users\\che\\IdeaProjects\\aerodisk-double-controller2'
]
for project in projects:
    print("-"*50)
    print("'%s' project statistics:" % project.title())
    path = os.path.join('.', project)
    trees = [t for t in get_trees(path) if t]
    verbs += get_top_verbs_in_path(trees)
    names += get_top_functions_names_in_path(trees)
    words += get_all_words_in_path(trees)

top_size = 200
print('\n Total %s verbs, %s unique:' % (len(verbs), len(set(verbs))))
for verb, occurrence in verbs:
    print("\t verb: '%s', occurrence: %d" % (verb, occurrence))
print('\n Total %s function names, %s unique:' % (len(names), len(set(names))))
for name, occurrence in names:
    print("\t name: '%s', occurrence: %d" % (name, occurrence))
print('\n Total %s words, %s unique:' % (len(words), len(set(words))))
for word, occurrence in words:
    print("\t word: '%s', occurrence: %d" % (word, occurrence))
