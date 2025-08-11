"""
auto_insights_with_formula.py
Fully automated:
 - Reads CSV/XLSX
 - Cleans data
 - Prompts user for a custom formula
 - Applies formula to DataFrame
 - Saves cleaned dataset
 - Generates HTML report with embedded visualizations
"""

import sys, os, io, base64
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import simpledialog

sns.set(style="whitegrid", rc={"figure.figsize": (8,5)})

# ===== Settings =====
MIN_COL_NONNA_RATIO = 0.05
MAX_PAIRPLOT_COLS = 8
OUTPUT_DIR = "auto_insights_output"

# ===== Tkinter formula prompt =====
def ask_formula():
    root = tk.Tk()
    root.withdraw()  # Hide main window
    formula = simpledialog.askstring(
        title="Custom Formula",
        prompt="Enter a Python formula to add a new column.\nExample:\ndf['Total'] = df['Price'] * df['Quantity']"
    )
    root.destroy()
    return formula

# ===== File handling =====
def read_data(path):
    ext = path.lower().split('.')[-1]
    if ext == "csv":
        return pd.read_csv(path, low_memory=False)
    elif ext in ("xls", "xlsx"):
        return pd.read_excel(path)
    else:
        raise ValueError("Unsupported extension. Use .csv, .xls or .xlsx")

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    return OUTPUT_DIR

def save_fig_to_base64(plt):
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

# ===== Cleaning =====
def clean_dataframe(df):
    df = df.replace(r'^\s*$', np.nan, regex=True)
    before_shape = df.shape
    df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')
    df = df.drop_duplicates()
    thresh = int(MIN_COL_NONNA_RATIO * len(df))
    if thresh > 0:
        df = df.dropna(axis=1, thresh=thresh)
    after_shape = df.shape
    return df, before_shape, after_shape

# ===== Insights =====
def make_numeric_distribution_plots(num_df):
    plots = {}
    for col in num_df.columns:
        fig, axes = plt.subplots(2, 1, figsize=(8,6), gridspec_kw={'height_ratios':[3,1]})
        sns.histplot(num_df[col].dropna(), kde=True, ax=axes[0])
        axes[0].set_title(f"Distribution: {col}")
        sns.boxplot(x=num_df[col].dropna(), ax=axes[1])
        plots[col] = save_fig_to_base64(plt)
    return plots

def make_categorical_barplots(cat_df):
    plots = {}
    for col in cat_df.columns:
        top = cat_df[col].fillna("(missing)").value_counts().nlargest(10)
        plt.figure(figsize=(8,4))
        sns.barplot(x=top.values, y=top.index)
        plt.title(f"Top categories: {col}")
        plt.xlabel("Count")
        plots[col] = save_fig_to_base64(plt)
    return plots

def make_correlation_heatmap(num_df):
    plt.figure(figsize=(8,6))
    corr = num_df.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu", center=0)
    plt.title("Correlation matrix")
    return save_fig_to_base64(plt), corr

def make_pairplot(num_df):
    cols = num_df.columns[:MAX_PAIRPLOT_COLS]
    if len(cols) < 2:
        return None
    g = sns.pairplot(num_df[cols].dropna().sample(n=min(500, len(num_df)), random_state=1))
    buf = io.BytesIO()
    g.fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close('all')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

# ===== HTML Report =====
def build_html_report(meta, col_info_html, missing_html, desc_html, topk_html,
                      num_plots_b64, cat_plots_b64, corr_heat_b64, pairplot_b64):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""
    <html><head>
      <meta charset="utf-8"/>
      <title>Auto Insights Report</title>
      <style>
        body{{font-family:Arial; margin:20px;}}
        h1,h2{{color:#222}}
        img{{max-width:100%; border:1px solid #ddd; padding:6px; background:#fff}}
        table{{border-collapse:collapse; width:100%}}
        th,td{{border:1px solid #ccc; padding:6px; font-size:12px}}
      </style>
    </head><body>
      <h1>Auto Insights Report</h1>
      <p><b>Generated:</b> {now}</p>
      <h2>Dataset Summary</h2>
      <pre>{meta}</pre>
      <h2>Columns & Types</h2>{col_info_html}
      <h2>Missing Values</h2>{missing_html}
      <h2>Descriptive Statistics</h2>{desc_html}
      <h2>Top Categories</h2>{topk_html}
    """
    for col, b64 in num_plots_b64.items():
        html += f"<h3>{col}</h3><img src='data:image/png;base64,{b64}' />"
    html += "<h2>Categorical Plots</h2>"
    for col, b64 in cat_plots_b64.items():
        html += f"<h3>{col}</h3><img src='data:image/png;base64,{b64}' />"
    if corr_heat_b64:
        html += "<h2>Correlation Heatmap</h2><img src='data:image/png;base64,{corr_heat_b64}' />"
    if pairplot_b64:
        html += "<h2>Pairplot</h2><img src='data:image/png;base64,{pairplot_b64}' />"
    html += "</body></html>"
    return html

# ===== Main Pipeline =====
def run_pipeline(input_path):
    outdir = ensure_output_dir()
    df = read_data(input_path)
    original_shape = df.shape

    df, before_shape, after_shape = clean_dataframe(df)

    # === Ask for formula ===
    formula = ask_formula()
    if formula:
        try:
            exec(formula, {"df": df, "np": np, "pd": pd})
            print("✅ Formula applied successfully.")
        except Exception as e:
            print(f"⚠ Error applying formula: {e}")

    numeric_df = df.select_dtypes(include=[np.number])
    categorical_df = df.select_dtypes(exclude=[np.number])

    meta = f"Original: {original_shape}\nAfter cleaning: {after_shape}"
    col_info_html = df.dtypes.to_frame("dtype").to_html()
    missing_html = df.isnull().sum().to_frame("missing_count").assign(missing_pct=lambda x: (x["missing_count"]/len(df)).round(3)).to_html()
    desc_html = df.describe(include='all').transpose().to_html()
    topk_html = "".join([f"<h4>{c}</h4>{categorical_df[c].fillna('(missing)').value_counts().head(10).to_frame('count').to_html()}" for c in categorical_df.columns])

    num_plots_b64 = make_numeric_distribution_plots(numeric_df) if not numeric_df.empty else {}
    cat_plots_b64 = make_categorical_barplots(categorical_df) if not categorical_df.empty else {}
    corr_b64, _ = make_correlation_heatmap(numeric_df) if numeric_df.shape[1] > 1 else (None, None)
    pairplot_b64 = make_pairplot(numeric_df) if not numeric_df.empty else None

    html = build_html_report(meta, col_info_html, missing_html, desc_html, topk_html,
                             num_plots_b64, cat_plots_b64, corr_b64, pairplot_b64)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    df.to_csv(os.path.join(outdir, f"cleaned_data_{timestamp}.csv"), index=False)
    df.to_excel(os.path.join(outdir, f"cleaned_data_{timestamp}.xlsx"), index=False)
    with open(os.path.join(outdir, f"insights_report_{timestamp}.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print("\n📊 Report generated successfully.")

# ===== Entry Point =====
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auto_insights_with_formula.py path/to/data.csv")
        sys.exit(1)
    run_pipeline(sys.argv[1])
