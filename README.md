cricbuzz
========

For fetching Live Cricket Score from cricbuzz

Usage:
------

An example of how to get live scores.

    	   from cricbuzz import *    	   
    	   cric = CricbuzzParser()
    	   match = cric.getXml()
    	   details = cric.handleMatches(match) #Returns Match details as a Dictionary. Parse it according to requirements.
    

Known Issues:
-------------
1. The XML file from CricBuzz changes frequently. It raises out an exception, when no match is being played on.

Bug Report:
-----------
Issue it here: https://github.com/psibi/cricbuzz/issues

License:
--------
GNU General Public License v3 (GPLv3)

