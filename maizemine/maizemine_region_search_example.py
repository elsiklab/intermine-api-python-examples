#!/usr/bin/env python3

"""Genomic region search for MaizeMine

This script uses the InterMine API to programmatically search for features 
within genomic regions for a specified organism (and optionally, assembly).

More details on the region search, including the formats allowed for the genome 
coordinates, can be found here:
https://maizemine.rnet.missouri.edu/maizemine/genomicRegionSearch.do

For this demo, the search results are stored as 2D arrays, displayed as a 
table, grouped by region. Each row is a feature, and the columns are the 
feature attributes: primary identifier and symbol, type, location.
"""

import sys
sys.path.append("..")
from region_search_default.region_search_default import region_search

MAIZEMINE_URL = "https://maizemine.rnet.missouri.edu/maizemine"


def main():
    print("MaizeMine region search demo\n")
    printSpacer()

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

    region_search(MAIZEMINE_URL, org, features, regions, assembly)
    printSpacer()

    #--------------------------------------------------------------------------
    # Example 2
    print("Example 2: Extend each region at both sides (optional)\n")
    print("Repeat the search above, extending the regions at both")
    print("sides by a specified amount (given as an integer).\n")

    # Extend regions by this amount:
    extend = 30000

    region_search(MAIZEMINE_URL, org, features, regions, assembly, extend)
    printSpacer()

    #--------------------------------------------------------------------------
    # Example 3
    print("Example 3: Perform a strand-specific search on a single region.\n")

    # Strand: +
    region_search(MAIZEMINE_URL, org, features, regions, assembly, 0, True)

    # Strand: -
    features = ["Exon", "Gene", "MRNA"]
    regions = ["chr3:117230800..115909390"]
    region_search(MAIZEMINE_URL, org, features, regions, assembly, 0, True)


def printSpacer():
    """Print spacer between examples.
    """
    print("------------------------------------------------------------------")


if __name__ == "__main__":
    main()
