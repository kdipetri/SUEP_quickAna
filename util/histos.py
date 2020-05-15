import ROOT
from DataFormats.FWLite import Events, Handle
from plothelper import *
import sys
import time


def getSample(f):
    # mScalar, mPion, T
    f = f.replace("step4_MINIAOD_mMed-","")
    f = f.replace("_13TeV-pythia8_n-10_part-1.root","")
    f = f.replace("infiles/","")
    f = f.replace(".txt","")
    return f 

def getTriggerList():
    f="util/triggers.txt"
    trigs=[]
    for line in open(f,"r").readlines():
        if "#" not in line: 
            trigs.append(line.split()[0])
    return trigs

def triggerPlots(event,triggerBits,triggerPrescales,trigger_list):
       
    return passed_trigger

def loop(f,sample):

    # get events
    # Events takes either
    # - single file name
    # - list of file names
    # - VarParsing options
    events = Events( f )
    
    # create handles and labels outside of loop
    triggerBits = Handle('edm::TriggerResults')
    triggerBitLabel = ("TriggerResults","","HLT")
    triggerPrescales = Handle("pat::PackedTriggerPrescales")
    triggerPrescaleLabel  =  "patTrigger"

    jet_handle = Handle('std::vector<pat::Jet>')
    jet_label = ("slimmedJets")
    met_handle = Handle('std::vector<pat::MET>')
    met_label = ("slimmedMETs")

    pflow_handle  = Handle ('std::vector<pat::PackedCandidate>')
    pflow_label   = ("packedPFCandidates")
    lostTracks_handle  = Handle ('std::vector<pat::PackedCandidate>')
    lostTracks_label   = ("packedPFCandidates")

    trigger_list = getTriggerList()

    
    # loop over events
    ievt = 0
    for event in events:
        
        # for debug
        #print(ievt)
        ievt+=1
        if ievt > 100: break 

        if ievt%100==0 : print(ievt)
    
        # use getByLabel, just like in cmsRun
        event.getByLabel(triggerBitLabel, triggerBits)
        event.getByLabel(triggerPrescaleLabel, triggerPrescales)
        event.getByLabel(pflow_label, pflow_handle)
        event.getByLabel(lostTracks_label, lostTracks_handle)
        event.getByLabel(met_label, met_handle)
        event.getByLabel(jet_label, jet_handle)

        # get the product
        pflow_cands   = pflow_handle.product()
        lost_tracks = lostTracks_handle.product()
        jets = jet_handle.product()
        met = met_handle.product()

        # * 
        # Trigger Plots  
        # * 
        passed_trigger=0
        passed_ht=0
        passed_met=0
        passed_jet=0
        names = event.object().triggerNames(triggerBits.product())
        for i in range(triggerBits.product().size()):
            trigger  = names.triggerName(i)
            prescale = triggerPrescales.product().getPrescaleForIndex(i)
            passed   = triggerBits.product().accept(i)

            for trig in trigger_list:  
                if trig in trigger and passed==1: 
                    passed_trigger=1 
                    if "HLT_PFHT" in trigger: passed_ht=1
                    elif "MET" in trigger   : passed_met=1
                    elif "Jet" in trigger   : passed_jet=1
            
            #for path in trigger_paths: 
            #    if path in trigger and prescale==1:  
            #        if ievt==1: print("Trigger {} : pass {}".format(trigger,passed)) 
            #        if passed==1 : print("Trigger {} : pass {}".format(trigger,passed))

        plot1D("h_trigger"     ,";passed" , passed_trigger ,2,-0.5,1.5)        
        plot1D("h_trigger_ht"  ,";passed" , passed_ht      ,2,-0.5,1.5)        
        plot1D("h_trigger_met" ,";passed" , passed_met     ,2,-0.5,1.5)        
        plot1D("h_trigger_jet" ,";passed" , passed_jet     ,2,-0.5,1.5)        


        # *
        # Jets
        # * 
        njets_30=0
        ht=0# scalar sum of jets with pt 30, eta<2.4
        mht=0# negative vector sum of jets with pt 30, eta<2.4
        mht_vector = ROOT.TLorentzVector()
        p4 = ROOT.TLorentzVector()
        for jet in jets:  
            if abs(jet.eta())<2.4 and jet.pt() > 30:
                njets_30+=1
                ht+=jet.pt()
                p4.SetPtEtaPhiE(jet.pt(),jet.eta(),jet.phi(),jet.energy())
                mht_vector+=p4
                plot1D("h_jet_pt" ,";jet pt" , jet.pt() , 30,0,100)
                plot1D("h_jet_eta",";jet eta", jet.eta(), 30,-3.5,3.5)
                plot1D("h_jet_phi",";jet phi", jet.phi(), 30,-3.5,3.5)
        
        plot1D("h_njets",";njets", njets_30, 15,-0.5,14.5)
        plot1D("h_ht"   ,";ht"   , ht      , 50,0,2000)
        plot1D("h_mht"  ,";mht"  , mht_vector.Pt(), 30,0,1000)
        if passed_trigger:
            plot1D("h_trig_njets",";njets", njets_30, 15,-0.5,14.5)
            plot1D("h_trig_ht"   ,";ht"   , ht      , 50,0,2000)
            plot1D("h_trig_mht"  ,";mht"  , mht_vector.Pt(), 30,0,1000)


        # *
        # Particle Flow Candidates 
        # * 
        n_tracks=0
        n_neutral=0
        n_pcand=0
        for p in pflow_cands: 
            # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2017#Packed_ParticleFlow_Candidates
            if p.fromPV() < 2 : continue # isolation definition
            if abs(p.eta()) > 2.5 : continue #eta
            if p.pt() < 1.0 : continue # re-evaluate later
            if p.charge()!=0 and p.trackHighPurity()==0 : continue #tracks high purity
            
            n_pcand+=1
            
            if p.charge() != 0: # track 
                n_tracks+=1
                plot1D("h_pf_charged_pt"    ,";pt"     , p.pt()    , 100,0,100)
                plot1D("h_pf_charged_ptzoom",";pt"     , p.pt()    , 100,0,10)
                plot1D("h_pf_charged_qual"  ,";quality", p.trackHighPurity(), 2,-0.5,1.5)
                plot1D("h_pf_charged_eta"   ,";eta"    , p.eta()   , 100,-3.5,3.5)
                plot1D("h_pf_charged_phi"   ,";phi"    , p.phi()   , 100,-3.5,3.5)
            else : # neutral 
                n_neutral+=1
                plot1D("h_pf_neutral_pt"    ,";pt"    , p.pt()    , 100,0,100)
                plot1D("h_pf_neutral_ptzoom",";pt"    , p.pt()    , 100,0,10)
                plot1D("h_pf_neutral_e"     ,";energy", p.energy(), 100,0,100)
                plot1D("h_pf_neutral_eta"   ,";eta"   , p.eta()   , 100,-3.5,3.5)
                plot1D("h_pf_neutral_phi"   ,";phi"   , p.phi()   , 100,-3.5,3.5)

            # eventually, are pflow objects in jets? 
            # eventually are jets truth matched to dark sector decay products or isr?
            #print("pt",p.pt())
            #print("eta",p.eta())
            #print("phi",p.phi())
            #print("e",p.energy())
            #print("charge",p.charge())
        plot1D("h_pf_npfs"         , ";npfs"   , n_pcand       ,100,0,1000)
        plot1D("h_pf_ntracks"      , ";ntracks", n_tracks      ,100,0,1000)
        plot1D("h_pf_nneutrals"    , ";ntracks", n_neutral     ,100,0,1000)

    
    # save output
    fout = ROOT.TFile.Open("outputs/hist_{}.root".format(sample),"RECREATE")
    c1 = ROOT.TCanvas("c1","",900,800)
    c2 = ROOT.TCanvas("c2","",900,800)
    drawAll1D(c1)
    drawAll2D(c2)

    return

    
def makeHistos():

    start = time.time()
    setStyle() 
    
    # Get input files
    path = "root://cmseos.fnal.gov//store/user/kdipetri/SUEP/Production_v0.0/2018/MINIAOD"
    #infile = "step4_MINIAOD_mMed-1000_mDark-2_temp-2_decay-generic_13TeV-pythia8_n-10_part-1.root"
    #infile = "infiles/mMed-125_mDark-2_temp-2_decay-generic.txt"
    #infile = "infiles/mMed-400_mDark-2_temp-2_decay-generic.txt"
    infile = "infiles/mMed-750_mDark-2_temp-2_decay-generic.txt"
    #infile = "infiles/mMed-1000_mDark-2_temp-2_decay-generic.txt"
    if len(sys.argv) > 1: 
        infile = sys.argv[1]
    
    if "root" in infile : 
        f = "{}/{}".format(path,infile) 
    elif "txt" in infile : 
        f = []
        for line in open(infile,"r").readlines(): 
            filename = "{}/{}".format(path,line.strip())
            f.append(filename)    
    else : print("ERROR unknown input format")

    # get sample name and loop
    sample = getSample(infile)
    print(sample)
    loop(f,sample) 
    
    
    print("It took {} s".format(time.time()-start))

if __name__ == "__main__":
    makeHistos()
