import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text
import sys
import os
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database import get_engine
from app.components import apply_custom_css, render_sidebar

st.set_page_config(page_title="Ανάλυση Περιοχών", page_icon="🗺️", layout="wide")
apply_custom_css()

st.title("🗺️ Γεωγραφική Ανάλυση (Regions)")
st.markdown("Σύγκριση της τουριστικής κίνησης ανά περιφέρεια/νομό.")

@st.cache_data(ttl=3600)
def load_data() -> pd.DataFrame:
    query = "SELECT * FROM tourism_data"
    try:
        engine = get_engine()
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn)
            
        if 'receipts' in df.columns:
            df['receipts'] = df['receipts'] * 1_000_000
        if 'turnover' in df.columns:
            df['turnover'] = df['turnover'] * 1_000
            
        return df
    except Exception as e:
        st.error(f"Σφάλμα σύνδεσης με τη βάση: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Δεν βρέθηκαν δεδομένα.")
    st.stop()

# --- SIDEBAR FILTERS ---
render_sidebar()

# Filter df by NUTS length
df = df[df['geo'].str.len() == 4]

# Filters
years = sorted(df['year'].unique().tolist())
col_filter, col_export = st.columns([3, 1])

with col_filter:
    selected_year = st.selectbox("Επιλέξτε Έτος", ["Όλα τα Έτη"] + years)

if selected_year != "Όλα τα Έτη":
    filtered_df = df[df['year'] == selected_year]
    title_suffix = f"({selected_year})"
else:
    filtered_df = df
    title_suffix = "(Συνολικά 2019-2024)"

# Aggregate by region
region_data = filtered_df.groupby(['geo', 'geo_label'])[['arrivals', 'receipts', 'overnights']].sum().reset_index()

with col_export:
    st.markdown("<br>", unsafe_allow_html=True)
    csv = region_data.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')
    st.download_button(
        label="📥 Λήψη (CSV)",
        data=csv,
        file_name=f'regional_data_{selected_year}.csv',
        mime='text/csv',
    )

st.divider()

# --- MAP SECTION ---
@st.cache_data
def get_geojson():
    url = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_60M_2021_4326_LEVL_2.geojson"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

geojson = get_geojson()

if geojson:
    st.subheader("Χάρτης Αφίξεων")
    fig_map = px.choropleth(
        region_data,
        geojson=geojson,
        locations="geo",
        featureidkey="properties.NUTS_ID",
        color="arrivals",
        hover_name="geo_label",
        color_continuous_scale="Blues",
        title=f"Χάρτης Τουριστικών Αφίξεων Ελλάδα {title_suffix}"
    )
    # Focus map on Greece
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.warning("Δεν ήταν δυνατή η φόρτωση του χάρτη από την Eurostat.")

st.divider()

# Create tabs for charts instead of squished columns
tab1, tab2, tab3 = st.tabs(["📊 Αφίξεις", "🛏️ Διανυκτερεύσεις", "💶 Έσοδα"])

with tab1:
    st.subheader("Top 10 Περιοχές (Αφίξεις)")
    top_arrivals = region_data.sort_values(by="arrivals", ascending=False).head(10)
    fig_bar = px.bar(
        top_arrivals, x="arrivals", y="geo_label", 
        orientation='h',
        title=f"Κορυφαίες 10 Περιοχές σε Αφίξεις {title_suffix}",
        labels={"arrivals": "Αφίξεις", "geo_label": "Περιοχή"},
        color="arrivals",
        color_continuous_scale="Blues"
    )
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("Top 10 Περιοχές (Διανυκτερεύσεις)")
    top_overnights = region_data.sort_values(by="overnights", ascending=False).head(10)
    fig_bar_overnights = px.bar(
        top_overnights, x="overnights", y="geo_label", 
        orientation='h',
        title=f"Κορυφαίες 10 Περιοχές σε Διανυκτερεύσεις {title_suffix}",
        labels={"overnights": "Διανυκτερεύσεις", "geo_label": "Περιοχή"},
        color="overnights",
        color_continuous_scale="Purples"
    )
    fig_bar_overnights.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
    st.plotly_chart(fig_bar_overnights, use_container_width=True)

with tab3:
    st.subheader("Μερίδιο Εσόδων")
    top_receipts = region_data.sort_values(by="receipts", ascending=False).head(5)
    # Group the rest into 'Άλλες Περιοχές'
    other_receipts = region_data.sort_values(by="receipts", ascending=False).iloc[5:]['receipts'].sum()
    
    pie_data = pd.DataFrame({
        'geo_label': top_receipts['geo_label'].tolist() + ['Άλλες Περιοχές'],
        'receipts': top_receipts['receipts'].tolist() + [other_receipts]
    })
    
    fig_pie = px.pie(
        pie_data, values="receipts", names="geo_label", 
        title=f"Κατανομή Εσόδων (Top 5 + Άλλες) {title_suffix}",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_layout(height=500)
    st.plotly_chart(fig_pie, use_container_width=True)
