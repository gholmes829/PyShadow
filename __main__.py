"""
Author: Grant Holmes
Email: g.holmes429@gmail.com
Created: 12/1/21
"""

import argparse
import obfuscate

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', help='relative path to directory to recursively obfuscate or to file to obfuscate.')
    parser.add_argument('output_name', help='name of generated executable.')
    parser.set_defaults(func = obfuscate.run)
    args = parser.parse_args()
    args.func(args)