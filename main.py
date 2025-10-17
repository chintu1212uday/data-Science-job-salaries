
# main.py - convenience wrapper
# Use this to run the EDA script before launching Streamlit if you want.
import os
print('Running EDA analysis to generate outputs...')
os.system('python eda_analysis.py')
print('To run the Streamlit app, execute: streamlit run app.py')


# main.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Check if Streamlit is available
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except:
    STREAMLIT_AVAILABLE = False

# Create output folder if not exists
if not os.path.exists('output'):
    os.makedirs('output')

def generate_report(df):
    # Summary statistics
    summary = df.describe()

    # Plot average salary by experience
    plt.figure(figsize=(6,4))
    df.groupby('experience_level')['salary'].mean().plot(kind='bar', color='skyblue')
    plt.title('Average Salary by Experience Level')
    plt.ylabel('Salary')
    plt.tight_layout()
    plt.savefig('output/salary_plot.png')
    plt.close()

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Data Science Job Salaries Report", ln=True, align='C')

    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(0, 10, "Summary Statistics:", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 5, summary.to_string())

    pdf.ln(10)
    pdf.cell(0, 10, "Plots:", ln=True)
    pdf.image('output/salary_plot.png', w=150)

    # Save PDF
    pdf_path = "output/Job_Salaries_Report.pdf"
    pdf.output(pdf_path)
    return pdf_path

def run_streamlit():
    st.title("Data Science Job Salaries Report Generator")
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Data Preview")
        st.dataframe(df.head())

        st.subheader("Summary Statistics")
        st.dataframe(df.describe())

        st.subheader("Average Salary by Experience Level")
        fig, ax = plt.subplots()
        df.groupby('experience_level')['salary'].mean().plot(kind='bar', ax=ax, color='skyblue')
        ax.set_ylabel('Salary')
        st.pyplot(fig)

        if st.button("Generate PDF Report"):
            pdf_path = generate_report(df)
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="Job_Salaries_Report.pdf")

def run_matplotlib():
    file_path = input("Enter CSV file path (default: dataset/data.csv): ").strip()
    if file_path == "":
        file_path = "dataset/data.csv"

    if not os.path.exists(file_path):
        print("CSV file not found!")
        return

    df = pd.read_csv(file_path)
    print("\nSummary Statistics:\n")
    print(df.describe())

    # Plot average salary by experience
    plt.figure(figsize=(6,4))
    df.groupby('experience_level')['salary'].mean().plot(kind='bar', color='skyblue')
    plt.title('Average Salary by Experience Level')
    plt.ylabel('Salary')
    plt.tight_layout()
    plot_path = 'output/salary_plot.png'
    plt.savefig(plot_path)
    plt.show()

    # Generate PDF report
    pdf_path = generate_report(df)
    print(f"\nReport generated successfully: {pdf_path}")

if __name__ == "__main__":
    if STREAMLIT_AVAILABLE:
        run_streamlit()
    else:
        run_matplotlib()
