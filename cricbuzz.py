#!/usr/bin/python

import xml.dom.minidom
import urllib2

class CricbuzzParser():
    
    def __init__(self):
        # self.getXml(url)
        pass
       
    def getXml(self):
        #Change coding here
        r = urllib2.Request("http://synd.cricbuzz.com/j2me/1.0/livematches.xml",
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8"})
        f = urllib2.urlopen(r)
        doc = xml.dom.minidom.parse(f)
        node = doc.documentElement
        matches = node.getElementsByTagName("match")
        return matches

    def handleMatches(self,matches):
        """This function handles the element <match> and
        avoids duplicate matches to be processed. """
        duplicate = []
        match_details = []
        mchDesc = matches[0].getAttribute("mchDesc")
        duplicate.append(mchDesc)
        match_detail = self.handleMatch(matches[0])
        match_details.append(match_detail)
        match_detail = self.handleTestMatch(matches[0])
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
                match_detail = self.handleTestMatch(match)
                match_details.append(match_detail)
        return match_details

    def handleTestMatch(self,match):
        """For handling Test Matches.
        To Do: Write Code for Parsing Innings detail"""
        series = match.getAttribute("srs")
        mtype = match.getAttribute("type")
        if mtype != "TEST":
            return None
        else:
            inngs = []
            match_desc = match.getAttribute("mchDesc")
            mground = match.getAttribute("grnd")
            match_of_the_series =  match.getAttribute("mnum")
            states = match.getElementsByTagName("state")
            batting_team = match.getElementsByTagName("btTm")
            bowling_team = match.getElementsByTagName("blgTm")
            batting_team_name = batting_team[0].getAttribute("sName")
            bowling_team_name = bowling_team[0].getAttribute("sName")
            bowling_innings = bowling_team[0].getElementsByTagName("Inngs")
            batting_innings = batting_team[0].getElementsByTagName("Inngs")

            for i in range (len(batting_innings)):
                bat_runs = {"Runs": batting_innings[i].getAttribute("r")}
                bat_overs = {"Overs": batting_innings[i].getAttribute("ovrs")}
                bat_wkts = {"Wickets": batting_innings[i].getAttribute("wkts")}
                desc1 = {"Desc": batting_innings[i].getAttribute("desc")}
                inngs_detail = [desc1,bat_runs,bat_wkts,bat_overs]
                inngs.append(inngs_detail)
            inngs.insert(0,"Team:" + batting_team_name)
            batting_team_inngs = inngs
            inngs = []
           
            for i in range (len(bowling_innings)):
                bowl_runs = {"Runs": bowling_innings[i].getAttribute("r")}
                bowl_overs = {"Overs": bowling_innings[i].getAttribute("ovrs")}
                bowl_wkts = {"Wickets": bowling_innings[i].getAttribute("wkts")}
                desc1 = {"Desc": bowling_innings[i].getAttribute("desc")}
                inngs_detail = [desc1,bowl_runs,bowl_wkts,bowl_overs]
                inngs.append(inngs_detail)
            inngs.insert(0,"Team:" + bowling_team_name)
            bowling_team_inngs = inngs

            for state in states:
                match_cstate = state.getAttribute("mchState")
                mstatus = state.getAttribute("status")
                if mstatus.startswith("Starts") or mstatus.startswith("Coming"):
                    return None       #Match hasn't started Yet.

        return {"Series": series,"Match Format":"TEST","Team":match_desc,"Venue":mground,"Match State":match_cstate,"Match Status":mstatus,"Match Details":{"Batting Team":batting_team_inngs,"Bowling Team":bowling_team_inngs}} 
        
            
    def handleMatch(self,match):
        """Handles ODI and T20 matches"""
        bowl_runs  = None
        bowl_wkts = None
        bowl_overs = None
        series = match.getAttribute("srs")
        mtype = match.getAttribute("type")
        if mtype == "TEST":
            return None
        match_desc = match.getAttribute("mchDesc")
        mground = match.getAttribute("grnd")
        states = match.getElementsByTagName("state")
        for state in states:
            match_cstate = state.getAttribute("mchState")
            mstatus = state.getAttribute("status")
            if mstatus.startswith("Starts") or mstatus.startswith("Coming"):
                return None       #Match hasn't started Yet.
        try:
            batting_team = match.getElementsByTagName("btTm")
            bowling_team = match.getElementsByTagName("blgTm")
            batting_team_name = batting_team[0].getAttribute("sName")
            bowling_team_name = bowling_team[0].getAttribute("sName")
            innings = match.getElementsByTagName("Inngs")
            bat_runs = innings[0].getAttribute("r")
            bat_overs = innings[0].getAttribute("ovrs")
            bat_wkts = innings[0].getAttribute("wkts")
        except Exception:
            #Match is comple. Only Result is availabe now and btTm tag has been changed to Tm
            #So, now only status of the match is important. Initialize none to other parameters.
            batting_team = None
            bowling_team = None
            batting_team_name = None
            bowling_team_name = None
            innings = None
            bat_runs = None
            bat_overs = None
            bat_wkts = None
        try:
            bowl_runs = innings[1].getAttribute("r")
            bowl_overs = innings[1].getAttribute("ovrs")
            bowl_wkts = innings[1].getAttribute("wkts")
        except Exception:
            # The opponent team hasn't yet started to Bat.
            pass
        return { "Series": series, "Match Format": mtype, "Team":match_desc, "Venue":mground, "Match State":match_cstate,"Match Status":mstatus, "Batting team":batting_team_name, "Bowling team":bowling_team_name, "Batting Team Runs":bat_runs, "Batting Team Overs":bat_overs, "Batting Team Wickets":bat_wkts, "Bowling Team Runs":bowl_runs, "Bowling Team Overs": bowl_overs, "Bowling Team Wickets": bowl_wkts }

if __name__ == '__main__':
    cric = CricbuzzParser()
    match = cric.getXml()
    details = cric.handleMatches(match) #Returns Match details as a Dictionary. Parse it according to requirements.
    # print details
    
