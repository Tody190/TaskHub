# coding=utf-8
__author__ = 'yangtao'
__version__ = '1.0'

def show(author=None, version=None):
    if author:
        print("author: %s"%author)
    if version:
        print("version: %s"%version)
    print("enjoy it!")
    print('')