# Data Science Job Salaries - Streamlit EDA Project

This project is auto-generated and includes:
- `app.py` : Streamlit interactive app to explore the Data Science Job Salaries dataset and a simple linear regression predictor.
- `eda_analysis.py` : Script that generates EDA plots to `outputs/` and a combined `EDA_report.pdf`.
- `main.py` : Convenience wrapper to run EDA generation then instruct on launching Streamlit.
- `data/cleaned_data.csv` : Cleaned dataset (from your uploaded CSV).
- `outputs/` : Generated images and `EDA_report.pdf`.
- `requirements.txt` : Required Python packages.

## How to run locally
1. Create a virtual environment and install requirements:
```
pip install -r requirements.txt
```
2. (Optional) Generate outputs first:
```
python eda_analysis.py
```
This will populate `outputs/` and produce `outputs/EDA_report.pdf`.

3. Run the Streamlit app:
```
streamlit run app.py
```

Inside the Streamlit UI you'll find download buttons for the cleaned CSV and the PDF report.

