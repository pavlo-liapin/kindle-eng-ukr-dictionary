import os
import subprocess
import shutil

# List of scripts to execute
scripts = [
    "00.sanitize.py",
    "01.crosslinks.py",
    "02.varcon-csv.py",
    "03.variants.py",
    "04.irregular-nouns.py",
    "05.filter-irregular-nouns.py",
    "06.regular-nouns.py",
    "07.adjectives.py",
    "08.filter-irregular-verbs.py",
    "09.irregular-verbs.py",
    "10.regular-verbs.py",
    "11.all-inflections.py",
    "12.clean-markup.py",
    "13.convert-to-xhtml.py",
]

# Mapping of scripts to specific validation output files
validation_mapping = {
    "00.sanitize.py": "temp/00.sanitize.txt",
    "01.crosslinks.py": "temp/01.crosslinks.txt",
    "03.variants.py": "temp/03.british-american-variants.txt",
    "05.filter-irregular-nouns.py": "temp/05.filter-irregular-nouns.txt",
    "08.filter-irregular-verbs.py": "temp/08.filter-irregular-verbs.txt",
    "11.all-inflections.py": "temp/11.all-inflections.txt",
    "12.clean-markup.py": "temp/12.clean-markup.txt",
}

# Colorful ASCII header and footer
HEADER = """
\033[1;36m
Preparing a dictionary...
\033[0m
"""

FOOTER = """
\033[1;32m
Finished!
\033[0m
"""

TEMP_DIR = "temp/"


def create_temp_directory():
    """Create the temp/ directory if it does not exist."""
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        print(f"\033[1;33mCreated directory: {TEMP_DIR}\033[0m")


def delete_temp_directory():
    """Delete the temp/ directory."""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        print(f"\033[1;33mDeleted directory: {TEMP_DIR}\033[0m")


def run_script(script_name):
    """Run a Python script located in the scripts/ directory and capture the output."""
    try:
        script_path = os.path.join("scripts", script_name)
        print(f"\033[1;34mRunning {script_path}...\033[0m")
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\033[1;31mError while running {script_name}: {e}\033[0m")
        return False
    return True


def run_validation_script(output_file):
    """Run the validation script with the specified output file as an argument."""
    try:
        print(f"\033[1;34mValidating {output_file}...\033[0m")
        subprocess.run(["python", "validate.py", output_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\033[1;31mError while validating {output_file}: {e}\033[0m")
        return False
    return True


def count_lines_and_words(filename):
    """Count the number of lines and words in the first column of a file."""
    try:
        line_count = 0
        word_count = 0

        with open(filename, 'r') as file:
            for line in file:
                line_count += 1
                columns = line.strip().split('\t')
                if columns and columns[0]:
                    words = columns[0].split('|')
                    word_count += len(words)

        print(f"\033[1;32mLines in file: {line_count}\033[0m")
        print(f"\033[1;32mWords in dictionary: {word_count}\033[0m")
    except FileNotFoundError:
        print(f"\033[1;31mError: File '{filename}' not found.\033[0m")
    except Exception as e:
        print(f"\033[1;31mAn error occurred: {e}\033[0m")


def main():
    print(HEADER)

    # Create the temp/ directory at the beginning
    create_temp_directory()

    try:
        for script in scripts:
            if not run_script(script):
                break  # Stop execution if a script fails

            # Run validation if the script has a corresponding output file
            if script in validation_mapping:
                output_file = validation_mapping[script]
                count_lines_and_words(output_file)  # Print lines and words count
                if not run_validation_script(output_file):
                    break
    finally:
        # Delete the temp/ directory at the end
        delete_temp_directory()

    print(FOOTER)


if __name__ == "__main__":
    main()