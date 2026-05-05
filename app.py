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

st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
           
    
    /* Main background */
    .main { background-color: #0e1117; overflow-x: hidden; }
    .main .block-container { padding-bottom: 2rem; }
    
    /* Hero title responsive */
    .hero-title {
        font-size: clamp(1.8rem, 5vw, 3.5rem);
        font-weight: 800;
        color: #ffffff;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: clamp(0.9rem, 2.5vw, 1.2rem);
        color: #a0aec0;
        margin-bottom: 2rem;
    }
    
    /* Stat row — wraps on mobile */
    .stat-row {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        margin-top: 1rem;
    }
    
    .stat-item {
        min-width: 80px;
    }
    
    .stat-number {
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        font-weight: 800;
        color: #e53e3e;
    }
    
    .stat-label {
        font-size: clamp(0.7rem, 2vw, 0.85rem);
        color: #a0aec0;
    }
    
    /* Report card */
    .report-card {
        background: #1a1f2e;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    
    /* Finding cards */
    .finding-card {
        background: #1a1f2e;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Responsive columns fix */
    @media (max-width: 640px) {
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        .hero-title {
            font-size: 1.8rem;
        }
        .stat-row {
            gap: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div style='padding: 4rem 2rem 2rem 2rem;'>
        <div class='hero-title'>In England, your postcode<br>can predict your future.</div>
        <div class='hero-subtitle'>
            We analysed 32,844 neighbourhoods across 317 Local Authorities.<br>
            Type yours below and see where you stand.
        </div>
    </div>
""", unsafe_allow_html=True)
st.markdown("""
    <div style='padding: 0 2rem 2rem 2rem;'>
        <div class='stat-row'>
            <div class='stat-item'>
                <div class='stat-number'>32,844</div>
                <div class='stat-label'>Neighbourhoods Analysed</div>
            </div>
            <div class='stat-item'>
                <div class='stat-number'>317</div>
                <div class='stat-label'>Local Authorities</div>
            </div>
            <div class='stat-item'>
                <div class='stat-number'>8x</div>
                <div class='stat-label'>Deprivation Gap</div>
            </div>
            <div class='stat-item'>
                <div class='stat-number'>2019</div>
                <div class='stat-label'>ONS Data</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)
st.caption("💡 Best experienced on desktop for full interactivity.")

# Load data
@st.cache_data
def load_data():
    df_la = pd.read_csv('deprivation_data.csv')
    df_la['imd_rank'] = df_la['avg_imd'].rank(ascending=False).astype(int)
    df_la = df_la.round(2)
    return df_la

df_la = load_data()
total_areas = len(df_la)

# Postcode input
st.markdown("---")
col1, col2, col3 = st.columns([1,2,1])
with col2:
    postcode = st.text_input(
        "",
        placeholder="Enter your postcode e.g. NG1 1AA",
        label_visibility="collapsed"
    )

if postcode:
    postcode_clean = postcode.strip().replace(" ", "")
    url = f"https://api.postcodes.io/postcodes/{postcode_clean}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        admin_district = data['result']['admin_district']
        area_data = df_la[df_la['la_name'] == admin_district]

        if not area_data.empty:
            rank = area_data['imd_rank'].values[0]
            imd = area_data['avg_imd'].values[0]
            edu = area_data['avg_education'].values[0]
            health = area_data['avg_health'].values[0]
            income = area_data['avg_income'].values[0]

            percentile = round((rank / total_areas) * 100)
            is_deprived = rank <= 158

            if is_deprived:
                rank_color = "#e53e3e"
                rank_message = f"ranks <strong style='color:{rank_color};'>{rank} out of {total_areas}</strong> most deprived in England — bottom <strong style='color:{rank_color};'>{percentile}%</strong>"
                emoji = "⚠️"
            else:
                rank_color = "#38a169"
                rank_message = f"ranks <strong style='color:{rank_color};'>{rank} out of {total_areas}</strong> — one of England's <strong style='color:{rank_color};'>least deprived</strong> areas 🌟"
                emoji = "✅"

            st.markdown(f"""
                <div style='background:#1a1f2e; border-radius:16px; 
                            padding:2rem; margin:2rem 0;'>
                    <h2 style='color:#ffffff; margin-bottom:0.5rem;'>
                        📍 {admin_district}
                    </h2>
                    <p style='color:#a0aec0; font-size:1.1rem;'>
                        {emoji} Your area {rank_message}
                    </p>
                    <p style='color:#718096; font-size:0.85rem;'>
                        Rank 1 = most deprived · Rank 317 = least deprived
                    </p>
                </div>
            """, unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🏚️ Deprivation", f"{imd:.1f}",
                         help="Overall deprivation score. Higher = more deprived.")
            with col2:
                st.metric("💷 Income", f"{income:.3f}",
                         help="Proportion of people in income poverty.")
            with col3:
                st.metric("🎓 Education", f"{edu:.1f}",
                         help="Education deprivation score. Higher = worse.")
            with col4:
                st.metric("🏥 Health", f"{health:.2f}",
                         help="Health deprivation. Negative = better than average.")
        else:
            st.warning("Area found but not in our England dataset.")
    else:
        st.error("Postcode not found. Please check and try again.")

# Tabs
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📊 Compare Areas", "🗺️ Explore Map", "💡 Key Findings"])

with tab1:
    st.subheader("Most vs Least Deprived Areas in England")
    st.caption("Hover over any bar to see the exact deprivation score.")
    
    most_deprived = df_la.nlargest(10, 'avg_imd').sort_values('avg_imd', ascending=False)
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

with tab2:
    st.subheader("Deprivation Across England")
    st.caption("Darker red = more deprived. Hover over any area to see its score.")

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
        labels={'avg_imd': 'Deprivation Score'},
        hover_data={'avg_education': True, 'avg_health': True}
    )

    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(
        coloraxis_colorbar=dict(
            title="Deprivation",
            tickvals=[10, 20, 30, 40],
            ticktext=['Low', 'Medium', 'High', 'Very High']
        ),
        height=600
    )

    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("💡 For best map experience, view on desktop.")

with tab3:
    st.subheader("💡 What The Data Tells Us")

    st.markdown("""
    <div style='background:#1a1f2e; border-radius:12px; padding:1.5rem; margin-bottom:1rem;'>
        <h3 style='color:#e53e3e;'>Finding 1 — The 8x Deprivation Gap</h3>
        <p style='color:#a0aec0;'>
            Blackpool (IMD: 45.9) is 8 times more deprived than Hart (IMD: 5.7). 
            Same country. Same NHS. Same government. Completely different realities.
            Deprivation directly mirrors education and health outcomes across all 317 areas.
        </p>
    </div>

    <div style='background:#1a1f2e; border-radius:12px; padding:1.5rem; margin-bottom:1rem;'>
        <h3 style='color:#f6ad55;'>Finding 2 — Light In The Darkness</h3>
        <p style='color:#a0aec0;'>
            Despite high deprivation, London boroughs (Hackney, Islington, Lambeth) 
            and Manchester significantly outperform on education. Urban environments, 
            university clusters and policy interventions can partially break the 
            deprivation cycle — but only in connected cities.
        </p>
    </div>

    <div style='background:#1a1f2e; border-radius:12px; padding:1.5rem; margin-bottom:1rem;'>
        <h3 style='color:#68d391;'>Finding 3 — The North/South Divide Is Real</h3>
        <p style='color:#a0aec0;'>
            The choropleth map tells a clear story — deprivation increases 
            significantly north of Derbyshire. The North East, North West and 
            Yorkshire contain the highest concentration of deprived areas while 
            Southern England dominates the least deprived. This isn't coincidence — 
            it's decades of unequal investment.
        </p>
    </div>

    <div style='background:#1a1f2e; border-radius:12px; padding:1.5rem;'>
        <h3 style='color:#76e4f7;'>So What?</h3>
        <p style='color:#a0aec0;'>
            Where you're born in England still significantly shapes your life outcomes. 
            The data suggests that urban agglomeration, educational investment and 
            targeted policy can partially offset deprivation — but without deliberate 
            intervention, postcode remains one of the strongest predictors of your future.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("The Evidence — Deprivation vs Education vs Health")
    st.caption("Each dot is a Local Authority. Colour shows health — red = worse, green = better. Hover to explore.")

    fig_scatter = px.scatter(
        df_la,
        x='avg_imd',
        y='avg_education',
        color='avg_health',
        hover_name='la_name',
        labels={
            'avg_imd': 'Deprivation Score',
            'avg_education': 'Education Score',
            'avg_health': 'Health Score'
        },
        color_continuous_scale='RdYlGn_r',
        height=500
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align:center; padding:2rem; color:#718096;'>
        <p style='font-size:0.9rem;'>
            Built by <strong style='color:#a0aec0;'>Abhishek Sonawane</strong> · MSc Data Science · 
            <a href='https://www.linkedin.com/in/abhishek-sonawane-13557b27a/' 
               target='_blank' style='color:#76e4f7;'>LinkedIn</a> · 
            <a href='https://github.com/abhishekpsonawane07' 
               target='_blank' style='color:#76e4f7;'>GitHub</a>
        </p>
        <p style='font-size:0.8rem;'>
            Data Source: 
            <a href='https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019' 
               target='_blank' style='color:#76e4f7;'>
               ONS Indices of Multiple Deprivation 2019
            </a>
            · Postcode lookup via 
            <a href='https://postcodes.io' target='_blank' style='color:#76e4f7;'>
                Postcodes.io
            </a>
        </p>
    </div>
""", unsafe_allow_html=True)