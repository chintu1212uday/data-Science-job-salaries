
"""EDA analysis script that generates plots into outputs/ and a combined PDF report.
Run: python eda_analysis.py
"""
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os

DATA_PATH = os.path.join('data', 'cleaned_data.csv')
OUT_DIR = 'outputs'
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
# simple plots with matplotlib
def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)

# numeric histograms
numeric = df.select_dtypes(include=['int64','float64']).columns.tolist()
for col in numeric:
    fig, ax = plt.subplots(figsize=(8,5))
    ax.hist(df[col].dropna(), bins=30)
    ax.set_title(f'Distribution of {col}')
    save(fig, f'{col}_distribution.png')

# categorical counts
cats = df.select_dtypes(include=['object']).columns.tolist()
for col in cats:
    counts = df[col].value_counts().head(20)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(counts.index.astype(str), counts.values)
    ax.set_xticklabels(counts.index.astype(str), rotation=45, ha='right')
    ax.set_title(f'Count of {col}')
    save(fig, f'{col}_countplot.png')

# combine PNGs to PDF
imgs = [os.path.join(OUT_DIR,f) for f in os.listdir(OUT_DIR) if f.lower().endswith('.png')]
imgs.sort()
if imgs:
    pil_imgs = [Image.open(i).convert('RGB') for i in imgs]
    pil_imgs[0].save(os.path.join(OUT_DIR,'EDA_report.pdf'), save_all=True, append_images=pil_imgs[1:])
print('EDA outputs saved in outputs/')
