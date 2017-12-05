import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Config as cms
process = cms.Process("TagAndProbe")

#isMC = True
isMC = False

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

#### handling of cms line options for tier3 submission
#### the following are dummy defaults, so that one can normally use the config changing file list by hand etc.

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
options.outputFile = 'NTuple.root'
options.inputFiles = []
options.maxEvents  = -999
options.parseArguments()

if not isMC: # will use 92X
    from Configuration.AlCa.autoCond import autoCond
    process.GlobalTag.globaltag = '92X_dataRun2_HLT_v7'
    process.load('TauTagAndProbe.TauTagAndProbe.DataAnalysis_noTagAndProbe_cff')
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            '/store/data/Run2017F/SingleMuon/MINIAOD/PromptReco-v1/000/306/456/00000/2EA49EC5-EAC7-E711-A9C5-FA163E83AE5D.root'
            #'/store/data/Run2017C/SingleMuon/MINIAOD/12Sep2017-v1/00000/001BA513-7DBB-E711-B839-7CD30ACE1762.root'
            #'/store/data/Run2017A/SingleMuon/MINIAOD/PromptReco-v2/000/296/168/00000/084C505D-784C-E711-8140-02163E019DA4.root'
            #'/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/282/092/00000/DE499C8E-1B8B-E611-8C93-02163E014207.root'
            #'/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/282/092/00000/ACA10D13-2D8B-E611-820E-FA163E8FD709.root'
            #'/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/282/092/00000/20AE9A37-2D8B-E611-8405-02163E0119B8.root'
            #/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/282/092/00000/1E61B437-358B-E611-91C5-02163E011AEE.root'
            #'/store/data/Run2016H/SingleMuon/MINIAOD/PromptReco-v2/000/282/092/00000/BC5DD41A-2E8B-E611-B4EF-02163E012B59.root'
           #'/store/mc/RunIISpring16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/40000/00200284-F15C-E611-AA9B-002590574776.root',
            # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/082EC2A0-4C28-E611-BC61-02163E014412.root',
            # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/1014078C-4C28-E611-85FB-02163E0141C1.root',
            # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/203E5176-4C28-E611-B4F8-02163E014743.root',
            # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/32508866-4C28-E611-A38D-02163E011BAF.root',
            # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/44AF1068-4C28-E611-80D0-02163E01367B.root',
            # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/5AF4B08A-4C28-E611-AEC9-02163E01342C.root',
            # '/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/6E3FD070-4C28-E611-9A1E-02163E011DC7.root',

            #'/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/7005DB70-4C28-E611-8628-02163E0144DD.root',
            #'/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/7C2CB76B-4C28-E611-8D90-02163E01467F.root',
            #'/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/199/00000/86B68469-4C28-E611-92A6-02163E01419C.root',
            #'/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/275/125/00000/24FC42B2-8036-E611-B42D-02163E012BD1.root'
        ),
        #eventsToProcess = cms.untracked.VEventRange('282092:1057805498')
    )
else:
    process.GlobalTag.globaltag = '92X_upgrade2017_TSG_For90XSamples_V2' #MC 25 ns miniAODv2
    #process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_miniAODv2' #MC 25 ns miniAODv2
    # process.GlobalTag.globaltag = '76X_dataRun2_16Dec2015_v0'
    process.load('TauTagAndProbe.TauTagAndProbe.MCanalysis_noTagAndProbe_cff')
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            '/store/mc/PhaseIFall16MiniAOD/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU28to62HcalNZSRAW_PhaseIFall16_90X_upgrade2017_realistic_v6_C1-v1/00000/182AC7D1-661B-E711-BA96-0242AC130006.root'            
            #'/store/mc/RunIISpring16MiniAODv2/GluGluHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU20to70HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/50000/B0D22F36-9567-E611-A5FB-0CC47A4DEE76.root'
            #'/store/mc/RunIISpring16MiniAODv2/GluGluHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU20to70HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/50000/B0D22F36-9567-E611-A5FB-0CC47A4DEE76.root'
            #'file:B0D22F36-9567-E611-A5FB-0CC47A4DEE76.root'
            #'/store/mc/RunIIFall15MiniAODv2/GluGluToRadionToHHTo2B2Tau_M-700_narrow_13TeV-madgraph/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/60000/2CD9692A-9EB8-E511-A944-FACADE0000C9.root'
            #'/store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/70000/02A85EE9-70BA-E511-A0A2-0CC47A4D7678.root',
            #'/store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/70000/08C274E5-70BA-E511-920F-0CC47A78A458.root',
            #'/store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/70000/06E9C8D6-79BA-E511-9EB0-0CC47A4D7600.root',
            #'/store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/70000/08B579D9-C7B8-E511-861F-00259021A526.root'

            #'/store/mc/RunIISpring16MiniAODv2/GluGluHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/80000/065837E2-DA38-E611-9157-008CFA50291C.root',
            #'/store/mc/RunIISpring16MiniAODv2/GluGluHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/80000/0C6A2B22-DA38-E611-AA0C-842B2B2AB616.root',
            #'/store/mc/RunIISpring16MiniAODv2/GluGluHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/80000/0EB9BEA7-D938-E611-85DD-0242AC130003.root',
            #'/store/mc/RunIISpring16MiniAODv2/GluGluHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/80000/12DC7ABE-DA38-E611-9BA2-0242AC130005.root'

        )
    )

if options.JSONfile:
    print "Using JSON: " , options.JSONfile
    process.source.lumisToProcess = LumiList.LumiList(filename = options.JSONfile).getVLuminosityBlockRange()

if options.inputFiles:
    process.source.fileNames = cms.untracked.vstring(options.inputFiles)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000)
)

if options.maxEvents >= -1:
    process.maxEvents.input = cms.untracked.int32(options.maxEvents)
if options.skipEvents >= 0:
    process.source.skipEvents = cms.untracked.uint32(options.skipEvents)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.p = cms.Path(
    #process.TAndPseq +
    process.NtupleSeq
)

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Adding ntuplizer
process.TFileService=cms.Service('TFileService',fileName=cms.string(options.outputFile))
