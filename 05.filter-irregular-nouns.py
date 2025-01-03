import re
from collections import defaultdict, OrderedDict

def process_file(input_path, output_path):
    """
    Process the input file to merge singular and plural forms into unified entries,
    preserving both the order of keys and their position in the input.
    Args:
        input_path (str): Path to the input file.
        output_path (str): Path to the output file.
    """
    # Dictionary to store relationships and values
    key_groups = defaultdict(list)
    key_to_column = {}
    singular_positions = OrderedDict()  # To track singular positions for output order
    key_order = OrderedDict()  # To preserve original order of keys in groups

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

            # Track the position of the first singular form in the input
            singular_positions[keys[0]] = idx

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

            # Find the first singular form in the group for positioning
            first_singular = next((k for k in group if k in singular_positions), group[0])
            resolved_groups[first_singular] = (canonical_form, key_to_column.get(first_singular, ""))

    # Ensure all singular forms have a position
    for singular in resolved_groups:
        if singular not in singular_positions:
            singular_positions[singular] = float('inf')  # Place it at the end if not tracked

    # Sort by the original position of singular forms
    sorted_entries = sorted(resolved_groups.items(), key=lambda x: singular_positions[x[0]])

    # Write the resolved data to the output file
    with open(output_path, "w", encoding="utf-8") as file:
        for _, (canonical_form, second_column) in sorted_entries:
            if second_column:
                file.write(f"{canonical_form}\t{second_column}\n")
            else:
                file.write(f"{canonical_form}\n")

    print(f"Processed file saved to {output_path}")


if __name__ == "__main__":
    input_file = "temp/03.british-american-variants.txt"  # Input file path
    output_file = "temp/05.filter-irregular-nouns.txt"  # Output file path

    process_file(input_file, output_file)
