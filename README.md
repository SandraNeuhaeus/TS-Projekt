### NAME
Connector Aligner - Find english equivalents for german connectors in sentence-aligned texts.

### TABLE OF CONTENTS
1. [ Description ](#description)  
2. [ Files ](#files)
3. [ Requirements ](#requirements)  
   1. [ Download corpus ](#download-corpus)
   2. [ Install Pandas ](#install-pandas)
   3. [ Install NumPy ](#install-numpy)
   4. [ Install tqdm ](#install-tqdm)
   5. [ Install NLTK ](#install-nltk)
   6. [ Install Giza++ ](#install-giza)
4. [ Usage ](#usage)  
   1. [ List approach alignment, disambiguated ](#list-approach-alignment-disambiguated)
   2. [ List approach alignment (without disambiguation) ](#list-approach-alignment-without-disambiguation)
   3. [ Naive alignment ](#naive-alignment)
   4. [ Giza++ alignment ](#giza-alignment)
5. [ Authors ](#authors)


### DESCRIPTION
We used sentence-aligned parallel texts from the Europarl corpus (https://www.statmt.org/europarl/) in german and english. The program searches the six constrastive connectors "aber", "doch", "jedoch", "allerdings", "andererseits" and "hingegen" and matches an english translation from the appropriate english sentence. To find the translation we used a list of english contrastive connectors and the positions of the words in the sentences.

### FILES

- `de-en/`  
  (Directory for the two parallel corpus files. Have to be placed by the user.)
- `giza/`
  - `prepare_data.py`
  - `run_giza.sh`
  - `giza-pp/`  
  (Has to be downloaded and placed by user.)
    - `euroarl_data/`  
    (Directory for Giza's output. Has to be placed.)
    - ... (Giza files/directories)
- `results/`  
(Contains results of the different approaches; list approach disambiguated, list approach, naive approach and Giza++.)
  - `disambig/`
  - `list/`
  - `naive/`
  - `giza/`
- `disambig_aligner.py`  
  (Combines disambiguation and list approach.)
- `list_aligner.py`  
- `naive_aligner.py`  
- `abstract_aligner.py`
- `disambiguator.py`
- `split_text.py`
- `giza_results.py`  
  (Makes Giza++ results readable.)

### REQUIREMENTS
The program is tested with python  3.6.12, 3.7.6. and 3.8.10.


#### Download corpus
https://www.statmt.org/europarl/v7/de-en.tgz (189 MB)

Consists of two files
- europarl-v7.de-en.de (314 MB)
- europarl-v7.de-en.en (274 MB)

Place them in `de-en/`.

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

#### Install NLTK
With anaconda or `pip`:
```
conda install -c anaconda nltk
pip install --user -U nltk
```

#### Install Giza++
Under Linux:
```
cd giza
git clone https://github.com/moses-smt/giza-pp.git
cd giza-pp
make
```
We only used Giza++ under Linux because it was developed for Linux. Under Windows/MacOS a few changes have to be made before you can compile the files. For further information use an online tutorial as https://sinaahmadi.github.io/posts/sentence-alignment-using-giza.html.

### USAGE

Our results are provided in the directory `results/`. To reproduce the results follow these instruction.

#### List approach alignment, disambiguated
Via command line:
```
python disambig_aligner.py
```
The results are saved to `results/disambig/`.

#### List approach alignment (without disambiguation)
```
python list_aligner.py
```
The results are saved to `results/list/`

#### Naive alignment
```
python naive_aligner.py
```
The results are saved to `results/naive/`.

#### Giza++ alignment

Create output directory:
```
cd giza
mkdir giza-pp/europarl_data  # directory for Giza's input/output
```
Run Giza:

**Warning:** Running Giza++ with a big corpus is very time intensive. Our run took over **twelve hours**.  
Further the produced files are very large. One should expect **3.5 GB** plus the size of the tokenized corpus which is required to run Giza.

Alternatively download the most important result file `Result.A3.final` from https://boxup.uni-potsdam.de/index.php/s/wA7sjLiCjLgH8gc (Password: Konnektor) and place it at `giza/giza-pp/europarl_data/output/`. (Url expires at 2nd September 2022)
After this you can reenter at `python giza_results.py`

Preprocess data:  
This step will produce the files `Source` and `Target` in `giza-pp/europarl_data/` (597 MB)
```
python prepare_data.py  # tokenizes corpus files
```
Final start of Giza++:
```
./run_giza.sh  # produces 3.5 GB
```
Extract required information from `giza/giza-pp/europarl_data/output/Result.A3.final`:
```
cd ..
python giza_results.py  # extracts required information from 'giza/giza-pp/europarl_data/output/Result.A3.final'
```
The results can be found in `results/giza/`.


### AUTHORS
Niclas Küken  
Leander Lukas  
Sandra Neuhäußer
