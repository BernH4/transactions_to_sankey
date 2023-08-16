import re
import pandas as pd
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

class Entry:
    def __init__(self, line, config):
        self.line = line
        #self.verwendungszweck = entry['']
        self.group, self.subgroup = self.associate_to_group(config)

    def printc(self, color, string):
        print(f"\n{color}{string}{Style.RESET_ALL}")
        
    def associate_to_group(self, config):
        group_matches = 0
        #Sollte nur eine Gruppe sein, falls doch mehr gematched werden wird das Ausgegeben, Array benötigt
        groups = []
        subgroups = []
        for  typ in config['typ']:
            for  spalte, regex in typ['suche']:
                try:
                    if re.search(regex, self.line[spalte], flags=re.IGNORECASE):
                        group_matches += 1
                        groups.append(typ['group'])
                        subgroups.append(typ['subgroup'])
                        break #Man kann für einen Typ mehrere Regexe angeben, matched einer ist es nicht nötig weitere auszuprobieren. Es werden aber weiterhin andere Typen ausprobiert ob diese auch matchen,  falls ja muss man eventuell die Regeln anpassen
                except TypeError:
                    # Keine IBAN in Buchung angegeben, wahrscheinlich weil Auszahlung Geldautomat
                    if spalte == 'IBAN Zahlungsbeteiligter' and pd.isnull(self.line[spalte]):
                        continue

        if group_matches > 1:
            #Hier debugger einschalten und gruppe multiple matches checken
            self.printc(Fore.RED, "Es wurden mehrere matches gefunden für folgende Zeile, eventuel Regeln anpassen:")
            print(self.line[['Name Zahlungsbeteiligter', 'Betrag','Buchungstag', 'Verwendungszweck']].to_string())
            print("Groups: ", groups[0], "\n", subgroups[0])
            return (None, None)
        elif group_matches == 0:
            self.printc(Fore.RED, "Folgende Zeile konnte nicht zugeordnet werden:")
            print(self.line[['Name Zahlungsbeteiligter', 'Betrag','Buchungstag', 'Verwendungszweck']].to_string())
            return (None, None)
        else:
            self.printc(Fore.GREEN, "OK:")
            print(self.line[['Name Zahlungsbeteiligter', 'Betrag','Buchungstag', 'Verwendungszweck']].to_string())
            print("Groups: ", groups[0], "\nSubgroup: ", subgroups[0])
            return (groups[0], subgroups[0])

