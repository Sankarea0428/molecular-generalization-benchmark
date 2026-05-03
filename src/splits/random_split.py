import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
input_path = Path('data/processed/bbbp_morgan_features.npz')
output_path = Path('data/processed/bbbp_random_split.npz')
test_size = 0.2
random_state = 42
def build_random_split():
    data= np.load(input_path)
    X = data['X']
    y = data['y']
    smiles = data['smiles']
    print(f'Loaded feature path{input_path}')
    print(f'Total output:{len(y)}')
    print(f'{X.shape}')
    print(f'{y.shape}')
    print(f'{smiles.shape}')
    X_train, X_test, y_train, y_test, smiles_train, smiles_test = train_test_split(
    X,
    y,
    smiles,
    test_size=test_size,
    random_state=random_state,
    stratify=y
)
    print({f'Test size:{len(X_test),len(y_test)}'})
    print({f"Train size{len(X_train),len(y_train)}"})
    print(f'Train label distribution:{pd.Series(y_train).value_counts()}')
    print(f'Test label distribution:{pd.Series(y_test).value_counts()}')
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
    print(f"Saved to: {output_path}")
    data = np.load(output_path)

    print(data.files)

    X_train_check = data["X_train"]
    X_test_check = data["X_test"]
    y_train_check = data["y_train"]
    y_test_check = data["y_test"]
    smiles_train_check = data["smiles_train"]
    smiles_test_check = data["smiles_test"]

    print(f"Loaded X_train shape: {X_train_check.shape}")
    print(f"Loaded X_test shape: {X_test_check.shape}")
    print(f"Loaded y_train shape: {y_train_check.shape}")
    print(f"Loaded y_test shape: {y_test_check.shape}")
    print(f"Loaded smiles_train shape: {smiles_train_check.shape}")
    print(f"Loaded smiles_test shape: {smiles_test_check.shape}")
if __name__ == "__main__":
    build_random_split()