import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------------- UI CONFIG ----------------
st.set_page_config(
    page_title="Aravind | Data Analytics Portfolio",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM HEADER ----------------
st.markdown("""
    <div style="text-align:center; padding:10px;">
        <h1>📊 Data Analytics Portfolio Dashboard</h1>
        <p style="color:gray;">Superstore Sales Analysis | Built with Streamlit + Plotly</p>
    </div>
""", unsafe_allow_html=True)

# ---------------- SAMPLE DATA ----------------
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 600

    df = pd.DataFrame({
        "Category": np.random.choice(["Furniture", "Office Supplies", "Technology"], n),
        "Region": np.random.choice(["East", "West", "Central", "South"], n),
        "Segment": np.random.choice(["Consumer", "Corporate", "Home Office"], n),
        "Sub-Category": np.random.choice(["Phones", "Chairs", "Binders", "Tables", "Storage"], n),
        "State": np.random.choice(["Tamil Nadu", "Karnataka", "Delhi", "Maharashtra"], n),
        "City": np.random.choice(["Chennai", "Bangalore", "Mumbai", "Delhi"], n),
        "Sales": np.random.randint(100, 8000, n),
        "Quantity": np.random.randint(1, 10, n),
        "Discount": np.random.rand(n),
    })

    df["Profit"] = df["Sales"] * np.random.uniform(-0.3, 0.5, n)
    df["Profit_Margin"] = (df["Profit"] / df["Sales"] * 100).round(2)
    return df

df = load_data()

# ---------------- SIDEBAR FILTER (PORTFOLIO STYLE) ----------------
st.sidebar.title("🎛️ Filters")

category = st.sidebar.multiselect("Category", df["Category"].unique(), df["Category"].unique())
region = st.sidebar.multiselect("Region", df["Region"].unique(), df["Region"].unique())
segment = st.sidebar.multiselect("Segment", df["Segment"].unique(), df["Segment"].unique())

filtered = df[
    (df["Category"].isin(category)) &
    (df["Region"].isin(region)) &
    (df["Segment"].isin(segment))
]

# ---------------- KPI CARDS ----------------
st.markdown("## 📌 Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Sales", f"${filtered['Sales'].sum():,.0f}")
c2.metric("📈 Profit", f"${filtered['Profit'].sum():,.0f}")
c3.metric("📦 Orders", len(filtered))
c4.metric("💹 Avg Margin", f"{filtered['Profit_Margin'].mean():.1f}%")

st.markdown("---")

# ---------------- VISUAL SECTION 1 ----------------
st.markdown("## 📊 Business Overview")

c1, c2 = st.columns(2)

with c1:
    fig = px.bar(
        filtered.groupby("Category")[["Sales", "Profit"]].sum().reset_index(),
        x="Category",
        y=["Sales", "Profit"],
        barmode="group",
        title="Sales vs Profit by Category"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.pie(
        filtered,
        names="Region",
        values="Sales",
        title="Sales Distribution by Region"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- VISUAL SECTION 2 ----------------
st.markdown("## 📊 Performance Deep Dive")

c3, c4 = st.columns(2)

with c3:
    fig = px.bar(
        filtered.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales"),
        x="Sales",
        y="Sub-Category",
        orientation="h",
        title="Top Sub-Categories"
    )
    st.plotly_chart(fig, use_container_width=True)

with c4:
    fig = px.scatter(
        filtered,
        x="Sales",
        y="Profit",
        color="Category",
        size="Quantity",
        title="Sales vs Profit Relationship"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- HEATMAP ----------------
st.markdown("## 🌡️ Category vs Region Analysis")

heat = filtered.pivot_table(
    values="Profit",
    index="Category",
    columns="Region",
    aggfunc="sum"
).fillna(0)

fig = px.imshow(heat, text_auto=True, title="Profit Heatmap")
st.plotly_chart(fig, use_container_width=True)

# ---------------- RAW DATA ----------------
st.markdown("## 📋 Dataset Preview")

st.dataframe(filtered.head(100), use_container_width=True)
