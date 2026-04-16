def chain_extractor(chain, pdb):
  'Extracts a pdb chain from a pdb file'
  chain_name = "../chain/"+chain+'.pdb'
  pdb_file = pdb+".pdb"
  chain_id = chain.split('_')[1]
  with open(chain_name, 'w') as writer:  
    with open(pdb_file, 'r') as reader:
      for line in reader:
        if line.startswith("ATOM") and line[21] == chain_id:
          writer.write(line)

with open('../chain/CHAINS.txt', 'r') as reader:
    chains=''
    for line in reader:
        chains+=line 
    chains = chains.split("\n")
with open('pdb.txt', 'r') as reader:
    pdbs=''
    for line in reader:
        pdbs+=line 
    pdbs = pdbs.split(",")

for el in chains:      
    chain_extractor(el, el[:-2])

