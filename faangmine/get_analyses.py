#!/usr/bin/env python3

"""Get FAANGMine Analyses

This script lists all of the available Analyses in FAANGMine (region 
search checkboxes in webapp) for a selected organism, grouped by 
BioProject category.
The output format is:

BioProject category
    Analysis 1
    Analysis 2
    ...

Use the Analysis names in the FAANGMine region search script.
Change the organism name to view analyses for another (default 
is Bos taurus).

Note: filtering by analyses is optional. Leaving the list empty will 
search all analyses for the specified feature types.
In particular, Genome features "analyses" are just sources (e.g., RefSeq, 
Ensembl).
"""

import collections
from intermine.webservice import Service

FAANGMINE_URL = "https://faangmine.rnet.missouri.edu/faangmine"


def main():
    service = Service(FAANGMINE_URL)

    print("List of BioProject categories and their analyses")
    print("Format:")
    print("BioProject category")
    print("\tAnalysis 1")
    print("\tAnalysis 2")
    print("\t" + "...\n")

    # Change org variable below to view analyses for another organism
    org = "Bos taurus"
    print("Analyses for", org + ":")

    analyses = collections.defaultdict(set)
    q = service.query("Analysis").\
        select("Analysis.source", "bioProject.category").\
        outerjoin("bioProject").\
        where("Analysis.organism.name", "=", org)

    for row in q.rows():
        analyses[row["bioProject.category"]].add(row["Analysis.source"])
       
    for key in sorted(analyses.keys()):
        print(key)
        print("\t" + "\n\t".join(sorted(analyses[key])))

    # Uncomment below to print analyses as list that can be copy-pasted
    # into region search script
    for key in sorted(analyses.keys()):
        print("Category:", key)
        print(sorted(analyses[key]))

if __name__ == "__main__":
    main()
