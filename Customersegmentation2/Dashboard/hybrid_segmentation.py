import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Lebarkan tampilan halaman
st.set_page_config(layout="wide")

# Judul aplikasi
st.title("Demographic Segmentation")

# URL dataset
url = "https://raw.githubusercontent.com/nahwan25/Machine-Learning/main/Customersegmentation2/Dataset/Hybrid_Segmentation_Head.csv"

# Load dataset
df = pd.read_csv(url)

# Sidebar Filter (Letakkan di kiri atas)
st.sidebar.header("Filter Data")
selected_class = st.sidebar.multiselect(
    "Pilih Cluster yang ingin ditampilkan:", df["Class"].unique(), default=df["Class"].unique()
)

# Filter dataset berdasarkan pilihan
df_filtered = df[df["Class"].isin(selected_class)]

# **Layout Grid: Lebarkan dataset (3/4) dibanding scatter plot (4/4)**
col1, col2 = st.columns([3, 4], gap="large")  

# **Kolom 1 (Kiri) - Dataset lebih luas**
with col1:
    st.subheader("Dataset")
    st.dataframe(df_filtered, use_container_width=True)

# **Kolom 2 (Kanan) - 3D Scatter Plot lebih besar**
with col2:
    st.subheader("3D Scatter Plot: Umur vs Nilai Belanja Setahun")
    fig = px.scatter_3d(
        df_filtered,
        x="Umur",
        y="NilaiBelanjaSetahun",
        z="Class",
        color="Class",
        title="3D Scatter Plot: Umur vs Nilai Belanja Setahun",
        labels={"Umur": "Umur", "NilaiBelanjaSetahun": "Nilai Belanja Setahun", "Class": "Cluster"},
        opacity=0.8
    )
    st.plotly_chart(fig, use_container_width=True)

# **Distribusi Pelanggan per Class (Lebih lebar, tengah layar)**
st.subheader("Distribusi Pelanggan per Class")
fig, ax = plt.subplots(figsize=(14, 6))  # Lebarkan grafik
sns.countplot(x='Class', data=df_filtered, palette="viridis", ax=ax)
ax.set_xlabel("Class")
ax.set_ylabel("Jumlah Pelanggan")
ax.set_title("Distribusi Pelanggan per Class")
st.pyplot(fig)
