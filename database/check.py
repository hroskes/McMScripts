#!/usr/bin/env python

################################
#
# check.py
#
#  Script to check status of requests and save in database
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sqlite3
import argparse
import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
import time


def getRequestSets():
    mcm = restful(dev=False)

    wmLHE_campagin  = "RunIIWinter15wmLHE"
    pLHE_campaign   = "RunIIWinter15pLHE"
    GS_campaign     = "RunIISummer15GS"
    DR_campaign     = "RunIIFall15DR76"
    Mini_campaign   = "RunIIFall15MiniAODv1"
    Miniv2_campaign = "RunIIFall15MiniAODv2"
    status_name = [["LHE_New", "LHE_Validating", "LHE_Validated", "LHE_Defined",
                    "LHE_Approved", "LHE_Submitted", "LHE_Done"],
                   ["GS_New", "GS_Validating", "GS_Validated", "GS_Defined",
                    "GS_Approved", "GS_Submitted", "GS_Done"],
                   ["DR_New", "DR_Validating", "DR_Validated", "DR_Defined",
                    "DR_Approved", "DR_Submitted", "DR_Done"],
                   ["MiniAOD_New", "MiniAOD_Validating", "MiniAOD_Validated",
                    "MiniAOD_Defined", "MiniAOD_Approved", "MiniAOD_Submitted",
                    "MiniAOD_Done"],
                   ["MiniAODv2_New", "MiniAODv2_Validating",
                    "MiniAODv2_Validated", "MiniAODv2_Defined",
                    "MiniAODv2_Approved", "MiniAODv2_Submitted",
                    "MiniAODv2_Done"]]

    conn = sqlite3.connect('EXO_MC_Requests.db')
    c = conn.cursor()
    c.execute('SELECT SetID, Tag FROM RequestSets')
    out = c.fetchall()

    print "Checking:"
    for request in out:
        print request[1]

        campaigns = ["", GS_campaign, DR_campaign, Mini_campaign, Miniv2_campaign]
        req_list = mcm.getA('requests', query='tags={0}'.format(
                request[1]))
        statuses = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        for req in req_list:
            if req['member_of_campaign'] == GS_campaign:
                if req['approval'] == "none" and req['status'] == "new":
                    statuses[1][0] += 1
                if req['approval'] == "validation" and req['status'] == "new":
                    statuses[1][1] += 1
                if req['approval'] == "validation" and req['status'] == "validation":
                    statuses[1][2] += 1
                if req['approval'] == "define" and req['status'] == "defined":
                    statuses[1][3] += 1
                if req['approval'] == "approve" and req['status'] == "approved":
                    statuses[1][4] += 1
                if req['approval'] == "submit" and req['status'] == "submitted":
                    statuses[1][5] += 1
                if req['approval'] == "submit" and req['status'] == "done":
                    statuses[1][6] += 1
        #print statuses
        #print request[0]
        for i in range(len(statuses)):
            for j in range(len(statuses[0])):
                c.execute('UPDATE RequestSets SET {0} = {1} WHERE SetID = {2}'.format(
                        status_name[i][j], statuses[i][j], request[0]))
        time.sleep(0.5)
    conn.commit()
    conn.close()

    return

def main():
    getRequestSets()

    return


if __name__ == '__main__':
    main()
