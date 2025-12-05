import glob
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib import request


def get_day_title(day):
    try:
        with request.urlopen(f"https://adventofcode.com/2025/day/{day}") as response:
            if response.status != 200:
                return ""
            html = response.read().decode("utf-8")
            match = re.search(r"<h2>--- Day \d+: (.*) ---</h2>", html)
            if match:
                return match.group(1).strip()
    except Exception:
        return ""
    return ""


def get_cell_code(script_path, part):
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
    script_code = ""
    with open(script_path, 'r') as f:
        script_code = f.read()

    cell_code = get_cell_code(script_path, part)

    if not cell_code:
        return None

    # We need to run the whole script, but time only the cell
    # A bit tricky without modifying the original script.
    # Let's try to inject timing code.

    modified_script = script_code.replace(
        cell_code,
        f"import time\nstart_time = time.time()\n{cell_code}\nend_time = time.time()\nprint(f'--execution-time--{{end_time - start_time}}')"
    )

    process = subprocess.run(
        ['python', '-c', modified_script],
        capture_output=True,
        text=True
    )

    output = process.stdout
    for line in output.split('\n'):
        if line.startswith('--execution-time--'):
            return float(line.split('--')[-1])
    return None

def format_time(seconds):
    if seconds is None:
        return "N/A"
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    if seconds > 60:
        minutes = int(seconds / 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes}m {remaining_seconds:02d}s"
    return f"{seconds:.2f}s"

def main():
    reset_flag = '--reset' in sys.argv or 'reset' in sys.argv

    results = {}
    if Path('README.md').exists() and not reset_flag:
        with open('README.md', 'r') as f:
            # Regex to capture day, part1, and part2 from the markdown table
            # Supports both old format `| 01 | ...` and new format `| [01 - ...] | ...`
            pattern = r"\| (?:\[(?P<day1>\d+)[^\]]*\]|(?P<day2>\d+)) \| (?P<part1>[^|]+) \| (?P<part2>[^|]+) \|"
            for line in f:
                match = re.search(pattern, line)
                if match:
                    day = int(match.group('day1') or match.group('day2'))
                    results[day] = {
                        'part1': match.group('part1').strip(),
                        'part2': match.group('part2').strip()
                    }

    day_scripts = sorted(glob.glob('day*.py'))
    new_days_benchmarked = False
    for script_path in day_scripts:
        day = int(Path(script_path).stem.replace('day', ''))

        # If day is not in results, or if reset flag is present, benchmark it
        if day not in results or reset_flag:
            new_days_benchmarked = True
            print(f"Benchmarking Day {day:02d}...")
            part1_time = time_script_part(script_path, 1)
            part2_time = time_script_part(script_path, 2)
            results[day] = {
                'part1': format_time(part1_time),
                'part2': format_time(part2_time)
            }

    if not new_days_benchmarked and not reset_flag:
        print("No new days to benchmark. Checking for title/format updates.")

    # Fetch titles and generate new README
    print("Fetching titles and generating README.md...")
    sorted_days = sorted(results.keys())
    with open('README.md', 'w') as f:
        f.write('# Advent of Code 2025\n\n')
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

if __name__ == '__main__':
    main()
