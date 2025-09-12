#!/usr/bin/env python3

"""Genomic region search for FAANGMine

This script uses the InterMine API to programmatically search for features 
within genomic regions for a specified organism (and optionally, assembly).

More details on the region search, including the formats allowed for the genome 
coordinates, can be found here:
https://faangmine.rnet.missouri.edu/faangmine/genomicRegionSearch.do

For this demo, the search results are displayed as a table, grouped by region.
The results are also stored as a list of results Rows for further processing. In that
case, displaying the query results can be disabled by passing displayOutput=false to 
region_search().
"""

import os, sys
from dotenv import load_dotenv
from intermine.webservice import Service
sys.path.append("..")
from region_search_faangmine.region_search_faangmine import region_search

MINE_URL = "https://faangmine.rnet.missouri.edu/faangmine"


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
    print("FAANGMine region search demo\n")
    printSpacer()

    # Uncomment below to use API key (recommended)
    #service = Service(MINE_URL, token=get_API_key())
    # Comment out below if using API key above
    service = Service(MINE_URL)

    #--------------------------------------------------------------------------
    # Example 1
    print("Example 1: Simple region search for genome features\n")
    print("Search for B. taurus features of type exon, gene, mRNA, or SNV")
    print("within specified regions (given as a list of strings in the form")
    print("'chromosome:start..end').\n")
    
    # Selected organism
    org = "Bos taurus"
    # Selected feature types (as list of strings)
    # See get_feature_class_names.py for list of feature class names
    features = ["Exon", "Gene", "MRNA", "SNV"]
    # Selected regions (as list of strings)
    # See https://faangmine.rnet.missouri.edu/faangmine/genomicRegionSearch.do
    # for details on accepted region string formats
    regions = ["1:580045..580045", "5:5001231..5010365"]

    results = region_search(service, org, features, regions)

    # Further processing examples:
    # Retrieve list of all primary identifiers from results:
    primaryIds = [row["primaryIdentifier"] for row in results]
    # Retreive list of gene ids from results:
    geneIds = [row["primaryIdentifier"] for row in results if \
               row["SequenceFeature.sequenceOntologyTerm.name"] == "gene"]
    print("List of gene ids: " + ','.join(geneIds))
    # Retrieve only RefSeq gene ids:
    geneIds = [row["primaryIdentifier"] for row in results if \
               row["SequenceFeature.sequenceOntologyTerm.name"] == "gene" \
               and row["source"] == "RefSeq"]
    print("List of RefSeq gene ids: " + ','.join(geneIds))
    # Remove duplicates if any:
    geneIds = list(set(geneIds))
    print("List of unique RefSeq gene ids: " + ','.join(geneIds)) 

    printSpacer()

    #--------------------------------------------------------------------------
    # Example 2
    print("Example 2: Add assembly to the region search (optional)\n")
    print("Repeat the search in the example above, restricting to a specified")
    print("assembly.\n(For reference only; currently in FAANGMine each")
    print("organism only has one assembly loaded.)\n")
    
    # Selected assembly
    assembly = "ARS-UCD1.2"

    reuslts = region_search(service, org, features, regions, assembly)
    printSpacer()

    #--------------------------------------------------------------------------
    # Example 3
    print("Example 3: Restrict to selected analyses, given as a list of ")
    print("strings of analysis sources.\n")

    # Analyses:
    # Run get_analyses.py to get all possible analysis sources
    analyses = [
        "ATAC_adipose_SRX9176775",
        "ATAC_adipose_SRX9176776",
        "ATAC_cerebellum_SRX9176779"
    ]
    # Features need to match analyses, use checkboxes on webapp as guide
    features = ["OpenChromatinRegion"]

    results = region_search(service, org, features, regions, assembly, analyses)

    #--------------------------------------------------------------------------
    # Example 4
    print("Example 4: Extend each region at both sides (optional)\n")
    print("Repeat the search in Example 1, extending the regions at both")
    print("sides by a specified amount (given as an integer).\n")

    # Example 1 search params:
    features = ["Exon", "Gene", "MRNA", "SNV"]

    # Extend regions by this amount:
    extend = 30000

    # Pass empty set for analyses to search all
    results = region_search(service, org, features, regions, assembly, [], extend)
    printSpacer()

    #--------------------------------------------------------------------------
    # Example 5
    print("Example 5: Perform a strand-specific search on a single region.\n")

    # Strand: +
    results = region_search(service, org, features, regions, assembly, [], 0, True)

    # Strand: -
    features = ["Exon", "Gene", "MRNA", "LncRNA"]
    regions = ["1:4990900..4943500"]
    results = region_search(service, org, features, regions, assembly, [], 0, True)
    # Set printOutput=False to skip printing results to screen, for example:
    #results = region_search(service, org, features, regions, None, 0, True, False)


def printSpacer():
    """Print spacer between examples.
    """
    print("------------------------------------------------------------------")


if __name__ == "__main__":
    main()
