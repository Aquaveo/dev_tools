# -*- coding: utf-8 -*-
"""
build documentation for library
"""
import argparse
import os
import re
import subprocess
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
    arguments = argparse.ArgumentParser(description="Build libary docs.")
    arguments.add_argument(
        dest='doxygen_dir', type=str, nargs='?',
        help='Doxygen Directory'
    )
    arguments.add_argument(
        dest='sphinx_dir', type=str, nargs='?',
        help='python conf directory'
    )
    parsed_args = arguments.parse_args()

    # User input mode if no positional arguments are given
    if not parsed_args.doxygen_dir:
        parsed_args.doxygen_dir = input(
            "Doxygen Directory [{}]:".format(
                parsed_args.doxygen_dir or "./Doxygen")
        ) or parsed_args.doxygen_dir or os.path.join('.', 'Doxygen')
        parsed_args.sphinx_dir = input(
            "Sphinx Directory [{}]:".format(
                parsed_args.sphinx_dir or "./pydocs/source")
        ) or parsed_args.sphinx_dir or os.path.join('.', 'pydocs', 'source')

    parsed_args.doxygen_dir = is_dir(parsed_args.doxygen_dir)
    parsed_args.sphinx_dir = is_dir(parsed_args.sphinx_dir)

    return parsed_args

def build_docs(_doxygen_dir, _sphinx_dir):
    print("------------------------------------------------------------------")
    print(" Build documentation")
    print("------------------------------------------------------------------")

    print(_doxygen_dir)
    print(_sphinx_dir)

    cmd_doxygen = ['doxygen']
    pydocs_output = os.path.join(_doxygen_dir, "html", "pydocs")
    cmd_sphinx = [
        'sphinx-build', '-b', 'html', '-W',
        '-w', 'sphinx_warnings.log', _sphinx_dir, pydocs_output
    ]
    os.chdir(_doxygen_dir)
    print("Building doxygen...")
    subprocess.run(cmd_doxygen)

    if not os.path.isdir(pydocs_output):
        os.mkdir(pydocs_output)

    print("Building sphinx...")
    subprocess.run(cmd_sphinx)

    print("Checking for doxygen warnings...")
    with open('doxy_warn.log', 'r') as dw:
        dw_warnings = dw.readlines()
        dw_count = len(dw_warnings)
    warnings = False
    if dw_count > 0:
        warnings = True
        print('Warnings found in doxygen:')
        for w in dw_warnings:
            print('\t{}'.format(str(w).strip()))
    else:
        print('\tNone found!')

    print("Checking for sphinx warnings...")
    with open('sphinx_warnings.log', 'r') as sw:
        sw_warnings = sw.readlines()
        sw_count = len(sw_warnings)
    if sw_count > 0:
        warnings = True
        print('Warnings found in sphinx:')
        for w in sw_warnings:
            print('\t{}'.format(str(w).strip()))
    else:
        print('\tNone found!')

    os.system("pause")

    if warnings:
        return 1
    else:
        return 0


if __name__ == "__main__":
    args = get_args()
    rc = build_docs(args.doxygen_dir, args.sphinx_dir)
    if rc != 0:
        print("Tests failed...")
        exit(1)
