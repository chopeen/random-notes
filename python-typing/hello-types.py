from typing import List

'''
https://www.python.org/dev/peps/pep-3107/

Because Python's 2.x series lacks a standard way of annotating a function's parameters and return values, a variety of
tools and libraries have appeared to fill this gap. Some utilise the decorators introduced in "PEP 318", while others
parse a function's docstring, looking for annotations there.

This PEP aims to provide a single, standard way of specifying this information, reducing the confusion caused by
the wide variation in mechanism and syntax that has existed until this point.
'''


def main():
    ints: List[int] = [1, 2, 3, 'a']
    sep: str = '|'

    # TODO: how to make it fail because of invalid type?
    # sep: str = 9

    csv = ints_to_csv(ints, sep)
    print(csv)


def ints_to_csv(ints: List[int], sep: str) -> str:
    ints = map(lambda x: str(x), ints)
    return sep.join(ints)


if __name__ == '__main__':
    main()
