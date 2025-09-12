#!/usr/bin/env python3

"""Genomic region search for MaizeMine

This script uses the InterMine API to programmatically search for features 
within genomic regions for a specified organism (and optionally, assembly).

More details on the region search, including the formats allowed for the genome 
coordinates, can be found here:
https://maizemine.rnet.missouri.edu/maizemine/genomicRegionSearch.do

For this demo, the search results are displayed as a table, grouped by region.
The results are also stored as a list of results Rows for further processing. In that
case, displaying the query results can be disabled by passing displayOutput=false to 
region_search().
"""

import os, sys
from dotenv import load_dotenv
from intermine.webservice import Service
sys.path.append("..")
from region_search_default.region_search_default import region_search

MINE_URL = "https://maizemine.rnet.missouri.edu/maizemine"


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
    print("MaizeMine region search demo\n")
    printSpacer()
    
    # Uncomment below to use API key (recommended)
    #service = Service(MINE_URL, token=get_API_key())
    # Comment out below if using API key above
    service = Service(MINE_URL)

    #--------------------------------------------------------------------------
    # Example 1
    print("Example 1: Simple region search\n")
    print("Search for Z. mays features of type gene or mRNA within specified")
    print("regions (given as a list of strings in the form")
    print("'chromosome:start..end').\n")
    
    # Selected organism (required)
    org = "Zea mays"
    # Selected assembly (required)
    assembly = "Zm-B73-REFERENCE-NAM-5.0"
    # Selected feature types (as list of strings) (required)
    # See get_feature_class_names.py for list of feature class names
    features = ["Gene", "MRNA"]
    # Selected regions (as list of strings) (required)
    # See https://maizemine.rnet.missouri.edu/maizemine/genomicRegionSearch.do
    # for details on accepted region string formats
    regions = ["chr1:29733..37349", "chr3:114909387..117230788"]

    results = region_search(service, org, features, regions, assembly)

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
    print("Example 2: Extend each region at both sides (optional)\n")
    print("Repeat the search above, extending the regions at both")
    print("sides by a specified amount (given as an integer).\n")

    # Extend regions by this amount:
    extend = 30000

    results = region_search(service, org, features, regions, assembly, extend)
    printSpacer()

    #--------------------------------------------------------------------------
    # Example 3
    print("Example 3: Perform a strand-specific search on a single region.\n")

    # Strand: +
    results = region_search(service, org, features, regions, assembly, 0, True)

    # Strand: -
    features = ["Exon", "Gene", "MRNA"]
    regions = ["chr3:117230800..115909390"]
    results = region_search(service, org, features, regions, assembly, 0, True)
    # Set printOutput=False to skip printing results to screen, for example:
    #results = region_search(service, org, features, regions, assembly, 0, True, False)

def printSpacer():
    """Print spacer between examples.
    """
    print("------------------------------------------------------------------")


if __name__ == "__main__":
    main()
