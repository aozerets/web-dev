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
    trees = []
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
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
    return trees


Path = ''


def get_trees(_path, with_filenames=False, with_file_content=False):
    filenames = []
    _path = Path
    for dirname, dirs, files in os.walk(_path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                filenames.append(os.path.join(dirname, file))
                if len(filenames) == 100:
                    break
    print(f'total {len(filenames)} files')
    trees = read_files(filenames, with_filenames, with_file_content)
    print('trees generated')
    return trees


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    return [w for w in function_name.split('_') if is_verb(w)]


def split_snake_case_name_to_words(name):
    return [n for n in name.split('_') if n]


def filter_underscores(_list):
    return [f for f in _list if not (f.startswith('__') and f.endswith('__'))]


def get_all_words_in_path(_path):
    trees = [t for t in get_trees(_path) if t]
    function_names = filter_underscores(flat([get_all_names(t) for t in trees]))
    return flat([split_snake_case_name_to_words(function_name) for function_name in function_names])


def get_names(trees):
    node_names = flat([[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees])
    return filter_underscores(node_names)


def get_top_verbs_in_path(_path, _top_size=10):
    global Path
    Path = _path
    trees = [t for t in get_trees(None) if t]
    functions = get_names(trees)
    print('functions extracted')
    verbs = flat([get_verbs_from_function_name(function_name) for function_name in functions])
    return collections.Counter(verbs).most_common(_top_size)


def get_top_functions_names_in_path(_path, _top_size=10):
    trees = get_trees(_path)
    function_names = get_names(trees)
    return collections.Counter(function_names).most_common(_top_size)


words = []
projects = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
]
for project in projects:
    path = os.path.join('.', project)
    words += get_top_verbs_in_path(path)

top_size = 200
print(f'total {len(words)} words, {len(set(words))} unique')
for word, occurrence in collections.Counter(words).most_common(top_size):
    print(word, occurrence)
