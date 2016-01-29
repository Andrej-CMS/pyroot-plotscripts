import sys
import os
sys.path.insert(0, '../')
from scriptgenerator import *
from plotutils import *

path='/nfs/dust/cms/user/hmildner/trees0108/'
name='anplots'
sel_singleel="(N_LooseMuons==0)" # need to veto muon events in electron dataset to avoid double countung
sel_singlemu="(N_LooseElectrons==0)" # and vice versa...
mcweight='(2.61)*(N_LooseElectrons==0||N_LooseMuons==0)' # some weights are only applied on mc
# selections for categories
sel1="((N_TightLeptons==1)*(N_LooseLeptons==1)*(N_BTagsM>=2)*(N_Jets>=4))" # l+jets channel
name1="1lge4ge2"

s43="(N_Jets==4&&N_BTagsM==3)"
s44="(N_Jets==4&&N_BTagsM>=4)"
s53="(N_Jets==5&&N_BTagsM==3)"
s54="(N_Jets==5&&N_BTagsM>=4)"
s62="(N_Jets>=6&&N_BTagsM==2)"
s63="(N_Jets>=6&&N_BTagsM==3)"
s64="(N_Jets>=6&&N_BTagsM>=4)"


# data samples (name, color, path to files, selection, nickname_without_special_characters,optional: number of events for cross check)
samples_data=[Sample('SingleMu',ROOT.kBlack,path+'/mu_*/*nominal*.root',sel_singlemu,'SingleMu'),
              Sample('SingleEl',ROOT.kBlack,path+'/el_*/*nominal*.root',sel_singleel,'SingleEl')
              ]

# mc samples
samples=[Sample('t#bar{t}H',ROOT.kBlue+1,path+'/ttH*/*nominal*.root',mcweight,'ttH') ,     
#         Sample('t#bar{t}',ROOT.kRed+1,path+'/ttbar/*nominal*.root',mcweight,'ttbar') ,     
         Sample('t#bar{t}+lf',ROOT.kRed-7,path+'/ttbar/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusCC==0&&GenEvt_I_TTPlusBB==0)','ttl'),
         Sample('t#bar{t}+c#bar{c}',ROOT.kRed+1,path+'/ttbar/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusCC==1)','ttcc'),
         Sample('t#bar{t}+b',ROOT.kRed-2,path+'/ttbar/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusBB==1)','tt1b'),
         Sample('t#bar{t}+2b',ROOT.kRed+2,path+'/ttbar/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusBB==2)','tt2b'),
         Sample('t#bar{t}+b#bar{b}',ROOT.kRed+3,path+'/ttbar/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusBB==3)','ttbb'),  
         Sample('Single Top',ROOT.kMagenta,path+'/st*/*nominal*.root',mcweight,'SingleTop') , 
         Sample('V+jets',ROOT.kGreen-3,path+'/??ets*/*nominal*.root',mcweight,'Vjets') , 
         Sample('t#bar{t}+V',ROOT.kBlue-10,path+'/tt?_*/*nominal*.root',mcweight,'ttV'),         
         Sample('Diboson',ROOT.kAzure+2,path+'/??/*nominal*.root',mcweight,'Diboson') , 
#         Sample('QCD',ROOT.kYellow ,path+'/QCD*/*nominal*root',mcweight,'QCD') , 
]

categoriesJT=[("(N_Jets>=6&&N_BTagsM==2)","6j2t",""),
              ("(N_Jets==4&&N_BTagsM==3)","4j3t","0.2"),
              ("(N_Jets==5&&N_BTagsM==3)","5j3t","0.15"),
              ("(N_Jets>=6&&N_BTagsM==3)","6j3t","0.1"),
              ("(N_Jets==4&&N_BTagsM>=4)","4j4t","0.2"),
              ("(N_Jets==5&&N_BTagsM>=4)","5j4t","0.2"),             
              ("(N_Jets>=6&&N_BTagsM>=4)","6j4t","0.1")]

categoriesSplitBDT=[]
categoriesSplitBDT.append(categoriesJT[0])
for cat in categoriesJT[1:]:
    categoriesSplitBDT.append(('('+cat[0]+"*(BDT_common5_output<"+cat[2]+"))",cat[1]+"l"))
    categoriesSplitBDT.append(('('+cat[0]+"*(BDT_common5_output>="+cat[2]+"))",cat[1]+"h"))


# book plots
label="#geq 1 lepton, #geq 4 jets, #geq 2 b-tags"
catstringSplitByBDT="0"
for i,cat in enumerate(categoriesSplitBDT):
    catstringSplitByBDT+=("+"+str(i+1)+"*"+cat[0])


plots=[Plot(ROOT.TH1F("JT" ,"jet-tag categories",9,-0.5,8.5),"3*max(min(N_BTagsM-2,2),0)+max(min(N_Jets-4,2),0)","(N_BTagsM>=2&&N_Jets>=4)",label),
       Plot(ROOT.TH1F("JTsplitByBDT" ,"2D analysis B categories",len(categoriesSplitBDT),0.5,0.5+len(categoriesSplitBDT)),catstringSplitByBDT,"(N_BTagsM>=2&&N_Jets>=6||N_BTagsM>=3&&N_Jets>=4)"),
       Plot(ROOT.TH1F("N_Jets","Number of ak4 jets",7,3.5,10.5),"N_Jets",'',label),
       Plot(ROOT.TH1F("N_BTagsM","Number of b-tags",4,1.5,5.5),"N_BTagsM",'',label),
       Plot(ROOT.TH1F("CSV0","B-tag of leading jet",22,-.1,1),"Jet_CSV[0]",'',label),
       Plot(ROOT.TH1F("CSV1","B-tag of second jet",22,-.1,1),"Jet_CSV[1]",'',label),
       Plot(ROOT.TH1F("CSV","B-tag of all jets",22,-.1,1),"Jet_CSV",'',label),
       
       Plot(ROOT.TH1F("pt1","p_{T} of leading jet",50,0,500),"Jet_Pt[0]",'',label),
       Plot(ROOT.TH1F("pt2","p_{T} of second jet",50,0,500),"Jet_Pt[1]",'',label),
       Plot(ROOT.TH1F("pt3","p_{T} of third jet",40,0,400),"Jet_Pt[2]",'',label),
       Plot(ROOT.TH1F("pt4","p_{T} of fourth jet",60,0,300),"Jet_Pt[3]",'',label),
       Plot(ROOT.TH1F("pt5","p_{T} of fifth jet",40,0,200),"Jet_Pt[4]",'',label),
       Plot(ROOT.TH1F("pt6","p_{T} of sixth jet",40,0,200),"Jet_Pt[5]",'',label),
       Plot(ROOT.TH1F("pt7","p_{T} of seventh jet",40,0,100),"Jet_Pt[6]",'',label),

       Plot(ROOT.TH1F("eta1","#eta of leading jet",50,-2.5,2.5),"Jet_Eta[0]",'',label),
       Plot(ROOT.TH1F("eta2","#eta of second jet",50,-2.5,2.5),"Jet_Eta[1]",'',label),
       Plot(ROOT.TH1F("phij1","#phi of leading jet",64,-3.2,3.2),"Jet_Phi[0]",'',label),
       Plot(ROOT.TH1F("phij2","#phi of second jet",64,-3.2,3.2),"Jet_Phi[1]",'',label),
       Plot(ROOT.TH1F("Evt_HT_Jets","Sum p_{T} jets",75,0,1500),"Evt_HT_Jets",'',label),
       Plot(ROOT.TH1F("ptalljets","p_{T} of all jets",60,0,300),"Jet_Pt",'',label),
       Plot(ROOT.TH1F("csvalljets","csv of all jets",44,-.1,1),"Jet_CSV",'',label),
       Plot(ROOT.TH1F("leppt","lepton p_{T}",50,0,200),"LooseLepton_Pt[0]",'',label),
       Plot(ROOT.TH1F("lepeta","lepton #eta",50,-2.5,2.5),"LooseLepton_Eta[0]",'',label),
       Plot(ROOT.TH1F("eliso","electron relative isolation",50,0,0.15),"Electron_RelIso[0]",'',label),
       Plot(ROOT.TH1F("muiso","muon relative isolation",50,0,0.15),"Muon_RelIso[0]",'',label),
       Plot(ROOT.TH1F("MET","missing transverse energy",50,0,200),"Evt_Pt_MET",'',label),
       Plot(ROOT.TH1F("METphi","MET #phi",64,-3.2,3.2),"Evt_Phi_MET",'',label),
       Plot(ROOT.TH1F("N_PrimaryVertices","Reconstructed primary vertices",26,-.5,25.5),"N_PrimaryVertices",'',label),
       Plot(ROOT.TH1F("CSVpt1","B-tag of jets with p_{T} between 30 and 40 GeV",44,-.1,1),"Jet_CSV",'Jet_Pt>30&&Jet_Pt<40',label),
       Plot(ROOT.TH1F("CSVpt2","B-tag of jets with p_{T} between 40 and 60 GeV",44,-.1,1),"Jet_CSV",'Jet_Pt>40&&Jet_Pt<60',label),
       Plot(ROOT.TH1F("CSVpt3","B-tag of jets with p_{T} between 60 and 100 GeV",44,-.1,1),"Jet_CSV",'Jet_Pt>60&&Jet_Pt<100',label),
       Plot(ROOT.TH1F("CSVpt4","B-tag of jets with p_{T} over 100 GeV",44,-.1,1),"Jet_CSV",'Jet_Pt>100',label),
       Plot(ROOT.TH1F("CSVeta1","B-tag of jets with abs(#eta) between 0 and 0.4",44,-.1,1),"Jet_CSV",'fabs(Jet_Eta)<0.4',label),
       Plot(ROOT.TH1F("CSVeta2","B-tag of jets with abs(#eta) between 0.4 and 0.8",44,-.1,1),"Jet_CSV",'fabs(Jet_Eta)>0.4&&fabs(Jet_Eta)<0.8',label),
       Plot(ROOT.TH1F("CSVeta3","B-tag of jets with abs(#eta) between 0.8 and 1.6",44,-.1,1),"Jet_CSV",'fabs(Jet_Eta)>0.8&&fabs(Jet_Eta)<1.6',label),
       Plot(ROOT.TH1F("CSVeta4","B-tag of jets with abs(#eta) between 0.8 and 1.6",44,-.1,1),"Jet_CSV",'fabs(Jet_Eta)>1.6',label),
      
       ]
# plot parallel -- alternatively there are also options to plot more traditional that also return lists of histo lists
outputpath=plotParallel(name,2000000,plots,samples+samples_data)
listOfHistoLists=createHistoLists_fromSuperHistoFile(outputpath,samples,plots,1)
listOfHistoListsData=createHistoLists_fromSuperHistoFile(outputpath,samples_data,plots,1)
ntables=0
# do some post processing
for hld,hl in zip(listOfHistoListsData,listOfHistoLists):
    if "JT" in hld[0].GetName() and not "JTsplitByBDT" in hld[0].GetName():
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
        tablepath=("/".join((outputpath.split('/'))[:-1]))+"/"+name+"_yields"
        ntables+=1
        # make an event yield table
        eventYields(hld,hl,samples,tablepath)

for hld,hl in zip(listOfHistoListsData,listOfHistoLists):
    if "JTsplitByBDT" in hld[0].GetName():       
        for h in hld+hl:
            for i,cat in enumerate(categoriesSplitBDT):
                h.GetXaxis().SetBinLabel(i+1,cat[1])
                print cat[1]
        tablepath=("/".join((outputpath.split('/'))[:-1]))+"/"+name+"_yields2"

# plot dataMC comparison
labels=[plot.label for plot in plots]

lolT=transposeLOL(listOfHistoLists)
plotDataMCan(listOfHistoListsData,transposeLOL(lolT[1:]),samples[1:],lolT[0],samples[0],20,name,False,labels)

listOfHistoLists=createHistoLists_fromSuperHistoFile(outputpath,samples,plots,1)
listOfHistoListsData=createHistoLists_fromSuperHistoFile(outputpath,samples_data,plots,1)
ntables=0
# do some post processing
for hld,hl in zip(listOfHistoListsData,listOfHistoLists):
    if "JT" in hld[0].GetName() and not "JTsplitByBDT":
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
for hld,hl in zip(listOfHistoListsData,listOfHistoLists):
    if "JTsplitByBDT" in hld[0].GetName():       
        for h in hld+hl:
            for i,cat in enumerate(categoriesSplitBDT):
                h.GetXaxis().SetBinLabel(i+1,cat[1])



# plot dataMC comparison
labels=[plot.label for plot in plots]

lolT=transposeLOL(listOfHistoLists)
plotDataMCan(listOfHistoListsData,transposeLOL(lolT[1:]),samples[1:],lolT[0],samples[0],20,name+'_log',True,labels)
