#!/usr/bin/env python3

"""Simple database query in MaizeMine

This script uses the InterMine API to programmatically run a database query in 
MaizeMine.
"""

import os
from dotenv import load_dotenv
import itertools
from intermine.webservice import Service

MAIZEMINE_URL = "https://maizemine.rnet.missouri.edu/maizemine"


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
    print("MaizeMine simple query demo\n")

    # Uncomment below to use API key (recommended)
    #service = Service(MAIZEMINE_URL, token=get_API_key())
    # Comment out below if using API key above
    service = Service(MAIZEMINE_URL)

    print("Query XML:")
    print("<query model=\"genomic\" view=\"Gene.symbol Gene.source Gene.primaryIdentifier Gene.proteins.name\" sortOrder=\"Gene.symbol ASC\">")
    print("  <constraint path=\"Gene.organism.name\" op=\"=\" value=\"Zea mays\" code=\"A\" />")
    print("</query>")

    query = service.new_query("Gene")
    query.add_view("symbol", "source", "primaryIdentifier", "proteins.name")
    query.add_constraint("organism.name", "=", "Zea mays", code = "A")

    N = 25
    print("Number of results:", len(query.rows()))
    print("First", N, "rows:")
    for row in itertools.islice(query.rows(),N):
        print(row["symbol"], row["source"], row["primaryIdentifier"], row["proteins.name"])


if __name__ == "__main__":
    main()
