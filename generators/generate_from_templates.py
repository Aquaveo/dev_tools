# -*- coding: utf-8 -*-
"""
Build library from source
"""
import argparse
import os
import re
import subprocess

GENERATORS = {
    'make': None,
    'vs2013': 'Visual Studio 12 2013 Win64',
    'vs2015': 'Visual Studio 14 2015 Win64',
}


def is_dir(_dir_name):
    """
    Check if the given directory is actually a directory

    Args:
        _dir_name (str): path to a directory

    Returns:
        The abs path to the given directory

    Raises:
        TypeError: If `_dir_name` is not a directory.
    """
    if not os.path.isdir(_dir_name):
        msg = "{} is not a directory".format(_dir_name)
        raise TypeError(msg)
    else:
        return os.path.abspath(_dir_name)


def is_file(_file_name):
    """
    Check if the given file is actually a file.

    Args:
        _file_name (str): path to a file

    Returns:
        The abs path to the given file

    Raises:
        TypeError: If `_file_name` is not a file.
    """
    if not os.path.isfile(_file_name):
        msg = "{} is not a file".format(_file_name)
        raise TypeError(msg)
    else:
        return os.path.abspath(_file_name)


def get_args():
    """
    Get arguments for test script

    Returns:
        parsed used args to be used with the run_tests function

    Raises:
        TypeError: If any of the arguments are not the correct type
    """    
    arguments = argparse.ArgumentParser(description="Run Conan Python tests.")
    arguments.add_argument(
        dest='base_dir', type=str, nargs='?',
        help='location of of the library base directory'
    )
    arguments.add_argument(
        '-t', '--template', dest='template', type=str, nargs='+',
        help='template to be generated'
    )
    parsed_args = arguments.parse_args()

    # Templates
    available_templates = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, 'templates')
    for root, _, files in os.walk(template_path):
        for f in files:
            available_templates[f.split('.template')[0]] = \
                os.path.abspath(os.path.join(root, f))
    print(available_templates)
    return parsed_args

if __name__ == "__main__":
    args = get_args()
