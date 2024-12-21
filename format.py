from pathlib import Path
import re

def process_dictionary_file(input_file, output_file):
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Insert <head> with a link to style.css before <body>
    content = re.sub(
        r'(<body>)',
        r'<head><link rel="stylesheet" href="style.css" /></head>\1',
        content
    )

    # Replace \n with <br>
    content = content.replace('\\n', '<br>')

    # Delete all occurrences of [m1]
    content = content.replace('[m1]', '')

    content = content.replace('<font color="brown">□</font>', '<span class="marker">•</span>')

    # Remove <font color="green"> and <font color="steelblue"> with closing tags
    content = re.sub(r'<font color="green">(.*?)</font>', r'\1', content)  # Green
    content = re.sub(r'<font color="steelblue">(.*?)</font>', r'\1', content)  # Steelblue
    content = re.sub(r'<font color="darkred">(.*?)</font>', r'\1', content)  # Darkred

    # Insert <mbp:pagebreak /> before each </idx:entry>
    content = content.replace('</idx:entry>', '<mbp:pagebreak /></idx:entry>')

    # Wrap each <idx:orth> with <h5><dt>
    content = re.sub(
        r'(<idx:orth>.*?</idx:orth>)',
        r'<h5><dt>\1</dt></h5>',
        content
    )

    # Replace <div style="margin-left:1em"> with <span class="padding-1">
    content = re.sub(
        r'<div style="margin-left:1em">(.*?)</div>',
        r'<span class="padding-1">\1</span>',
        content,
        flags=re.DOTALL
    )

    # Replace <div style="margin-left:1em"> with <span class="padding-2">
    content = re.sub(
        r'<div style="margin-left:2em">(.*?)</div>',
        r'<span class="padding-2">\1</span>',
        content,
        flags=re.DOTALL
    )

    # Replace <div style="margin-left:3em"> with <span class="padding-3">
    content = re.sub(
        r'<div style="margin-left:3em"><span class="sec">(.*?)</span></div>',
        r'<span class="padding-3">\1</span>',
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'<font color="royalblue">(.*?)</font>',
        r'<span class="example">\1</span>',
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'<font color="red">(.*?)</font>',
        r'<span class="usage-bullet">\1</span>',
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'<font color="dodgerblue">(.*?)</font>',
        r'<span class="usage-value">\1</span>',
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'<font color="saddlebrown">(.*?)</font>',
        r'<span class="enum">\1</span>',
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'<font color="darkslateblue">(.*?)</font>',
        r'<span class="list-item">\1</span>',
        content,
        flags=re.DOTALL
    )

    # Remove all <div> wrappers
    # content = re.sub(r'<div[^>]*>', '', content)  # Remove opening <div> with any attributes
    # content = re.sub(r'</div>', '', content)  # Remove closing </div>

    # Replace <p> with <dd> and clean up any closing </p> tags
    content = re.sub(r'<p>', '<dd>', content)
    content = re.sub(r'</p>', '</dd>', content)

    # Write the processed content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

# File paths
input_file = "dictionary_letter_a.xhtml"
output_file = "dictionary.xhtml"

# Process the file
process_dictionary_file(input_file, output_file)

print(f"File processing complete. Output written to {output_file}")
