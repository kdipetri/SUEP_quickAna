import ROOT

hists1D = {}
hists2D = {}
plotdir = "plots/hists"

doPng=True
doPdf=False
doC=False

def setStyle():
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetLabelFont(42,"xyz")
    ROOT.gStyle.SetLabelSize(0.05,"xyz")
    ROOT.gStyle.SetTitleFont(42,"xyz")
    ROOT.gStyle.SetTitleFont(42,"t")
    ROOT.gStyle.SetTitleSize(0.06,"xyz")
    ROOT.gStyle.SetTitleSize(0.06,"t")

    ROOT.gStyle.SetPadBottomMargin(0.14)
    ROOT.gStyle.SetPadLeftMargin(0.14)

    ROOT.gStyle.SetPadGridX(0)
    ROOT.gStyle.SetPadGridY(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)

    ROOT.gStyle.SetTitleOffset(1,'y')
    ROOT.gStyle.SetLegendTextSize(0.04)
    ROOT.gStyle.SetGridStyle(3)
    ROOT.gStyle.SetGridColor(14)

    ROOT.gStyle.SetMarkerSize(1.0) #large markers
    ROOT.gStyle.SetHistLineWidth(2) # bold lines
    ROOT.gStyle.SetLineStyleString(2,"[12 12]") # postscript dashes

    #one = ROOT.TColor(2001,0.906,0.153,0.094)
    #two = ROOT.TColor(2002,0.906,0.533,0.094)
    #three = ROOT.TColor(2003,0.086,0.404,0.576)
    #four =ROOT.TColor(2004,0.071,0.694,0.18)
    #five =ROOT.TColor(2005,0.388,0.098,0.608)
    #six=ROOT.TColor(2006,0.906,0.878,0.094)
    #seven=ROOT.TColor(2007,0.99,0.677,0.614)
    #colors = [1,2001,2002,2003,2004]
    return       


def plot1D(name, title, x, nbinsx, xmin, xmax, weight=1.):
    if name in hists1D:
        # fill
        hists1D[name].Fill(x,weight)
    else : 
        # create and fill
        hist = ROOT.TH1F(name, title, nbinsx, xmin, xmax)
        hist.SetDirectory(0)
        hist.Fill(x,weight)
        hists1D[name] = hist
    return

def plot2D(name, title, x, y, nbinsx, xmin, xmax, nbinsy, ymin, ymax, weight=1.):
    if name in hists2D:
        # fill
        hists2D[name].Fill(x,y,weight)
    else : 
        # create and fill
        hist = ROOT.TH2F(name, title, nbinsx, xmin, xmax, nbinsy, ymin, ymax)
        hist.SetDirectory(0)
        hist.Fill(x,weight)
        hists2D[name] = hist

    return

def draw1D(c1,h, drawopt="hist"):  
    c1.cd() 
    c1.Clear()
    h.Draw(drawopt)
    if doPng: c1.Print("{}/{}.png".format(plotdir,h.GetName()))
    if doPdf: c1.Print("{}/{}.pdf".format(plotdir,h.GetName()))
    if doC  : c1.Print("{}/{}.C".format(plotdir,h.GetName()))
    h.Write()
    return 

def draw2D(c2, h, drawopt="COLZ"):  
    c2.cd() 
    c2.Clear()
    c2.SetTopMargin(0.05)
    c2.SetLeftMargin(0.2)
    c2.SetBottomMargin(0.2)
    c2.SetRightMargin(0.2);
    h.Draw(drawopt)

    if doPng: c2.Print("{}/{}.png".format(plotdir,h.GetName()))
    if doPdf: c2.Print("{}/{}.pdf".format(plotdir,h.GetName()))
    if doC  : c2.Print("{}/{}.C".format(plotdir,h.GetName()))
    h.Write()
    return 

def drawAll1D(c1,drawopt="hist"):
    for n, h in hists1D.items():
        draw1D(c1,h, drawopt);
    return

def drawAll2D(c2,drawopt="hist"):
    for n, h in hists2D.items():
        draw2D(c2,h, drawopt);
    return 
