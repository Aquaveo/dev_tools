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
    parser.add_argument('-w', '--windows', action='store_true',
                        help='The package version'
                        )

    parser.add_argument('name', type=str, 
                        help='The name of the package'
                        )
    args = parser.parse_args()

    if args.windows:
        export_cmd = "set"
        outfile = "set_env.bat"
    else:
        export_cmd = "export"
        outfile = "set_env.sh"

    with open(outfile, 'w+') as f:
        print(f"{export_cmd} CONAN_ARCHS={args.archs}", file=f)
        print(f"{export_cmd} CONAN_BUILD_TYPES={args.build_types}", file=f)
        print(f"{export_cmd} CONAN_CHANNEL={args.channel}", file=f)
        print(f'{export_cmd} CONAN_REFERENCE={args.name}/{args.version}', file=f)
        print(f'{export_cmd} CONAN_USERNAME=aquaveo', file=f)
        print(f"{export_cmd} XMS_VERSION={args.version}", file=f)

    print(f"Environment file generated. Please source '{outfile}' in your current shell.")
