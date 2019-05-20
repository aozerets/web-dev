
import ast
import os
import collections

from nltk import pos_tag

MAX_FILES_COUNT = 100
TOP_SIZE = 200


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return [item for sub_item in _list for item in sub_item]


def is_verb(_word):
    if not _word:
        return False
    pos_info = pos_tag([_word])
    return pos_info[0][1] == 'VB'


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


def get_verbs_from_function_name(function_name):
    return [w for w in function_name.split('_') if is_verb(w)]


def split_snake_case_name_to_words(_name):
    return [n for n in _name.split('_') if n]


def filter_underscores(_list):
    return [f for f in _list if not (f.startswith('__') and f.endswith('__'))]


def get_names(_trees):
    node_names = flat([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees])
    return filter_underscores(node_names)


def get_all_words_from_ast_nodes(_trees):
    all_words = filter_underscores(flat([get_all_words(t) for t in _trees]))
    path_words = flat([split_snake_case_name_to_words(w) for w in all_words])
    print('all words extracted')
    return collections.Counter(path_words).most_common(TOP_SIZE)


def get_top_verbs_from_ast_nodes(_trees):
    functions = get_names(_trees)
    path_verbs = flat([get_verbs_from_function_name(function_name) for function_name in functions])
    print('verbs extracted')
    return collections.Counter(path_verbs).most_common(TOP_SIZE)


def get_top_functions_names_from_ast_nodes(_trees):
    function_names = get_names(_trees)
    print('functions extracted')
    return collections.Counter(function_names).most_common(TOP_SIZE)


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
    'C:\\Users\\che\\IdeaProjects\\aerodisk-double-controller2',
]
for project in projects:
    print("-"*50)
    print("'%s' project statistics:" % project.title())
    path = os.path.join('.', project)
    filenames = get_filenames(path)
    print('total %s files' % len(filenames))
    trees = get_trees(filenames)
    print('trees generated')
    verbs += get_top_verbs_from_ast_nodes(trees)
    names += get_top_functions_names_from_ast_nodes(trees)
    words += get_all_words_from_ast_nodes(trees)

print('\n Total %s verbs, %s unique:' % (len(verbs), len(set(verbs))))
for verb, occurrence in verbs:
    print("  %s %s %d" % (verb, "-"*(25 - len(verb)), occurrence))
print('\n Total %s function names, %s unique:' % (len(names), len(set(names))))
for name, occurrence in names:
    print("  %s %s %d" % (name, "-"*(25 - len(name)), occurrence))
print('\n Total %s words, %s unique:' % (len(words), len(set(words))))
for word, occurrence in words:
    print("  %s %s %d" % (word, "-"*(25 - len(word)), occurrence))
