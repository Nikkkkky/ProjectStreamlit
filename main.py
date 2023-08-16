import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import mannwhitneyu, chi2_contingency, ttest_ind, shapiro

def run():
    columns = []
    selectableTests = ["Chi2 contingency test", "Mann Whitney test"]
    st.title("Data Artist")
    file = st.file_uploader("Choose a dataset (.csv)")
    if file is not None:
        try:
            df = pd.read_csv(file)
        except pd.errors.EmptyDataError:
            st.error("No data in dataset")        
        except pd.errors.ParserError:
            st.error("ParserError")
        if df.dropna().empty:
            st.error("Dataset is empty")
        else:
            columns = df.columns.to_list()   

        fst = st.selectbox(
            "First field",
            columns
        )
        sec = st.selectbox(
            "Second field",
            columns
        )
        st.header("Plot")
        plot = px.histogram(df, x = fst, y = sec)
        st.plotly_chart(plot)



        st.header("Tests")
        test = st.selectbox("Select test", selectableTests)
        if test == "Chi2 contingency test":
            contingency_table = pd.crosstab(df[fst], df[sec])
            _, pvalue, _, _ = chi2_contingency(contingency_table)
            st.write(f"Chi2 contingency test result: {pvalue:.3f}")
        if test == "Mann Whitney test":
            _, pvalue = mannwhitneyu(df[fst], df[sec])
            st.write(f"Mann Whitney U test result: {pvalue:.3f}")

if __name__=='__main__':
    run()