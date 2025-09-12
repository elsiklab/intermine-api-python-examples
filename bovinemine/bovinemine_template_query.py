#!/usr/bin/env python3

"""Template query example - BovineaMine

This script uses the InterMine API to programmatically run a template query 
and retrieve the results.

For this demo, the template query results will be printed to the screen.
"""

import os
from dotenv import load_dotenv
import itertools
from intermine.webservice import Service

MINE_URL = "https://bovinemine.rnet.missouri.edu/bovinemine"


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
    print("BovineMine templates demo\n")
    print("This example shows how to run the template query:"
        + "'Bovine Gene --> Expression'")
    print("See details at:", MINE_URL + 
          "/template.do?name=Gene_to_expression")

    # Uncomment below to use API key (recommended)
    #service = Service(MINE_URL, token=get_API_key())
    # Comment out below if using API key above
    service = Service(MINE_URL)

    # Template name from url after "name="
    template = service.get_template('Gene_to_expression')

    # Constraint values:
    # A    Gene.primaryIdentifier
    # B    Gene.expressionValues.FPKM
    # C    Gene.expressionValues.TPM

    rows = template.rows(
        A = {"op": "=", "value": "326601"},
        B = {"op": ">", "value": "0"},
        C = {"op": ">", "value": "0"}
    )

    N = 20

    # Print first N rows to screen
    # Below shows how each field may be accessed for further processing,
    # e.g., the gene ids are in row["primaryIdentifier"] in each row
    print("Number of results:", len(rows))
    print("First", N, "rows:")
    for row in itertools.islice(rows,N):
        print(row["primaryIdentifier"],
            row["source"], 
            row["Gene.expressionValues.FPKM"],
            row["Gene.expressionValues.TPM"],
            row["Gene.expressionValues.sraMetadata.btoName"],
            row["Gene.expressionValues.sraMetadata.organismPart"],
            row["Gene.expressionValues.sraMetadata.experimentId"],
            row["Gene.expressionValues.sraMetadata.sex"],
            row["Gene.expressionValues.sraMetadata.animalAgeAtCollection"]
            )

if __name__ == "__main__":
    main()
