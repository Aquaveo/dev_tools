# -*- coding: utf-8 -*-
"""
Run python conan tests for conan package
"""
import argparse
import os
import re
import sys
import unittest

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
        dest='test_dir', type=str, nargs='?',
        help='location of python test files'
    )
    arguments.add_argument(
        '-b', '--bin-dir', dest='bin_dir', type=str, default='.',
        help='location of binary files'
    )
    arguments.add_argument(
        '-c', '--conan-file', dest='conan_file', type=str,
        default='./conanbuildinfo.txt', help='path to conan info file'
    )
    parsed_args = arguments.parse_args()

    # User input mode if no positional arguments are given
    if not parsed_args.test_dir:
        while not parsed_args.test_dir:
            parsed_args.test_dir = input("Location of test files:")
        parsed_args.bin_dir = input(
            "Binary directory [{}]:".format(parsed_args.bin_dir)
        ) or parsed_args.bin_dir
        parsed_args.conan_file = input(
            "Conan file [{}]:".format(parsed_args.conan_file)
        ) or parsed_args.conan_file

    parsed_args.test_dir = is_dir(parsed_args.test_dir)
    parsed_args.bin_dir = is_dir(parsed_args.bin_dir)
    parsed_args.conan_file = is_file(parsed_args.conan_file)

    return parsed_args


def get_python_paths_for_conan_packages(_conan_file):
    """
    Get the python paths from the conan info files for aquaveo conan packages

    Args:
        _conan_file (str): path to the conan file with the package info

    Returns:
        A list of paths to be add to the system path for python packages

    Raises:
        TypeError: If any of the specified paths do not exist
    """
    list_of_paths = []
    py_path_re = r"PYTHONPATH=\[\"(.*)\"\]"
    with open(_conan_file, "r") as cf:
        for line in cf.readlines():
            l = re.search(py_path_re, line)
            if l:
                list_of_paths.append(os.path.abspath(l.group(1)))
    return list_of_paths


def run_tests(_test_dir, _bin_dir, _conan_file):
    """
    Function to run the test

    Args:
        _bin_dir (str): directory where the binary files are located
        _conan_file (str): conanbuildinfo.txt file for the build

    Returns:
        0 if tests are successful, 1 if tests have failed
    """
    # Setup working environment
    print("------------------------------------------------------------------")
    print("Running Tests")
    print("------------------------------------------------------------------")
    python_paths = get_python_paths_for_conan_packages(_conan_file)
    for path in python_paths:
        print(path)
        sys.path.append(path)
    print(_bin_dir)
    sys.path.append(_bin_dir)
    if os.path.isdir("_package"):
        sys.path.append(os.path.realpath("_package"))
    l = unittest.TestLoader()
    tests = l.discover(start_dir=_test_dir, pattern="*_pyt.py")
    test_results = unittest.TextTestRunner(verbosity=2).run(tests)
    return len(test_results.errors)


if __name__ == "__main__":
    args = get_args()
    rc = run_tests(args.test_dir, args.bin_dir, args.conan_file)
    if rc != 0:
        print("Tests failed...")
        exit(1)
