import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_superstore_____.csv', encoding='latin-1')
    df['Profit_Margin'] = ((df['Profit'] / df['Sales']) * 100).round(2)
    df['Profit_Loss'] = df['Profit'].apply(lambda x: ' Profit' if x > 0 else ' Loss')
    return df

df = load_data()

st.sidebar.title(" Filters")
selected_category = st.sidebar.multiselect("Category", options=df['Category'].unique(), default=df['Category'].unique())
selected_region = st.sidebar.multiselect("Region", options=df['Region'].unique(), default=df['Region'].unique())
selected_segment = st.sidebar.multiselect("Segment", options=df['Segment'].unique(), default=df['Segment'].unique())

filtered_df = df[(df['Category'].isin(selected_category)) & (df['Region'].isin(selected_region)) & (df['Segment'].isin(selected_segment))]

st.title("Superstore Sales Analytics Dashboard")
st.caption("Data Analytics Project | 9,994 Real Records")
st.markdown("---")

k1, k2, k3, k4, k5 = st.columns(5)
with k1: st.metric(" Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
with k2: st.metric(" Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
with k3: st.metric(" Total Orders", f"{len(filtered_df):,}")
with k4: st.metric(" Avg Discount", f"{filtered_df['Discount'].mean()*100:.1f}%")
with k5: st.metric(" Profit Margin", f"{filtered_df['Profit_Margin'].mean():.1f}%")

st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    cat_sales = filtered_df.groupby('Category')[['Sales','Profit']].sum().reset_index()
    fig1 = px.bar(cat_sales, x='Category', y=['Sales','Profit'], title=' Sales vs Profit by Category', barmode='group', color_discrete_sequence=['#636EFA','#00CC96'])
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    fig2 = px.pie(filtered_df.groupby('Region')['Sales'].sum().reset_index(), values='Sales', names='Region', title='🗺️ Sales by Region', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    sub_sales = filtered_df.groupby('Sub-Category')['Sales'].sum().reset_index().sort_values('Sales', ascending=True).tail(10)
    fig3 = px.bar(sub_sales, x='Sales', y='Sub-Category', title='Top 10 Sub-Categories', orientation='h', color='Sales', color_continuous_scale='Viridis')
    st.plotly_chart(fig3, use_container_width=True)
with c4:
    fig4 = px.pie(filtered_df.groupby('Segment')['Sales'].sum().reset_index(), values='Sales', names='Segment', title='👥 Sales by Segment', color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
c5, c6 = st.columns(2)
with c5:
    sub_profit = filtered_df.groupby('Sub-Category')['Profit'].sum().reset_index().sort_values('Profit', ascending=True)
    fig5 = px.bar(sub_profit, x='Profit', y='Sub-Category', title=' Profit by Sub-Category', orientation='h', color='Profit', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig5, use_container_width=True)
with c6:
    fig6 = px.scatter(filtered_df, x='Sales', y='Profit', color='Category', size='Quantity', title='💹 Sales vs Profit', color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
top_states = filtered_df.groupby('State')['Sales'].sum().reset_index().sort_values('Sales', ascending=False).head(10)
fig7 = px.bar(top_states, x='State', y='Sales', title='Top 10 States by Sales', color='Sales', color_continuous_scale='Blues')
fig7.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")
heatmap = filtered_df.pivot_table(values='Profit', index='Category', columns='Region', aggfunc='sum').fillna(0)
fig8 = px.imshow(heatmap, title='Profit Heatmap — Category vs Region', color_continuous_scale='RdYlGn', aspect='auto')
st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")
fig9 = px.scatter(filtered_df, x='Discount', y='Profit', color='Category', title=' Discount Impact on Profit', trendline='ols', color_discrete_sequence=px.colors.qualitative.Vivid)
st.plotly_chart(fig9, use_container_width=True)

st.markdown("---")
st.subheader("Raw Data")
search = st.text_input("Search by City or State")
show_df = filtered_df[['Ship Mode','Segment','City','State','Region','Category','Sub-Category','Sales','Quantity','Discount','Profit','Profit_Loss']]
if search:
    show_df = show_df[show_df['City'].str.contains(search, case=False) | show_df['State'].str.contains(search, case=False)]
st.dataframe(show_df.head(100), use_container_width=True)
