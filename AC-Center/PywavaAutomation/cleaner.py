#!/usr/bin/python3.10


################################################################################


import os


################################################################################


def clean_fold(path):
    for f in os.listdir(path):
        os.popen(f'del {path}\{f}')


################################################################################
