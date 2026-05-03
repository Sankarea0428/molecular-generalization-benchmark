\# Molecular Generalization Benchmark



\## Project Overview



This project investigates molecular generalization in a binary molecular property prediction task. The central question is whether random train-test splitting leads to overly optimistic performance estimates compared with scaffold-based splitting, where test molecules are structurally more distinct from training molecules.



In the first stage, this project uses the BBBP dataset, Morgan fingerprints, and two baseline models: Logistic Regression and Random Forest. The workflow covers SMILES cleaning, molecular featurization, random splitting, scaffold splitting, baseline model training, metric evaluation, and result visualization.



\---



\## Research Question



The main research question is:



\*\*Does random split overestimate model performance in molecular property prediction because structurally similar molecules may appear in both the training and test sets?\*\*



To examine this question, this project compares model performance under two data splitting strategies:



\- \*\*Random Split\*\*: molecules are randomly divided into training and test sets.

\- \*\*Scaffold Split\*\*: molecules are grouped by their Bemis–Murcko scaffolds, so the test set is structurally more distinct from the training set.



If performance is substantially higher under random split than under scaffold split, this suggests that random split may overestimate the model's ability to generalize to new regions of chemical space.



\---



\## Dataset



This project uses the \*\*BBBP\*\* dataset, a binary classification dataset for predicting blood-brain barrier permeability. Each molecule is represented by a SMILES string and a binary label.



After SMILES validity checking and canonicalization with \*\*RDKit\*\*, the cleaned dataset contains \*\*2,039 molecules\*\*.



\---



\## Methodology



\### 1. SMILES Preprocessing and Canonicalization



To ensure that molecular structures can be processed consistently, the input SMILES strings are checked using RDKit. Invalid SMILES and empty strings are removed. Valid molecules are then converted into canonical SMILES, which provide a standardized molecular string representation for downstream featurization.



\### 2. Molecular Featurization



Molecules are converted into numerical representations using \*\*Morgan fingerprints\*\*, a common type of circular molecular fingerprint.



In this project, the fingerprint configuration is:



\- \*\*Radius\*\*: 2

\- \*\*Bit vector length\*\*: 2048



This setting provides a standard baseline representation for molecular property prediction.



\### 3. Data Splitting Strategies



To investigate the impact of molecular structural similarity on model performance, two splitting strategies are implemented:



\- \*\*Random Split\*\*  

&#x20; Molecules are randomly divided into training and test sets. This setting may place structurally similar molecules in both sets, potentially leading to optimistic performance estimates.



\- \*\*Scaffold Split\*\*  

&#x20; Molecules are grouped according to their \*\*Bemis–Murcko scaffolds\*\*. Molecules sharing the same scaffold are kept in the same split, making the test set structurally more distinct from the training set.



\### 4. Baseline Models



Two classical machine learning models are used as baseline predictors:



\- \*\*Logistic Regression\*\*: a linear baseline model for binary classification.

\- \*\*Random Forest\*\*: a tree-based ensemble model capable of capturing non-linear feature interactions.



\### 5. Evaluation Metrics



Model performance is evaluated using:



\- \*\*Accuracy\*\*

\- \*\*Precision\*\*

\- \*\*Recall\*\*

\- \*\*F1-score\*\*

\- \*\*ROC-AUC\*\*



These metrics provide complementary views of classification performance, including overall correctness, positive-class prediction quality, sensitivity, and probability-based discrimination ability.



\---



\## Results



\### Performance Summary



| Split | Model | Accuracy | F1 | ROC-AUC |

|---|---|---:|---:|---:|

| Random | Logistic Regression | 0.8971 | 0.9352 | 0.9173 |

| Random | Random Forest | 0.8995 | 0.9374 | 0.9321 |

| Scaffold | Logistic Regression | 0.8655 | 0.9235 | 0.8003 |

| Scaffold | Random Forest | 0.8655 | 0.9275 | 0.7817 |



\### Key Finding



The results show a clear drop in \*\*ROC-AUC\*\* when moving from \*\*random split\*\* to \*\*scaffold split\*\*. This suggests that random split may provide an overly optimistic estimate of model generalization performance, while scaffold split offers a more stringent evaluation of structural generalization.



\---



\## Result Figures



\### ROC-AUC Comparison



!\[ROC-AUC Comparison](results/figures/roc\_auc\_comparison.png)



\### Core Metrics Comparison



!\[Core Metrics Comparison](results/figures/plot\_metrics\_comparison.png)



\---



\## How to Run



\### 1. Create and activate a virtual environment



```bash

python -m venv .venv

On Windows:

.venv\\Scripts\\activate

On macOS/Linux:

source .venv/bin/activate



Install dependencies

pip install -r requirements.txt



Run one experiment

The run\_experiment.py script supports one split strategy and one model at a time.



Example: random split + Logistic Regression



python run\_experiment.py --split random --model logistic\_regression



Example: scaffold split + Random Forest



python run\_experiment.py --split scaffold --model random\_forest

Supported split options:



random

scaffold



Supported model options:



logistic\_regression

random\_forest



Generate the metrics summary



python src/evaluation/metrics.py



This saves the summary table to:



results/tables/bbbp\_metrics\_summary.csv



Generate result figures



python src/visualization/plot\_results.py



This saves figures to:



results/figures/



Project Structure

mol-generalization-benchmark/

│

├── README.md

├── requirements.txt

├── run\_experiment.py

│

├── data/

│   ├── raw/

│   └── processed/

│

├── src/

│   ├── data/

│   ├── featurizers/

│   ├── splits/

│   ├── models/

│   ├── evaluation/

│   └── visualization/

│

├── results/

│   ├── tables/

│   └── figures/

│

└── report/



Current Scope and Limitations



This project is a first-stage benchmark and currently has the following scope:



one dataset: BBBP

one molecular representation: Morgan fingerprint

two baseline models: Logistic Regression and Random Forest

two split strategies: Random Split and Scaffold Split



Current limitations include:



no graph neural network baselines yet

no similarity-based or cluster-based split yet

no multi-dataset benchmark yet

no detailed error analysis yet



Future Work



Possible future extensions include:



adding similarity split and cluster split

evaluating graph neural network baselines

extending the benchmark to more molecular datasets

performing deeper error analysis on false positives and false negatives



Summary



This project builds a reproducible benchmark pipeline for evaluating molecular generalization under different data splitting strategies. The first-stage results suggest that random split may overestimate model performance, while scaffold split provides a stricter and more realistic test of structural generalization in molecular property prediction.

