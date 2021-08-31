# tee.py
# Purpose: A Python class with a write() method which, when 
# used instead of print() or sys.stdout.write(), for writing 
# output, will cause output to go to both sys.stdout and 
# the filename passed to the class's constructor. The output 
# file is called the teefile in the below comments and code.

# The idea is to do something roughly like the Unix tee command, 
# but from within Python code, using this class in your program.

# The teefile will be overwritten if it exists.

# The class also has a writeln() method which is a convenience 
# method that adds a newline at the end of each string it writes, 
# so that the user does not have to.

# Python's string formatting language is supported (without any 
# effort needed in this class), since Python's strings support it, 
# not the print method.

# Author: Vasudev Ram
# Web site: https://vasudevram.github.io
# Blog: https://jugad2.blogspot.com
# Product store: https://gumroad.com/vasudevram

from __future__ import print_function
import sys
from error_exit import error_exit


class Tee(object):
    def __init__(self, tee_filename):
        try:
            self.tee_fil = open(tee_filename, "w")
        except IOError as ioe:
            error_exit("Caught IOError: {}".format(repr(ioe)))
        except Exception as e:
            error_exit("Caught Exception: {}".format(repr(e)))

    def write(self, s):
        sys.stdout.write(s)
        self.tee_fil.write(s)

    def writeln(self, s):
        self.write(s + '\n')

    def close(self):
        try:
            self.tee_fil.close()
        except IOError as ioe:
            error_exit("Caught IOError: {}".format(repr(ioe)))
        except Exception as e:
            error_exit("Caught Exception: {}".format(repr(e)))