import re
import pandas as pd
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

class Entry:
    def __init__(self, line, config):
        self.line = line
        #self.verwendungszweck = entry['']
        self.category, self.subcategory = self.associate_to_category(config)

    def printc(self, color, string):
        print(f"\n{color}{string}{Style.RESET_ALL}")
        
    def associate_to_category(self, config):
        category_matches = 0
        #Sollte nur eine Gruppe sein, falls doch mehr gematched werden wird das Ausgegeben, Array benötigt
        categories = []
        subcategories = []
        for  typ in config['typ']:
            matches_for_curr_category = []
            for  spalte, regex in typ['suche']:
                content = self.line[spalte]
                # Check if content is NaN or None and assign empty string, else re.search will throw an error
                content = "" if  pd.isnull(content) else content
                matches_for_curr_category.append(re.search(regex, content, flags=re.IGNORECASE))
            
            if typ.get('match_type') == None or typ['match_type'] == "OR":
                if any(matches_for_curr_category):
                    category_matches += 1
                    categories.append(typ['category'])
                    subcategories.append(typ['subcategory'])
            elif typ['match_type'] == "AND":
                if all(matches_for_curr_category):
                    category_matches += 1
                    categories.append(typ['category'])
                    subcategories.append(typ['subcategory'])

        if category_matches > 1:
            #Hier debugger einschalten und gruppe multiple matches checken
            self.printc(Fore.RED, "Es wurden mehrere matches gefunden für folgende Zeile, eventuel Regeln anpassen:")
            print(self.line[['Name Zahlungsbeteiligter', 'Betrag','Buchungstag', 'Verwendungszweck']].to_string())
            print("Groups: ", categories[0], "\n", subcategories[0])
            return (None, None)
        elif category_matches == 0:
            self.printc(Fore.RED, "Folgende Zeile konnte nicht zugeordnet werden:")
            print(self.line[['Name Zahlungsbeteiligter', 'Betrag','Buchungstag', 'Verwendungszweck']].to_string())
            return (None, None)
        else:
            self.printc(Fore.GREEN, "OK:")
            print(self.line[['Name Zahlungsbeteiligter', 'Betrag','Buchungstag', 'Verwendungszweck']].to_string())
            print("Groups: ", categories[0], "\nSubcategory: ", subcategories[0])
            return (categories[0], subcategories[0])

