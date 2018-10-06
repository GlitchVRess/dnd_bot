import ctypes
import gc
import json
import operator
import random
import re
import sys

def float_or_int(number):
    """Checks if 'number' has a decimal. If it does, type it as float.
    else, type it as int. Used primarily for 'operand' prior to
    complex_math.
    """
    if '.' in number:
        return float(number)
    else:
        return int(number)


def simple_math(times, sides):
    """Generates multiple numbers from 1 to the number stored in 'sides'
    based on the number stored in 'times'. Returns the result as a
    list.
    """
    try:
        sub_subprocessor = ctypes.CDLL('./sfmt/sub_subprocessor.so')
    except Exception:
        exit_message = "Please run 'make' within installation directory.\n./sfmt/sub_subprocessor.so is missing."
        sys.exit(exit_message)

    sub_subprocessor.roll.argtypes = [ctypes.POINTER(ctypes.c_int)]
    sub_subprocessor.roll.restype = None
    values = (ctypes.c_int * times)()
    sub_subprocessor.roll(values, len(values), 1, sides)
    results = values
    del values
    return results


def complex_math(results, expression='+', operand=0):
    """Performs math based on the operator in the original message.
    Returns the results as a separate list.
    """
    operators = {'+':operator.add, 
     '-':operator.sub, 
     '*':operator.mul, 
     '//':operator.truediv, 
     '^':operator.pow, 
     '%':operator.mod, 
     '/':operator.floordiv}
    final_results = []
    for each in results:
        final_results.append(operators[expression](each, operand))

    return final_results


def build_message(string, results, final_results, comment=''):
    """Builds the return message for the discord bot to present the
    roll totals. Uses the lists returned by 'complex_math()' and
    'simple_math()'.
    """
    string = string.split(' #')[0]
    message = ('{0} ').format(string[6:])
    final_results = sum(final_results)
    message = ('{0} : {1}{2}').format(string[6:], final_results, comment)
    if len(str(message)) > 2000:
        message = 'SIRWHYYOUDOTHIS. MESSAGE TOO LONG. ABORT! ABORT!!!!!!'
    return message


def roll(string):
    """Checks if the string is a valid roll, if it is it exeutes
    'simple_math()', complex_math', and returns the message built by
    'build_message()'
    """
    r = re.compile('^!roll (\\d+)d(\\d+)(?:([\\+\\-\\/\\*\\^\\%]|\\/\\/)(\\d+(?:\\.\\d+)?))?(?:( #.+))?$')
    m = re.search(r, string)
    if not m:
        return 'This command did not meet the required syntax.'
    else:
        times = int(m.group(1))
        sides = int(m.group(2))
        comment = ''
        expression = '+'
        operand = 0
        if m.group(5):
            comment = m.group(5)
        if m.group(3):
            expression = m.group(3)
            operand = float_or_int(m.group(4))
        results = simple_math(times, sides)
        final_results = complex_math(results, expression, operand)
        message = build_message(string, results, final_results, comment)
        return message


def cast(string):
    """loading the casts.json first, then seeing if it matches, if it does,
    process roll(string).
    """
    casts = {}
    with open('casts.json') as (jsonData):
        casts = json.load(jsonData)
    if casts[string[6:]]:
        return roll(('!roll {0}').format(casts[string[6:]]))
    else:
        return 'This command did not meet the required syntax or match an existing cast.'
