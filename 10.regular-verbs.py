import csv
import spacy
import pyinflect  # Ensure pyinflect is installed: pip install pyinflect


def generate_verb_forms_spacy(base, nlp):
    """
    Generate verb forms (past tense, past participle, -ing form, third-person singular) using spaCy and pyinflect.
    Args:
        base (str): The base form of the verb.
        nlp: A spaCy language model instance.
    Returns:
        tuple: (past, past_participle, ing_form, third_person), or (None, None, None, None) if not applicable.
    """
    doc = nlp(base)

    token = doc[0]
    past = token._.inflect("VBD")  # Past tense
    past_participle = token._.inflect("VBN")  # Past participle
    ing_form = token._.inflect("VBG")  # Gerund (-ing form)
    third_person = token._.inflect("VBZ")  # Third-person singular

    return past, past_participle, ing_form, third_person


def process_file(input_path, irregular_csv_path, csv_output_path):
    """
    Process the input file to generate verb forms using spaCy and pyinflect,
    excluding irregular verbs, and write the base form along with derivatives to a CSV file.
    Args:
        input_path (str): Path to the input file.
        irregular_csv_path (str): Path to the irregular verbs CSV file.
        csv_output_path (str): Path to the output CSV file.
    """
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Load irregular verbs
    irregular_verbs = set()
    with open(irregular_csv_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            irregular_verbs.update(row)

    regular_verbs = []
    all_generated_forms = set()  # Track all generated forms to avoid duplicates

    # Read the input file
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Collect all existing entries
    existing_entries = set()
    for line in lines:
        key = line.split("\t", 1)[0].strip()
        for part in key.split("|"):
            existing_entries.add(part)

    for line in lines:
        original_line = line.strip()
        parts = original_line.split("\t", 1)
        keys = parts[0].strip().split("|")
        second_column = parts[1] if len(parts) > 1 else ""

        # Check if the entry is a verb
        if '<i class="p"><font color="green">v</font></i>' in second_column:
            for base in keys:
                if base in irregular_verbs:
                    continue

                # Generate all forms using spaCy and pyinflect
                past, past_participle, ing_form, third_person = generate_verb_forms_spacy(base, nlp)

                # Skip if forms are not generated
                if not all([past, past_participle, ing_form, third_person]):
                    continue

                # Use a set to collect unique missing forms
                unique_forms = {
                    past if past not in existing_entries else None,
                    past_participle if past_participle not in existing_entries else None,
                    ing_form if ing_form not in existing_entries else None,
                    third_person if third_person not in existing_entries else None,
                }

                # Remove None values and filter out globally generated forms
                unique_forms = sorted(
                    form for form in unique_forms if form and form not in all_generated_forms
                )

                # Add new forms to the global set
                all_generated_forms.update(unique_forms)

                # If any forms are missing, add the base and its unique missing forms to the CSV
                if unique_forms:
                    regular_verbs.append([base] + unique_forms)

    # Write the regular verbs to the CSV file
    with open(csv_output_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(regular_verbs)

    print(f"Processed regular verbs saved to {csv_output_path}")


if __name__ == "__main__":
    input_file = "temp/05.filter-irregular-nouns.txt"  # Input file path
    irregular_csv_path = "csv/verbs-irregular.csv"  # Irregular verbs CSV file path
    csv_output_file = "csv/verbs-regular.csv"  # CSV output file path

    process_file(input_file, irregular_csv_path, csv_output_file)