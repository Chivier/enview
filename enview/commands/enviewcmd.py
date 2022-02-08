from nubia import argument, command, context
import asyncio
import socket
import typing
import sys
import subprocess
import os
import pyperclip
import re
import readchar
from termcolor import cprint
import tempfile


class bcolors:
    """
    Colors for printing
    """
    HEADER = '\033[95m'
    WHITE = '\033[1;34;47m'
    OKBLUE = '\033[1;35m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def check_ipv6(address: str) -> bool:
    """
    Check if the address is a valid IPv6 address.
    :param address:
    :return: bool
    """
    try:
        socket.inet_pton(socket.AF_INET6, address)
        return True
    except socket.error:
        return False


def check_ipv4(address: str) -> bool:
    """
    Check if the address is a valid IPv4 address.
    :param address:
    :return: bool
    """
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False


def check_path(path: str) -> bool:
    """
    Check if the path is a valid path.
    :param path:
    :return: bool
    """
    if re.match(r'(\${[a-zA-Z_][a-zA-Z0-9_]*}|\$[a-zA-Z_][a-zA-Z0-9_]*|\/.*)'
                r'(/\${[a-zA-Z_][a-zA-Z0-9_]*}|/\$[a-zA-Z_][a-zA-Z0-9_]*|\/.*)*', path):
        return True
    else:
        return False


def check_path_group(path: str) -> bool:
    """
    Check if the path is a valid path group.
    :param path:
    :return: bcol

    WARNING: This function might conflict with `check_path`, since we cannot check if there are colons(:) in the path.
    """
    if path.find(':') == -1:
        return False
    path_list = path.split(':')
    for item in path_list:
        if not check_path(item):
            return False
    return True


def recognize_type(name: str) -> str:
    """
    Recognize the type of the environment variable.
    :param name:
    :return: type string
    """
    if check_ipv4(name):
        return "ipv4"
    if check_ipv6(name):
        return "ipv6"
    if check_path_group(name):
        return "path_group"
    if check_path(name):
        return "path"
    return "undefined"


def get_from_vim(initial_message: str) -> str:
    """
    Get the value from vim.
    :param initial_message:
    :return:
    """

    editor_name = os.environ.get('EDITOR', 'vim')

    with tempfile.NamedTemporaryFile(suffix=".enview_tmp") as tf:
        tf.write(initial_message.encode())
        tf.flush()
        subprocess.call([editor_name, tf.name])
        tf.seek(0)
        edited_message = tf.read().decode()
        return edited_message
    return ""


def get_environment_vars():
    """
    Get all environment variables.
    :return: env_vars
    """
    env_vars = os.environ.copy()
    env_vars.update(os.environ.copy())
    return env_vars


def compress_str(origin_str: str, width: int) -> str:
    """
    Compress a string to a specific width.
    :param origin_str:
    :param width:
    :return: if the length of the string is less than the width, fill space to the end of the string. Otherwise,
    compress the origin string.
    """
    if len(origin_str) <= width:
        return origin_str + " " * (width - len(origin_str))
    else:
        return origin_str[:width - 3] + "..."


def print_env_list(position=0, selected=0):
    """
    Print environment variables.
    :param position:
    :param selected:
    :return: Updated position and selected.
    """
    env_vars = get_environment_vars()
    rows, columns = os.popen('stty size', 'r').read().split()
    rows = int(rows) - 1
    columns = int(columns)
    name_width = int((columns - 3) * 0.4)
    value_width = (columns - 3) - name_width
    env_list = list(env_vars.items())
    # position bound:
    # row position range = [position, position + rows - 5]
    position_bound = position + rows - 5

    # console window is too small
    if columns < 5:
        return 0

    # prevent out of range
    if selected < 0:
        selected = 0
    if selected >= len(env_vars.keys()):
        selected = len(env_vars.keys()) - 1

    # slide window
    if selected < position:
        position = selected
        position_bound = position + rows - 5
    if selected > position_bound:
        position_bound = selected
        position = position_bound - rows + 5

    boundary_str = "+" + "-" * name_width + "+" + "-" * value_width + "+"
    cprint(boundary_str, 'green')
    cprint("| " + compress_str("Name", name_width - 2) + " | " + compress_str("Value", value_width - 2) + " |", 'green')
    cprint(boundary_str, 'green')

    # print environment variables
    for index in range(position, min(len(env_list), position_bound + 1)):
        key = env_list[index][0]
        value = repr(env_list[index][1])[1:-1]
        cprint("| ", 'green', end="")
        if index != selected:
            cprint(compress_str(key, name_width - 2), 'yellow', end="")
            cprint(" | ", 'green', end="")
            cprint(compress_str(value, value_width - 2), 'yellow', end="")
        else:
            name_str = compress_str(key, name_width - 2)
            name_str = f'{bcolors.WHITE}{name_str}{bcolors.ENDC}'
            value_str = compress_str(value, value_width - 2)
            value_str = f'{bcolors.WHITE}{value_str}{bcolors.ENDC}'
            print(name_str, end="")
            cprint(" | ", 'green', end="")
            print(value_str, end="")
        cprint(" |", 'green')

    cprint(boundary_str, 'green')
    return position, selected


def edit_mode(selected):
    """
    Edit the environment variable.
    :param selected:
    :return:
    """
    os.system('clear')
    env_vars = get_environment_vars()
    env_list = list(env_vars.items())
    key = env_list[selected][0]
    value = env_list[selected][1]
    # Without vim editor mode:
    # print(f"{bcolors.OKGREEN}Current value: {bcolors.ENDC}\n{bcolors.OKBLUE}{value}{bcolors.ENDC}")
    # new_value = input(f"{bcolors.OKGREEN}New value: \n{bcolors.ENDC}")
    new_value = get_from_vim(value)
    env_vars[key] = new_value
    os.environ.update(env_vars)
    return True


def edit_ipv4(selected):
    """
    Edit the environment variable.
    :param selected:
    :return:
    """
    os.system('clear')
    env_vars = get_environment_vars()
    env_list = list(env_vars.items())
    key = env_list[selected][0]
    value = env_list[selected][1]
    print(f"{bcolors.OKGREEN}Current value: {bcolors.ENDC}\n{bcolors.OKBLUE}{value}{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Suggested type: {bcolors.ENDC}\n{bcolors.FAIL}IPV4{bcolors.ENDC}")
    new_value = input(f"{bcolors.OKGREEN}New value: \n{bcolors.ENDC}")
    if check_ipv4(new_value):
        env_vars[key] = new_value
        os.environ.update(env_vars)
        return selected
    else:
        print(f"{bcolors.FAIL}Invalid IPv4 address.{bcolors.ENDC}")
        return selected


def edit_ipv6(selected):
    """
    Edit the environment variables
    :param selected:
    :return:
    """
    os.system('clear')
    env_vars = get_environment_vars()
    env_list = list(env_vars.items())
    key = env_list[selected][0]
    value = env_list[selected][1]
    print(f"{bcolors.OKGREEN}Current value: {bcolors.ENDC}\n{bcolors.OKBLUE}{value}{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Suggested type: {bcolors.ENDC}\n{bcolors.FAIL}IPV6{bcolors.ENDC}")
    new_value = input(f"{bcolors.OKGREEN}New value: \n{bcolors.ENDC}")
    if check_ipv6(new_value):
        env_vars[key] = new_value
        os.environ.update(env_vars)
        return selected
    else:
        print(f"{bcolors.FAIL}Invalid IPv6 address.{bcolors.ENDC}")
        return selected


def edit_path(selected):
    """
    Edit the environment variables
    :param selected:
    :return:
    """
    os.system('clear')
    env_vars = get_environment_vars()
    env_list = list(env_vars.items())
    key = env_list[selected][0]
    value = env_list[selected][1]
    print(f"{bcolors.OKGREEN}Current value: {bcolors.ENDC}\n{bcolors.OKBLUE}{value}{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Suggested type: {bcolors.ENDC}\n{bcolors.FAIL}PATH{bcolors.ENDC}")
    new_value = input(f"{bcolors.OKGREEN}New value: \n{bcolors.ENDC}")
    if check_path(new_value):
        env_vars[key] = new_value
        os.environ.update(env_vars)
        return selected
    else:
        print(f"{bcolors.FAIL}Invalid path.{bcolors.ENDC}")
        return selected


def print_path_list(path_list, position=0, selected=0):
    """
    Print the list of paths
    :param path_list:
    :param position:
    :param selected:
    :return:
    """
    rows, columns = os.popen('stty size', 'r').read().split()
    rows = int(rows) - 3  # 3 for the header
    columns = int(columns)

    if selected < 0:
        selected = 0
    if selected > len(path_list) - 1:
        selected = len(path_list) - 1

    position_bound = position + rows - 1
    if selected < position:
        position = selected
        position_bound = position + rows - 1
    if selected > position_bound:
        position_bound = selected
        position = position_bound - rows + 1

    for index in range(position, min(len(path_list), position_bound + 1)):
        if index == selected:
            cprint(compress_str(path_list[index], columns), 'red')
        else:
            cprint(compress_str(path_list[index], columns), 'yellow')

    return position, selected


def edit_path_group(selected):
    """
    Edit the environment variables
    :param selected:
    :return:
    """
    env_vars = get_environment_vars()
    env_list = list(env_vars.items())
    key = env_list[selected][0]
    value = env_list[selected][1]
    selected_path_index = 0
    path_position = 0
    path_list = value.split(":")

    os.system('clear')
    print(f"{bcolors.OKGREEN}Current value: {bcolors.ENDC}")
    print(f"Move with \"ws\" or \"jk\". Add to rear with \"a\". Add to front with \"A\". Change order with \"-=\".")
    print(f"Edit path with \"e\". Remove path with \"r\". Quit with \"q\".")
    print_path_list(path_list)

    while info := readchar.readchar():
        if info == 'q':
            break
        elif info == 's' or info == 'j':
            selected_path_index += 1
        elif info == 'w' or info == 'k':
            selected_path_index -= 1
        elif info == 'a':
            new_path = get_from_vim()
            if check_path(new_path):
                path_list.append(new_path)
        elif info == 'A':
            new_path = get_from_vim()
            if check_path(new_path):
                path_list.insert(0, new_path)
            selected_path_index += 1
        elif info == '+' or info == '=':
            if selected_path_index < len(path_list) - 1:
                selected_path_index += 1
                path_list[selected_path_index], path_list[selected_path_index - 1] = \
                    path_list[selected_path_index - 1], path_list[selected_path_index]
        elif info == '-':
            if selected_path_index > 0:
                selected_path_index -= 1
                path_list[selected_path_index], path_list[selected_path_index + 1] = \
                    path_list[selected_path_index + 1], path_list[selected_path_index]
        elif info == 'r':
            if len(path_list) >= 1:
                path_list.pop(selected_path_index)
        elif info == 'e':
            new_path = get_from_vim(path_list[selected_path_index])
            path_list[selected_path_index] = new_path

        os.system('clear')
        print(f"{bcolors.OKGREEN}Current value: {bcolors.ENDC}")
        print(f"Move with \"ws\" or \"jk\". Add to rear with \"a\". Add to front with \"A\". Change order with \"-=\".")
        print(f"Edit path with \"e\". Remove path with \"r\". Quit with \"q\".")
        path_position, selected_path_index = print_path_list(path_list=path_list,
                                                             position=path_position,
                                                             selected=selected_path_index)
        # print(f"position = {path_position}, index = {selected_path_index}")

    new_path_group = ":".join(path_list)
    print(new_path_group)
    env_vars[key] = new_path_group
    os.environ.update(env_vars)


def intelligent_edit_mode(selected):
    """
    Intelligent edit mode.
    :param selected:
    :return:
    """
    os.system('clear')
    env_vars = get_environment_vars()
    env_list = list(env_vars.items())
    key = env_list[selected][0]
    value = env_list[selected][1]
    vartype = recognize_type(value)
    if vartype == "undefined":
        edit_mode(selected)
    elif vartype == "ipv4":
        edit_ipv4(selected)
    elif vartype == "ipv6":
        edit_ipv6(selected)
    elif vartype == "path":
        edit_path(selected)
    elif vartype == "path_group":
        edit_path_group(selected)


@command("getall")
def getall():
    """
    Get all environment variables.
    """
    env_dict = get_environment_vars()
    for key, value in env_dict.items():
        cprint(key, 'green', end="")
        cprint(" = ", 'red', end="")
        cprint(value, 'yellow', end="\n")
    return 0


@command("edit")
def select():
    """
    Select environment variables.
    Move with "ws" or "jk" keys.
    Edit with "e"
    Goto with "g", "G" or ":[number]"
    Search with "/" and move with "nN"
    quit with "q"
    """
    os.system('clear')
    position = 0
    selected = 0
    print_env_list()
    search_list = []
    search_index = 0
    while info := readchar.readchar():
        if info == 's' or info == 'j':
            # move down
            selected += 1
        elif info == 'w' or info == 'k':
            # move up
            selected -= 1
        elif info == 'q':
            # quit
            break
        elif info == 'g':
            # move to the beginning
            selected = 0
        elif info == 'G':
            # move to the end
            selected = len(get_environment_vars()) - 1
        elif info == ":":
            # move to a specific line
            move_postion = int(input())
            if move_postion < 0:
                move_postion = 0
            if move_postion > len(get_environment_vars()):
                move_postion = len(get_environment_vars())
            selected = move_postion
        elif info == '/':
            # search
            search_str = input()
            found_flag = False
            for index, (key, value) in enumerate(get_environment_vars().items()):
                if search_str.lower() in key.lower():
                    selected = index
                    search_list.append(index)
                    found_flag = True
            if found_flag:
                search_index = 0
                selected = search_list[0]
        elif info == 'n':
            # search next
            if search_index < len(search_list) - 1:
                search_index += 1
                selected = search_list[search_index]
        elif info == 'N':
            # search previous
            if search_index > 0:
                search_index -= 1
                selected = search_list[search_index]
        elif info == 'e':
            edit_mode(selected)
        elif info == 'i':
            intelligent_edit_mode(selected)

        os.system('clear')
        position, selected = print_env_list(position=position, selected=selected)

    os.system('clear')


@command("save")
def save():
    """
    Save environment variables.
    """
    filename = input("Save file name: (Default: env.txt)\n").strip()
    if filename == "":
        filename = "env.txt"
    if os.path.exists(filename):
        print("File already exists. Overwrite? ([y]/n)")
        flag = input().strip().lower()
        if flag == "n":
            return 0

    with open(filename, "w") as f:
        for key, value in get_environment_vars().items():
            f.write(f"export {key}=\"{repr(value)[1:-1]}\"\n")
    return 0


@command("setenv")
@argument("name", type=str)
def setenv(name: str, value: str):
    """
    Set environment variable.
    """
    os.environ[name] = value
    return 0


@command("clip")
def clip():
    """
    clip all the variables to the clipboard.
    """
    clipstr = ""
    for key, value in get_environment_vars().items():
        clipstr += f"export {key}=\"{repr(value)[1:-1]}\"\n"
    pyperclip.copy(clipstr)
    return 0
