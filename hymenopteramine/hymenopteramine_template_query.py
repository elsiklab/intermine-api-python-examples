#!/usr/bin/env python3

"""Template query example - HymenopteraMine

This script uses the InterMine API to programmatically run a template query 
and retrieve the results.

For this demo, the template query results will be printed to the screen.
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
    print("HymenopteraMine templates demo\n")
    print("This example shows how to run the template query:"
        + "'Gene ID -> Homologues'")
    print("See details at:", HMINE_URL + "/template.do?name=Gene_Orthologues")

    # Uncomment below to use API key (recommended)
    #service = Service(HMINE_URL, token=get_API_key())
    # Comment out below if using API key above
    service = Service(HMINE_URL)

    template = service.get_template('Gene_Orthologues')

    # Constraint values:
    # A    Gene.primaryIdentifier
    # B    Gene.homologues.lastCommonAncestor
    # C    Gene.homologues.dataSets.name

    rows = template.rows(
        A = {"op": "=", "value": "102676332"},
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

    # Uncomment to view all rows:
    #for row in rows:
    #    print(row["organism.shortName"], row["primaryIdentifier"], row["symbol"], row["description"], \
    #        row["homologues.homologue.organism.shortName"], \
    #        row["homologues.homologue.primaryIdentifier"], row["homologues.homologue.symbol"], \
    #        row["homologues.homologue.description"], \
    #        row["homologues.orthologueCluster.primaryIdentifier"], row["homologues.lastCommonAncestor"])


if __name__ == "__main__":
    main()
