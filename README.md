# enview

Enview (environment viewer) is a simple, fast, and powerful environment viewer (and editor).

![show](resources/show.gif)

## OS Surpport
It now supports Linux and Windows.

## Dependencies
- Python (`>=3.8`)

## Installation

```bash
pip install .
```

## Usage

```bash
enview
```
- getall: Display all the environment variables.
- edit: Display all the environment variables in a neat way. You can select any variable you like to edit. 
    - Move up with keys 'w' or 'k'. Move down with keys 's' or 'j'. 
    - Go to the top and bottom with keys 'g' and 'G', respectively.
    - Go to the environment variable according to its position in the list by ":[number]".
    - Search for variables with "/". For next or prior result, press 'n' or 'N' respectively.
    - Edit with 'e'.
    - Edit in intelligent mode with 'i'.
- conflict: Check if there is any conflict between the environment variables and the current environment variables. Argument ['varname'] is required.
- optimize: Remove the duplicates in path group. 
- setenv: Set the value of a specified environment variable. Arguments ['value', 'name'] are required.
- clip: Clip all the environment variables to the clipboard.
- save: Save all the environment variables in the format "export name=value" to the current directory. The default file name is "env.txt"(Press enter when prompted).
- Exit the program with 'quit', 'q' or 'exit'.
- For more information, use 'help' command.

