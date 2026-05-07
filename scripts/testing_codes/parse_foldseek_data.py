#######################################################################################
				# IMPORTING LIBRARIES #
#######################################################################################


import pandas as pd
import numpy as np

#######################################################################################
                                # IMPORTING DATA #
#######################################################################################

def make_df(file, dfname, delimitor):
    'Takes file path and makes pandas data frame'
    try:
        dfname = pd.read_csv(file, sep = delimitor)
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
    return dfname

foldseek = make_df('../../data/out.tsv', 'foldseek', '\t')

		    ############################################
		    ### ONLY KEEPS PAIRS WITH TM-SCORE ≥ 0.6 ###
		    ############################################

foldseek_parsed = foldseek[foldseek['TM-score']>=0.6].reset_index(drop=True)

                    ############################################
                    ### GRAPH DATAFRAME: remove index column ###
                    ############################################

graph_df = make_df('../../data/Chain_ID_graph.tsv', 'graph_df', '\t')

del graph_df['Unnamed: 0']


#######################################################################################
                                # CHEKING PAIRS IN DFs #
#######################################################################################

# List of ID1 for chain graph
chain_1 = list(graph_df['Chain_ID1'])
# List of ID2 for chain graph
chain_2 = list(graph_df['Chain_ID2'])
# List of ID1 for FS tsv
foldseek_1 =list(foldseek_parsed['ID_1'])
# List of ID2 for FS tsv
foldseek_2 = list(foldseek_parsed['ID_2'])

# List of pairs in chain graph
pairs_gf = []
# Dictionary = pair : edge_pdb
pair_pdb = {}
# Dictionary = pair : edge_up
pair_up = {}

for i in range(len(chain_1)):
  p = (chain_1[i], chain_2[i])
  pairs_gf.append(p)
  pair_pdb[p]=graph_df['Edge_PDB'][i]
  pair_up [p]=graph_df['Edge_UP'][i]

# List of pairs in FS
pairs_fs = []
# Dictionary = pair: TM-score
pair_tm = {}
# List of TM-scores
tm_scores = []

for i in range(len(foldseek_1)):
  p = (foldseek_1[i],foldseek_2[i])
  pairs_fs.append(p)
  tm_scores = foldseek_parsed['TM-score'][i]
  pair_tm[p] = foldseek_parsed['TM-score'][i]
  if p not in pairs_gf:
    pair_pdb[p]=''
    pair_up [p]=''
i = 0
not_shared = []
for pair in pairs_gf:
  if pair not in pairs_fs:
    i += 1
    not_shared.append(pair)
    pair_tm[pair]=0

print(len(not_shared))

print(len(list(pair_tm.keys())) == len(pairs_fs) + len(not_shared))

id1 = []
id2 = []
pdb = []
up = []
sim = []
for pair in pair_tm:
  id1.append(pair[0])
  id2.append(pair[1])
  pdb.append(pair_pdb[pair])
  up.append(pair_up[pair])
  sim.append(pair_tm[pair])

grafodemme = pd.DataFrame({'ID1':id1, 'ID2':id2, 'Edge_PDB': pdb, 'Edge_UP': up, 'TM-score': sim})
print(grafodemme.head())
grafodemme.to_csv('../../data/final_graph.tsv', sep = '\t')
