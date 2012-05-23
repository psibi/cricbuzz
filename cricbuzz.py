#!/usr/bin/python

import xml.dom.minidom
import urllib2

class CricbuzzParser():
    
    def __init__(self,url):
        # self.getXml(url)
        pass
       
    def getXml(self,url):
        #Change coding here
        doc = xml.dom.minidom.parse("./fa.xml")
        node = doc.documentElement
        matches = node.getElementsByTagName("match")
        return matches

    def handleMatches(self,matches):
        duplicate = []
        match_details = []
        mchDesc = matches[0].getAttribute("mchDesc")
        duplicate.append(mchDesc)
        match_detail = self.handleMatch(matches[0])
        match_details.append(match_detail)
        for match in matches:
            flag = False
            mchDesc = match.getAttribute("mchDesc")
            #If list duplicate is empty, then populate it initially.
            for entry in duplicate:
                if entry == mchDesc: #If duplicate is found
                    flag = True
            if flag is not True:
                duplicate.append(mchDesc)
                match_detail = self.handleMatch(match)
                match_details.append(match_detail)
        return match_details

    def handleMatch(self,match):
        series = match.getAttribute("srs")
        mtype = match.getAttribute("type")
        match_desc = match.getAttribute("mchDesc")
        mground = match.getAttribute("grnd")
        states = match.getElementsByTagName("state")
        for state in states:
            match_cstate = state.getAttribute("mchState")
            mstatus = state.getAttribute("status")
        batting_team = match.getElementsByTagName("btTm")
        bowling_team = match.getElementsByTagName("blgTm")
        batting_team_name = batting_team[0].getAttribute("sName")
        bowling_team_name = bowling_team[0].getAttribute("sName")
        batting_innings = match.getElementsByTagName("Inngs")
        bat_runs = batting_innings[0].getAttribute("r")
        bat_overs = batting_innings[0].getAttribute("ovrs")
        bat_wkts = batting_innings[0].getAttribute("wkts")
        bowling_innings = match.getElementsByTagName("Inngs")
        bowl_runs = bowling_innings[0].getAttribute("r")
        bowl_overs = bowling_innings[0].getAttribute("ovrs")
        bowl_wkts = bowling_innings[0].getAttribute("wkts")
        return { "Series": series, "Match Format": mtype, "Team":match_desc, "Venue":mground, "Match State":match_cstate,"Match Status":mstatus, "Batting team":batting_team_name, "Bowling team":bowling_team_name, batting_team_name + " Runs":bat_runs, batting_team_name + " Overs":bat_overs, batting_team_name + " Wickets":bat_wkts, bowling_team_name + " Runs": bowl_runs, bowling_team_name + " Overs"+ bowl_overs, bowling_team_name + " Wickets": bowl_wkts }

if __name__ == '__main__':
    cric = CricbuzzParser(None)
    match = cric.getXml(None)
    det = cric.handleMatches(match)
    print det


        
