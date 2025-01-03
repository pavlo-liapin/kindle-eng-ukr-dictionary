from pathlib import Path
import re

def process_dictionary_file(input_file, output_file):
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace \n with <br>
    content = content.replace('\\n', '<br>')

    # Delete all occurrences of [m1]
    content = content.replace('[m1]', '')

    content = content.replace('<font color="brown">□</font>', '•')

    # Remove <font color="green"> and <font color="steelblue"> with closing tags
    content = re.sub(r'<font color="green">(.*?)</font>', r'\1', content)  # Green
    content = re.sub(r'<font color="steelblue">(.*?)</font>', r'\1', content)  # Steelblue
    content = re.sub(r'<font color="darkred">(.*?)</font>', r'\1', content)  # Darkred
    content = re.sub(r'<font color="darkslateblue">(.*?)</font>', r'\1', content)  # Darkred

    # Replace <<word>> with <a href="#word">word</a>
    content = re.sub(r"&lt;&lt;(.*?)&gt;&gt;", r'<a href="#\1">\1</a>', content)

    # Replace <div style="margin-left:1em">
    content = re.sub(
        r'<div style="margin-left:1em">(.*?)</div>',
        r'&ensp;\1',
        content,
        flags=re.DOTALL
    )

    # Replace <div style="margin-left:2em">
    content = re.sub(
        r'<div style="margin-left:2em">(.*?)</div>',
        r'&ensp;&ensp;\1',
        content,
        flags=re.DOTALL
    )

    # Replace <div style="margin-left:3em">
    content = re.sub(
        r'<div style="margin-left:3em"><span class="sec">(.*?)</span></div>',
        r'&ensp;&ensp;&ensp;\1',
        content,
        flags=re.DOTALL
    )

    content = re.sub(
      r'<span class="ex">(.*?)</span>',
      r'<span>\1</span>',
      content,
      flags=re.DOTALL
    )

    content = re.sub(
      r'<i class="p">(.*?)</i>',
      r'<em>\1</em>',
      content,
      flags=re.DOTALL
    )

    content = re.sub(
      r'<font color="(royalblue|red|dodgerblue|saddlebrown)">(.*?)</font>',
      r'<span>\2</span>',
      content,
      flags=re.DOTALL
    )

    # Write the processed content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

# File paths
input_file = "temp/11.all-inflections.txt"
output_file = "temp/12.clean-markup.txt"

# Process the file
process_dictionary_file(input_file, output_file)

print(f"File processing complete. Output written to {output_file}")
