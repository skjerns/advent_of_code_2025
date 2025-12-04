import requests
import joblib
import numpy as np

mem = joblib.Memory('.')
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
with open('session', 'r') as f:
    SESSION_COOKIE = f.read().strip()  # Replace with your session cookie

#%% functions
def get_lines(day, year=YEAR, session_cookie=SESSION_COOKIE):
    return get_input(day, year, session_cookie).split('\n')

def get_matrix(day, year=YEAR, session_cookie=SESSION_COOKIE, dtype=None):
    lines = get_lines(day, year, session_cookie)
    return lines2matrix(lines)

def input2matrix(string, dtype=None):
    return lines2matrix(string.split('\n'), dtype=dtype)

def lines2matrix(lines, dtype=None):
    return np.array([list(line) for line in lines], dtype=dtype)



@mem.cache
def get_input(day, year=YEAR, session_cookie=SESSION_COOKIE):
    """
    Downloads the puzzle input for a specific day from Advent of Code.

    Args:
        day (int): The day of the puzzle (1-25).
        year (int): The year of the Advent of Code event.
        session_cookie (str): Your session cookie for authentication.

    Returns:
        str: The puzzle input as a string.
    """
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
