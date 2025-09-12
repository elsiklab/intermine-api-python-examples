#!/usr/bin/env python3

"""Genomic region search (FAANGMine)

This script uses the InterMine API to programmatically search for features within 
genomic regions for a specified organism (and optionally, assembly).

Compatible with FAANGMine only. See region_search_default.py for AquaMine, BovineMine, 
HymenopteraMine, and MaizeMine examples. The query for FAANGMine includes Analyses which 
is not in other mines.

For this demo, the search results are displayed as a table, grouped by region, with the 
columns: primary identifier and symbol, source, type, and location.
Setting printOutput=False skips printing the results to the screen.

To allow for further processing of the search results, this function returns the array 
of query result Rows, where fields may be accessed by name, e.g., 
row["primaryIdentifier"], row["symbol"].
"""

import pandas as pd

def region_search(service, org, features, regions, assembly=None, 
                  analyses=[], extend=0, strandSpecific=False, printOutput=True):
    """Perform a genomic region search and displays results per region.

    Parameters
    ---------
    service: class
        Connection to InterMine WebService instance
    org : str
        Organism full name
    features: list of str
        List of feature types, as they appear in the PathQuery API 
        (http://intermine.org/im-docs/docs/api/pathquery).
        See get_feature_class_names.py for all feature class names
    regions: list of str
        List of genomic regions
    assembly: str or None, optional
        Assembly name (default is to search across all assemblies in database)
    analyses: list of str, optional
        List of analyses (default is to search across all analyses in database)
        See get_analyses.py for analysis names per organism
    extend: int, optional
        Extend regions at both sides by this amount (default is 0)
    strandSpecific: bool, optional
        Perform a strand-specific region search (default is False)
    printOutput: bool, optional
        Display region search results as a formatted table (default is True)
    """

    # Echo search parameters
    print("Organism:", org)
    print("Feature types:", ', '.join(features))
    if (assembly):
        print("Assembly:", assembly)
    if (analyses):
        print("Analyses:", ', '.join(analyses))
    if (extend):
        print("Extend regions:", str(extend), "bp")
    if (strandSpecific):
        print("Strand-specific search enabled")
    print()
    
    # To store all results together for further processing
    allRows = []

    # Search for features in each region
    for region in regions:
        if printOutput: print("Region:", region)

        # Call to parse_region extends region by amount specified 
        # (if present - optional)
        # and sets strand based on whether start < end
        # (for strand-specific search - optional)
        searchRegion, strand = parse_region(region, extend)
        if (extend and printOutput):
            print("Extended region:", searchRegion)
        if (strandSpecific and printOutput):
            print("Strand:", strandToStr(strand))

        # Perform the region search query:
        # Overlap query expects list of regions
        # Could run one query for all regions but all results would be combined
        # Here we are separating the results by region as the webapp does
        searchRegion = [searchRegion]
        
        # Can retrieve results through data model or query API
        # This script uses query API 
        # Many examples in InterMine Python documentation: 
        # https://github.com/intermine/intermine-ws-python-docs
        # View get_results_by_query() function for more details
        qRows = get_results_by_query(service, org, features, analyses, 
                                     searchRegion, assembly, extend, 
                                     strandSpecific, strand)

        for row in qRows:
            allRows.append(row)

        # Additional processing if printing results table to screen
        if printOutput:
            tbl = []

            print("Number of results:", len(qRows))
            
            for row in qRows:
                # Store location as a string of the form "chromosome:start-end"
                chrId = row["SequenceFeature.chromosome.primaryIdentifier"]
                start = str(row["SequenceFeature.chromosomeLocation.start"])
                end = str(row["SequenceFeature.chromosomeLocation.end"])
                loc = chrId + ":" + start + "-" + end
                # Store the feature primary identifier + symbol, feature type, and
                # location string
                # NoneType returned if a field has no value in the database.
                # For example, some features have no symbol, which is why
                # row["SequenceFeature.symbol"] is explicitly converted to a string
                # below (displaying "None" if no symbol present)
                featureLabel = (row["primaryIdentifier"] + " "
                             + str(row["symbol"]))
                feature = [
                    featureLabel, 
                    row["SequenceFeature.sequenceOntologyTerm.name"],
                    row["SequenceFeature.source"],
                    loc
                ]
                tbl.append(feature)

            # Using pandas DataFrame to display results in formatted table similar 
            # to webapp HTML table of results
            df = pd.DataFrame(data=tbl, columns=["Feature", "Type", 
                                                 "Analysis/Source", "Location"])

            # Begin counting rows at 1:
            df.index = df.index + 1
            # Display the table of results for this region:
            if (df.empty):
                print("No overlap features found")
            else:
                print(df.to_string())
            print()
    
    return allRows            


def get_results_by_query(service, org, features, analyses, searchRegion, 
                         assembly, extend, strandSpecific, strand):
    """Retrieve features overlapping searchRegion using InterMine query API.

    Parameters
    ---------
    service: intermine.webservice.Service
        InterMine WebService object
    org : str
        Organism full name
    features: list of str
        List of feature types, as they appear in the PathQuery API 
        (http://intermine.org/im-docs/docs/api/pathquery).
    analyses: list of str
        List of analyses (if empty, search across all analyses in database)
    regions: list of str
        List of genomic regions
    assembly: str or None
        Assembly name (if None, search across all assemblies in database)
    extend: int
        Extend regions at both sides by this amount
    strandSpecific: bool
        Perform a strand-specific region search
    strand: int
        Strand (1 if region start < end, -1 otherwise)

    Returns
    -------
    list of Rows
    """

    # Initialize query
    q = service.new_query()

    # Add constraints (restrict to selected features, org, and region)
    q.add_constraint("SequenceFeature", "ISA", features)
    q.add_constraint("organism.name", "=", org)
    if (analyses):
        q.add_constraint("source", "ONE OF", analyses)
    q.add_constraint("chromosomeLocation", "OVERLAPS", searchRegion)
    if (assembly):
        q.add_constraint("chromosome.assembly", "=", assembly)
    if (strandSpecific):
        q.add_constraint("chromosomeLocation.strand", "=", strand)

    # Add fields to display: primary identifier, symbol, feature type, 
    # location (chromosome, start, end)
    q.add_view("SequenceFeature.primaryIdentifier", 
               "SequenceFeature.symbol",
               "SequenceFeature.sequenceOntologyTerm.name",
               "SequenceFeature.source",
               "SequenceFeature.chromosome.primaryIdentifier",
               "SequenceFeature.chromosomeLocation.start", 
               "SequenceFeature.chromosomeLocation.end"
              )

    return q.rows()


def parse_region(region, extend):
    """Parse region string to extend start and end by extend parameter.

    Parameters
    ---------
    region: str
        Genomic region string
    extend: int
        Extend region at both sides by this amount

    Returns
    -------
    tuple str, str
        Region string extended at both sides, strand (1 or -1)
        Strand is 1 if region start < end, -1 otherwise

    """
    # Determine region format used and extend coordinates by specified amount.
    # This is a quick & dirty format check, would be better to use regex.
    # If a single region format is used throughout scripts then simply use the 
    # appropriate extendedRegion line with the corresponding separators between 
    # chromosome ID and coordinates.

    # Initialize
    chrID = chrSplit = coordSplit = ""
    start = end = 0

    if ":" and ".." in region:
        # Expected format: chromosome:start..end
        chrSplit = ":"
        coordSplit = ".."
    elif ":" and "-" in region:
        chrSplit = ":"
        coordSplit = "-"
    elif "\t" in region:
        chrSplit = coordSplit = '\t'
    else:
        raise ValueError(region + " doesn't match any supported format.")
    
    chrID = region.split(chrSplit)[0]
    [start, end] = region.split(chrSplit)[1].split(coordSplit)
    strand = 1
    # If start > end, reverse for search and set strand=-1
    if (int(start) > int(end)):
        tmp = start
        start = end
        end = tmp
        strand = -1

    # Extend start and end coords (start at zero if start < extend amount)
    extStart = max(int(start) - extend, 0)
    extEnd = int(end) + extend
    
    extRegion = chrID + chrSplit + str(extStart) + coordSplit + str(extEnd)
    return extRegion, strand


def strandToStr(strand):
    """Print strand as a string ("+" or "-") based on its integer value.

    Parameters
    ---------
    strand: int
        Strand represented as an integer (1 or -1)

    Returns
    -------
    str
        Strand represented as a string (+ or -)
    """
    return "+" if (strand > 0) else "-"

