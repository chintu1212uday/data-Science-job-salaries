
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title='Data Science Job Salaries', layout='wide')
st.title(' Data Science Job Salaries - Interactive EDA & Prediction Dashboard')

# Try importing Plotly, fallback to Matplotlib
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except Exception:
    import matplotlib.pyplot as plt
    PLOTLY_AVAILABLE = False

# File uploader
uploaded_file = st.sidebar.file_uploader(" Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(" File uploaded successfully! Using your uploaded dataset.")
else:
    default_path = os.path.join('data', 'cleaned_data.csv')
    df = pd.read_csv(default_path)
    st.sidebar.info(" Using default dataset (cleaned_data.csv)")

st.sidebar.header('Filters')
experience = st.sidebar.multiselect('Experience Level', options=df.get('experience_level', pd.Series()).dropna().unique().tolist())
company_size = st.sidebar.multiselect('Company Size', options=df.get('company_size', pd.Series()).dropna().unique().tolist())
job_title = st.sidebar.selectbox('Job Title (sample)', options=[None] + df.get('job_title', pd.Series()).dropna().unique().tolist()[:50])

filtered = df.copy()
if experience and 'experience_level' in df.columns:
    filtered = filtered[filtered['experience_level'].isin(experience)]
if company_size and 'company_size' in df.columns:
    filtered = filtered[filtered['company_size'].isin(company_size)]
if job_title and 'job_title' in df.columns:
    filtered = filtered[filtered['job_title'] == job_title]

st.subheader(' Dataset Preview')
st.dataframe(filtered.head(50))

salary_col = 'salary_in_usd' if 'salary_in_usd' in filtered.columns else ('salary' if 'salary' in filtered.columns else None)

# --- Plotly visualizations (fallback to Matplotlib) ---
if salary_col:
    st.subheader(' Salary Distribution')
    if PLOTLY_AVAILABLE:
        fig = px.histogram(filtered, x=salary_col, nbins=30, title='Salary Distribution (USD)', color_discrete_sequence=['#007bff'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8,4))
        ax.hist(filtered[salary_col].dropna(), bins=30, color='skyblue')
        ax.set_xlabel('Salary (USD)'); ax.set_ylabel('Count')
        st.pyplot(fig)

if salary_col and 'experience_level' in filtered.columns:
    st.subheader(' Salary by Experience Level')
    if PLOTLY_AVAILABLE:
        fig = px.box(filtered, x='experience_level', y=salary_col, color='experience_level', title='Salary by Experience Level')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig, ax = plt.subplots(figsize=(8,4))
        groups = filtered.groupby('experience_level')[salary_col].apply(list)
        ax.boxplot([groups[l] for l in groups.index], labels=groups.index)
        ax.set_ylabel('Salary (USD)')
        st.pyplot(fig)

if 'job_title' in filtered.columns:
    st.subheader(' Top 10 Job Titles (by count)')
    top = filtered['job_title'].value_counts().head(10)
    if PLOTLY_AVAILABLE:
        fig = px.bar(top[::-1], x=top[::-1].values, y=top[::-1].index, orientation='h', title='Top 10 Job Titles (by count)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig, ax = plt.subplots(figsize=(8,4))
        ax.barh(top.index[::-1], top.values[::-1])
        ax.set_xlabel('Count')
        st.pyplot(fig)

# --- Downloads ---
st.sidebar.header(' Downloads')
if uploaded_file is not None:
    csv_bytes = uploaded_file.getvalue()
else:
    with open(os.path.join('data', 'cleaned_data.csv'), 'rb') as f:
        csv_bytes = f.read()
st.sidebar.download_button(' Download current CSV', csv_bytes, file_name='data_used.csv')

pdf_path = os.path.join('outputs', 'EDA_report.pdf')
if os.path.exists(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()
    st.sidebar.download_button(' Download EDA report (PDF)', pdf_bytes, file_name='EDA_report.pdf')

# --- Simple Linear Regression ---
st.subheader(' Simple Salary Predictor (Linear Regression)')
if salary_col and st.button('Train & Show Basic Metrics'):
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import mean_absolute_error, mean_squared_error

        df_model = df[[salary_col]].copy()
        if 'experience_level' in df.columns:
            df_model['exp_code'] = df['experience_level'].astype('category').cat.codes
        if 'job_type' in df.columns:
            df_model['jobtype_code'] = df['job_type'].astype('category').cat.codes

        X = df_model.drop(columns=[salary_col]).fillna(0)
        y = df_model[salary_col].fillna(df_model[salary_col].median())

        if X.shape[1] > 0:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LinearRegression().fit(X_train, y_train)
            preds = model.predict(X_test)
            st.write('MAE:', mean_absolute_error(y_test, preds))
            st.write('MSE:', mean_squared_error(y_test, preds))
            st.write('R2 (train):', model.score(X_train, y_train))
        else:
            st.warning(' Not enough features to train the model.')
    except Exception as e:
        st.error(f'Error: {e}')
