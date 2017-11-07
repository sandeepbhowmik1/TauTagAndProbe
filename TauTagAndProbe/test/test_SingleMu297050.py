import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Config as cms
process = cms.Process("TagAndProbe")

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
options.outputFile = 'NTuple_SingleMu.root'
options.inputFiles = []
options.maxEvents  = -999
options.parseArguments()



# START ELECTRON CUT BASED ID SECTION
#
# Set up everything that is needed to compute electron IDs and
# add the ValueMaps with ID decisions into the event data stream
#

# Load tools and function definitions
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

process.load("RecoEgamma.ElectronIdentification.ElectronMVAValueMapProducer_cfi")


#**********************
dataFormat = DataFormat.MiniAOD
switchOnVIDElectronIdProducer(process, dataFormat)
#**********************

process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")
# overwrite a default parameter: for miniAOD, the collection name is a slimmed one
process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag('slimmedElectrons')

from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry
process.egmGsfElectronIDSequence = cms.Sequence(process.egmGsfElectronIDs)

# Define which IDs we want to produce
# Each of these two example IDs contains all four standard 
my_id_modules =[
'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',    # both 25 and 50 ns cutbased ids produced
'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_50ns_V1_cff',
'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',                 # recommended for both 50 and 25 ns
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff', # will not be produced for 50 ns, triggering still to come
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',    # 25 ns trig
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_50ns_Trig_V1_cff',    # 50 ns trig
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',   #Spring16
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff',   #Spring16 HZZ

] 


#Add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)


egmMod = 'egmGsfElectronIDs'
mvaMod = 'electronMVAValueMapProducer'
regMod = 'electronRegressionValueMapProducer'
egmSeq = 'egmGsfElectronIDSequence'
setattr(process,egmMod,process.egmGsfElectronIDs.clone())
setattr(process,mvaMod,process.electronMVAValueMapProducer.clone())
setattr(process,regMod,process.electronRegressionValueMapProducer.clone())
setattr(process,egmSeq,cms.Sequence(getattr(process,mvaMod)*getattr(process,egmMod)*getattr(process,regMod)))
process.electrons = cms.Sequence(getattr(process,mvaMod)*getattr(process,egmMod)*getattr(process,regMod))





if not isMC:
    from Configuration.AlCa.autoCond import autoCond
    process.GlobalTag.globaltag = '92X_dataRun2_HLT_v3'
    process.load('TauTagAndProbe.TauTagAndProbe.tagAndProbe_cff')
    process.TagAndProbe.useMassCuts = cms.bool(False)
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            '/store/data/Run2017B/SingleMuon/RAW-RECO/MuTau-PromptReco-v1/000/297/488/00000/0CAAC254-9D5B-E711-8206-02163E01A792.root'
        ),
    )



else:
    process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_miniAODv2' #MC 25 ns miniAODv2
    # process.GlobalTag.globaltag = '76X_dataRun2_16Dec2015_v0'
    process.load('TauTagAndProbe.TauTagAndProbe.MCanalysis_cff')
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(            
            '/store/mc/RunIISpring16MiniAODv2/GluGluHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU20to70HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/50000/B0D22F36-9567-E611-A5FB-0CC47A4DEE76.root'
        )
    )

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

process.p = cms.Path(
    process.TAndPseq +
    process.NtupleSeq
)

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Adding ntuplizer
process.TFileService=cms.Service('TFileService',fileName=cms.string(options.outputFile))
