# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-06-15 11:00:19
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-06-15 11:00:53

def main():
    exit = input('input [e] to close, [c] to continue: ')
    while exit not in ('c', 'e'):
        exit = input('input [e] to close, [c] to continue: ')
    else:
        if exit == 'c':
            main()
