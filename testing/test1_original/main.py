"""
Test header
"""

import sys
import helper

def main():
    return helper.add(*sys.argv[1:][::-1])

if __name__ == '__main__':
    print(main())