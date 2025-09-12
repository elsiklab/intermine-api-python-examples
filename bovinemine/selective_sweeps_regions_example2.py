#!/usr/bin/env python3

"""Genomic region search example querying Selective Sweeps data from BovineMine

This script uses the InterMine API to programmatically search for HaplotypeBlocks
within specified genomic regions.

After the HaplotypeBlock identifiers are retrieved from the region search query,
a second query is run on these HaplotypeBlock ids to get other fields specific to 
this class, e.g., population, breed, breed class, breed origin. The overlapping
genes ids, symbols, and sources are also queried. The results are displayed and
the gene ids are stored separately.

Lastly, the overlapping gene ids from the above query are used to create and save
a list of those genes that can be viewed in the webapp (for example, to perform
enrichment analyses for this list). Creating and saving a list requires an API
token to be generated for the account under "MyMine" and this token to be passed
as a parameter to Service().

This script uses the region_search() function from region_search_default.
"""

import os, sys
from dotenv import load_dotenv
import pandas as pd
from intermine.webservice import Service
sys.path.append("..")
from region_search_default.region_search_default import region_search
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

    # Selected feature types (as list of strings)
    # In this case just one type, 'HaplotypeBlock'
    features = ["HaplotypeBlock"]

    # Selected regions (as list of strings)
    # See https://bovinemine.rnet.missouri.edu/bovinemine/genomicRegionSearch.do
    # for details on accepted region string formats
    regions = ["6:33774948..33774948", 
               "12:18394407..18394407", 
               "20:69174801..69174801", 
               "25:12512507..12512507", 
               "26:31085230..31085230"
              ]

    results = region_search(service, "Bos taurus", features, regions)
    # Uncomment below to not display results to screen
    #results = region_search(service, "Bos taurus", features, regions, None, 0, False, False)

    # Get list of HaplotypeBlock primary identifiers (exclude duplicates)
    primaryIds = list(set([row["primaryIdentifier"] for row in results]))
    print(str(len(primaryIds)) + " HaplotypeBlock ids found:")
    print(', '.join(primaryIds))
    print()

    # Now run a second query to get HaplotypeBlock fields and overlapping gene info
    # Note that could edit the function called in region_search() to add in these
    # fields and avoid the extra query, as in selective_sweeps_regions_example.py
    print("Retrieving additional HaplotypeBlock fields and overlapping gene info")
    q = service.new_query("HaplotypeBlock")
    q.add_view("primaryIdentifier", 
               "population", 
               "breed", 
               "breedClass", 
               "breedOrigin", 
               "overlappingGenes.primaryIdentifier",
               "overlappingGenes.symbol", 
               "overlappingGenes.source"
               )
    q.add_constraint("primaryIdentifier", "ONE OF", primaryIds)

    # Display query results (optional)
    # Change to False to not display table of results to screen
    displayResults = True
    if displayResults:
        tbl = []
        print("Number of results:", len(q.rows()))
        
        for row in q.rows():
            feature = [row["population"], 
                       row["breed"], 
                       row["breedClass"],
                       row["breedOrigin"],
                       row["overlappingGenes.primaryIdentifier"],
                       row["overlappingGenes.symbol"],
                       row["overlappingGenes.source"]
                       ]
            tbl.append(feature)

        # Using pandas DataFrame to display results in formatted table similar 
        # to webapp HTML table of results
        tblCols = ["Population", 
                   "Breed", 
                   "Breed class", 
                   "Breed origin",
                   "Gene id",
                   "Gene symbol",
                   "Gene source"
                   ]
        df = pd.DataFrame(data=tbl, columns=tblCols)

        # Begin counting rows at 1:
        df.index = df.index + 1
        # Display the table of results for this region:
        if (df.empty):
            print("No overlap features found")
        else:
            print(df.to_string())
        print()

    # Retrieve gene ids from results
    geneIds = [row["overlappingGenes.primaryIdentifier"] for row in q.rows()]

    # Lastly, save list of overlapping gene ids (requires API key)
    # append time to create a unique list name
    ts = time.time()
    listName = "Example list of HaplotypeBlock overlapping Genes created " + str(ts)
    lm=service.list_manager()
    lm.create_list(content=geneIds, list_type="Gene",name=listName)
    print("List " + listName + " created and saved. " +
           "This list can be accessed under MyMine -> Lists.")


if __name__ == "__main__":
    main()
