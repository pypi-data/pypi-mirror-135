import curses
import sys

from docutils.parsers.rst.directives.tables import align


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def remove_suffix(text, suffix):
    if text.endswith(suffix):
        return text[:-len(suffix)]
    return text


def is_word(line, target_index):
    return line[target_index + 1].lower() not in ' \n' or line[target_index - 1].lower() not in ' \n'


def find_word_start_index(line, target_index):
    index = target_index - 1
    while index >= 0:
        if line[index].lower() in ' \n':
            return index
        index = index - 1
    return target_index


def find_word_end_index(line, target_index):
    index = target_index + 1
    while index <= len(line):
        if line[index].lower() in ' \n':
            return index
        index = index + 1
    return target_index


def to_lines(line, length):
    lines = []
    while True:
        if len(line) <= length:
            lines.append(line)
            break

        if not is_word(line, length - 1):
            lines.append(line[:length - 1])
            sub_line = line[:length - 1]
            line = line[length - 1:].strip()
        else:
            index = find_word_start_index(line, length - 1)
            sub_line = line[:index]
            line = line[index:].strip()

        lines.append(sub_line)

    return lines


def read_file(file_path):
    with open(file_path) as f:
        return f.read()


def view_curses_colors():
    def print_color(stdscr):
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        try:
            for i in range(0, 255):
                stdscr.addstr(str(i) + " ", curses.color_pair(i))
        except curses.ERR:
            # End of screen reached
            pass
        stdscr.getch()

    curses.wrapper(print_color)


def color_print(msg):
    def func(stdscr):
        stdscr.scrollok(True)  # enable scrolling, so it can print string with new lines

        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(124, 123, -1)  # changes the definition of color pair 124
        curses.init_pair(197, 196, -1)  # changes the definition of color pair 197
        try:
            stdscr.addstr(msg + " ", curses.color_pair(124))
            stdscr.addstr("\n\npress any key to exit view", curses.color_pair(197))  # red text
        except curses.ERR:
            # End of screen reached
            pass
        stdscr.getch()

    curses.wrapper(func)


def proto_print(msg):
    sys.stdout.write(u"\u001b[38;5;" + str(229) + "m " + msg)
    print(u"\u001b[0m")


def print_info(msg):
    sys.stdout.write(u"\u001b[38;5;" + str(38) + "m " + msg)
    print(u"\u001b[0m")


def show_colors():
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
    print(u"\u001b[0m")  # clear


def split(line: str, x: int):
    """
    split a line every x characters
    :param line: original line need to be split.
    :param x: max length of split lines
    :return: a string list that all elements are not more than x characters.
    """
    return [line[i: i + x] for i in range(0, len(line), x)]


def add_prefix(lines: [str], prefix: str):
    return [prefix + line for line in lines]


def add_suffix(lines: [str], suffix: str):
    return [line + suffix for line in lines]


def align_lines_with_filler(text: str, length: int, filler: str = " ", align='left'):
    """
    align text
    :param text: text to be formatted.
    :param length: max length limitation for each line.
    :param filler: the character used to added to the line to make sure the length is the same for lines.
    :param align: the way of alignment, left, right or center
    :return: formatted string lines
    """
    lines = text.split("\n")

    formatted_lines = []
    for line in lines:
        formatted_lines.extend(to_lines(line, length))

    lines = formatted_lines
    if align == 'left':
        return [f"{line.strip()}{filler * (length - len(line.strip()))}" for line in lines]

    if align == 'right':
        return [f"{filler * (length - len(line.strip()))}{line.strip()}" for line in lines]

    if align == 'center':
        processed_lines = []
        for line in lines:
            filler_amount = int((length - len(line.strip())) / 2)
            if (length - len(line.strip())) % 2 == 1:
                line = f"{filler * filler_amount}{line.strip() + ' '}{filler * filler_amount}"
            else:
                line = f"{filler * filler_amount}{line.strip()}{filler * filler_amount}"
            processed_lines.append(line)
        return processed_lines

    return lines


def replace_at_start(line: str, new: str):
    """
    replace the start substring with same length of new string from the start of the line with the new string.
    :param line: lien to be processed.
    :param new: new string.
    :return: replaced line.
    """
    if len(line) <= len(new):
        return new[:len(line)]
    else:
        return f"{new}{line[len(new):]}"
