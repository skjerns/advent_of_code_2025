import csv
import glob
import re
import os
import subprocess
import sys
import time
from pathlib import Path
from urllib import request

# Configuration
CSV_FILE = Path('benchmarks.csv')
README_FILE = Path('README.md')
# The year for Advent of Code, set to 2025 as per the original script's URL
AOC_YEAR = 2025


def get_day_title(day):
    """
    Fetches the title for an Advent of Code day from the website.

    Parameters
    ----------
    day : int
        The day number (1-25).

    Returns
    -------
    str
        The day title, or an empty string if retrieval fails.
    """
    try:
        url = f"https://adventofcode.com/{AOC_YEAR}/day/{day}"
        with request.urlopen(url) as response:
            if response.status != 200:
                return ""
            html = response.read().decode("utf-8")
            match = re.search(r"<h2>--- Day \d+: (.*) ---</h2>", html)
            if match:
                return match.group(1).strip()
    except Exception:
        pass
    return ""


def get_cell_code(script_path, part):
    """
    Extracts the code for a specific part cell from a Python script.

    Parameters
    ----------
    script_path : str
        Path to the Python script.
    part : int
        The part number (1 or 2).

    Returns
    -------
    str
        The extracted code cell content.
    """
    with open(script_path, 'r') as f:
        lines = f.readlines()

    cell_lines = []
    in_cell = False
    for line in lines:
        if line.strip() == f'#%% part {part}':
            in_cell = True
            continue
        elif line.strip().startswith('#%%'):
            in_cell = False
            continue

        if in_cell:
            cell_lines.append(line)

    return "".join(cell_lines)

def time_script_part(script_path, part):
    """
    Executes a script and times the execution of a specific part cell.

    Parameters
    ----------
    script_path : str
        Path to the Python script.
    part : int
        The part number (1 or 2).

    Returns
    -------
    float or None
        The execution time in seconds, or None if the cell is not found.
    """
    with open(script_path, 'r') as f:
        script_code = f.read()

    cell_code = get_cell_code(script_path, part)

    if not cell_code:
        return None

    # Inject timing code into the cell content
    timing_injection = (
        f"import time\n"
        f"start_time = time.time()\n"
        f"{cell_code}\n"
        f"end_time = time.time()\n"
        f"print(f'--execution-time--{{end_time - start_time}}')"
    )

    # Replace the original cell code with the timed version

    modified_script = script_code.replace(
        cell_code,
        timing_injection
    )
    modified_script = f'__file__ = "{script_path}"\n' +  modified_script

    # Run the modified script using the python interpreter
    process = subprocess.run(
        [sys.executable, '-c', modified_script],
        capture_output=True,
        text=True
    )

    output = process.stdout
    if not output:
        raise Exception(f'error benchmarking {script_path}: {process.stderr}')
    for line in output.split('\n'):
        if line.startswith('--execution-time--'):
            try:
                ttime = float(line.split('--')[-1])
                print(f'-- {os.path.basename(script_path)}:{part} - {ttime:.4f}')
                return ttime
            except ValueError as e:
                print(f'error benchmarking {e}')
                return None
    return None

def format_time(seconds):
    """
    Formats a time duration into a human-readable string.

    Parameters
    ----------
    seconds : float or None
        The time in seconds.

    Returns
    -------
    str
        The formatted time string.
    """
    if seconds is None:
        return "N/A"
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    if seconds > 60:
        minutes = int(seconds / 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes}m {remaining_seconds:02d}s"
    return f"{seconds:.2f}s"

def load_benchmarks():
    """
    Loads benchmark results from the CSV file.

    Returns
    -------
    dict
        A dictionary mapping day number (int) to a dict of results.
    """
    results = {}
    if not CSV_FILE.exists():
        return results

    print(f"Loading results from {CSV_FILE}...")
    try:
        with open(CSV_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    day = int(row['Day'])
                    results[day] = {
                        'part1': row['Part 1'],
                        'part2': row['Part 2']
                    }
                except ValueError:
                    # Skip invalid rows
                    continue
    except Exception as e:
        print(f"Error loading CSV: {e}. Recalculating all days.")
        return {} # Treat as missing if corrupted
    return results

def save_benchmarks(results):
    """
    Saves benchmark results to the CSV file.

    Parameters
    ----------
    results : dict
        The results dictionary to save.
    """
    print(f"Saving results to {CSV_FILE}...")
    try:
        with open(CSV_FILE, 'w', newline='') as f:
            fieldnames = ['Day', 'Part 1', 'Part 2']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for day in sorted(results.keys()):
                writer.writerow({
                    'Day': day,
                    'Part 1': results[day]['part1'],
                    'Part 2': results[day]['part2']
                })
    except Exception as e:
        print(f"Error saving CSV: {e}")

def main():
    if README_FILE.exists():
        README_FILE.unlink()
        print(f"Removed existing {README_FILE} to force refresh.")

    # 1. Load existing benchmarks
    existing_results = load_benchmarks()
    # Deep copy to track changes and avoid modifying the loaded data directly
    results = dict(existing_results)

    day_scripts = sorted(glob.glob('day*.py'))

    # 2. Identify and benchmark missing days
    days_to_benchmark = []

    # Check if we need to recalculate all days (CSV was missing/corrupt)
    if not existing_results:
        print("CSV file missing or empty. Benchmarking all found days.")
        days_to_benchmark = [int(Path(s).stem.replace('day', '')) for s in day_scripts]
    else:
        # Benchmark only days not present in the loaded results
        for script_path in day_scripts:
            day = int(Path(script_path).stem.replace('day', ''))
            if day not in existing_results:
                days_to_benchmark.append(day)

    if not days_to_benchmark and existing_results:
        print("No new days to benchmark. Using existing results.")

    days_benchmarked = 0
    for script_path in day_scripts:
        day = int(Path(script_path).stem.replace('day', ''))

        if day in days_to_benchmark:
            print(f"Benchmarking Day {day:02d}...")
            part1_time = time_script_part(script_path, 1)
            part2_time = time_script_part(script_path, 2)
            results[day] = {
                'part1': format_time(part1_time),
                'part2': format_time(part2_time)
            }

            days_benchmarked += 1
            # Simple rate limit to avoid overwhelming AOC server if titles are fetched
            time.sleep(0.5)

    # 3. Save updated results to CSV
    if days_benchmarked > 0:
        save_benchmarks(results)
    elif not existing_results and days_benchmarked == 0:
        print("No days found to benchmark. Skipping CSV save.")

    # 4. Generate README
    if results:
        print(f"Fetching titles and generating {README_FILE}...")
        sorted_days = sorted(results.keys())
        with open(README_FILE, 'w') as f:
            f.write(f'# Advent of Code {AOC_YEAR}\n\n')
            f.write('Benchmark runtimes per day\n\n')
            f.write('| Day | Part 1 | Part 2 |\n')
            f.write('|---|---|---|\n')

            for day in sorted_days:
                result = results[day]
                title = get_day_title(day)
                day_str = f"{day:02d}"
                if title:
                    day_str += f" - {title}"

                script_name = f'day{day:02d}.py'
                f.write(f'| [{day_str}]({script_name}) | {result["part1"]} | {result["part2"]} |\n')

                # Rate limit for title fetching from AOC
                time.sleep(0.1)
    else:
        print("No results to generate README.md.")

if __name__ == '__main__':
    main()
