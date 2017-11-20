import os
import json
from subprocess import Popen, PIPE

isMC = True
#isMC = False

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def splitInBlocks (l, n):
    """split the list l in n blocks of equal size"""
    k = len(l) / n
    r = len(l) % n

    i = 0
    blocks = []
    while i < len(l):
        if len(blocks)<r:
            blocks.append(l[i:i+k+1])
            i += k+1
        else:
            blocks.append(l[i:i+k])
            i += k

    return blocks

###########

njobs = 200
#filelist = open("fileList_MC_RAW.txt")
filelist = open("ZeroBias_Run306091_RAW.txt")
#filelist = open("ZeroBias_Run305310_RAW.txt")
#filelist = open("VBF_HToInvisible_M125_13TeV_powheg_pythia8_RAW.txt")
#filelist = open("VBFHToTauTau_M125_13TeV_powheg_pythia8_FlatPU28to62HcalNZSRAW_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1.txt")
#filelist = open("ZeroBias1-5_Run283171.txt")

#filelist = open("fileList_ZeroBias.txt")
#filelist = open("Data_SingleMu_2016RunB_PromptRecov2_1Luglio.txt")

#folder = "ZeroBias1-5_Run283171_WithMarch2017Layer1_ShapeVeto_04_05_17"
#folder = "MC_L1_Hinv_HF_TPs_29_05_17"
folder = "ZeroBias_Run306091_RAW_mode"
#folder = "ZeroBias_Run305310_RAW_mode"
#folder = "MC_L1_May2017Layer1_HF_TPs_17_05_17"
#folder = "MC_L1_May2017Layer1_HF_TPs_29_05_17"
#folder = "Data_ZeroBias_Run277420_12x12"
#folder = "MC_RAW_12x12"
#folder = "MC_RAW_9x9"
#folder = "testSubmitT3TAndP2Luglio"

JSONfile = "/home/llr/cms/davignon/json_DCSONLY.txt"
#JSONfile = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-275125_13TeV_PromptReco_Collisions16_JSON.txt"

###########

os.system ('source /opt/exp_soft/cms/t3/t3setup')

os.system('mkdir ' + folder)
files = [f.strip() for f in filelist]
print "Input has" , len(files) , "files" 
if njobs > len(files) : njobs = len(files)
filelist.close()

fileblocks = splitInBlocks (files, njobs)

from das_client import get_data

for idx, block in enumerate(fileblocks):
    #print idx, block

    outRootName = folder + '/Ntuple_' + str(idx) + '.root'
    outJobName  = folder + '/job_' + str(idx) + '.sh'
    outListName = folder + "/filelist_" + str(idx) + ".txt"
    outLogName  = os.getcwd() + "/" + folder + "/log_" + str(idx) + ".txt"

    jobfilelist = open(outListName, 'w')
    for f in block: jobfilelist.write(f+"\n")
    jobfilelist.close()

    if not isMC:
        cmsRun = "cmsRun reEmulL1_ZeroBias.py maxEvents=-1 inputFiles_load="+outListName + " outputFile="+outRootName + " >& " + outLogName
        #cmsRun = "cmsRun reEmulL1_ZeroBias.py maxEvents=-1 inputFiles_load="+outListName + " outputFile="+outRootName + " JSONfile="+JSONfile + " >& " + outLogName
    else:
        cmsRun = "cmsRun reEmulL1_MC_L1Only.py maxEvents=-1 inputFiles_load="+outListName + " outputFile="+outRootName + " >& " + outLogName

    skimjob = open (outJobName, 'w')
    skimjob.write ('#!/bin/bash\n')
    skimjob.write ('export X509_USER_PROXY=~/.t3/proxy.cert\n')
    skimjob.write ('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
    skimjob.write ('cd %s\n' % os.getcwd())
    skimjob.write ('export SCRAM_ARCH=slc6_amd64_gcc472\n')
    skimjob.write ('eval `scram r -sh`\n')
    skimjob.write ('cd %s\n'%os.getcwd())
    skimjob.write (cmsRun+'\n')
    skimjob.close ()

    os.system ('chmod u+rwx ' + outJobName)
    command = ('/opt/exp_soft/cms/t3/t3submit_new -long \'' + outJobName +"\'")
#    command = ('/opt/exp_soft/cms/t3/t3submit_new -short -q cms \'' + outJobName +"\'")
    print command
    #os.system (command)
