#!/usr/bin/env python3

"""Genomic region search (AquaMine, HymenopteraMine, MaizeMine)

This script uses the InterMine API to programmatically search for features 
within genomic regions for a specified organism (and optionally, assembly).

Compatible with AquaMine, HymenopteraMine, and MaizeMine.

For this demo, the search results are stored as 2D arrays, displayed as a 
table, grouped by region. Each row is a feature, and the columns are the 
feature attributes: primary identifier and symbol, type, location.
"""

import os
from dotenv import load_dotenv
import pandas as pd
from intermine.webservice import Service

def region_search(mineUrl, org, features, regions, assembly=None, extend=0, 
                  strandSpecific=False):
    """Perform a genomic region search and displays results per region.

    Parameters
    ---------
    mineUrl: str
        Full URL to InterMine instance
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
    extend: int, optional
        Extend regions at both sides by this amount (default is 0)
    strandSpecific: bool, optional
        Perform a strand-specific region search (default is False)
    """

    # Uncomment below to use API key (recommended)
    #service = Service(mineUrl, token=get_API_key())
    # Comment out below if using API key above
    service = Service(mineUrl)

    # Echo search parameters
    print("Organism:", org)
    print("Feature types:", ', '.join(features))
    if (assembly):
        print("Assembly:", assembly)
    if (extend):
        print("Extend regions:", str(extend), "bp")
    if (strandSpecific):
        print("Strand-specific search enabled")
    print()

    # Search for features in each region
    for region in regions:
        print("Region:", region)

        # Call to parse_region extends region by amount specified 
        # (if present - optional)
        # and sets strand based on whether start < end
        # (for strand-specific search - optional)
        searchRegion, strand = parse_region(region, extend)
        if (extend):
            print("Extended region:", searchRegion)
        if (strandSpecific):
            print("Strand:", strandToStr(strand))

        # Perform the region search query:
        # Overlap query expects list of regions
        # Could run one query for all regions but all results would be combined
        # Here we are separating the results by region as the webapp does
        searchRegion = [searchRegion]
        
        # QUERY OPTIONS 
        # -------------
        # Can retrieve results through data model or query API
        # This script uses query API; comment out and uncomment 
        # get_results_by_model to run with other option

        # Option 1: Using queries (Query class)
        # Many examples in InterMine Python documentation: 
        # https://github.com/intermine/intermine-ws-python-docs
        # View get_results_by_query() function for more details
        resTbl = get_results_by_query(service, org, features, searchRegion, 
                                      assembly, extend, strandSpecific, strand)

        # Option 2: Use the data model (Model class)
        # As seen in https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4086141/
        # View get_results_by_model() function for more details
        #resTbl = get_results_by_model(service, org, features, searchRegion, 
        #                             assembly, extend, strandSpecific, strand)

        # Using pandas DataFrame to display results in formatted table similar 
        # to webapp HTML table of results
        df = pd.DataFrame(data=resTbl, columns=["Feature", "Type", "Location"])

        # Begin counting rows at 1:
        df.index = df.index + 1
        # Display the table of results for this region:
        if (df.empty):
            print("No overlap features found")
        else:
            print(df.to_string())
        print()


def get_results_by_query(service, org, features, searchRegion, assembly, 
                         extend, strandSpecific, strand):
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
    list of list of str
        2D array of results where each row is a list of feature attributes
    """

    # Initialize query
    q = service.new_query()

    # Add constraints (restrict to selected features, org, and region)
    q.add_constraint("SequenceFeature", "ISA", features)
    q.add_constraint("organism.name", "=", org)
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
               "SequenceFeature.chromosome.primaryIdentifier",
               "SequenceFeature.chromosomeLocation.start", 
               "SequenceFeature.chromosomeLocation.end"
              )
    print("Number of results:", len(q.rows()))

    # Iterate through results and store as 2D array:
    # Initialize array
    tbl = []
    for row in q.rows():
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
        featureLabel = (row["SequenceFeature.primaryIdentifier"] + " " 
                     + str(row["SequenceFeature.symbol"]))
        feature = [
            featureLabel, 
            row["SequenceFeature.sequenceOntologyTerm.name"], 
            loc
        ]
        tbl.append(feature)

    return tbl


def get_results_by_model(service, org, features, searchRegion, assembly, 
                         extend, strandSpecific, strand):
    """Retrieve features overlapping searchRegion using InterMine data model.

    Parameters
    ---------
    service: intermine.webservice.Service
        InterMine WebService object
    org : str
        Organism full name
    features: list of str
        List of feature types, as they appear in the PathQuery API 
        (http://intermine.org/im-docs/docs/api/pathquery).
    regions: list of str
        List of genomic regions
    assembly: str or None
        Assembly name (if "None", search across all assemblies in database)
    extend: int
        Extend regions at both sides by this amount
    strandSpecific: bool
        Perform a strand-specific region search
    strand: int
        Strand (1 if region start < end, -1 otherwise)

    Returns
    -------
    list of list of str
        2D array of results where each row is a list of feature attributes
    """

    q = service.model.SequenceFeature.\
                where("SequenceFeature", "ISA", features).\
                where("organism.name", "=", org).\
                where("chromosomeLocation", "OVERLAPS", searchRegion)
    if (assembly):
        q = q.where("chromosome.assembly", "=", assembly)
    if (strandSpecific):
        q = q.where("chromosomeLocation.strand", "=", strand)
    print("Number of results:", len(q.results()))

    # Iterate through results and store as 2D array:
    # Initialize array
    tbl = []
    for feature in q.results():
        # Store location as a string of the form "chromosome:start-end"
        loc = (feature.chromosome.primaryIdentifier + ":" 
            + str(feature.chromosomeLocation.start) + "-" 
            + str(feature.chromosomeLocation.end))
        # Store the feature primary identifier + symbol, feature type, and 
        # location string
        # NoneType returned if a field has no value in the database. 
        # For example, some features have no symbol, which is why 
        # feature.symbol is explicitly converted to a string below (displaying 
        # "None" if no symbol present)
        thisRow = [feature.primaryIdentifier + " " + str(feature.symbol), feature.type, loc]
        tbl.append(thisRow)

    # Additional notes:
    # To see all possible fields (primaryIdentifier, symbol, etc.), uncomment 
    # the following code snippet):
    #sf = service.model.get_class("SequenceFeature")
    #print(sf.fields)

    return tbl


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

