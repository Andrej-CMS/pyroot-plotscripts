import ROOT

# Put Plotsscript output here
inputpath='/nfs/dust/cms/user/shwillia/BoostedTTHScripts/LimitCalculation/Setup_160222/pyroot-plotscripts/ANplots/workdir/76controlplotsPlusBoosted_JER/output.root'

# Histogram used for reweighting
histname='JTByBDToptC'

# Start with number binbias (e.g. 4 for N_Jets)
binbias=0

# Bin Selections
binSelections=[ ("((N_Jets>=6&&N_BTagsM==2)&&!"+boosted+")","6j2t","","",""),
                ("((N_Jets==4&&N_BTagsM==3)&&!"+boosted+")","4j3t","0.2","0.2","0.2"),
                ("((N_Jets==5&&N_BTagsM==3)&&!"+boosted+")","5j3t","0.15","0.15","0.15"),
                ("((N_Jets>=6&&N_BTagsM==3)&&!"+boosted+")","6j3t","0.1","0.1","0.1"),
                ("((N_Jets==4&&N_BTagsM>=4)&&!"+boosted+")","4j4t","0.2","0.2","0.2"),
                ("((N_Jets==5&&N_BTagsM>=4)&&!"+boosted+")","5j4t","0.2","0.2","0.2"),             
                ("((N_Jets>=6&&N_BTagsM>=4)&&!"+boosted+")","6j4t","0.1","0.1","0.1"),
                ("((N_Jets>=4&&N_BTagsM>=2)&&"+boosted+")","boosted","0.1","0.1","0.1")
]

# name of wsystematic
systname='CMS_res_j'

# Get weights for the following processes
processes=[ 'ttH',
            'ttbarOther',
            'ttbarPlusCCbar',
            'ttbarPlusB',
            'ttbarPlus2B',
            'ttbarPlusBBbar',
            'SingleTop',
            'Vjets',
            'Diboson'
]

# Get file
infile = ROOT.TFile(inputpath)
keys = infile.GetListOfKeys()

hists=[[ROOT.TH1F(),ROOT.TH1F(),ROOT.TH1F()] for proc in processes]

for key in keys:
  keyname = key.GetName()
 
  if not histname in keyname:
    continue
  
  procindex=-1
  systtype=-1
  
  for iproc,proc in enumerate(processes):
    
    if proc == keyname.split('_')[0]:
      procindex=iproc
    else:
      continue
    
    if systname in keyname:
      if systname+'Up' in keyname:
        systtype=1
      if systname+'Down' in keyname:
        systtype=2
    else:
      systtype=0
        
  if procindex<0 or systtype<0:
    continue
  
  hists[procindex][systtype]=infile.Get(keyname)

weights=[]
for hists in hists:
  upRatio   =hists[1]
  downRatio =hists[2]
  
  upRatio.Divide(hists[0])
  downRatio.Divide(hists[0])
  
  weights.append([])
  
  nbins=hists[0].GetNbinsX()
  
  for bin in range(nbins):
    weights[-1].append([upRatio.GetBinContent(bin+1),downRatio.GetBinContent(bin+1)])

upstrings=[]
downstrings=[]

for proc in weights:
  
  upstring='('
  downstring='('
  
  for ibin,jetbin in enumerate(proc):
    
    upstring+='('+str(jetbin[0])+'*('+binSelections[ibin]+'))'
    downstring+='('+str(jetbin[1])+'*('+binSelections[ibin]+'))'
    
    if ibin < len(proc)-1:
      upstring+='+'
      downstring+='+'
    else:
      upstring+=')'
      downstring+=')'
    
  upstrings.append(upstring)
  downstrings.append(downstring)
  
print upstrings
print downstrings

outfile = open(systname+'_weights.txt', 'w')
outfile.write(systname+'Up Weights:\n')
for iproc,proc in enumerate(upstrings):
  outfile.write(processes[iproc]+':   '+proc+'\n')
outfile.write('\n')
outfile.write(systname+'Down Weights:\n')
for iproc,proc in enumerate(downstrings):
  outfile.write(processes[iproc]+':   '+proc+'\n')
outfile.close()