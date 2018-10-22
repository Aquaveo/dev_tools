# -*- coding: utf-8 -*-
"""
Sets environmental variables necessary to build via build.py
"""
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-a', '--archs', type=str, default='x86_64',
                        help='A list of architetures to build the package for'
                        )
    parser.add_argument('-c', '--channel', type=str, default='stable',
                        help='The channel in which to place the package'
                        )
    parser.add_argument('-t', '--build-types', type=str, default='Release',
                        help='A list of build configurations to build'
                        )
    parser.add_argument('-v', '--version', type=str, default='99.99.99',
                        help='The package version'
                        )

    parser.add_argument('name', type=str, 
                        help='The name of the package'
                        )
    args = parser.parse_args()

    os.environ["CONAN_ARCHS"] = args.archs
    os.environ["CONAN_BUILD_TYPES"] = args.build_types
    os.environ["CONAN_CHANNEL"] = args.channel
    os.environ["CONAN_REFERENCE"] = f"{args.name}/{args.version}"
    os.environ["CONAN_USERNAME"] = "aquaveo"
    os.environ["XMS_VERSION"] = args.version

    print("Current CONAN Environmental Variables:")
    for key, value in os.environ.items():
        if "CONAN" in key:
            print(f"{key}: {value}")
