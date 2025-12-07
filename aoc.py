import requests
import joblib
import numpy as np
import inspect
import re
import os
import datetime
import warnings

mem = joblib.Memory('./joblib')
#%% things that are often used

step = {'^': [-1, 0],
                '>': [0, 1],
                'v': [1, 0],
                '<': [0, -1],
                0: [-1, 0],
                1: [0, 1],
                2: [1, 0],
                3: [0, -1]}
dir2int =  {'^': 0,
            '>': 1,
            'v': 2,
            '<': 3}

turn_clock = {'^': '>',
         '>': 'v',
         'v': '<',
         '<': '^',
         0: 1,
         1: 2,
         2: 3,
         4: 0}

turn_counter = {'^': '<',
                 '>': '^',
                 'v': '>',
                 '<': 'v'}

#%% Constants
AOC_URL = "https://adventofcode.com"

YEAR = 2025  # Change this to the desired year

if YEAR!=(curr_year:=datetime.datetime.now().year):
    warnings.warn(f'year is set to {YEAR}, but today is {curr_year=}')

with open('session', 'r') as f:
    SESSION_COOKIE = f.read().strip()  # Replace with your session cookie

#%% functions
def get_lines(day=None, filename=None, year=YEAR, session_cookie=SESSION_COOKIE):
    return get_input(day, filename, year, session_cookie).split('\n')

def get_matrix(day=None, filename=None, year=YEAR, session_cookie=SESSION_COOKIE, dtype=None):
    lines = get_lines(day, filename, year, session_cookie)
    return lines2matrix(lines)

def input2matrix(string, dtype=None):
    return lines2matrix(string.split('\n'), dtype=dtype)

def lines2matrix(lines, dtype=None):
    return np.array([list(line) for line in lines], dtype=dtype)

@mem.cache
def get_example(day=None, filename=None, year=YEAR):
    """
    Downloads the puzzle description page and extracts the first code example.

    Args:
        day (int, optional): The day of the puzzle. Infers from caller if None.
        filename (str, optional): Script filename to infer day from.
        year (int): The event year.

    Returns:
        str: The extracted example text.
    """
    # Infer day if needed
    if day is None:
        f = filename if filename else inspect.stack()[1].filename
        day = int(re.search(r'day(\d{1,2})\.py$', os.path.basename(f), re.IGNORECASE).group(1))

    # Fetch page
    url = f"{AOC_URL}/{year}/day/{day}"
    response = requests.get(url, cookies={"session": SESSION_COOKIE})
    response.raise_for_status()

    # Extract first <pre><code>...</code></pre> block using DOTALL to match newlines
    match = re.search(r'<pre><code>(.*?)</code></pre>', response.text, re.DOTALL)

    if match:
        return match.group(1).strip()

    raise ValueError(f"No example code block found for Day {day}.")


@mem.cache
def get_input(day=None, filename=None, year=YEAR, session_cookie=SESSION_COOKIE):
    """
    Downloads the puzzle input for a specific day from Advent of Code.

    Requires either 'day' to be provided (int 1-25) or 'filename' to be
    provided (str, e.g., 'day01.py') or inferred from the calling script.

    Args:
        day (int, optional): The day of the puzzle (1-25).
        filename (str, optional): The filename to infer the day from.
                                  Defaults to None, which attempts to infer
                                  from the caller script.
        year (int): The year of the Advent of Code event.
        session_cookie (str): Your session cookie for authentication.

    Returns:
        str: The puzzle input as a string.
    """
    # Assert XOR condition: Only one of 'day' or 'filename' (or neither, if inferring) can be set.
    # Note: If day=None and filename=None, it proceeds to infer from the caller script.
    if day is not None and filename is not None:
        raise ValueError("Cannot supply both 'day' and 'filename'.")

    # Infer Day from Filename (either provided or from caller script)
    if day is None:
        basename = os.path.basename(filename)
        match = re.search(r'day(\d{1,2})\.py$', basename, re.IGNORECASE)
        # Extract day number: e.g., 'day01.py' -> '01' -> 1
        day = int(match.group(1))

    # Validate day
    day = int(day)
    if not (1 <= day <= 25):
        raise ValueError("Day must be between 1 and 25.")

    # Construct the URL for the puzzle input
    url = f"{AOC_URL}/{year}/day/{day}/input"

    # Set up cookies for authentication
    cookies = {"session": session_cookie}

    # Make the request
    response = requests.get(url, cookies=cookies)

    # Check for errors
    if response.status_code == 200:
        print(f"Successfully downloaded input for Day {day}, {year}.")
        return response.text.strip()
    elif response.status_code == 404:
        raise Exception(f"Puzzle for Day {day}, {year} is not available yet.")
    else:
        raise Exception(f"Failed to fetch puzzle input: {response.status_code} - {response.reason}")

def print_matrix(matrix):
    lines = '\n'.join([''.join(r) for r in matrix])
    print(lines)
    return
