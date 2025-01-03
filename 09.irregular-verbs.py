import re
import csv
from collections import defaultdict, OrderedDict

def process_irregular_verbs_to_csv(input_path, csv_output_path):
    """
    Process the input file to merge irregular verb forms (past and past participle)
    into unified entries and write them into a CSV file using commas as delimiters.
    Args:
        input_path (str): Path to the input file.
        csv_output_path (str): Path to the CSV output file.
    """
    # Dictionary to store relationships and positions
    key_groups = defaultdict(set)  # Use sets to avoid duplicate entries
    verb_positions = OrderedDict()  # To track base verb positions for output order

    # Regular expressions for irregular verb patterns
    past_pattern = re.compile(
        r"^(.*?)\s+<div style=\"margin-left:1em\"><i class=\"p\"><font color=\"green\">past</font></i> <i class=\"p\"><font color=\"green\">від</font></i> &lt;&lt;([^<>&]*?)&gt;&gt;</div>$"
    )
    past_participle_pattern = re.compile(
        r"^(.*?)\s+<div style=\"margin-left:1em\"><i class=\"p\"><font color=\"green\">p\.p\.</font></i> <i class=\"p\"><font color=\"green\">від</font></i> &lt;&lt;([^<>&]*?)&gt;&gt;</div>$"
    )

    # Read and parse the input file
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        line = line.strip()

        # Match past forms
        past_match = past_pattern.match(line)
        if past_match:
            past_form = past_match.group(1).strip()
            base_forms = past_match.group(2).strip().split("|")  # Split by |
            for base in base_forms:
                key_groups[base.strip()].add(past_form)
                key_groups[past_form].add(base.strip())
            continue

        # Match past participle forms
        pp_match = past_participle_pattern.match(line)
        if pp_match:
            pp_form = pp_match.group(1).strip()
            base_forms = pp_match.group(2).strip().split("|")  # Split by |
            for base in base_forms:
                key_groups[base.strip()].add(pp_form)
                key_groups[pp_form].add(base.strip())
            continue

        # Regular lines
        parts = line.split("\t", 1)
        keys = parts[0].strip().split("|")  # Split by |

        # Track the position of the first base form in the input
        for key in keys:
            verb_positions[key.strip()] = idx

    # Resolve all key groups into canonical forms
    resolved_entries = []
    seen_keys = set()

    for key in key_groups:
        if key not in seen_keys:
            # Resolve all related keys
            stack = [key]
            group = set()
            while stack:
                current = stack.pop()
                if current not in seen_keys:
                    seen_keys.add(current)
                    group.add(current)
                    stack.extend(k for k in key_groups[current] if k not in seen_keys)

            # Extract base, past, and past participle forms
            base_forms = sorted(k for k in group if k in verb_positions)
            related_forms = sorted(k for k in group if k not in verb_positions)

            if base_forms:
                # Add each base form with its associated related forms to the output
                for base in base_forms:
                    # Replace vertical bars with commas in related forms
                    cleaned_related = [form for related in related_forms for form in related.split("|")]
                    resolved_entries.append([base] + cleaned_related)

    # Write the resolved data to the CSV file
    with open(csv_output_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(resolved_entries)

    print(f"Processed irregular verbs saved to {csv_output_path}")


if __name__ == "__main__":
    input_file = "temp/05.filter-irregular-nouns.txt"  # Input file path
    csv_output_file = "temp/verbs-irregular.csv"  # CSV output file path

    process_irregular_verbs_to_csv(input_file, csv_output_file)