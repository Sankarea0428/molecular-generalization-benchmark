import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path 
summary_path = Path('results/tables/bbbp_metrics_summary.csv')
figures_dir = Path('results/figures/')
def load_summary():
    df = pd.read_csv(summary_path)
    print(df.shape)
    print(list(df.columns))
    print(df.head())
    return df
def plot_roc_auc_comparison(df):
    figures_dir.mkdir(parents=True, exist_ok=True)

    plot_df = df.pivot(
        index="model_name",
        columns="split_name",
        values="roc_auc"
    )

    ax = plot_df.plot(kind="bar", figsize=(8, 5))

    ax.set_title("ROC-AUC Comparison: Random Split vs Scaffold Split")
    ax.set_ylabel("ROC-AUC")
    ax.set_xlabel("Model")
    ax.set_ylim(0, 1)
    ax.legend(title="Split")

    plt.tight_layout()

    output_path = figures_dir / "roc_auc_comparison.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved ROC-AUC figure to: {output_path}")
def plot_metrics_comparison(df):
    figures_dir.mkdir(parents=True, exist_ok=True)
    metrics = ["accuracy", "f1", "roc_auc"]
    plot_df = df.copy()
    plot_df['experiment'] = plot_df['split_name'] +'/' + plot_df['model_name']
    plot_df = plot_df.set_index('experiment')[metrics]
    ax = plot_df.plot(kind = 'bar',figsize = (8,5))
    plt.title("Core Metrics Comparison")
    plt.ylabel("Score")
    plt.xlabel("Experiment")
    plt.ylim(0, 1) 
    plt.legend(title="Metric")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    output_path = figures_dir / 'plot_metrics_comparison.png'
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved ROC-AUC figure to: {output_path}")

if __name__ == "__main__":
    summary_df = load_summary()
    plot_roc_auc_comparison(summary_df)
    plot_metrics_comparison(summary_df)