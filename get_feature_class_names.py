#!/usr/bin/env python3

"""Get feature class names

This script lists all of the feature class names as they appear in the 
PathQuery API (http://intermine.org/im-docs/docs/api/pathquery).

When defining the list of features in the region search code, use the class 
name rather than the human-readable name (e.g., "MRNA" rather than "mRNA").
"""

from intermine.webservice import Service

AQUAMINE_URL = "https://aquamine.rnet.missouri.edu/aquamine"
FAANGMINE_URL = "https://faangmine.rnet.missouri.edu/faangmine"
HMINE_URL = "https://hymenopteramine.rnet.missouri.edu/hymenopteramine"
MAIZEMINE_URL = "https://maizemine.rnet.missouri.edu/maizemine"


def main():
    # Select desired mine URL:
    mineUrl = AQUAMINE_URL

    service = Service(mineUrl)

    print("All feature class names in", mineUrl + ":")
    allClassNames = service.model.classes.keys()
    for className in sorted(allClassNames):
        print(className)


if __name__ == "__main__":
    main()
