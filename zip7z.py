# -*- coding: utf-8 -*-

import os
import subprocess

PATH = os.path.dirname(__file__)
FILE = os.path.join(PATH, '7z.exe')


def _generateCompressCommand(inputfilelist, outputfile, outputtype,
                             password=None):
    inputfiles = ' '.join(inputfilelist)
    command = r'%s a -y -r -t%s' % (FILE, outputtype)
    if password:
        command += r' -p%s' % password
    command += r' %s %s' % (outputfile, inputfiles)
    return command


def _generateUncompressCommand(inputfile, outputpath, password=None):
    command = r'%s x -y -r -o%s' % (FILE, outputpath)
    if password:
        command += r' -p%s' % password
    command += ' ' + inputfile
    return command


def compressToZip(inputfilelist, outputfile, password=None):
    command = _generateCompressCommand(inputfilelist, outputfile, 'zip', password)
    return not subprocess.call(command, shell=True)


def compressTo7z(inputfilelist, outputfile, password=None):
    command = _generateCompressCommand(inputfilelist, outputfile, '7z', password)
    return not subprocess.call(command, shell=True)


def uncompress(inputfile, outputpath, password=None):
    command = _generateUncompressCommand(inputfile, outputpath, password)
    return not subprocess.call(command, shell=True)
