import re
import csv
from collections import defaultdict, OrderedDict

def process_file(input_path, csv_output_path):
    """
    Process the input file to merge singular and plural forms into unified entries,
    and write the singular and plural forms into a CSV file.
    Args:
        input_path (str): Path to the input file.
        csv_output_path (str): Path to the CSV output file.
    """
    # Dictionary to store relationships and values
    key_groups = defaultdict(list)
    singular_positions = OrderedDict()  # To track singular positions for output order

    # Read and parse the input file
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        line = line.strip()

        # Match plural forms
        plural_match = re.match(
            r"^(.*?)\s+<div style=\"margin-left:1em\"><i class=\"p\"><font color=\"green\">pl</font></i>.*?&lt;&lt;([^<>&]*?)&gt;&gt;</div>$",
            line,
        )
        if plural_match:
            plural_form = plural_match.group(1).strip()
            singular_forms = plural_match.group(2).strip().split("|")
            # Link plural form with singular forms
            for singular in singular_forms:
                key_groups[singular].append(plural_form)
                key_groups[plural_form].append(singular)
        else:
            # Regular lines
            parts = line.split("\t", 1)
            keys = parts[0].strip().split("|")

            # Track the position of the first singular form in the input
            singular_positions[keys[0]] = idx

    # Resolve all key groups into canonical forms
    resolved_entries = []
    seen_keys = set()

    for key in key_groups:
        if key not in seen_keys:
            # Resolve all related keys
            stack = [key]
            group = []
            while stack:
                current = stack.pop()
                if current not in seen_keys:
                    seen_keys.add(current)
                    group.append(current)
                    stack.extend(k for k in key_groups[current] if k not in seen_keys)

            # Extract singular and plural forms
            singulars = [k for k in group if k in singular_positions]
            plurals = [k for k in group if k not in singular_positions]

            if singulars:
                # Add each singular form with its associated plurals to the output
                for singular in singulars:
                    resolved_entries.append((singular, "|".join(plurals)))

    # Write the resolved data to the CSV file
    with open(csv_output_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(resolved_entries)

    print(f"Processed irregular nouns saved to {csv_output_path}")


if __name__ == "__main__":
    input_file = "temp/03.british-american-variants.txt"  # Input file path
    csv_output_file = "csv/nouns-irregular.csv"  # CSV output file path

    process_file(input_file, csv_output_file)
