# -*- coding: utf-8 -*-

"""
/*
*
* Auther： Wenjie Zheng <wjzheng@robosense.cn>
* File:    winprint.py
*
*/
"""

import ctypes, sys

# 增加Windows cmd/Power Shell 颜色兼容
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
# 字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色
# 由于该函数的限制，应该是只有这16种，可以前景色与背景色组合。也可以几种颜色通过或运算组合，组合后还是在这16种颜色中

# Windows CMD命令行 字体颜色定义 text colors
FOREGROUND_BLACK = 0x00  # black.
FOREGROUND_DARKBLUE = 0x01  # dark blue.
FOREGROUND_DARKGREEN = 0x02  # dark green.
FOREGROUND_DARKSKYBLUE = 0x03  # dark skyblue.
FOREGROUND_DARKRED = 0x04  # dark red.
FOREGROUND_DARKPINK = 0x05  # dark pink.
FOREGROUND_DARKYELLOW = 0x06  # dark yellow.
FOREGROUND_DARKWHITE = 0x07  # dark white.
FOREGROUND_DARKGRAY = 0x08  # dark gray.
FOREGROUND_BLUE = 0x09  # blue.
FOREGROUND_GREEN = 0x0a  # green.
FOREGROUND_SKYBLUE = 0x0b  # skyblue.
FOREGROUND_RED = 0x0c  # red.
FOREGROUND_PINK = 0x0d  # pink.
FOREGROUND_YELLOW = 0x0e  # yellow.
FOREGROUND_WHITE = 0x0f  # white.

# Windows CMD命令行 背景颜色定义 background colors
BACKGROUND_DARKBLUE = 0x10  # dark blue.
BACKGROUND_DARKGREEN = 0x20  # dark green.
BACKGROUND_DARKSKYBLUE = 0x30  # dark skyblue.
BACKGROUND_DARKRED = 0x40  # dark red.
BACKGROUND_DARKPINK = 0x50  # dark pink.
BACKGROUND_DARKYELLOW = 0x60  # dark yellow.
BACKGROUND_DARKWHITE = 0x70  # dark white.
BACKGROUND_DARKGRAY = 0x80  # dark gray.
BACKGROUND_BLUE = 0x90  # blue.
BACKGROUND_GREEN = 0xa0  # green.
BACKGROUND_SKYBLUE = 0xb0  # skyblue.
BACKGROUND_RED = 0xc0  # red.
BACKGROUND_PINK = 0xd0  # pink.
BACKGROUND_YELLOW = 0xe0  # yellow.
BACKGROUND_WHITE = 0xf0  # white.
# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool


# reset white
def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

def printblack(msg):    # black.
    set_cmd_text_color(FOREGROUND_BLACK)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printdarkblue(msg):     # dark blue.
    set_cmd_text_color(FOREGROUND_DARKBLUE)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printdarkgreen(msg):    # dark green.
    set_cmd_text_color(FOREGROUND_DARKGREEN)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printdarkskyblue(msg):      # dark skyblue.
    set_cmd_text_color(FOREGROUND_DARKSKYBLUE)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printdarkred(msg):      # dark red.
    set_cmd_text_color(FOREGROUND_DARKRED)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printdarkpink(msg):     # dark pink.
    set_cmd_text_color(FOREGROUND_DARKPINK)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printdarkyellow(msg):     # dark yellow.
    set_cmd_text_color(FOREGROUND_DARKYELLOW)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printdarkwhite(msg):     # dark white.
    set_cmd_text_color(FOREGROUND_DARKWHITE)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printdarkgray(msg):     # dark gray.
    set_cmd_text_color(FOREGROUND_DARKGRAY)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printblue(msg):     # blue.
    set_cmd_text_color(FOREGROUND_BLUE)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printgreen(msg):    # green.
    set_cmd_text_color(FOREGROUND_GREEN)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printskyblue(msg):  # skyblue.
    set_cmd_text_color(FOREGROUND_SKYBLUE)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printred(msg):  # red.
    set_cmd_text_color(BACKGROUND_YELLOW | FOREGROUND_RED)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printpink(msg):     # pink.
    set_cmd_text_color(FOREGROUND_PINK)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printyellow(msg):   # yellow.
    set_cmd_text_color(FOREGROUND_YELLOW)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()

def printwhite(msg): # white.
    set_cmd_text_color(FOREGROUND_WHITE)
    sys.stdout.write(msg)
    print('', end='', flush=True)
    resetColor()