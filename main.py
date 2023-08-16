import re
import toml
import pandas as pd
from collections import defaultdict

# Eigene Klasse
from entry import Entry


entries = []
def process_csv(csv_file, config_file):
    # Load the TOML config file
    with open(config_file, 'r') as f:
        config = toml.load(f)

    # Compile the regex patterns from the config file
    #patterns = {}
    #for group, rule in config['typ'].items():
    #    patterns[group] = re.compile(rule)

    # Read the CSV file using pandas
    df = pd.read_csv(csv_file, delimiter=";")
    

    # Loop over each row in the CSV file
    for index, row in df.iterrows():
        entries.append(Entry(row, config))
        # Associate the line with the matched groups
        #print(f"Line {index+1}: {line} -> Groups: {matched_groups}")  # Modify this line based on your desired output
        
    #for entry in entries:
    #    print(entry.group)
        
    #grouped_entries = defaultdict(list)
    #for entry in entries:
    #    grouped_entries[entry.group].append(entry)
    #    grouped_people = defaultdict(list)
    #
    ## Print the grouped result
    #for category, group in grouped_entries.items():
    #    print(f"Category {category}:")
    #    print("Sum: ", sum(float(entry.line['Betrag'].replace(",", ".")) for entry in group))
    #    for entry in group:
    #        print(f"  {entry.line['Name Zahlungsbeteiligter']}")
    #        print(f"  {entry.line['Betrag']}")
            

    print("fertig")

# Example usage
#process_csv('combined_18.05.2023.csv', 'config.toml')
process_csv('2023.csv', 'config.toml')

