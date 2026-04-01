# 1. Data Investigation

For each method's training dataset, the following aspects were investigated:

- the **source dataset(s)** used for training (e.g., SKEMPI versions, additional datasets)
- the **availability of curated subsets or named datasets** (when provided by the authors)    
- the **composition of mutations**, including single, double, and multiple single residue variations (SRVs)  
- the **number of protein complexes and proteins** represented in the dataset  
- the **total number of mutations** available for each method  
- the **distribution UniProt identifiers per complex** (from 1 to 8, where C1: Single UniProt per Complex and so on) 

These elements allow a consistent comparison of dataset size, diversity, and redundancy across methods.

| Method | [BeAtMuSiC](https://academic.oup.com/nar/article/41/W1/W333/1106169)<br>(2013) | [BindProfX](https://www.sciencedirect.com/science/article/pii/S0022283616305174?via%3Dihub)<br>(2017; [download](https://aideepmed.com/BindProfX/download/)) | [SSIPe](https://academic.oup.com/bioinformatics/article/36/8/2429/5674037)<br>(2019) | [mCSM-PPI2](https://academic.oup.com/nar/article/47/W1/W338/5494729#supplementary-data)<br>(2019; [download](https://biosig.lab.uq.edu.au/mcsm_ppi2/datasets)) | [MutaBind2](https://www.sciencedirect.com/science/article/pii/S2589004220301231#appsec1)<br>(2020; [download](https://lilab.jysw.suda.edu.cn/research/mutabind2/download)) | [SAAMBE-3D](https://www.mdpi.com/1422-0067/21/7/2563)<br>(2020) | [MuToN](https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202402918)<br>(2024; [download](https://zenodo.org/records/10445253)) | [PIANO](https://www.nature.com/articles/s42003-024-07066-9)<br>(2024; [download](https://doi.org/10.5281/zenodo.13375314)) | [ProBASS](https://academic.oup.com/bioinformatics/article/41/5/btaf270/8127915)<br>(2025; [download](http://github.com/sagagugit/ProBASS)) | [DDMut-PPI](https://academic.oup.com/nar/article/52/W1/W207/7680621)<br>(2025; [download](https://biosig.lab.uq.edu.au/ddmut_ppi/datasets)) |
|:-------|:------------------:|:----------------------------:|:--------------:|:----------------------------:|:----------------------------:|:------------------:|:--------------:|:--------------:|:----------------:|:------------------:|
| **Source** | SKEMPI 1 | SKEMPI 1 | SKEMPI 2 | SKEMPI 2 | SKEMPI 2 | SKEMPI 2 | SKEMPI 2.0 | SKEMPI 2.0; AB-bind; SKEMPI 1.0 | SKEMPI 2.0 + own data | SKEMPI 1.0 and 2.0 |
| **Name** | - | - | - | S4169 | S4191; M1707 | - | - | - | - | S4169 |
| **Single Mutations** | 2007 | 1131 | 1666 | 4169 | 4191 | 3753 | - | 4310 | 2325 | 4169 |
| **Complexes (S.M.)** | - | - | - | 319 | 265 | 299 | - | 321 | - | 319 |
| **Proteins (S.M.)** | - | - | - | 658 | 480 | - | - | 718 | - | 658 |
| **Double Mutations** | - | 195 | - | - | - | - | - | - | 25840 | - |
| **Complexes (D.M.)** | - | - | - | - | - | - | - | - | - | - |
| **Proteins (D.M.)** | - | - | - | - | - | - | - | - | - | - |
| **Multiple Mutations** | - | 76 | 538 | - | 1707 | - | - | - | - | - |
| **Complexes (M.M.)** | - | - | - | - | 120 | - | - | - | - | - |
| **Proteins (M.M.)** | - | - | - | - | 221 | - | - | - | - | - |
| **Total Mutations** | 2007 | 1402 | 2204 | 4169 | 5898 | 3753 | 5091 | 4310 | 28165 | 4169 |
| **Total Complexes** | - | 114 | 118 | 319 | 385 | 299 | 345 | 321 | 132 | 319 |
| **Total Proteins** | - | - | - | 658 | 701 | - | 711 | 718 | 262 | 658 |
| **C1** | - | 28 | - | 61 | 54 | - | 66 | 38 | 1 | 61 |
| **C2** | - | 121 | - | 202 | 186<br>77 | - | 214 | 228 | 127 | 202 |
| **C3** | - | 6 | - | 24 | 14<br>13 | - | 29 | 27 | 1 | 24 |
| **C4** | - | 1 | - | 12 | 3<br>1 | - | 13 | 13 | 1 | 12 |
| **C5** | - | 0 | - | 6 | 0 | - | 7 | 6 | 0 | 6 |
| **C6** | - | 1 | - | 1 | 0 | - | 1 | 4 | 0 | 1 |
| **C7** | - | 1 | - | 3 | 0 | - | 3 | 3 | 0 | 3 |
| **C8** | - | 0 | - | 2 | 0 | - | 2 | 2 | 0 | 2 | 
