import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
random_split_path = Path('data/processed/bbbp_random_split.npz')
scaffold_split_path = Path('data/processed/bbbp_scaffold_split.npz')
result_dir = Path('results/tables')
def load_split_file(split_path):
    data = np.load(split_path)
    X_train = data['X_train']
    y_train = data['y_train']
    X_test = data['X_test']
    y_test = data['y_test']
    smiles_train = data['smiles_train']
    smiles_test = data['smiles_test']
    return X_train,X_test,y_train,y_test,smiles_train,smiles_test
def baseline_models():
    models = {}
    models['logistic_regression'] = LogisticRegression(max_iter=1000,random_state=42)
    models['random_forest'] = RandomForestClassifier(n_estimators=300,random_state=42,n_jobs=-1)
    return models
def train_and_predict(model, X_train, y_train, X_test):
    model.fit(X_train, y_train)
    y_pre = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    return y_pre, y_proba
def save_predictions(y_test, y_pred, y_proba, smiles_test, model_name, split_name):
    result_dir.mkdir(parents = True,exist_ok=True)
    result_df = pd.DataFrame({
        "y_test": y_test,
        "y_pred": y_pred,
        "y_proba": y_proba,
        "smiles_test": smiles_test,
        "model_name": model_name,
        "split_name": split_name
    })
    output_path = result_dir / f'{split_name}_{model_name}_predictions.csv'
    result_df.to_csv(output_path, index=False)
    print(f"Saved predictions to: {output_path}")

def run_baselines():
    split_files = {
        "random": random_split_path,
        "scaffold": scaffold_split_path
    }
    for split_name, split_path in split_files.items():
        X_train, X_test, y_train, y_test, smiles_train, smiles_test = load_split_file(split_path)
        models = baseline_models()
        print(f"{split_name} loaded:")
        print(f"X_train shape: {X_train.shape}")
        print(f"X_test shape: {X_test.shape}")
        print(f"y_train shape: {y_train.shape}")
        print(f"y_test shape: {y_test.shape}")
        print(f"smiles_train shape: {smiles_train.shape}")
        print(f"smiles_test shape: {smiles_test.shape}")
        for model_name,model in models.items():
            print(f"Training model: {model_name} on {split_name}")
            y_pred, y_proba = train_and_predict(model, X_train, y_train, X_test)
            # print(f"y_pred shape: {y_pred.shape}")
            # print(f"y_proba shape: {y_proba.shape}")
            # print("First 5 y_pred:", y_pred[:5])
            # print("First 5 y_proba:", y_proba[:5])
            save_predictions(
            y_test=y_test,
            y_pred=y_pred,
            y_proba=y_proba,
            smiles_test=smiles_test,
            model_name=model_name,
            split_name=split_name
        )
    # check_path = Path("results/tables/random_logistic_regression_predictions.csv")

    # check_df = pd.read_csv(check_path)

    # print("Loaded prediction file:", check_path)
    # print("Shape:", check_df.shape)
    # print("Columns:", list(check_df.columns))
    # print(check_df.head())

if __name__ == "__main__":
    run_baselines()

