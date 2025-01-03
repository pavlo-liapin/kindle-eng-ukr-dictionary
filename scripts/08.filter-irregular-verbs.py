import re
from collections import defaultdict, OrderedDict

def process_irregular_verbs(input_path, output_path):
    """
    Process the input file to merge irregular verb forms (past and past participle)
    into unified entries, preserving both the order of keys and their position in the input.
    Args:
        input_path (str): Path to the input file.
        output_path (str): Path to the output file.
    """
    # Dictionary to store relationships and values
    key_groups = defaultdict(list)
    key_to_column = {}
    verb_positions = OrderedDict()  # To track verb positions for output order
    key_order = OrderedDict()  # To preserve original order of keys in groups

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
            base_forms = past_match.group(2).strip().split("|")
            # Link past form with base forms
            for base in base_forms:
                key_groups[base].append(past_form)
                key_groups[past_form].append(base)
            continue

        # Match past participle forms
        pp_match = past_participle_pattern.match(line)
        if pp_match:
            pp_form = pp_match.group(1).strip()
            base_forms = pp_match.group(2).strip().split("|")
            # Link past participle form with base forms
            for base in base_forms:
                key_groups[base].append(pp_form)
                key_groups[pp_form].append(base)
            continue

        # Regular lines
        parts = line.split("\t", 1)
        keys = parts[0].strip().split("|")
        second_column = parts[1] if len(parts) > 1 else ""

        # Preserve original order of keys
        for key in keys:
            if key not in key_order:
                key_order[key] = len(key_order)

        # Link all keys in the same group
        for key in keys:
            key_groups[key].extend(k for k in keys if k != key)
            if key not in key_to_column:
                key_to_column[key] = second_column

        # Track the position of the first base form in the input
        verb_positions[keys[0]] = idx

    # Resolve all key groups into canonical forms
    resolved_groups = {}
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

            # Preserve original input order of keys
            group.sort(key=lambda x: key_order.get(x, float('inf')))
            canonical_form = "|".join(group)

            # Find the first base form in the group for positioning
            first_base = next((k for k in group if k in verb_positions), group[0])
            resolved_groups[first_base] = (canonical_form, key_to_column.get(first_base, ""))

    # Ensure all base forms have a position
    for base in resolved_groups:
        if base not in verb_positions:
            verb_positions[base] = float('inf')  # Place it at the end if not tracked

    # Sort by the original position of base forms
    sorted_entries = sorted(resolved_groups.items(), key=lambda x: verb_positions[x[0]])

    # Write the resolved data to the output file
    with open(output_path, "w", encoding="utf-8") as file:
        for _, (canonical_form, second_column) in sorted_entries:
            if second_column:
                file.write(f"{canonical_form}\t{second_column}\n")
            else:
                file.write(f"{canonical_form}\n")

    print(f"Processed file saved to {output_path}")


if __name__ == "__main__":
    input_file = "temp/05.filter-irregular-nouns.txt"  # Input file path
    output_file = "temp/08.filter-irregular-verbs.txt"  # Output file path

    process_irregular_verbs(input_file, output_file)