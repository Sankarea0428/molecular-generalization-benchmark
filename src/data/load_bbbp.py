from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "BBBP.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "bbbp_clean.csv"


def find_column(df: pd.DataFrame, candidate_names: list[str]) -> str:
# 从可能的列名列表中找到存在的列名。
    for name in candidate_names:
        if name in df.columns:
            return name

    raise ValueError(
        f"None of the candidate columns {candidate_names} were found. "
        f"Available columns are: {list(df.columns)}"
    )


def load_and_clean_bbbp(raw_path: Path = RAW_DATA_PATH) -> pd.DataFrame:

    # 加载BBBP数据 标准化列 删除无SMILES结构缺失样本 返回数据集 仅保留smiles的分子结构式以及相应的分子标签

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Cannot find raw dataset at: {raw_path}\n"
            f"Please put BBBP.csv into data/raw/"
        )

    df = pd.read_csv(raw_path)

    print("Raw dataset loaded.")
    print(f"Raw shape: {df.shape}")
    print(f"Raw columns: {list(df.columns)}")

    smiles_col = find_column(df, ["smiles", "SMILES", "Smiles"])
    label_col = find_column(df, ["label", "Label", "p_np", "target", "y", "class", "Class"])

    clean_df = df[[smiles_col, label_col]].copy()

    clean_df = clean_df.rename(
        columns={
            smiles_col: "smiles",
            label_col: "label",
        }
    )

    clean_df = clean_df.dropna(subset=["smiles"]).copy()

    clean_df["smiles"] = clean_df["smiles"].astype(str).str.strip()

    clean_df = clean_df[clean_df["smiles"] != ""].copy()

    print("\nClean dataset created.")
    print(f"Clean shape: {clean_df.shape}")

    print("\nLabel distribution:")
    print(clean_df["label"].value_counts(dropna=False).sort_index())

    return clean_df


def save_clean_bbbp(clean_df: pd.DataFrame, output_path: Path = PROCESSED_DATA_PATH) -> None:
# 保存已经缓存的数据集
    output_path.parent.mkdir(parents=True, exist_ok=True)

    clean_df.to_csv(output_path, index=False)

    print(f"\nClean dataset saved to: {output_path}")


def main() -> None:
    clean_df = load_and_clean_bbbp()
    save_clean_bbbp(clean_df)


if __name__ == "__main__":
    main()