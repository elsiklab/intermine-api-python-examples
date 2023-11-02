#!/usr/bin/env python3

"""Lists example - HymenopteraMine

This script uses the InterMine API to create a list of Gene IDs, save the  
list, and run a template query using the values from this list. 

For this demo, the Gene IDs are loaded from the input file named 
"identifiers.txt" and the template query results are printed to the screen.
"""

import os
from dotenv import load_dotenv
import itertools
from intermine.webservice import Service

HMINE_URL = "https://hymenopteramine.rnet.missouri.edu/hymenopteramine"


def get_API_key():
    """Get API key from .env file.

    Returns
    -------
    str
        API key loaded from file
    """

    if(not load_dotenv()):
        raise OSError("Unable to load API key; make sure .env file exists")

    return os.getenv('API_KEY')


def main():
    print("HymenopteraMine lists demo\n")

    # API key required to save lists to account
    service = Service(HMINE_URL, token=get_API_key())

    # Load identifiers from input file:
    identifiers = []
    with open("identifiers.txt") as f:
        for line in f:
            identifiers.append(line.rstrip())

    # Create list and save to your InterMine account:
    listName = "My Example O. bicornis list"
    lm=service.list_manager()
    # Check if list with this name already exists:
    mylist = lm.get_list(listName)
    if (not mylist):
        lm.create_list(content=identifiers,list_type="Gene",name=listName)
        print("Saved list:", listName)
    else:
        print("A list named", listName, "already exists, cannot create list "
            + "with the same name")

    # Run template, restricting gene IDs to those in newly created list:
    print("Running template: Gene ID --> Homologues")
    print("See details at:", HMINE_URL + "/template.do?name=Gene_Orthologues")
    template = service.get_template('Gene_Orthologues')

    # Constraint values:
    # A    Gene
    # B    Gene.homologues.lastCommonAncestor
    # C    Gene.homologues.dataSets.name

    rows = template.rows(
        A = {"op": "IN", "value": listName},
        B = {"op": "=", "value": "Holometabola"},
        C = {"op": "=", "value": "HGD-Ortho data set"}
    )

    N = 10

    print("Number of results:", len(rows))
    print("First", N, "rows:")
    for row in itertools.islice(rows,N):
        print(row["organism.shortName"], row["primaryIdentifier"], row["symbol"], row["description"], \
            row["homologues.homologue.organism.shortName"], \
            row["homologues.homologue.primaryIdentifier"], row["homologues.homologue.symbol"], \
            row["homologues.homologue.description"], \
            row["homologues.orthologueCluster.primaryIdentifier"], row["homologues.lastCommonAncestor"])

    # To delete list (uncomment below):
    #lm.delete_lists([listName])
    #print("List named", listName, "deleted")


if __name__ == "__main__":
    main()
