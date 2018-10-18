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
        dest='cmake_dir', type=str, nargs='?',
        help='location of CMakeList.txt'
    )
    arguments.add_argument(
        dest='build_dir', type=str, nargs='?',
        help='location of build files'
    )
    arguments.add_argument(
        dest='profile', type=str, nargs='?',
        help='profile to build'
    )
    arguments.add_argument( 
        dest='generator', type=str, nargs='?',
        help='files to generate. (vs2013, vs2015, or make)'
    )
    arguments.add_argument(
        '-g', '-gui', dest='use_gui', action='store_true',
        help='use gui interface'
    )
    parsed_args = arguments.parse_args()

    # Profiles
    precompile_profiles = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    profile_path = os.path.join(script_dir, '..', 'profiles')
    for root, _, files in os.walk(profile_path):
        for f in files:
            precompile_profiles[f] = os.path.abspath(os.path.join(root, f))

    if not parsed_args.cmake_dir or not parsed_args.build_dir \
            or parsed_args.profile or not parsed_args.generator:
        parsed_args.cmake_dir = input("CMakeList.txt location [{}]:".format(
            parsed_args.cmake_dir or '.'
        )) or '.'
        parsed_args.build_dir = input("build location [{}]:".format(
            parsed_args.build_dir or '.'
        )) or '.'
        print("Available Profiles: {}".format(', '.join(precompile_profiles.keys())))
        parsed_args.profile = input("profile [{}]:".format(
            parsed_args.profile or '.\\default'
        )) or '.\\default'
        print("Available Generators: {}".format(', '.join(GENERATORS.keys())))
        parsed_args.generator = input("generator [{}]".format(
            parsed_args.generator or 'make'
        )) or 'make'

        parsed_args.cmake_dir = is_dir(parsed_args.cmake_dir)
        parsed_args.build_dir = is_dir(parsed_args.build_dir)

        if not parsed_args.profile in precompile_profiles.keys():
            parsed_args.profile = is_file(parsed_args.profile)
        else:
            parsed_args.profile = precompile_profiles[parsed_args.profile]

        # Generators
        if parsed_args.generator not in GENERATORS:
            msg = 'specified generator not supported "{}". ' \
                      'Must be one of [{}]'.format(
                          parsed_args.generator, ", ".join(GENERATORS.keys())
                          )
            raise TypeError(msg)

    return parsed_args


def conan_install(_profile, _cmake_dir, _build_dir):
    print("------------------------------------------------------------------")
    print(" Generating conan info")
    print("------------------------------------------------------------------")
    subprocess.call([
        'conan', 'install', '-if', _build_dir,
        '-pr', _profile, _cmake_dir
    ])
    os.system("pause")


def get_cmake_options(_build_dir):
    print("------------------------------------------------------------------")
    print(" Setting up cmake options")
    print("------------------------------------------------------------------")
    conan_options = {}
    conan_option_re = r'(pybind|testing|xms){1}=(True|False)'
    conan_info_file = os.path.join(_build_dir, 'conaninfo.txt')
    with open(conan_info_file, 'r') as cf:
        for line in cf.readlines():
            o = re.search(conan_option_re, line)
            if o:
                conan_options[o.group(1)] = o.group(2)
    cmake_options = []
    cmake_options.append('-DBUILD_TESTING={}'.format(
        conan_options.get('testing', 'False')))
    cmake_options.append('-DIS_PYTHON_BUILD={}'.format(
        conan_options.get('pybind', 'False')))
    cmake_options.append('-DXMS_BUILD={}'.format(
        conan_options.get('xms', 'False')))

    uses_python = conan_options.get('pybind', 'False')
    is_testing = conan_options.get('testing', 'False')
    if uses_python != 'False':
        python_target_version = input('Target Python Version [3.6]:') or "3.6"
        cmake_options.append('-DPYTHON_TARGET_VERSION={}'.format(
            python_target_version
        ))
    elif is_testing != 'False':
        test_files = input('Path to test files [.\\test_files]:') or ".\\test_files"
        has_test_files = test_files != 'NONE'
        if not os.path.isdir(test_files) and has_test_files:
            print("Specified path to test files does not exist! Aborting...")
            exit(1)
        else:
            test_files = os.path.abspath(test_files)

        if has_test_files:
            cmake_options.append('-DXMS_TEST_PATH={}'.format(
                test_files
            ))

    lib_version = input('Library Version [99.99.99]:') or "99.99.99"
    cmake_options.append('-DXMS_VERSION={}'.format(lib_version))

    print("Cmake Options:")    
    for o in cmake_options:
        print("\t{}".format(o))
    os.system("pause")
    return cmake_options


def run_cmake(_cmake_dir, _build_dir, _generator, _cmake_options):
    print("------------------------------------------------------------------")
    print(" Running cmake")
    print("------------------------------------------------------------------")
    cmd = ['cmake']
    gen = GENERATORS[_generator]
    if gen:
        cmd += ['-G', '{}'.format(gen)]
    cmd += _cmake_options
    cmd.append(_cmake_dir)
    os.chdir(_build_dir)
    subprocess.run(cmd)
    os.system("pause")

if __name__ == "__main__":
    args = get_args()
    conan_install(args.profile, args.cmake_dir, args.build_dir)
    my_cmake_options = get_cmake_options(args.build_dir)
    run_cmake(args.cmake_dir, args.build_dir, args.generator, my_cmake_options)
