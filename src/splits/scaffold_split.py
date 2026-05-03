import numpy as np
import pandas as pd
from pathlib import Path
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit import RDLogger
RDLogger.DisableLog("rdApp.warning")
input_path = Path('data/processed/bbbp_morgan_features.npz')
output_path = Path('data/processed/bbbp_scaffold_split.npz')
test_size =  0.2
def smiles_to_scaffold(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return ''
    scaffold = MurckoScaffold.MurckoScaffoldSmiles(mol=mol)
    return scaffold


def build_scaffold_split():
    data = np.load(input_path)
    X = data['X']
    y = data['y']
    smiles = data['smiles']
    print(f"Loaded feature file: {input_path}")
    print(f"Total samples: {len(y)}")
    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape}")
    print(f"smiles shape: {smiles.shape}")
    scaffold_to_indices = {}
    for idx, smile in enumerate(smiles):
        scaffold = smiles_to_scaffold(smile)
        if scaffold not in scaffold_to_indices:
           scaffold_to_indices[scaffold] = []
        scaffold_to_indices[scaffold].append(idx)
    num_scaffolds = len(scaffold_to_indices)
    largest_scaffold_size = max(len(indices) for indices in scaffold_to_indices.values())
    print(f"Unique scaffolds: {num_scaffolds}")
    print(f"Largest scaffold size: {largest_scaffold_size}")
    scaffold_groups = scaffold_to_indices.values()
    scaffold_groups = sorted(scaffold_groups,key=len,reverse=True)
    target_test_size = int(len(y) * test_size)
    train_indices = []
    test_indices = []
    for group in scaffold_groups:
        if len(test_indices) < target_test_size:
            test_indices.extend(group)
        else:
            train_indices.extend(group)
    train_indices = np.array(train_indices,dtype=int)
    test_indices = np.array(test_indices,dtype=int)
    actual_test_ratio = len(test_indices) / len(y)

    print(f"Target test size: {target_test_size}")
    print(f"Actual test size: {len(test_indices)}")
    print(f"Actual test ratio: {actual_test_ratio:.3f}")
    X_train = X[train_indices]
    X_test = X[test_indices]
    y_train = y[train_indices]
    y_test = y[test_indices]
    smiles_train = smiles[train_indices]
    smiles_test = smiles[test_indices]
    print(f"Train size: {len(y_train)}")
    print(f"Test size: {len(y_test)}")

    print("Train label distribution:")
    print(pd.Series(y_train).value_counts())

    print("Test label distribution:")
    print(pd.Series(y_test).value_counts())
    output_path.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(
        output_path,
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        smiles_train=smiles_train,
        smiles_test=smiles_test
    )
    print(f'The npz file download into {output_path}')
if __name__ == "__main__":
    build_scaffold_split()