import streamlit as st # type: ignore
import pandas as pd # type: ignore
from io import BytesIO 

st.set_page_config(page_title="File Converter", layout="wide" )
st.title("📁 File Converter & Cleaner")
st.write("upload CSV or EXCEL files, clean data, and convert formats ")

uploaded_file = st.file_uploader("Upload CSV or EXCEL files.", type=["csv", "xlsx"], accept_multiple_files=True) 

if uploaded_file:
    for file in uploaded_file:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f" 🔎{file.name} - preview")
        st.dataframe(df.head())

       
        if st.checkbox(f" file missing values - {file.name}"):
                df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
                st.success(f"Successfully  filled missing values")
                st.dataframe(df.head())

        selected_colums = st.multiselect(f"Select Columns - {file.name} ", df.columns, default=df.columns )
        df = df[selected_colums]
        st.dataframe(df.head())

        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(f"Convert {file.name} to: ",["CSV","Excel"], key=file.name)  

        if st.button(f"⬇️ Download {file.name} as {format_choice}"):
             output = BytesIO()
             if format_choice == "CSV":
                 df.to_csv(output, index=False)
                 mime = "text/csv"
                 new_name = file.name.replace(ext, "csv")
             else:
                 df.to_excel(output, index=False)
                 mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                 new_name = file.name.replace(ext, "xlsx")
                 output.seek(0)
                 st.download_button("⬇️ Download File ", file_name=new_name, data=output, mime=mime, )
                 st.success("Processing Completed 🎉 ")


                  
         

       

 

