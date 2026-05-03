
import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score,precision_score,f1_score,roc_auc_score,recall_score
predictions_dir = Path('results/tables')
output_path = predictions_dir / "bbbp_metrics_summary.csv"
def build_metrics_summary():
    predictions_file = list(predictions_dir.glob("*_predictions.csv"))
    predictions_file = sorted(predictions_file)
    print(f'Found prediction files:{len(predictions_file)}')
    summary_rows = []
    for file in predictions_file:
        print(f'{file}')
        df = pd.read_csv(file)
        required_columns = ["y_test","y_pred","y_proba",'smiles_test','model_name','split_name']
        missing_columns = []
        for column in required_columns:
            if column not in df.columns:
                missing_columns.append(column)
        if len(missing_columns)>0:
            raise ValueError(f"The {missing_columns} missing")
        model_name = df["model_name"].iloc[0]
        split_name = df["split_name"].iloc[0]
        print(f"{file.name} {df.shape} {model_name} {split_name}")
        y_test = df['y_test']
        y_pred = df['y_pred']
        y_proba = df['y_proba']
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_proba)
        summary_rows.append({
    "split_name": split_name,
    "model_name": model_name,
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1": f1,
    "roc_auc": roc_auc,
    "n_test": len(y_test),
    "prediction_file": file.name
})
        print(
        f"{split_name} | {model_name} | "
        f"accuracy={accuracy:.4f} | "
        f"precision={precision:.4f} | "
        f"recall={recall:.4f} | "
        f"f1={f1:.4f} | "
        f"roc_auc={roc_auc:.4f}"
        )
    summary_df = pd.DataFrame(summary_rows)
    summary_df = summary_df[
    [
        "split_name",
        "model_name",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "n_test",
        "prediction_file",
    ]
] 
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(output_path,index=False)
    print('\nMetrics summary')
    print(f'{summary_df}')
    print(f'The file saved into {output_path}')

if __name__ == "__main__":
    build_metrics_summary()