if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
//Headers for the data items
#endif
void print_data() {
    TFile file("root://cmsxrootd.fnal.gov//store/user/kdipetri/SUEP/Production_v0.0/2018/MINIAOD/step4_MINIAOD_mMed-1000_mDark-2_temp-2_decay-generic_13TeV-pythia8_n-10_part-1.root");

    edm::EventBase const & event = ev;

    for( ev.toBegin(); ! ev.atEnd(); ++ev) {
        fwlite::Handle<std::vector<...> > objs;
        objs.getByLabel(ev,"....");
        std::cout <<" size "<<objs.ptr()->size()<<std::endl;
        edm::Handle<vector<reco::Vertex> > vertices;
        event.getByLabel( edm::InputTag("offlinePrimaryVertices"), vertices);
        ...
    }
}
