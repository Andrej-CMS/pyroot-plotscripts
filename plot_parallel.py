from scriptgenerator import *
from plotutils import *
import sys

path='/nfs/dust/cms/user/hmildner/trees1122/'
name='allplots'
sel_singleel="(N_LooseMuons==0)" # need to veto muon events in electron dataset to avoid double countung
sel_singlemu="(N_LooseElectrons==0)" # and vice versa...
mcweight='(2.54*Weight_PV)*(N_LooseElectrons==0||N_LooseMuons==0)' # some weights are only applied on mc
# selections for categories
sel_all="((N_TightLeptons==1)*(N_LooseLeptons==1)*(N_BTagsM>=2)*(N_Jets>=4))" # l+jets channel
sel_muchan="((N_TightMuons==1)*(N_LooseMuons==1)*(N_LooseElectrons==0)*(N_BTagsM>=2)*(N_Jets>=4))" # e+jets channel
sel_echan="((N_TightElectrons==1)*(N_LooseElectrons==1)*(N_LooseMuons==0)*(N_BTagsM>=2)*(N_Jets>=4))" # mu+jets channel
sel_zmu="((N_TightMuons==2)*(N_LooseMuons==2)*(N_LooseElectrons==0)*(DiMuon_M>81)*(DiMuon_M<101))" # z-control region for elel
sel_zel="((N_TightElectrons==2)*(N_LooseElectrons==2)*(N_LooseMuons==0)*(DiElectron_M>81)*(DiElectron_M<101))" # z-control region for mumu
sel_wmu="((N_TightMuons==1)*(N_LooseMuons==1)*(N_LooseElectrons==0)*(N_Jets>=0))" # W to mu
sel_wel="((N_TightElectrons==1)*(N_LooseElectrons==1)*(N_LooseMuons==0)*(N_Jets>=0))" # W to el
sel_pretagmu="((N_TightMuons==1)*(N_LooseMuons==1)*(N_LooseElectrons==0)*(N_Jets>=4))" # e+jets channel without btag
sel_pretagel="((N_TightElectrons==1)*(N_LooseElectrons==1)*(N_LooseMuons==0)*(N_Jets>=4))" # mu+jets channel without btag
sel_notagmu="((N_TightMuons==1)*(N_LooseMuons==1)*(N_LooseElectrons==0)*(N_BTagsM==0)*(N_Jets>=4))" # e+jets channel without btag
sel_notagel="((N_TightElectrons==1)*(N_LooseElectrons==1)*(N_LooseMuons==0)*(N_BTagsM==0)*(N_Jets>=4))" # mu+jets channel without btag
catsels=[sel_all,sel_echan,sel_muchan,sel_zmu,  sel_zel,   sel_wmu,  sel_wel, sel_pretagmu,sel_pretagel,sel_notagmu,sel_notagel]
catnames=["",    "_echan", "_muchan","_ztomumu","_ztoelel","_wtomu","_wtoel","_pretagmu",   "_pretagel","_notagmu",  "_notagel"] # names of categories
cattitles=["1 lepton, #geq 4 jets #geq 2 tags","1 #mu #geq 4 jets #geq 2 tags","1 electron #geq 4 jets #geq 2 tags","2 #mu, |m_{#mu#mu}-m_{Z}| #leq 10 GeV","2 e, |m_{ee}-m_{Z}| #leq 10 GeV","1 #mu","1 electron","1 #mu #geq 4 jets","1 electron #geq 4 jets","1 #mu #geq 4 jets == 0 tags","1 electron #geq 4 jets == 0 tags"]
# data samples (name, color, path to files, selection, nickname_without_special_characters,optional: number of events for cross check)
samples_data=[Sample('SingleMu',ROOT.kBlack,path+'/mu_*/*nominal*.root',sel_singlemu,'SingleMu',8427020+6226674),
              Sample('SingleEl',ROOT.kBlack,path+'/el_*/*nominal*.root',sel_singleel,'SingleEl',4692772+3638693)
              ]

# mc samples
samples=[Sample('t#bar{t}H',ROOT.kBlue+1,path+'/ttH*/*nominal*.root',mcweight,'ttH',1822862) ,     
         Sample('t#bar{t}',ROOT.kRed+1,path+'/ttbar/*nominal*.root',mcweight,'ttbar',24010004) ,     
         Sample('Single Top',ROOT.kMagenta,path+'/st*/*nominal*.root',mcweight,'SingleTop',2301345) , 
         Sample('W+jets',ROOT.kGreen-3,path+'/Wjets/*nominal*.root',mcweight,'Wjets',13599271) , 
         Sample('Z+jets',ROOT.kAzure-2 ,path+'/Zjets_*/*nominal*root',mcweight,'Zjets',10352375) , 
         Sample('QCD',ROOT.kYellow ,path+'/QCD*/*nominal*root',mcweight,'QCD',9979) , 
]

# book plots
plots=[Plot(ROOT.TH1F("JT" ,"jet-tag categories",9,-0.5,8.5),"3*max(min(N_BTagsM-2,2),0)+max(min(N_Jets-4,2),0)","(N_BTagsM>=2&&N_Jets>=4)"),
       Plot(ROOT.TH1F("N_Jets","Number of ak4 jets",11,-0.5,10.5),"N_Jets",''),
       Plot(ROOT.TH1F("N_BTagsM","Number of b-tags",6,-0.5,5.5),"N_BTagsM",''),
       Plot(ROOT.TH1F("CSV0","B-tag of leading jet",44,-.1,1),"Jet_CSV[0]",''),
       Plot(ROOT.TH1F("CSV1","B-tag of second jet",44,-.1,1),"Jet_CSV[1]",''),
       Plot(ROOT.TH1F("CSV","B-tag of all jets",44,-.1,1),"Jet_CSV",''),
       Plot(ROOT.TH1F("CSVpt1","B-tag of jets with p_{T} between 30 and 40 GeV",44,-.1,1),"Jet_CSV",'Jet_Pt>30&&Jet_Pt<40'),
       Plot(ROOT.TH1F("CSVpt2","B-tag of jets with p_{T} between 40 and 60 GeV",44,-.1,1),"Jet_CSV",'Jet_Pt>40&&Jet_Pt<60'),
       Plot(ROOT.TH1F("CSVpt3","B-tag of jets with p_{T} between 60 and 100 GeV",44,-.1,1),"Jet_CSV",'Jet_Pt>60&&Jet_Pt<100'),
       Plot(ROOT.TH1F("CSVpt4","B-tag of jets with p_{T} over 100 GeV",44,-.1,1),"Jet_CSV",'Jet_Pt>100'),
       Plot(ROOT.TH1F("CSVeta1","B-tag of jets with abs(#eta) between 0 and 0.4",44,-.1,1),"Jet_CSV",'fabs(Jet_Eta)<0.4'),
       Plot(ROOT.TH1F("CSVeta2","B-tag of jets with abs(#eta) between 0.4 and 0.8",44,-.1,1),"Jet_CSV",'fabs(Jet_Eta)>0.4&&fabs(Jet_Eta)<0.8'),
       Plot(ROOT.TH1F("CSVeta3","B-tag of jets with abs(#eta) between 0.8 and 1.6",44,-.1,1),"Jet_CSV",'fabs(Jet_Eta)>0.8&&fabs(Jet_Eta)<1.6'),
       Plot(ROOT.TH1F("CSVeta4","B-tag of jets with abs(#eta) between 0.8 and 1.6",44,-.1,1),"Jet_CSV",'fabs(Jet_Eta)>1.6'),
       
       Plot(ROOT.TH1F("pt1","p_{T} of leading jet",50,0,500),"Jet_Pt[0]",''),
       Plot(ROOT.TH1F("pt2","p_{T} of second jet",50,0,500),"Jet_Pt[1]",''),
       Plot(ROOT.TH1F("eta1","#eta of leading jet",50,-2.5,2.5),"Jet_Eta[0]",''),
       Plot(ROOT.TH1F("eta2","#eta of second jet",50,-2.5,2.5),"Jet_Eta[1]",''),
       Plot(ROOT.TH1F("phij1","#phi of leading jet",64,-3.2,3.2),"Jet_Phi[0]",''),
       Plot(ROOT.TH1F("phij2","#phi of second jet",64,-3.2,3.2),"Jet_Phi[1]",''),
       Plot(ROOT.TH1F("Evt_HT_Jets","Sum p_{T} jets",75,0,1500),"Evt_HT_Jets",''),
       Plot(ROOT.TH1F("N_BoostedJets","Number of CA 1.5 jets",5,-0.5,4.5),"N_BoostedJets",''),
       Plot(ROOT.TH1F("ptalljets","p_{T} of all jets",60,0,300),"Jet_Pt",''),
       Plot(ROOT.TH1F("csvalljets","csv of all jets",44,-.1,1),"Jet_CSV",''),
       Plot(ROOT.TH1F("leppt","lepton p_{T}",50,0,200),"LooseLepton_Pt[0]"),
       Plot(ROOT.TH1F("lepeta","lepton #eta",50,-2.5,2.5),"LooseLepton_Eta[0]"),
       Plot(ROOT.TH1F("eliso","electron relative isolation",50,0,0.5),"Electron_RelIso[0]"),
       Plot(ROOT.TH1F("muiso","muon relative isolation",50,0,0.5),"Muon_RelIso[0]"),
       Plot(ROOT.TH1F("MET","MET",50,0,200),"Evt_Pt_MET"),
       Plot(ROOT.TH1F("METphi","MET #phi",64,-3.2,3.2),"Evt_Phi_MET"),
       Plot(ROOT.TH1F("N_PrimaryVertices","Reconstructed primary vertices",31,-.5,30.5),"N_PrimaryVertices",''),
       ]
# plot parallel -- alternatively there are also options to plot more traditional that also return lists of histo lists
outputpath=plotParallel(name,2000000,plots,samples+samples_data,catnames,catsels)
listOfHistoLists=createHistoLists_fromSuperHistoFile(outputpath,samples,plots,1,catnames)
listOfHistoListsData=createHistoLists_fromSuperHistoFile(outputpath,samples_data,plots,1,catnames)
ntables=0
# do some post processing
for hld,hl in zip(listOfHistoListsData,listOfHistoLists):
    if "JT" in hld[0].GetName():
        for h in hld+hl:
            h.GetXaxis().SetBinLabel(1,'4j2t')
            h.GetXaxis().SetBinLabel(2,'5j2t')
            h.GetXaxis().SetBinLabel(3,'6j2t')
            h.GetXaxis().SetBinLabel(4,'4j3t')
            h.GetXaxis().SetBinLabel(5,'5j3t')
            h.GetXaxis().SetBinLabel(6,'6j3t')
            h.GetXaxis().SetBinLabel(7,'4j4t')
            h.GetXaxis().SetBinLabel(8,'5j4t')
            h.GetXaxis().SetBinLabel(9,'6j4t')
        tablepath=("/".join((outputpath.split('/'))[:-1]))+"/"+name+"_yields"+catnames[ntables]
        ntables+=1
        # make an event yield table
        eventYields(hld,hl,samples,tablepath)

# plot dataMC comparison
labels=[]
for c in cattitles:
    labels+=([c]*len(plots))
plotDataMC(listOfHistoListsData,listOfHistoLists,samples,name,False,labels)
# plot dataMC comparison with logscale
#plotDataMC(listOfHistoListsData,listOfHistoLists,samples,name,True,"")
