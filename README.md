### NAME
?Contrastive connectors in parallel texts? - Find english equivalents for german connectors in sentence-aligned texts.

### DESCRIPTION
We used sentence-aligned parallel texts from the Europarl corpus (https://www.statmt.org/europarl/) in german and english. The program searches the six constrastive connectors "aber", "doch", "jedoch", "allerdings", "andererseits" and "hingegen" and matches an english translation from the appropriate english sentence. To find the translation we used a list of english contrastive connectors and the positions of the words in the sentences.

### FILES

...

### REQUIREMENTS
The program is tested with python 3.7.6., 3.6.12 and 3.8.10.


#### Download corpus
https://www.statmt.org/europarl/v7/de-en.tgz (189 MB)

Consists of two files
- europarl-v7.de-en.de (314 MB)
- europarl-v7.de-en.en (274 MB)


#### Install Pandas
With anaconda/miniconda or with `pip`:
```
conda install pandas
pip install pandas
```
#### Install NumPy
With anaconda/miniconda or with `pip`:
```
conda install numpy
pip install numpy
```

#### Install tqdm
With anaconda or with `pip`:
```
conda install -c anaconda tqdm
pip install tqdm
```

### USAGE
...


### AUTHORS
Niclas Küken  
Leander Lukas  
Sandra Neuhäußer
