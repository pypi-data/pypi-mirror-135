'''
validation

This program contains many useful functions for validation of input and output.

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   validation.py contains various useful modules for validation of input and
   output
  Version 0.0.1:
   An updated description and various bug fixes. Cleaner looking code with more
   comments. Addition of several different biases, now imports random.
 0.1
  Version 0.1.0:
    ——Friday, the fifteenth day of the firstmonth Janurary, 2021——
   Code is shorter by about fifty lines, and yet its functionality has
   increased... Simplicity is better! Who knew?
  Version 0.1.1:
   Small bugfixes
  Version 0.1.2:
   Code cleanup.
  Version 0.1.3:
   Bugfixes, conforming to PEP
'''

if __name__ == '__main__':
    __package__ = 'usefulpy'
__author__ = 'Austin Garcia'
__version__ = '0.1.3'
__all__ = ('YesOrNo', 'are_floats', 'are_integers', 'bool_', 'boolinput',
           'floatinput', 'floatlistinput', 'fromdatainput', 'getYesOrNo',
           'intinput', 'intlistinput', 'is_complex', 'is_float',
           'is_floatlist', 'is_integer', 'is_intlist', 'isbool', 'makelist',
           'merge_dicts', 'multi_in', 'multicheck', 'trycomplex', 'tryfloat',
           'tryint', 'trynumber', 'trytype', 'validdate', 'validinput',
           'validquery')


from collections import abc
import datetime

_chastise = '\n Your input was invalid, please try again\n'

# for easier reference of the function type.
function = type(lambda: None)


def is_function(s):
    '''Check whether variable s points to a function, not the same as callable'''
    return type(s) is function


def is_integer(s):
    '''Check if an object is an integer or can be turned into an integer without
losing any value'''
    try:
        return int(float(s)) == float(s)
    except Exception:
        return False


def are_integers(*a):
    '''Return True if is_integer is True for all objects in a'''
    return all(map(is_integer, a))


def intinput(Prompt='', beginning='', ending=None, Chastisement=_chastise):
    '''Continue to repeat an input prompt until the prompt can be converted
into an integer.'''
    intstr = input(beginning + Prompt)
    while not is_integer(intstr):
        print(Chastisement)
        intstr = input(Prompt)
    if ending is not None:
        print(ending)
    return int(intstr)


def tryint(s):
    '''Try to turn an object into an integer'''
    if type(s) is int:
        return s
    if is_integer(s):
        try:
            return int(s)
        except Exception:
            return int(float(s))
    return s


def fromrepr(s: str):
    '''Supposed to be the inverse of repr(x)=s'''
    try:
        return eval(s)
    except Exception:
        return s


def makelist(*s):
    '''Makes a list out of nearly any input of any type'''
    if len(s) == 0:
        return []
    if len(s) > 1:
        return [makelist(n) for n in s]
    s1 = s[0]
    if type(s1) is list:
        return s
    if type(s1) in (tuple, set):
        return list(s)
    if type(s1) is str:
        try:
            return makelist(eval(s1))
        except Exception:
            return s1.split()
    try:
        return [x for x in s1]
    except Exception:
        return [s1]


def is_intlist(s):
    '''Check if a list is composed solely of integers'''
    try:
        Valid = list(map(is_integer, s))
        return all(Valid)
    except Exception:
        return False


def intlistinput(Prompt='', beginning='', ending=None, Chastisement=_chastise):
    '''Continue to repeat an input prompt until the input can be converted
into a list of integers'''
    numsstr = input(beginning + Prompt)
    while not is_intlist(numsstr):
        print(Chastisement)
        numsstr = input(Prompt)
    if ending is not None:
        print(ending)
    return list(map(int, numsstr))


def is_float(s):
    '''Check if an object can be turned into a float'''
    try:
        return float(s) == float(s)
    except Exception:
        return False


def are_floats(*a):
    '''Return True if is_integer is True for all objects in a'''
    return all(map(is_float, a))


def floatinput(Prompt='', beginning='', ending=None, Chastisement=_chastise):
    '''Continue to repeat an input prompt until the prompt can be converted
into a float.'''
    floatstr = input(beginning + Prompt)
    while not is_float(floatstr):
        print(Chastisement)
        floatstr = input(Prompt)
    if ending is not None:
        print(ending)
    return float(floatstr)


def is_floatlist(s):
    '''Check if a list is composed solely of numbers'''
    try:
        list(map(float, s.split()))
        return True
    except Exception:
        return False


def floatlistinput(Prompt='', beginning='', ending=None,
                   Chastisement=_chastise):
    '''Continue to repeat an input prompt until the prompt can be converted
into a list of floats.'''
    numsstr = input(beginning + Prompt)
    while not is_floatlist(numsstr):
        print(Chastisement)
        numsstr = input(Prompt)
    if ending is not None:
        print(ending)
    return list(map(float, numsstr))


def _getinp(numinputs, *Prompts, inputtype=None):
    '''Get a number of inputs in a certain type based on prompts'''
    # support for valid inputs
    if not type(numinputs) == int:
        raise ValueError
    if inputtype is None:
        inputtype = input
    if len(Prompts) == 0:
        Prompts = ('',)
    if len(Prompts) > numinputs:
        raise ValueError
    inp = []
    for num in range(numinputs):
        try:
            inp.append(inputtype(Prompts[num]))
        except Exception:
            inp.append(inputtype(Prompts[-1]))
    return inp


def validinput(validquery, *Prompt, returnclass=str, numinputs=None,
               beginning='', ending=None, Chastisement=_chastise,
               ninput=None):
    '''Continue to repeat an input prompt until the prompt is validated by
validquery'''
    '''This part is a big mess despite its simple job. there can be multiple
prompts at once. and numinputs is the number of inputs... this will overide
number of prompts if specified. validquery is the function that returns True
when the input is valid, the returnclass is the function or type that
the final input is put through. ninput is the type of input required for
the arguments and the various input prompts...
like I said... big mess'''
    # Making sure there is a prompt (and thus, an input taken)
    if len(Prompt) == 0:
        Prompt = ('',)
    # if numinputs is not specified
    if numinputs is None:
        numinputs = len(Prompt)
    if len(Prompt) > numinputs:
        raise ValueError()
    # To make the first prompt different
    firstPrompt = list(Prompt).copy()
    firstPrompt[0] = beginning + firstPrompt[0]
    # gets the various inputs at once with _getinp
    inp = _getinp(numinputs, *firstPrompt, inputtype=ninput)
    while not validquery(*inp):
        print(Chastisement)
        inp = _getinp(numinputs, *Prompt, inputtype=ninput)
    if ending is not None:
        print(ending)
    return returnclass(*inp)


def isbool(s):
    '''Check if s is a boolean value'''
    n = type(s)
    return s in ('True', 'False') if n is str else n is bool


def bool_(x):
    '''bool_(x) -> bool'''
    return bool({'True': True, 'False': False}.get(x))


def boolinput(Prompt):
    '''Continue to repeat an input prompt until the input is
'True' or 'False'.'''
    return bool_(validinput(isbool, Prompt))


def fromdatainput(data, prompt=''):
    '''Continue to repeat an input prompt until the input is a value from the
list 'data'.'''
    datum = input(prompt)
    while datum not in data:
        datum = input(prompt)
    return datum


def multicheck(data, checks, threshhold=1):
    '''Check checks on data, threshold is the number of checks that need
to return a True value'''
    try:
        data = iter(data)
    except Exception:
        data = iter((data,))
    try:
        checks = iter(checks)
    except Exception:
        checks = iter((checks,))
    count = 0
    for n in data:
        for c in checks:
            try:
                if c(n):
                    count += 1
                if count >= threshhold:
                    return True
            except Exception:
                pass
    return False


def multi_in(data1, data2, threshhold=1):
    '''Check if any item in data1 is in data2. Threshold is the number of
matches there has to be'''
    try:
        data1 = iter(data1)
    except Exception:
        data1 = iter((data1,))
    try:
        data2 = iter(data2)
    except Exception:
        data2 = iter((data2,))
    count = 0
    for n in data1:
        if n in data2:
            count += 1
        if count >= threshhold:
            return True
    return False


affirmatives = ('ye', 'do', 'course', 'would', 'sure')
negatives = ('no', 'n\'t', 'na', 'stop')


def YesOrNo(Response):
    '''Check if a text is an affirmative or a negative'''
    response, Response = Response.lower(), None
    if response in ('true', 't', 'y'):
        return True
    if response in ('false', 'n', 'f'):
        return False
    for n in affirmatives:
        if n in response:
            Response = True
            break
    for n in negatives:
        if n in response:
            Response = False
            break
    if 'why' in response:
        Response = not Response
    return Response


def getYesOrNo(Prompt='', beginning='', ending=None, Chastisement=_chastise):
    '''Continue to repeat an input prompt until the prompt can be converted
into a boolean value, this includes variations of Yes and No.'''
    response = input(beginning + Prompt)
    while YesOrNo(response) is None:
        print(Chastisement)
        response = input(Prompt)
    if ending is not None:
        print(ending)
    return YesOrNo(response)


def validdate(year, month, day):
    '''Check if a year, month, day combo is valid'''
    try:
        datetime.date(year, month, day)
        return True
    except Exception:
        return False


def validquery(ntype, *s):
    '''Check if s can be converted into a type ntype'''
    try:
        if type(*s) == ntype:
            return True
    except Exception:
        pass
    try:
        ntype(*s)
        return True
    except Exception:
        return False


def trytype(ntype, *s):
    '''Try to convert data s into a type ntype'''
    if len(s) == 1:
        s = s[0]
        if type(s) == ntype:
            return s
        if validquery(ntype, s):
            return ntype(s)
        return s
    if validquery(ntype, *s):
        return ntype(*s)
    return s


def merge_dicts(a, b, exclude=True, fill_val=None):
    ndict = {}
    for key in a:
        if key in b:
            ndict[key] = (a[key], b[key])
    if exclude:
        return ndict
    for key in b:
        ndict[key] = (a.get(key, fill_val), b.get(key, fill_val))
    return ndict


def _flatten(iterable):
    '''flatten an iterable'''
    for value in iterable:
        if isinstance(value, abc.Iterable):
            if not isinstance(value, (str, bytes)):
                yield from _flatten(value)
                continue
        yield value


def tryfloat(s):
    '''Convert s to a float if is_float(s)'''
    s = tryeval(s)
    try:
        return float(s)
    except Exception:
        return s


# Only kept to support older functions. will soon be removed.
def tryeval(s):
    '''Tries to evaluate a string if it is a string. returns input if it cannot
be evaluated'''
    if type(s) is str:
        try:
            return eval(s)
        except Exception:
            return s
    return s


def is_complex(s):
    '''Return True if s can be interpreted as a complex number'''
    s = tryeval(s)
    try:
        complex(s)
        return True
    except Exception:
        return False


def trycomplex(s):
    '''Tries to convert s into a complex number'''
    s = tryeval(s)
    try:
        return complex(s)
    except Exception:
        return s


def trynumber(s):
    '''Convert it into the simplest of an int, float, or complex'''
    s = tryeval(s)
    if type(s) in (int, float, complex):
        return tryint(s)
    if is_integer(s):
        try:
            return int(s)
        except Exception:
            return int(float(s))
    if is_float(s):
        return float(s)
    if is_complex(s):
        return complex(s)
    return s

# eof
