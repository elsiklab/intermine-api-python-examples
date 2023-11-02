#!/usr/bin/env python3

"""Genomic region search for FAANGMine

This script uses the InterMine API to programmatically search for features 
within genomic regions for a specified organism (and optionally, assembly).

More details on the region search, including the formats allowed for the genome 
coordinates, can be found here:
https://faangmine.rnet.missouri.edu/faangmine/genomicRegionSearch.do

For this demo, the search results are stored as 2D arrays, displayed as a 
table, grouped by region. Each row is a feature, and the columns are the 
feature attributes: primary identifier + symbol, type, analysis, location.
"""

import sys
sys.path.append("..")
from region_search_faangmine.region_search_faangmine import region_search

FAANGMINE_URL = "https://faangmine.rnet.missouri.edu/faangmine"


def main():
    print("FAANGMine region search demo\n")
    printSpacer()

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

    region_search(FAANGMINE_URL, org, features, regions)
    printSpacer()

    #--------------------------------------------------------------------------
    # Example 2
    print("Example 2: Add assembly to the region search (optional)\n")
    print("Repeat the search in the example above, restricting to a specified")
    print("assembly.\n(For reference only; currently in FAANGMine each")
    print("organism only has one assembly loaded.)\n")
    
    # Selected assembly
    assembly = "ARS-UCD1.2"

    region_search(FAANGMINE_URL, org, features, regions, assembly)
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

    region_search(FAANGMINE_URL, org, features, regions, assembly, analyses)

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
    region_search(FAANGMINE_URL, org, features, regions, assembly, [], extend)
    printSpacer()

    #--------------------------------------------------------------------------
    # Example 5
    print("Example 5: Perform a strand-specific search on a single region.\n")

    # Strand: +
    region_search(FAANGMINE_URL, org, features, regions, assembly, [], 0, True)

    # Strand: -
    features = ["Exon", "Gene", "MRNA", "LncRNA"]
    regions = ["1:4990900..4943500"]
    region_search(FAANGMINE_URL, org, features, regions, assembly, [], 0, True)


def printSpacer():
    """Print spacer between examples.
    """
    print("------------------------------------------------------------------")


if __name__ == "__main__":
    main()
