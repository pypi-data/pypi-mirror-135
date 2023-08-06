import os
import sys


def load_py_file(file_path, remove_insert_path='new'):
    """
    :param file_path:

    :param remove_insert_path:
        'any' to remove inserted path even the path is in path list before performing this function
        'new' (default) to remove inserted path from sys path list if this path was not in list before
        False to do nothing
    """
    # TODO remove inserted path?
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    file_name_no_suffix = os.path.splitext(os.path.basename(file_name))[0]
    sys.path.insert(-1, file_dir)
    content = {}
    try:
        exec(f'import py file {file_name}', {}, content)
    except ModuleNotFoundError:
        raise FileNotFoundError(f'Not find input file {file_name} with basename {file_name_no_suffix} in {file_dir}')
    return content['content']
