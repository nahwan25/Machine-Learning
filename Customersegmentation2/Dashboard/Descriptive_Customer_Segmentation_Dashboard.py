import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/nahwan25/Machine-Learning/main/Customersegmentation2/Dataset/Customer%20Segmentation.txt"
    return pd.read_csv(url, delimiter="\t")  # Pastikan file ada di repo GitHub

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")
gender_filter = st.sidebar.multiselect("Pilih Jenis Kelamin", df["Jenis Kelamin"].unique(), default=df["Jenis Kelamin"].unique())
profesi_filter = st.sidebar.multiselect("Pilih Profesi", df["Profesi"].unique(), default=df["Profesi"].unique())
umur_range = st.sidebar.slider("Pilih Rentang Umur", int(df["Umur"].min()), int(df["Umur"].max()), (int(df["Umur"].min()), int(df["Umur"].max())))

# Filter dataset
df_filtered = df[(df["Jenis Kelamin"].isin(gender_filter)) & 
                 (df["Profesi"].isin(profesi_filter)) & 
                 (df["Umur"].between(umur_range[0], umur_range[1]))]

st.title("📊 Descriptive Customer Segmentation Dashboard")

# Hitung jumlah pria dan wanita setelah filter
gender_counts = df_filtered["Jenis Kelamin"].value_counts()

# Display jumlah pria dan wanita dalam kolom metrik
colA, colB = st.columns(2)
colA.metric(label="👨‍💼 Jumlah Pria", value=gender_counts.get("Pria", 0))
colB.metric(label="👩‍💼 Jumlah Wanita", value=gender_counts.get("Wanita", 0))

# Layout 2x2 grid untuk visualisasi
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# 1. Rata-rata Belanja Berdasarkan Jenis Kelamin
with col1:
    gender_spending = df_filtered.groupby('Jenis Kelamin')['NilaiBelanjaSetahun'].mean()
    fig, ax = plt.subplots(figsize=(7,5))
    sns.barplot(x=gender_spending.index, y=gender_spending.values, palette="Blues", ax=ax)
    ax.set_xlabel("Jenis Kelamin")
    ax.set_ylabel("Rata-rata Nilai Belanja Setahun")
    ax.set_title("Perbandingan Rata-rata Belanja")
    for i, val in enumerate(gender_spending.values):
        ax.text(i, val, f"{int(val):,}", ha='center', va='bottom', fontsize=12)
    st.pyplot(fig)

# 2. Rata-rata Belanja Berdasarkan Profesi
with col2:
    profesi_spending = df_filtered.groupby('Profesi')['NilaiBelanjaSetahun'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x=profesi_spending.values, y=profesi_spending.index, palette="viridis", ax=ax)
    ax.set_xlabel("Rata-rata Nilai Belanja Setahun")
    ax.set_ylabel("Profesi")
    ax.set_title("Rata-rata Belanja Berdasarkan Profesi")
    for i, val in enumerate(profesi_spending.values):
        ax.text(val, i, f"{int(val):,}", ha='left', va='center', fontsize=12)
    st.pyplot(fig)

# 3. Hubungan Umur dan Nilai Belanja
with col3:
    fig, ax = plt.subplots(figsize=(8,5))
    sns.scatterplot(x=df_filtered['Umur'], y=df_filtered['NilaiBelanjaSetahun'], alpha=0.7, ax=ax)
    sns.regplot(x=df_filtered['Umur'], y=df_filtered['NilaiBelanjaSetahun'], scatter=False, color='red', ax=ax)
    ax.set_xlabel("Umur")
    ax.set_ylabel("Nilai Belanja Setahun")
    ax.set_title("Hubungan Umur dan Nilai Belanja")
    st.pyplot(fig)

# 4. Distribusi Umur Pelanggan
with col4:
    fig, ax = plt.subplots(figsize=(8,5))
    sns.histplot(df_filtered['Umur'], bins=10, kde=True, color="purple", ax=ax)
    ax.set_xlabel("Umur")
    ax.set_ylabel("Frekuensi")
    ax.set_title("Distribusi Umur Pelanggan")
    st.pyplot(fig)

# Tampilkan DataFrame setelah filter
st.subheader("📌 Data Pelanggan (Setelah Filter)")
st.dataframe(df_filtered)
