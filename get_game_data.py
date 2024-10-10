import os
import json
import shutil
from subprocess import PIPE, run
import sys


# Variables that specifies what we are looking for in our directories
GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]


# Find all files and match any directories that have "game" in them
def find_all_game_paths(source):

    game_paths = []

    # Walk recursively through source directory passed into os.walk()
    for root, dirs, files in os.walk(source):
        # Since we only care about the top level directory, just run once
        for directory in dirs:
            # Get name of directory and match against GAME_DIR_PATTERN
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)

        break

    return game_paths


def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        # Split path into dir and base part
        _, dir_name = os.path.split(path)
        # Remove game aspect
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names


# Checks if the dir exists. If not then create, otherwise don't create
def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


# Copy source into destination
def copy_and_overwrite(source, dest):
    # Recursive copy
    if os.path.exists(dest):
        # Remove destination folder
        shutil.rmtree(dest)
    shutil.copytree(source, dest)


def make_json_metadata_file(path, game_dirs):
    # Data to be written to JSON file
    data = {"gameNames": game_dirs, "numberOfGames": len(game_dirs)}

    with open(path, "w") as f:
        json.dump(data, f)


def compile_game_code(path):
    # Determine name of file we want to compile
    code_file_name = None
    # Loop through all files
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break

        break

    # Make sure that we did have a code file
    if code_file_name is None:
        return

    # Otherwise, compile the file
    command = GAME_COMPILE_COMMAND + [code_file_name]
    run_command(command, path)


def run_command(command, path):
    cwd = os.getcwd()
    # Change working directory into this path
    os.chdir(path)

    # Run command
    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print("compile results", result)

    # Change directory back to cwd we were in before we changed directories
    os.chdir(cwd)


# Source is where we are looking, target is where we want to put our new directory
def main(source, target):
    # Need to create a complete path from location of python file
    # to whatever the directory is

    # current working directory we ran the .py file from
    cwd = os.getcwd()

    # create paths
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    print(game_paths)

    new_game_dirs = get_name_from_paths(game_paths, "_game")
    print(new_game_dirs)

    create_dir(target_path)

    # Perform copy operation
    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)

    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)


# Parse out command line arguments
if __name__ == "__main__":
    # Grab command line arguments here
    args = sys.argv

    # $ python3 get_game_data.py data new_data
    # $ ['get_game_data.py', 'data', 'new_data']
    print(args)

    # Make sure we have a valid number of arguments
    # For example: file name and 2 extra arguments
    # $ python3 get_game_data.py data
    # $ Exception: You must pass a source and target directory - only.
    if len(args) != 3:
        raise Exception("You must pass a source and target directory - only.")

    source, target = args[1:]
    main(source, target)
