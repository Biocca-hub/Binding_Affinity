# Importing necessary libraries
#from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
import requests
import json

################################################################################
############################## FUNCTION DEFINITION #############################
################################################################################

def make_df(file, dfname, delimitor):
    'Takes file path and makes pandas data frame'
    try:
        dfname = pd.read_csv(file, sep = delimitor)
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
    return dfname

################################################################################
############################# Making DF from datasets ##########################
################################################################################
'''
file_path='../../data/datasets/s4169.csv'
s4169=make_df(file_path, 's4169', '\t')
file_path='../../data/datasets/skempi_v2.csv'
skempi=make_df(file_path, 'skempi', ';')


# extracting PDB IDS for API queries
pdb_ids = list((s4169['pdb'].value_counts().to_dict()).keys())


#Necessary links:

chain_ids = 'https://www.ebi.ac.uk/pdbe/api/pdb/entry/molecules/' #api for chains

uniprot_id = 'https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/' #api to map chain to uniprot

oligomer_type = 'https://www.ebi.ac.uk/pdbe/api/pdb/entry/summary/' #api for oligomer type

experiment = 'https://www.ebi.ac.uk/pdbe/api/pdb/entry/experiment/' #api for experimental method and resolution


# Retrieving information through PDB Europe API

pdb_rep = [] #list of PDB IDs with repetitions
all_chains = [] # List of chain identification letters
all_chain_ids = [] # List of chain id in the format: 'PDBID_Chainletter', e.g. '3BT1_A'
expmets = [] # List of experimental method for sturcture determination
resos = [] # List of structure resolution (in Armstrong, A)
oligos = [] # List of oligomer types
all_uniprot_ids = {} # Dictionary with key = Uniprot ID and value = list of chain ids
all_uniprot_cov = {} # Dictionary with key = Uniprot ID and value = list of coverage values
all_uniprot_cov_res = {} # Dictionary with key = Uniprot ID and value = list of number of covered residues
unip_pdb = {} # Dictionary with key = Uniprot ID  and value = list of PDB IDs

################################################################################
################ API interrogation for each one of the PDB IDs #################
################################################################################

for id in pdb_ids:

  ###########################################################################
  ######################## Uniprot Related Informations #####################
  ###########################################################################


  # Each PDB can have one or more UP ID(s)
  uniprot_url = uniprot_id+id.lower()
  r = requests.get(uniprot_url)
  data = r.json().get(id.lower()).get('UniProt', {})
  # Each UP ID related to the PDB ID has some useful informations related to it:
  for u in data:
    mappings = (data[u]['mappings'])
    all_uniprot_ids[u] = all_uniprot_ids.get(u, [])
    all_uniprot_cov[u]=all_uniprot_cov.get(u,[])
    all_uniprot_cov_res[u]=all_uniprot_cov_res.get(u,[])
    unip_pdb[u]=unip_pdb.get(u,[])
    for c in mappings:
      chain = c.get('chain_id')
      # Relative chain
      chain_id = id+"_"+chain
      # Positions of first and last covered residue
      cov_res = c.get('end').get('residue_number')-c.get('start').get('residue_number')
      # Coverage (fration of UP sequence that is described in the structure file)
      coverage = c.get('coverage')
      all_uniprot_ids[u].append(chain_id)
      all_uniprot_cov[u].append(coverage)
      all_uniprot_cov_res[u].append(cov_res)

      ########################
      # Report PDB with UPID #
      ########################
      if id not in unip_pdb[u]:
        unip_pdb[u].append(id)

  ###########################################################################
  ###################### Structure Related Informations #####################
  ###########################################################################

  oligo_url = oligomer_type+id.lower()
  r = requests.get(oligo_url)
  data = r.json().get(id.lower())
  assemblies = data[0].get('assemblies', [])
  for a in assemblies:
    # From preferred assembly, store info about oligomer type (how many subunits, homo or etero)
    if a.get('preferred') == True:
      oligomer = a.get('form', '')+'_'+a.get('name','')

  method_url = experiment+id.lower()
  r = requests.get(method_url)
  data = r.json().get(id.lower())
  emet = data[0].get('experimental_method')
  res = data[0].get('resolution')

  chains = chain_ids+id.lower()
  r = requests.get(chains)
  data = r.json().get(id.lower())
  for el in data:
    if el.get('molecule_type') == 'polypeptide(L)':
      for c in el.get('in_chains'):
        chain_id = id+"_"+c
        pdb_rep.append(id) # PDB x chain (repeats same if necessary)
        all_chains.append(c) # Chain identificative letter
        all_chain_ids.append(chain_id) # Chain ID in the form '3BT1_B'
        expmets.append(emet) # Experimental method
        resos.append(res) # Resolution
        oligos.append(oligomer) # Oligomer type


###############################################################################
######### Useful Dictionaries: mapping between IDs, IDs and metrics  ##########
###############################################################################

print('There are ', len(all_chains), ' chains')

# Stores key = chain, value = uniprot list
all_chains_with_uniprot = {}
for key in all_uniprot_ids:
  for chain in all_uniprot_ids[key]:
    if chain not in all_chains_with_uniprot.keys():
      all_chains_with_uniprot[chain]=[]
      all_chains_with_uniprot[chain].append(key)
    else:
      all_chains_with_uniprot[chain].append(key)
print('There are ',len(all_chains_with_uniprot), ' chains with uniprot ID')

# list of the chains not mapped on a uniprot id
chains_without_uniprot = []
for key in all_chain_ids:
  if key not in all_chains_with_uniprot:
    chains_without_uniprot.append(key)
print('There are ',len(chains_without_uniprot), ' chains with no uniprot ID')

################################################################################
########################## METADATA TABLE CONSTRUCTION #########################
################################################################################

# List of uniprot IDs to make column of metadata df
upid_column = []
for el in all_chain_ids:
  if el in all_chains_with_uniprot.keys():
    upid_column.append(','.join(all_chains_with_uniprot[el]))
  else:
    upid_column.append('Not Mapped')

# Finalizing metadata df columns
all_chains_cov = {}
all_chains_cov_res = {}
for key in all_uniprot_ids:
  for i in range(len(all_uniprot_ids[key])):
    all_chains_cov[all_uniprot_ids[key][i]]=all_uniprot_cov[key][i]
    all_chains_cov_res[all_uniprot_ids[key][i]]=all_uniprot_cov_res[key][i]
cov_column = []
cov_res_column = []
for el in all_chain_ids:
  if el in all_chains_with_uniprot.keys():
    cov_column.append(all_chains_cov[el])
    cov_res_column.append(all_chains_cov_res[el])
  else:
    cov_column.append('Not Mapped')
    cov_res_column.append('Not Mapped')

metadata = pd.DataFrame({'PDB_ID':pdb_rep,
                         'Oligomer_type':oligos,
                         'Experimental_method': expmets,
                         'Resolution(Å)':resos,
                         'Chain_ID':all_chains,
                         'Uniprot_ID':upid_column,
                         'Covered_residues':cov_res_column,
                         'Coverage':cov_column,
                         })
print(metadata.shape)
print(metadata['Uniprot_ID'].head(15))
print(metadata['Uniprot_ID'].tail(15))

################################################################################
##################### DATA: analysis and table construction ####################
################################################################################

s4169['Chain_ID']=s4169['pdb'].to_numpy()+'_'+s4169['mutation'].str[1]

up_id_col_data = []
mut_chain = s4169['Chain_ID'].to_list()
for i in range(len(mut_chain)):
  if mut_chain[i] in all_chains_with_uniprot.keys():
    up_id_col_data.append(','.join(all_chains_with_uniprot[mut_chain[i]]))
  else:
    up_id_col_data.append('Not Mapped')

s4169['Uniprot_ID']=up_id_col_data

unique_upids=[]
for el in up_id_col_data:
  el = el.split(',')
  for id in el:
    if id not in unique_upids:
      unique_upids.append(id)
unique_chains=[]
for el in all_chain_ids:
  if el in s4169['Chain_ID'].to_list() and el not in unique_chains:
    unique_chains.append(el)
print('There are', len(unique_chains), '/1199 chains in the dataset')
print('There are ', len(unique_upids), '/325 uniprot ids in the dataset')

print(s4169.head())

'''
################################################################################
################################# Making final DF ##############################
################################################################################
file_path = 'metadata_28_04.tsv'
metadata = make_df(file_path, 'metadata', '\t')
file_path = 's4169_28_04.tsv'
s4169 = make_df(file_path, 's4169', '\t')
file_path = '../../data/datasets/skempi_v2.csv'
skempi2 = make_df(file_path, 'skempi2', ';')

s4169_mutations = s4169['mutation'].to_list()
s4169_chains = []
s4169_pdb=s4169['pdb'].to_list()
for i in range(len(s4169_mutations)):
  s4169_chains.append(s4169_pdb[i]+'_'+s4169_mutations[i][1]+'_'+s4169_mutations[i])
s4169['unique']=s4169_chains

dfs = [metadata, skempi2, s4169]
df_names = ['metadata', 'skempi2','s4169']

skempi_pdb = skempi2['#Pdb'].to_list()
skempi_mutations = skempi2['Mutation(s)_PDB'].to_list()
skempi_chain_id = []

for i in range(len(skempi_pdb)):
  skempi_pdb[i] = skempi_pdb[i].split('_')[0]
  skempi_chain_id.append(skempi_pdb[i].split('_')[0]+'_'+skempi_mutations[i][1])

skempi_uni = []
for i in range(len(skempi_mutations)):
  skempi_uni.append(skempi_pdb[i]+'_'+skempi_mutations[i][1]+'_'+skempi_mutations[i])

skempi = pd.DataFrame({'PDB_ID':skempi_pdb,
		       'Chain_ID': skempi_chain_id,
		       'unique': skempi_uni,
		       'Location':skempi2['iMutation_Location(s)'],
		       'DDG_method':skempi2['Method'],
		       'PDB_mut': skempi2['Mutation(s)_PDB'],
		       'Clean_mut':skempi2['Mutation(s)_cleaned'],
		       'Affinity_M': skempi2['Affinity_mut_parsed'],
		       'Affinity_WT':skempi2['Affinity_wt_parsed'],
		       'Out_type':skempi2['Hold_out_type'],
		       'Out_protein':skempi2['Hold_out_proteins'],
		       'Skempi_v': skempi2['SKEMPI version']})

dfs.append(skempi)
df_names.append('skempi')

s4943 = skempi.merge(s4169, left_on=['unique'], right_on=['unique'], how='inner')

s4943 = pd.DataFrame({'PDB_ID': s4943['PDB_ID'],
		      'Chain_ID': s4943['Chain_ID_x'],
		      'Uniprot_ID': s4943['Uniprot_ID'],
		      'Location': s4943['Location'],
		      'DDG_method': s4943['DDG_method'],
		      'DDG': s4943['actual'],
		      'PDB_mut': s4943['PDB_mut'],
		      'Clean_mut': s4943['Clean_mut'],
		      'Affinity_M': s4943['Affinity_M'],
		      'Affinity_WT': s4943['Affinity_WT'],
		      'unique': s4943['unique'],
		      'Out_type': s4943['Out_type'],
		      'Out_protein': s4943['Out_protein'],
    		      'Skempi_v': s4943['Skempi_v'],
       	 	      'sampling_fold': s4943['sampling_fold']})

dfs.append(s4943)
df_names.append('s4943')

for i in range(len(dfs)):
  print(df_names[i], 'shape is:', dfs[i].shape)
  print(df_names[i], 'column names are:', dfs[i].columns)
  print(dfs[i].head(3))
  print('\n\n\n')

print(len(np.unique(s4943['unique'].to_list())))
print(len(np.unique(s4943['Uniprot_ID'].to_list())))

s4943.to_csv('s4943_28_04.tsv', sep='\t', index=False)

folds = s4943['sampling_fold'].value_counts().to_dict()
print(folds)


'''
################################################################################
###################### SAVING METADATA AND 'DATA' TABLES #######################
################################################################################

#out = Path('metadata_28/04.tsv')
#out.parent.mkdir(parents=True, exist_ok=True)
metadata.to_csv('metadata_28_04.tsv', sep='\t', index=False)
#out = Path('s4169_28/04.tsv')
#out.parent.mkdir(parents=True, exist_ok=True)
s4169.to_csv('s4169_28_04.tsv', sep='\t', index=False)

# Dictionary in which every PDB is a key linked to the amount of its occurrences
pdb_occurrences = s4169['pdb'].value_counts().to_dict()

# Dictionary in which every chain is a key linked to the amount of its occurrences
chain_occurrences = s4169['Chain_ID'].value_counts().to_dict()

# Dictionary in which every uniprot ID is a key linked to the amount of its occurrences
upid_occurrences = s4169['Uniprot_ID'].value_counts().to_dict()

# Dictionaries that counts the amount of PDB IDs per Uniprot ID and viceversa:
pdb_x_up = s4169.groupby('Uniprot_ID')['pdb'].apply(list).to_dict()
up_x_pdb = s4169.groupby('pdb')['Uniprot_ID'].apply(list).to_dict()
chain_x_up = s4169.groupby('Uniprot_ID')['Chain_ID'].apply(list).to_dict()
chain_x_pdb = s4169.groupby('pdb')['Chain_ID'].apply(list).to_dict()


print('Shape of data df: ', s4169.shape)
print(s4169.head(15))
print('\n\n')

print('Max amount of PDB occurrences:', max(pdb_occurrences.values()))
print('Max amount of chain occurrences:', max(chain_occurrences.values()))
print('Max amount of uniprot occurrences:', max(upid_occurrences.values()))
'''
