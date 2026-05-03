import numpy as np
import pandas as pd
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
input_path = Path('data/processed/bbbp_rdkit_clean.csv')
output_path = Path('data/processed/bbbp_morgan_features.npz')
radius = 2
n_bits = 2048
def smiles_to_mol(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    else:
        return mol
def mol_to_morgan_fp(mol,radius,n_bits):
    fp = AllChem.GetMorganFingerprintAsBitVect(
        mol,
        radius,
        nBits=n_bits
    )
    arr = np.zeros(n_bits,dtype=np.int8)
    DataStructs.ConvertToNumpyArray(fp,arr)
    return arr
def featurize_dataframe(df,radius,n_bits):
    fingerprints = []
    labels = []
    valid_smiles = []
    for index,row in df.iterrows():
        smiles = row['smiles']
        label = row['label']
        mol = smiles_to_mol(smiles)
        if mol is None:
            continue
        fp = mol_to_morgan_fp(mol,radius,n_bits)
        fingerprints.append(fp)
        labels.append(label)
        valid_smiles.append(smiles)
    X = np.array(fingerprints, dtype=np.int8)
    y = np.array(labels,dtype=np.int8)
    smiles_array = np.array(valid_smiles)
    return X,y, smiles_array
def build_morgan_features():#读取文件 显示csv的basis
    df = pd.read_csv(input_path)
    if "smiles" not in df.columns or 'label' not in df.columns:
        raise ValueError('Input file must contain smiles and label columns.')
    input_rows = len(df)
    print(f"Loaded file: {input_path}")
    print(f'input rows:{input_rows}')
    print(f'Morgan fingerprint parameters:radius={radius},n_bit={n_bits}')

    X, y, smiles_array = featurize_dataframe(df, radius, n_bits)
    print(f'freaturelize rows:{len(y)}')
    print(f'freaturelize matrix shape:{X.shape}')
    print(f"Label vector shape: {y.shape}")
    print()
    print("Label distribution:")
    print(pd.Series(y).value_counts())
    output_path.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(
        output_path,    
        X=X,            
        y=y,            
        smiles=smiles_array
    )
    # data = np.load(output_path)
    # # print(f'{X},{y},{smiles_array}')
    # X_check = data['X']
    # y_check = data['y']
    # smiles_check = data['smiles']
    # print(f'{X_check.shape}')
    # print(f'{y_check.shape}')
    # print(f'{smiles_check.shape}')
if __name__ == "__main__":
    build_morgan_features()

