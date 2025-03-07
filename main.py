import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up Our app
st.set_page_config(page_title="Data-Sweeper", layout="wide")
st.title("🧹 Data-Sweeper")
st.write("Transform your file between CSV and Excel format, built-in Data Clean and Visualization")

# Corrected Parameter (added "s")
upload_file = st.file_uploader("📂 Upload your File (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_file:
    for file in upload_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file: {file_ext}")
            continue

        # Display info about the file
        st.write(f"📄 **File Name:** {file.name}")
        st.write(f"📏 **File Size:** {file.size / 1024:.2f} KB")

        # Show first 5 rows
        st.write("🔍 **Preview the Head of the DataFrame**")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"🧼 Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed")

            with col2:
                if st.button(f"🩹 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Filled")

        # Column Selection
        st.subheader("📊 Select Columns for Conversion")
        selected_columns = st.multiselect(f"📌 Choose Columns", df.columns, default=df.columns)
        df = df[selected_columns]

        # Data Visualization
        st.subheader("📈 Data Visualization")
        if st.checkbox(f"📊 Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion
        st.subheader("🔄 Convert Options")
        conversion_type = st.radio(f"📥 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"🔄 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("✅ All files have been processed successfully! 🚀")
