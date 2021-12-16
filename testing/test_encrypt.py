"""

"""

from icecream import ic

def test_encrypt():
    key = 177
    data = 'abc'

    for char in data:
        ic(char)

        ic(ord(char))
        ic(key)
        ic(ord(char) ^ key)

        ic(bin(ord(char)))
        ic(bin(key))
        ic(bin(ord(char) ^ key))

        ic(chr(ord(char) ^ key))
        ic('Decrypting')

        ic(ord(chr(ord(char) ^ key)))
        ic(key)
        ic(ord(chr(ord(char) ^ key)) ^ key)

        ic(bin(ord(chr(ord(char) ^ key))))
        ic(bin(key))
        ic(bin(ord(chr(ord(char) ^ key)) ^ key))
        
        assert ic(chr(ord(chr(ord(char) ^ key)) ^ key)) == char
        ic('\n')

def main():
    tests = [
        test_encrypt
    ]

    for test in tests: test()

if __name__ == '__main__':
    main()