#!/usr/bin/env python3

"""Genomic region search for AquaMine

This script uses the InterMine API to programmatically search for features 
within genomic regions for a specified organism (and optionally, assembly).

More details on the region search, including the formats allowed for the genome 
coordinates, can be found here:
https://aquamine.rnet.missouri.edu/aquamine/genomicRegionSearch.do

For this demo, the search results are stored as 2D arrays, displayed as a 
table, grouped by region. Each row is a feature, and the columns are the 
feature attributes: primary identifier and symbol, type, location.
"""

import sys
sys.path.append("..")
from region_search_default.region_search_default import region_search

AQUAMINE_URL = "https://aquamine.rnet.missouri.edu/aquamine"


def main():
    print("AquaMine region search demo\n")
    printSpacer()

    #--------------------------------------------------------------------------
    # Example 1
    print("Example 1: Simple region search\n")
    print("Search for O. mykiss features of type exon, gene, or mRNA")
    print("within specified regions (given as a list of strings in the form")
    print("'chromosome:start..end').\n")
    
    # Selected organism
    org = "Oncorhynchus mykiss"
    # Selected feature types (as list of strings)
    # See get_feature_class_names.py for list of feature class names
    features = ["Exon", "Gene", "MRNA"]
    # Selected regions (as list of strings)
    # See https://aquamine.rnet.missouri.edu/aquamine/genomicRegionSearch.do
    # for details on accepted region string formats
    regions = ["1:4973300..4990880", "3:5078530..5082200"]

    region_search(AQUAMINE_URL, org, features, regions)
    printSpacer()

    #--------------------------------------------------------------------------
    # Example 2
    print("Example 2: Add assembly to the region search (optional)\n")
    print("Repeat the search in the example above, restricting to a specified")
    print("assembly.\n(For reference only; currently in AquaMine each")
    print("organism only has one assembly loaded.)\n")
    
    # Selected assembly
    assembly = "USDA_OmyKA_1.1"

    region_search(AQUAMINE_URL, org, features, regions, assembly)
    printSpacer()

    #--------------------------------------------------------------------------
    # Example 3
    print("Example 3: Extend each region at both sides (optional)\n")
    print("Repeat the search in Example 1, extending the regions at both")
    print("sides by a specified amount (given as an integer).\n")

    # Extend regions by this amount:
    extend = 30000

    # Could either use assembly specified above, or set assembly=None to search 
    # across all assemblies (for AquaMine it doesn't matter; the results 
    # will be the same):
    region_search(AQUAMINE_URL, org, features, regions, assembly, extend)
    #region_search(AQUAMINE_URL, org, features, regions, None, extend)
    printSpacer()

    #--------------------------------------------------------------------------
    # Example 4
    print("Example 4: Perform a strand-specific search on a single region.\n")

    # Strand: +
    region_search(AQUAMINE_URL, org, features, regions, assembly, 0, True)

    # Strand: -
    features = ["Exon", "Gene", "MRNA", "LncRNA"]
    regions = ["1:4990900..4943500"]
    region_search(AQUAMINE_URL, org, features, regions, assembly, 0, True)


def printSpacer():
    """Print spacer between examples.
    """
    print("------------------------------------------------------------------")


if __name__ == "__main__":
    main()
