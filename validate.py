import sys

def count_repeated_occurrences(filename):
    """
    Count repeated occurrences of items in the first column and find keys with empty second columns.
    Args:
        filename (str): Path to the tab-separated TXT file.
    Returns:
        tuple: Number of repeated items, a dictionary of repeated items with their counts,
               and a list of keys with empty second columns.
    """
    repeated_occurrences = {}
    keys_with_empty_second_column = []

    with open(filename, 'r') as file:
        for line in file:
            columns = line.strip().split('\t')

            # Process the first column for repeated occurrences
            if len(columns) > 0:
                first_column = columns[0].split('|')
                for item in first_column:
                    if item in repeated_occurrences:
                        repeated_occurrences[item] += 1
                    else:
                        repeated_occurrences[item] = 1

            # Check if the second column is empty
            if len(columns) < 2 or not columns[1].strip():
                keys_with_empty_second_column.extend(columns[0].split('|'))

    # Filter repeated items (count > 1)
    repeated_items = {item: count for item, count in repeated_occurrences.items() if count > 1}
    return len(repeated_items), repeated_items, keys_with_empty_second_column


def main():
    # Check if filename is provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python index.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        num_repeated, repeated_list, empty_second_column_keys = count_repeated_occurrences(filename)

        # Display repeated occurrences if any
        if num_repeated > 0:
            print(f'Number of repeated occurrences: {num_repeated}')
            print('Full list of repeated occurrences:')
            for item, count in repeated_list.items():
                print(f'{item}: {count}')

        # Display keys with empty second columns if any
        if empty_second_column_keys:
            print('\nKeys with empty second column:')
            for key in empty_second_column_keys:
                print(key)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()