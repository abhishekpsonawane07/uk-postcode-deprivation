import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

st.set_page_config(
    page_title="Does Your Postcode Decide Your Life?",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Does Your Postcode Decide Your Life?")
st.subheader("Analysing deprivation, education and health across 317 English Local Authorities")
st.markdown("**Data Source:** ONS Indices of Multiple Deprivation 2019")

# Load and process data
@st.cache_data
def load_data():
    df = pd.read_excel('File_7_-_All_IoD2019_Scores__Ra.xlsx', 
                       sheet_name='IOD2019_Scores')
    df = df[[
        'LSOA code (2011)',
        'Local Authority District code (2019)',
        'Local Authority District name (2019)',
        'Index of Multiple Deprivation (IMD) Score',
        'Income Score (rate)',
        'Education, Skills and Training Score',
        'Health Deprivation and Disability Score'
    ]]
    df.columns = ['lsoa_code', 'la_code', 'la_name', 
                  'imd_score', 'income_score', 
                  'education_score', 'health_score']
    df_la = df.groupby('la_name').agg(
        avg_imd=('imd_score', 'mean'),
        avg_income=('income_score', 'mean'),
        avg_education=('education_score', 'mean'),
        avg_health=('health_score', 'mean')
    ).reset_index()
    return df_la

df_la = load_data()

# Headline metrics
st.markdown("---")
col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        label="Least Deprived Area", 
        value="Hart",
        delta="IMD Score: 5.7"
    )
    
with col2:
    st.metric(
        label="Most Deprived Area",
        value="Blackpool",
        delta="IMD Score: 45.9",
        delta_color="inverse"
    )


with col3:
    st.metric(
        label="Deprivation Gap",
        value="8x",
        delta="317 Local Authorities analysed"
    )

# Choropleth Map
st.markdown("---")
st.subheader("🗺️ Deprivation Across England")

@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/eng/lad.json"
    response = requests.get(url)
    return response.json()

geojson_data = load_geojson()

fig_map = px.choropleth(
    df_la,
    geojson=geojson_data,
    locations='la_name',
    featureidkey='properties.LAD13NM',
    color='avg_imd',
    color_continuous_scale='RdYlGn_r',
    title='Deprivation Score by Local Authority',
    labels={'avg_imd': 'Deprivation Score'}
)

fig_map.update_geos(fitbounds="locations", visible=False)
fig_map.update_layout(
    title_font_size=20,
    coloraxis_colorbar=dict(
        title="Deprivation Score",
        tickvals=[10, 20, 30, 40],
        ticktext=['Low', 'Medium', 'High', 'Very High']
    )
)

st.plotly_chart(fig_map, use_container_width=True)

# Bar Chart
st.markdown("---")
st.subheader("📊 Most vs Least Deprived Areas")

most_deprived = df_la.nlargest(10, 'avg_imd').sort_values('avg_imd', ascending=True)
least_deprived = df_la.nsmallest(10, 'avg_imd').sort_values('avg_imd', ascending=False)

fig_bar = go.Figure()

fig_bar.add_trace(go.Bar(
    x=most_deprived['avg_imd'],
    y=most_deprived['la_name'],
    orientation='h',
    name='Most Deprived',
    marker_color='crimson'
))

fig_bar.add_trace(go.Bar(
    x=least_deprived['avg_imd'],
    y=least_deprived['la_name'],
    orientation='h',
    name='Least Deprived',
    marker_color='green'
))

fig_bar.update_layout(
    title='Top 10 Most vs Least Deprived Local Authorities',
    xaxis_title='Average Deprivation Score',
    barmode='group',
    height=500
)

st.plotly_chart(fig_bar, use_container_width=True)

# Scatter Chart
st.markdown("---")
st.subheader("🔵 Deprivation vs Education")
st.markdown("Each dot is a Local Authority. Colour shows health score — **red = worse health, green = better health.**")

fig_scatter = px.scatter(
    df_la,
    x='avg_imd',
    y='avg_education',
    color='avg_health',
    hover_name='la_name',
    title='Deprivation vs Education vs Health',
    labels={
        'avg_imd': 'Average Deprivation Score (higher = more deprived)',
        'avg_education': 'Average Education Score (higher = worse)',
        'avg_health': 'Health Score'
    },
    color_continuous_scale='RdYlGn_r'
)

st.plotly_chart(fig_scatter, use_container_width=True)

# Postcode Lookup
st.markdown("---")
st.subheader("🔍 Look Up Your Postcode")
st.markdown("Type any UK postcode to see how deprived your area is.")

postcode = st.text_input("Enter a UK postcode (e.g. NG1 1AA):")

if postcode:
    # Clean the postcode
    postcode_clean = postcode.strip().replace(" ", "")
    
    # Fetch from Postcodes.io API
    url = f"https://api.postcodes.io/postcodes/{postcode_clean}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        admin_district = data['result']['admin_district']
        st.success(f"📍 Your area: **{admin_district}**")
        
        # Match to our deprivation data
        area_data = df_la[df_la['la_name'] == admin_district]
        
        if not area_data.empty:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Deprivation Score", 
                         f"{area_data['avg_imd'].values[0]:.1f}")
            with col2:
                st.metric("Income Score", 
                         f"{area_data['avg_income'].values[0]:.3f}")
            with col3:
                st.metric("Education Score", 
                         f"{area_data['avg_education'].values[0]:.1f}")
            with col4:
                st.metric("Health Score", 
                         f"{area_data['avg_health'].values[0]:.2f}")
        else:
            st.warning("Area found but not in our dataset.")
    else:
        st.error("Postcode not found. Please check and try again.")