import pandas as pd
from pathlib import Path
from rdkit import Chem
def clean_smiles_with_rdkit():
    input_path = Path("data/processed/bbbp_clean.csv")
    output_path = Path("data/processed/bbbp_rdkit_clean.csv")
    df = pd.read_csv(input_path)
    print("Input data shape:", df.shape)
    count_input = len(df)
    if "smiles" not in df.columns or "label" not in df.columns:
        raise ValueError("Input file must contain smiles and label columns.")
    df['smiles'] = df['smiles'].astype(str).str.strip()
    df = df[df["smiles"] != ""].copy()
    df["canonical_smiles"] = df["smiles"].apply(canonicalize_smiles)
    count_invalid = df["canonical_smiles"].isna().sum()
    df = df.dropna(subset=["canonical_smiles"]).copy()
    df["smiles"] = df["canonical_smiles"]
    df = df[['smiles','label']].copy()
    df.to_csv(output_path, index=False)
    print("Input samples:", count_input)
    print("Invalid SMILES:", count_invalid)
    print("Cleaned label distribution:")
    print(df["label"].value_counts())
def canonicalize_smiles(smiles):
    mol = Chem.MolFromSmiles(smiles)#把纯文本的分子描述变成真实的分子对象
    if mol is None:
        return None
    return Chem.MolToSmiles(mol, canonical=True)
if __name__ == "__main__":
    clean_smiles_with_rdkit()
