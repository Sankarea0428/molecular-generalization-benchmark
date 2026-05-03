from src.data.load_bbbp import main
import argparse
from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score
from src.models.baselines import load_split_file,baseline_models,train_and_predict,save_predictions
def parse_args():
    parser = argparse.ArgumentParser(description='Run one molecular generalization baseline experiment.')
    parser.add_argument(
    '--split',
    choices=['random', 'scaffold'],
    required=True,
    help='Specify which split method to use: random or scaffold'
)
    parser.add_argument(
    "--model",
    choices=["logistic_regression", "random_forest"],
    required=True,
    help="Specify which baseline model to use"
)
    return parser.parse_args()
def get_split_path(split_name):
    split_paths = {
        "random": Path("data/processed/bbbp_random_split.npz"),
        "scaffold": Path("data/processed/bbbp_scaffold_split.npz"),
    }

    return split_paths[split_name]
def get_model(model_name):
    models = baseline_models()
    return models[model_name]
if __name__ == "__main__":
    args = parse_args()

    split_path = get_split_path(args.split)
    model = get_model(args.model)

    print("Selected split:", args.split)
    print("Selected split file:", split_path)
    print("Selected model:", args.model)
    print("Model object:", model)

    X_train, X_test, y_train, y_test, smiles_train, smiles_test = load_split_file(split_path)
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"y_test shape: {y_test.shape}")
    print(f"smiles_train shape: {smiles_train.shape}")
    print(f"smiles_test shape: {smiles_test.shape}")

    y_pred,y_proba = train_and_predict(model,X_train,y_train,X_test)

    print(f"y_pred shape: {y_pred.shape}")
    print(f"y_proba shape: {y_proba.shape}")
    save_predictions(
    y_test = y_test,
    y_pred = y_pred,
    y_proba = y_proba,
    smiles_test = smiles_test,
    model_name = args.model,
    split_name = args.split
)
    accuracy = accuracy_score(y_test,y_pred)
    precision = precision_score(y_test, y_pred,zero_division=0)
    recall = recall_score(y_test, y_pred,zero_division=0)
    f1 = f1_score(y_test, y_pred,zero_division=0)
    roc_auc = roc_auc_score(y_test,y_proba)
    print("Experiment metrics:")
    print(f"split: {args.split}")
    print(f"model: {args.model}")
    print(f"accuracy: {accuracy:.4f}")
    print(f"precision: {precision:.4f}")
    print(f"recall: {recall:.4f}")
    print(f"f1: {f1:.4f}")
    print(f"roc_auc: {roc_auc:.4f}")
    # python run_experiment.py