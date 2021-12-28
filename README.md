# Memoire_M2

## Structure

.
├── bibliographie
│   └── biblio.txt (contain links)
├── data
│   ├── intermediate (dataframe use for other operation)
│   └── old (deprecated datframes)
│   └── ressources (Raw dataset: Verser2018 and Ragni2016
│   └── results 
├── notebooks
│   ├── 01_explore_Ragni_Verser.ipynb (data exploration)
│   └── 02_Preparation_des_donnees.py (data preparation)
│   └── 03_NSP_bert.ipynb (models based on Next Sentece Prediction with Bert)
│   └── 04_few_shot_MSLI.py (model based on MSLI for entailement prediction)
│   └── 05_result_analysis.ipynb (comparison between models prediction and human answers)
│   └── syllogism.py (Contain Syllogism class with has diverse useful method to analyse the raw dataset)
├── requierements.txt

## How to use

"pip3 install requierements.txt" in your virtual env
Warning: some of the link to the dataframe are broken, this is an intermediate version of the project, the result are good in the result folder but the code doesn't correspond to it. An another version with more advanced results should correct that.
