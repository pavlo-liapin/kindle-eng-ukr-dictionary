import os

txt_file = "temp/12.clean-markup.txt"

xhtml_header = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<html xmlns:math="http://exslt.org/math" xmlns:svg="http://www.w3.org/2000/svg"\n'
    '  xmlns:tl="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"\n'
    '  xmlns:saxon="http://saxon.sf.net/" xmlns:xs="http://www.w3.org/2001/XMLSchema"\n'
    '  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
    '  xmlns:cx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"\n'
    '  xmlns:dc="http://purl.org/dc/elements/1.1/"\n'
    '  xmlns:mbp="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"\n'
    '  xmlns:mmc="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"\n'
    '  xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf">\n'
    '<head><link rel="stylesheet" href="style.css" /></head>\n'
    '<body>\n'
    '<mbp:frameset>\n'
)
xhtml_footer = (
    '</mbp:frameset>\n'
    '</body>\n'
    '</html>\n'
)

# Process the generated file and write to XHTML formats
batch_size = 15000
entry_count = 0
file_count = 1
output_file = f"output/dictionary-{file_count}.xhtml"
outfile = open(output_file, "w", encoding="utf-8")
outfile.write(xhtml_header)

with open(txt_file, "r", encoding="utf-8") as infile:
    for line in infile:
        if line.strip():
            parts = line.split('\t', 1)  # Adjust delimiter as needed
            if len(parts) == 2:
                headword, definition = parts

                # Handle synonyms in headword (split by "|")
                synonyms = headword.split('|')
                main_headword = synonyms[0].strip()
                inflections = synonyms[1:]  # Treat additional synonyms as inflections

                # Build dictionary entry
                entry = f'<idx:entry name="default" scriptable="yes" spell="yes">'
                entry += f'<h5><dt><idx:orth value="{main_headword}">{main_headword}'

                # Add inflections (if any)
                if inflections:
                    entry += '<idx:infl>'
                    for inflection in inflections:
                        entry += f'<idx:iform value="{inflection.strip()}" />'
                    entry += '</idx:infl>'

                entry += f'</idx:orth></dt></h5>'
                entry += f'<dd>{definition.strip()}</dd><mbp:pagebreak /></idx:entry>\n'

                # Write to the current output file
                outfile.write(entry)
                entry_count += 1

                # Check if batch size limit is reached
                if entry_count >= batch_size:
                    outfile.write(xhtml_footer)
                    outfile.close()
                    print(f"Written {entry_count} entries to {output_file}")

                    # Start a new file
                    file_count += 1
                    output_file = f"output/dictionary-{file_count}.xhtml"
                    outfile = open(output_file, "w", encoding="utf-8")
                    outfile.write(xhtml_header)
                    entry_count = 0

# Close the final file
outfile.write(xhtml_footer)
outfile.close()
print(f"Final entries written to {output_file}")
