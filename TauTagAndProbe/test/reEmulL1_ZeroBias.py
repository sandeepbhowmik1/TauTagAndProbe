import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

isMC = False
#isMC = False

#process = cms.Process("ZeroBias",eras.Run2_2016)
process = cms.Process("ZeroBias",eras.Run2_2017)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

#all above present before
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
#process.load('Configuration.StandardSequences.EndOfProcess_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.load('Configuration.StandardSequences.Services_cff')
#process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
#process.load('FWCore.MessageService.MessageLogger_cfi')
#process.load('Configuration.EventContent.EventContent_cff')
#process.load('Configuration.Geometry.GeometryExtended2016Reco_cff')
#process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')

#process.load('Configuration.StandardSequences.Services_cff')
#process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
#process.load('FWCore.MessageService.MessageLogger_cfi')
#process.load('Configuration.EventContent.EventContent_cff')
#process.load('SimGeneral.MixingModule.mixNoPU_cfi')
#process.load('Configuration.Geometry.GeometryExtended2016Reco_cff')
#process.load('Configuration.StandardSequences.MagneticField_cff')
#process.load('Configuration.StandardSequences.RawToDigi_cff')
#process.load('Configuration.StandardSequences.EndOfProcess_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')



options = VarParsing.VarParsing ('analysis')

options.register ('skipEvents',
                  -1, # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "Number of events to skip")
options.register ('JSONfile',
                  "", # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.string,          # string, int, or float
                  "JSON file (empty for no JSON)")
options.outputFile = 'NTuple_ZeroBias.root'
options.inputFiles = []
options.maxEvents  = -999

options.parseArguments()

import FWCore.Utilities.FileUtils as FileUtils

if not isMC: # will use 80X
    from Configuration.AlCa.autoCond import autoCond
    process.GlobalTag.globaltag = '92X_dataRun2_HLT_v7'
    #process.GlobalTag.globaltag = '80X_dataRun2_Prompt_v8'
    process.load('TauTagAndProbe.TauTagAndProbe.zeroBias_cff')
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            #'file:BCB1EC0B-5E26-E611-8240-02163E0145B8.root'
            '/store/data/Run2017C/ZeroBias/RAW/v1/000/300/806/00000/02C685A4-567D-E711-9C28-02163E0127B8.root',
            #'/store/data/Run2016E/ZeroBias/RAW/v2/000/277/420/00000/02E63363-A052-E611-8FD7-FA163E249562.root'
            #'/store/data/Run2016E/ZeroBias/RAW/v2/000/276/831/00000/04145A1E-A54B-E611-A0C6-FA163E6A5A26.root'
            #'/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/BCB1EC0B-5E26-E611-8240-02163E0145B8.root'
            #'/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/7005DB70-4C28-E611-8628-02163E0144DD.root',
        ),
    )

else: # will use 80X
    from Configuration.AlCa.autoCond import autoCond
    process.GlobalTag.globaltag = '92X_upgrade2017_TSG_For90XSamples_V2'#for VBF Hinv
    #process.GlobalTag.globaltag = '90X_upgrade2017_TSG_Hcal_V3'#for VBF Hinv
    #process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_v14'#for VBF HTT
    #process.GlobalTag.globaltag = 'auto:run2_mc'
    #process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_v6' #MC 25 ns miniAODv2
    #process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_v3' #MC 25 ns miniAODv2
    #process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_miniAODv2' #MC 25 ns miniAODv2
    process.load('TauTagAndProbe.TauTagAndProbe.zeroBias_cff')
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            #'file:BCB1EC0B-5E26-E611-8240-02163E0145B8.root'
            'file:0A3E7062-D365-E611-BCF4-001EC9AF0377.root'
            #'/store/mc/RunIISpring16DR80/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU20to70HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/50000/0A3E7062-D365-E611-BCF4-001EC9AF0377.root'
            #'/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/BCB1EC0B-5E26-E611-8240-02163E0145B8.root'
            #'/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/7005DB70-4C28-E611-8628-02163E0144DD.root',
        ),
    )

process.schedule = cms.Schedule()

## L1 emulation stuff

if not isMC:
    from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAW 
    process = L1TReEmulFromRAW(process)
else:
    from L1Trigger.Configuration.customiseReEmul import L1TReEmulMCFromRAW
    process = L1TReEmulMCFromRAW(process) 
    from L1Trigger.Configuration.customiseUtils import L1TTurnOffUnpackStage2GtGmtAndCalo 
    process = L1TTurnOffUnpackStage2GtGmtAndCalo(process)
    #from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAWsimTP
    #process = L1TReEmulFromRAWsimTP(process)

process.load("L1Trigger.L1TCalorimeter.caloStage2Params_2017_v1_10_mean_inconsistent_cfi")
#process.load("L1Trigger.L1TCalorimeter.caloStage2Params_2017_v1_4_cfi")
#process.load("L1Trigger.L1TCalorimeter.caloStage2Params_2016_v3_2_cfi")

#### handling of cms line options for tier3 submission
#### the following are dummy defaults, so that one can normally use the config changing file list by hand etc.



if options.JSONfile:
    print "Using JSON: " , options.JSONfile
    process.source.lumisToProcess = LumiList.LumiList(filename = options.JSONfile).getVLuminosityBlockRange()

if options.inputFiles:
    process.source.fileNames = cms.untracked.vstring(options.inputFiles)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

if options.maxEvents >= -1:
    process.maxEvents.input = cms.untracked.int32(options.maxEvents)
if options.skipEvents >= 0:
    process.source.skipEvents = cms.untracked.uint32(options.skipEvents)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.load('EventFilter.L1TRawToDigi.caloStage2Digis_cfi')
process.caloStage2Digis.InputLabel = cms.InputTag('rawDataCollector')

process.p = cms.Path (
    process.RawToDigi +
    process.caloStage2Digis +
    process.L1TReEmul +
    process.NtupleZeroBiasSeq
)
process.schedule = cms.Schedule(process.p) # do my sequence pls

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Adding ntuplizer
process.TFileService=cms.Service('TFileService',fileName=cms.string(options.outputFile))
