import ROOT
from plothelper import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)

setStyle()

def jetGraph(c,hist):

	c.cd()
	graph = ROOT.TGraph()
	i=0
	
	txt = ROOT.TText()
	txt.SetNDC()
	txt.SetTextFont(42);
	txt.SetTextSize(0.03);
	for xbin in range(1,hist.GetNbinsX()+1):
		for ybin in range(1,hist.GetNbinsY()+1):
			pt  = hist.GetBinContent(xbin,ybin)
			if pt > 0:
				eta = hist.GetXaxis().GetBinCenter(xbin)
				phi = hist.GetYaxis().GetBinCenter(ybin)
				x=((eta+4)/9)#-0.04
				y=((phi+4)/9)+0.15
				#print(x,y)
				txt.DrawText(x,y,"pT={:.0f} GeV".format(pt))
				graph.SetPoint(i,eta,phi)
				i+=1

	graph.SetMarkerStyle(24)
	graph.SetMarkerColor(ROOT.kBlack)
	graph.SetMarkerSize(8)
	graph.Draw("P")
	return graph

def clean2D(hist):
	hist.GetZaxis().SetTitle("pflow pT [GeV]")
	hist.GetZaxis().SetTitleOffset(1.3)
	return

def sample(f):
	s = f.replace("outputs/hist_","")
	s = s.replace(".root","")
	return s

def event(name):
	event=name.replace("h_display_","")
	event=event.replace("_pflow","")
	return event

def getEvents(filename):

	c=ROOT.TCanvas("c","",900,800)
	c.SetRightMargin(0.22)

	f=ROOT.TFile.Open(filename)
	for key in f.GetListOfKeys():
	    name=key.GetName()
	    if "h_display" in name and "pflow" in name:
	        hist=f.Get(name)
	        clean2D(hist)
	        hist.Draw("COLZ")

	        c.Print("plots/displays/{}_{}.png".format(sample(filename),event(name)))

	        hist_jets=f.Get(name.strip("pflow")+"jets")
	        graph_jets=jetGraph(c,hist_jets)
	        graph_jets.Draw("P")

	        c.Print("plots/displays/{}_{}_jets.png".format(sample(filename),event(name)))
            

files=[]
files.append("outputs/hist_TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8.root")
files.append("outputs/hist_TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8.root")
files.append("outputs/hist_TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8.root")
files.append("outputs/hist_QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8.root")
files.append("outputs/hist_QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8.root")
files.append("outputs/hist_QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8.root")
files.append("outputs/hist_mMed-1000_mDark-2_temp-2_decay-generic.root")
files.append("outputs/hist_mMed-125_mDark-2_temp-2_decay-generic.root")
files.append("outputs/hist_mMed-400_mDark-2_temp-2_decay-generic.root")
files.append("outputs/hist_mMed-750_mDark-2_temp-2_decay-generic.root")

for f in files: 
	getEvents(f)
