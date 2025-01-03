import re

def process_cross_links(input_path, output_path):
    """
    Process cross-links in the input file. For each line with <font color="green">див.</font>:
    - Add the variation to the linked word's key.
    - Remove the original line with the cross-link.
    - Ensure the output lines are stable and sorted.
    
    Args:
        input_path (str): Path to the input TXT file.
        output_path (str): Path to the output TXT file.
    """
    # Dictionary to hold variations to add
    variations = {}

    # Regular expression to match specific cross-link lines
    cross_link_pattern = re.compile(r"^(.*?)\s+<div .*?><i class=\"p\"><font color=\"green\">див\.</font></i> &lt;&lt;(.*?)&gt;&gt;</div>$")

    # Read and process the file
    updated_lines = []
    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Check if the line matches the specific cross-link pattern
            match = cross_link_pattern.match(line.strip())
            if match:
                key = match.group(1).strip()
                linked_word = match.group(2).strip()

                # Add the variation to the dictionary
                if linked_word in variations:
                    variations[linked_word].add(key)
                else:
                    variations[linked_word] = {key}
            else:
                # Keep non-cross-link lines
                updated_lines.append(line.strip())

    # Update lines with new variations
    final_lines = []
    for line in updated_lines:
        parts = line.split("\t")
        if len(parts) > 1:
            key = parts[0]
            if key in variations:
                # Sort variations alphabetically and append to the key
                extra_variations = "|".join(sorted(variations[key]))
                if extra_variations not in key:
                    key = f"{key}|{extra_variations}"
                parts[0] = key
        final_lines.append("\t".join(parts))

    # Write the updated file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(final_lines) + "\n")

    print(f"Processed file saved as: {output_path}")


# Usage
if __name__ == "__main__":
    input_path = "temp/00.sanitize.txt"  # Path to the input TXT file
    output_path = "temp/01.crosslinks.txt"  # Path to the output TXT file

    # Process the file
    process_cross_links(input_path, output_path)
