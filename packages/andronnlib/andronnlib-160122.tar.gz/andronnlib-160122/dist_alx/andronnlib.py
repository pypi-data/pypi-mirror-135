# -*- coding: UTF-8 -*-

# <?python

# Andronn Library. Used in Andronn's projects.
# Copyright Andronn Inc. 2022.

from random import randint
from datetime import *

_modules_ = 0

def getTime():
    val = datetime.now()
    #print(val) # Debug only
    val = str(val.hour)+':'+str(val.minute)+':'+str(val.second)
    return val
_modules_ += 1

def showCopyright(arg, arg2):   # Shows the game copyright
    print('# '+str(arg)+' v.'+str(arg2)+'.')
    print('Copyright Andronn Inc. 2022.')
_modules_ += 1

def rstr(arg, arg2):    # Picks random string
    rstr = str(randint(int(arg), int(arg2)))
    return rstr
_modules_ += 1

def formPicker():   # Picks the random file format
    rnd = randint(1, 21)
    if rnd == 1:
        form = '.txt'   # Classic text document file
    elif rnd == 2:
        form = '.log'   # Logs file
    elif rnd == 3:
        form = '.html'  # HTML code file
    elif rnd == 4:
        form = '.py'    # Python code file
    elif rnd == 5:
        form = '.pptx'  # Powerpoint presentation file
    elif rnd == 6:
        form = '.php'   # PHP code file
    elif rnd == 7:
        form = '.exe'   # Widows executable file
    elif rnd == 8:
        form = '.dll'   # Dynamic Link Library file
    elif rnd == 9:
        form = '.zip'   # Compressed ZIP archive
    elif rnd == 10:
        form = '.ico'   # Icon file
    elif rnd == 11:
        form = '.ink'   # Shortcut file
    elif rnd == 12:
        form = '.md'    # Markdown text file
    elif rnd == 13:
        form = '.bin'   # Binary file
    elif rnd == 14:
        form = '.rtf'   # Rich Text Format text file
    elif rnd == 15:
        form = '.'      # Empty form
    elif rnd == 16:
        form = '.json'  # JSON config file
    elif rnd == 17:
        form = '.ini'   # INI config file
    elif rnd == 18:
        form = '.apk'   # Android executable file
    elif rnd == 19:
        form = '.conf'  # Config text file
    elif rnd == 20:
        form = '.java'  # Java code file
    else:
        form = '-1'     # Undefined form
    return form
_modules_ += 1

def n():            # New line
    print('\n')
_modules_ += 1

def p():            # Three #'s
    print('###')
_modules_ += 1

def np():           # New line + Three #'s
    n()
    p()
_modules_ += 1

def pn():           # Three #'s + New line
    p()
    n()
_modules_ += 1

def info(arg):      # Shows info text
    val = print(getTime()+' $ [INFO]: ',arg)
    return val
_modules_ += 1

def stat(arg):      # Shows status text
    val = print(getTime()+' --- [STATUS]: ',arg)
    return val
_modules_ += 1

def enter(lang):    # Asks user to press enter to continue
    if lang == 'eng':   # On English
        val = input(getTime()+' ## [ENTER]: Enter to continue...')
    elif lang == 'ru':  # On Russian
        val = input(getTime()+' ## [ENTER]: Enter чтобы продолжить...')
    else:               # Undefined (On English)
        val = input(getTime()+' ## [ENTER]: Enter to continue...')
    return val
_modules_ += 1

def warn(arg):      # Shows warning text
    val = print(getTime()+' !! [WARN]: ',arg)
    return val
_modules_ += 1

def ques(arg):      # Asks a question and returns answer
    val = input(getTime()+' $$ [QUESTION]: '+str(arg))
    return val
_modules_ += 1

def error(arg):     # Shows error text
    val = print(getTime()+' ??? [ERROR]: ',arg)
    return val
_modules_ += 1

def debug(arg):     # Shows debug text
    val = print(getTime()+' [DEBUG]: ',arg)
    return val
_modules_ += 1

def custom(title, arg):     # Shows text with custom prefix
    val = print(getTime()+' ['+str(title)+']: ',arg)
    return val
_modules_ += 1

print('''This script is using Andronn Library v.160122.
Succefully loaded '''+str(_modules_)+' library modules!')
n()

# python?>