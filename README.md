cricbuzz
========

For fetching Live Cricket Score from cricbuzz

Usage:
------

An example of how to get live scores.

    	   from cricbuzz import *    	   
    	   cric = CricbuzzParser()
    	   match = cric.getXml()
    	   details = cric.handleMatches(match) #Returns Match details as List of Dictionary. Parse it according to requirements.
    

License:
--------
GNU General Public License v3 (GPLv3)

Bug Report:
-----------
Issue it here: https://github.com/psibi/cricbuzz/issues

