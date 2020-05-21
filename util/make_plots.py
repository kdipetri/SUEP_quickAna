import ROOT
from array import array
from plothelper import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)

setStyle()

def adjust(hist):
    name = hist.GetName()
    #if "ntracks" in name: hist.Rebin()
    if "ntracks" in name: hist.GetXaxis().SetRangeUser(0,600)
    #if "npfs" in name: hist.Rebin()
    if "npfs" in name: 
        hist.GetXaxis().SetRangeUser(0,600)
    if "nneutrals" in name: 
        hist.GetXaxis().SetRangeUser(0,600)
        hist.GetXaxis().SetTitle("n neutrals")
    return

def clean1D(hist):
    # Clean
    adjust(hist)
    hist.SetLineWidth(2)
    hist.GetYaxis().SetNdivisions(505)
    hist.GetXaxis().SetNdivisions(505)
    hist.SetDirectory(0)
    hist.Scale(1.0/hist.Integral(0,-1))
    return hist

def get1D(mMed,mDark,temp,decay,histname):

    # Get hist
    filename = "outputs/hist_mMed-{}_mDark-{}_temp-{}_decay-{}.root".format(mMed,mDark,temp,decay)
    f = ROOT.TFile.Open(filename)
    hist = f.Get(histname)
    clean1D(hist)

    return hist

def getQCD(histname):

    # Get hist
    filename1 = "outputs/hist_QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8.root"# do slicing later
    filename2 = "outputs/hist_QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8.root"# do slicing later
    filename3 = "outputs/hist_QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8.root"# do slicing later
    f1 = ROOT.TFile.Open(filename1)
    f2 = ROOT.TFile.Open(filename2)
    f3 = ROOT.TFile.Open(filename3)
    hist1 = f1.Get(histname)
    hist2 = f2.Get(histname)
    hist3 = f3.Get(histname)
    hist1.Scale(1207) 
    hist2.Scale(119.9) 
    hist3.Scale(25.24) 
    hist1.Add(hist2)
    hist2.Add(hist3)
    clean1D(hist1)

    return hist1

def decay_label(decay):
    if "darkPhoHad" in decay: return "m_{A'}=0.7 GeV"
    if "darkPho" in decay: return "m_{A'}=0.5 GeV"
    if "generic" in decay: return "m_{A'}=m_{#phi}/2, A'#rightarrowu#bar{u}"

def makeROC(hists,labels,filename):
    c = ROOT.TCanvas(filename,"",800,800)

    dy = 0.05*len(hists)
    leg = ROOT.TLegend(0.18,0.86-dy,0.86,0.86)
    leg.SetTextSize(0.04)
    leg.SetBorderSize(0)

    for i,hist in enumerate(hists):
        if "QCD" in labels[i] : hbkg = hist

    ymax = 0
    mgraph = ROOT.TMultiGraph()
    for i,hist in enumerate(hists): 
        if "QCD" in labels[i]: continue
        eff_sig = []
        eff_bkg = []
        err = []
        for b in range(1,hist.GetNbinsX()+1):
            eff_sig.append( hist.Integral(b,-1) )
            eff_bkg.append( hbkg.Integral(b,-1) )
            err.append(0.000000001)
        
        graph = ROOT.TGraphErrors(len(err),array("d",eff_sig),array("d",eff_bkg),array("d",err),array("d",err))

        graph.SetLineColor(colors[i])
        mgraph.Add(graph)
        leg.AddEntry(graph,labels[i],"l")
    
    mgraph.SetTitle(";sig eff;bkg eff")
    mgraph.Draw("AELP")
    mgraph.GetYaxis().SetRangeUser(0.00000001,1)
    leg.Draw()
    c.SetLogy(1)
    c.SetLogx(0)
    c.Print("plots/{}.png".format(filename))
    c.SetLogy(0)
    c.SetLogx(0)
    

def compare1D(hists,labels,filename):
    c = ROOT.TCanvas(filename,"",800,800)

    dy = 0.05*len(hists)
    leg = ROOT.TLegend(0.18,0.86-dy,0.86,0.86)
    leg.SetTextSize(0.04)
    leg.SetBorderSize(0)

    ymax = 0
    for i,hist in enumerate(hists): 
        hist.SetLineColor(colors[i])
        if "QCD" in labels[i]: hist.SetLineColor(ROOT.kBlack) 
        if i==0: hist.Draw("hist")
        else : hist.Draw("hist same")

        if hist.GetMaximum() > ymax: ymax=hist.GetMaximum()

        leg.AddEntry(hist,labels[i],"l")

    

    leg.Draw()
    
    c.SetLogy(1)
    hists[0].GetYaxis().SetRangeUser(0.001,ymax*100)
    c.Print("plots/{}_log.png".format(filename))
    hists[0].GetYaxis().SetRangeUser(0,ymax*1.8)
    c.SetLogy(0)
    c.Print("plots/{}_lin.png".format(filename))

def compareMass(temp,mDark,decay,histname):
    mMeds = []
    mMeds.append(125)
    mMeds.append(400)
    mMeds.append(750)
    mMeds.append(1000)

    hists = []
    labels = []
    for mMed in mMeds:
        hists.append(get1D(mMed,mDark,temp,decay,histname))
        label = "m_{S}=%i GeV, %s"%(mMed,decay_label(decay))
        labels.append(label)

    hists.append(getQCD(histname))
    labels.append("QCD, H_{T}>1 TeV")
    
    compare1D(hists,labels,"compare_mMed/temp{}_mDark{}_decay_{}_{}".format(temp,mDark,decay,histname))
    if histname=="h_pf_ntracks": 
        makeROC(hists,labels,"roc_curve/temp{}_mDark{}_decay_{}_{}".format(temp,mDark,decay,histname))

def compareDecay(mMed,temp,mDark,histname):
    decays = []
    decays.append("darkPho")
    decays.append("darkPhoHad")
    decays.append("generic")

    hists = []
    labels = []
    for decay in decays:
        hists.append(get1D(mMed,mDark,temp,decay,histname))
        label = "m_{S}=%i GeV,%s"%(mMed,decay_label(decay))
        labels.append(label)
    
    compare1D(hists,labels,"compare_decay/mMed{}_temp{}_mDark{}_{}".format(mMed,temp,mDark,histname))


dists=[]
dists.append("h_jet_eta")	
dists.append("h_pf_charged_ptzoom")	
dists.append("h_pf_neutral_e")	
dists.append("h_trigger")	
dists.append("h_jet_pt")	
dists.append("h_trig_ht")	
dists.append("h_pf_charged_qual")	
dists.append("h_pf_neutral_ptzoom")	
dists.append("h_trigger_jet")	
dists.append("h_pf_neutral_pt")	
dists.append("h_pf_npfs")	
dists.append("h_pf_neutral_eta")	
dists.append("h_pf_charged_phi")	
dists.append("h_pf_ntracks")	
dists.append("h_trigger_ht")	
dists.append("h_pf_neutral_phi")	
dists.append("h_trigger_met")	
dists.append("h_trig_njets")	
dists.append("h_trig_mht")	
dists.append("h_mht")	
dists.append("h_ht")	
dists.append("h_pf_charged_pt")	
dists.append("h_njets")	
dists.append("h_jet_phi")	
dists.append("h_pf_charged_eta")	
dists.append("h_pf_nneutrals")

for dist in dists:
    #compareMass(2,2,"darkPho",dist)
    #compareMass(2,2,"darkPhoHad",dist)
    compareMass(2,2,"generic",dist)
    #compareDecay(750,2,2,dist)
