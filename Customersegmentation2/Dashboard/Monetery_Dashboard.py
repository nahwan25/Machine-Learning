import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df1 = pd.read_csv("https://raw.githubusercontent.com/nahwan25/Machine-Learning/refs/heads/main/Customersegmentation2/Dataset/Monetery_Dataset.csv")

# Sidebar filter
selected_class = st.sidebar.multiselect("Filter Kelas Pelanggan", df1["Class"].unique(), default=df1["Class"].unique())
df_filtered = df1[df1["Class"].isin(selected_class)]

# Title
st.title("Monetary Segmentation")

# **Baris Pertama**
col1, col2 = st.columns(2)

# Kolom 1 - Tampilkan dataset
with col1:
    st.subheader("Dataset Pelanggan")
    st.dataframe(df_filtered)

# Kolom 2 - Pie Chart
with col2:
    st.subheader("Distribusi Kelas Pelanggan")
    class_counts = df_filtered["Class"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(class_counts, labels=class_counts.index, autopct='%1.1f%%', colors=['blue', 'orange', 'green'])
    ax.set_title("Distribusi Kelas")
    st.pyplot(fig)

# **Baris Kedua**
col3, col4 = st.columns(2)

# Kolom 3 - Histogram
with col3:
    st.subheader("Distribusi Nilai Belanja")
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.histplot(df_filtered["NilaiBelanjaSetahun"], bins=20, kde=True, color='blue', ax=ax)
    ax.set_xlabel("Nilai Belanja Setahun")
    ax.set_ylabel("Jumlah Pelanggan")
    st.pyplot(fig)

# Kolom 4 - Bar Chart Rata-rata Nilai Belanja
with col4:
    st.subheader("Rata-rata Nilai Belanja")
    avg_spending = df_filtered.groupby("Class")["NilaiBelanjaSetahun"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.barplot(x=avg_spending.index, y=avg_spending.values, palette='coolwarm', ax=ax)
    ax.set_xlabel("Kategori Pelanggan")
    ax.set_ylabel("Rata-rata Nilai Belanja")
    st.pyplot(fig)