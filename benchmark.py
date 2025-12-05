import glob
import subprocess
import sys
import time
from pathlib import Path

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
            for line in f:
                if not line.strip().startswith('|'):
                    continue
                parts = [p.strip() for p in line.strip().split('|')]
                if len(parts) >= 5 and parts[1].isdigit():
                    day = int(parts[1])
                    part1_str = parts[2]
                    part2_str = parts[3]
                    results[day] = {'part1': part1_str, 'part2': part2_str}

    day_scripts = sorted(glob.glob('day*.py'))
    new_days_benchmarked = False
    for script_path in day_scripts:
        day = int(Path(script_path).stem.replace('day', ''))

        if day in results and not reset_flag:
            continue

        new_days_benchmarked = True
        print(f"Benchmarking Day {day:02d}...")
        part1_time = time_script_part(script_path, 1)
        part2_time = time_script_part(script_path, 2)

        results[day] = {
            'part1': format_time(part1_time),
            'part2': format_time(part2_time)
        }

    if not new_days_benchmarked and not reset_flag:
        print("No new days to benchmark.")
        return

    # Generate README.md
    sorted_days = sorted(results.keys())
    with open('README.md', 'w') as f:
        f.write('# Advent of Code 2025\n')
        f.write('# Here are the benchmarks per day\n')
        f.write('| Day | Part 1 | Part 2 |\n')
        f.write('|---|---|---|\n')
        for day in sorted_days:
            result = results[day]
            f.write(f'| {day:02d} | {result["part1"]} | {result["part2"]} |\n')

if __name__ == '__main__':
    main()
