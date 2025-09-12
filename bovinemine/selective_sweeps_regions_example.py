#!/usr/bin/env python3

"""Genomic region search example querying Selective Sweeps data from BovineMine

This script uses the InterMine API to programmatically search for HaplotypeBlocks
within specified genomic regions.

The overlapping gene ids from the query are used to create and save a list of those 
genes that can be viewed in the webapp (for example, to perform enrichment analyses 
for this list). Creating and saving a list requires an API token to be generated for 
the account under "MyMine" and this token to be passed as a parameter to Service().

This script can be run standalone (does not depend on 'region_search_default').
"""

from intermine.webservice import Service
import os, sys
from dotenv import load_dotenv
import time

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
    print("Selective Sweeps regions search demo")
    service = Service(MINE_URL, token=get_API_key())

    # Selected regions (as list of strings)
    # See https://bovinemine.rnet.missouri.edu/bovinemine/genomicRegionSearch.do
    # for details on accepted region string formats
    regions = ["6:33774948..33774948", 
               "12:18394407..18394407",
               "20:69174801..69174801", 
               "25:12512507..12512507", 
               "26:31085230..31085230"
              ]
    print("Regions:")
    print(', '.join(regions))

    # Initialize query 
    q = service.new_query("HaplotypeBlock")

    # Add constraints
    # Restricting organism=bos taurus technically not necessary for this data set
    # but including as an example
    q.add_constraint("organism.name", "=", "Bos taurus")
    q.add_constraint("chromosomeLocation", "OVERLAPS", regions)

    # Add fields
    q.add_view("primaryIdentifier",
                "population", 
                "breed", 
                "breedClass", 
                "breedOrigin", 
                "overlappingGenes.primaryIdentifier",
                "overlappingGenes.symbol", 
                "overlappingGenes.source"
                )

    # Example of how to get list of HaplotypeBlock primary identifiers from results
    haplotypeBlockIds = list(set([row["primaryIdentifier"] for row in q.rows()]))
    print(str(len(haplotypeBlockIds)) + " HaplotypeBlock ids:")
    print(', '.join(haplotypeBlockIds))

    # Retrieve gene ids from results
    geneIds = list(set([row["overlappingGenes.primaryIdentifier"] for row in q.rows()]))
    print(str(len(geneIds)) + " overlapping Gene ids:")
    print(', '.join(geneIds))

    # Save list of overlapping gene ids (requires API key)
    # append time to create a unique list name
    ts = time.time()
    listName = "Example list of HaplotypeBlock overlapping Genes created " + str(ts)
    lm=service.list_manager()
    lm.create_list(content=geneIds, list_type="Gene",name=listName)
    print("List " + listName + " created and saved. " + 
          "This list can be accessed under MyMine -> Lists.")


if __name__ == "__main__":
    main()

