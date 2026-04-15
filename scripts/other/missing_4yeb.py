def chain_extractor(chain, pdb):
  'Extracts a pdb chain from a pdb file'
  chain_name = chain+'.pdb'
  pdb_file = pdb+".pdb"
  chain_id = chain[-1]
  with open(chain_name, 'w') as writer:  
    with open(pdb_file, 'r') as reader:
      for line in reader:
        if line.startswith("ATOM") and line[21] == chain_id:
          writer.write(line)

chains = ['4YEB_A', '4YEB_B']

for el in chains:
  chain_extractor(el, el[:-2])