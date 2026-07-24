import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text
import sys
import os
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database import get_engine
from app.components import apply_custom_css, render_sidebar, load_fallback_df
from app.translations import t

st.set_page_config(page_title="Regional Analysis", page_icon="🗺️", layout="wide")
apply_custom_css()

# Render Sidebar with Language Toggle
render_sidebar()
lang = st.session_state.get("lang", "el")

st.title(t("regions_title", lang))
st.markdown(t("regions_subtitle", lang))

@st.cache_data(ttl=3600)
def load_data() -> pd.DataFrame:
    query = "SELECT * FROM tourism_data"
    try:
        engine = get_engine()
        if engine:
            with engine.connect() as conn:
                df = pd.read_sql(text(query), conn)
            if not df.empty:
                if 'receipts' in df.columns:
                    df['receipts'] = df['receipts'] * 1_000_000
                if 'turnover' in df.columns:
                    df['turnover'] = df['turnover'] * 1_000
                return df
    except Exception as e:
        pass
        
    return load_fallback_df()

df = load_data()

if df.empty:
    st.warning("No data found.")
    st.stop()

# Filter df by NUTS length
df = df[df['geo'].str.len() == 4]

# Filters
years = sorted(df['year'].unique().tolist())
col_filter, col_export = st.columns([3, 1])

with col_filter:
    all_years_label = t("all_years", lang)
    selected_year = st.selectbox(t("select_year", lang), [all_years_label] + years)

if selected_year != all_years_label:
    filtered_df = df[df['year'] == selected_year]
    title_suffix = f"({selected_year})"
else:
    filtered_df = df
    title_suffix = f"({t('all_years', lang)} 2019-2024)"

# Aggregate by region
region_data = filtered_df.groupby(['geo', 'geo_label'])[['arrivals', 'receipts', 'overnights']].sum().reset_index()
region_data['alos'] = region_data['overnights'] / region_data['arrivals']
region_data['daily_yield'] = region_data['receipts'] / region_data['overnights']

with col_export:
    st.markdown("<br>", unsafe_allow_html=True)
    csv = region_data.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')
    st.download_button(
        label=t("download_csv", lang),
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
    st.subheader(t("map_title", lang))
    fig_map = px.choropleth(
        region_data,
        geojson=geojson,
        locations="geo",
        featureidkey="properties.NUTS_ID",
        color="arrivals",
        hover_name="geo_label",
        color_continuous_scale="Blues",
        title=f"{t('map_title', lang)} {title_suffix}"
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# Create tabs for charts and side-by-side comparison
tab1, tab2, tab3, tab_alos, tab_yield, tab4 = st.tabs([
    t("tab_arrivals", lang), 
    t("tab_overnights", lang), 
    t("tab_receipts", lang), 
    t("tab_alos", lang), 
    t("tab_yield", lang), 
    t("tab_compare", lang)
])

with tab1:
    top_arrivals = region_data.sort_values(by="arrivals", ascending=False).head(10)
    fig_bar = px.bar(
        top_arrivals, x="arrivals", y="geo_label", 
        orientation='h',
        title=f"{t('tab_arrivals', lang)} {title_suffix}",
        labels={"arrivals": t("col_arrivals", lang), "geo_label": t("col_geo_label", lang)},
        color="arrivals",
        color_continuous_scale="Blues"
    )
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    top_overnights = region_data.sort_values(by="overnights", ascending=False).head(10)
    fig_bar_overnights = px.bar(
        top_overnights, x="overnights", y="geo_label", 
        orientation='h',
        title=f"{t('tab_overnights', lang)} {title_suffix}",
        labels={"overnights": t("col_overnights", lang), "geo_label": t("col_geo_label", lang)},
        color="overnights",
        color_continuous_scale="Purples"
    )
    fig_bar_overnights.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
    st.plotly_chart(fig_bar_overnights, use_container_width=True)

with tab3:
    top_receipts = region_data.sort_values(by="receipts", ascending=False).head(5)
    other_label = "Other Regions" if lang == "en" else "Άλλες Περιοχές"
    other_receipts = region_data.sort_values(by="receipts", ascending=False).iloc[5:]['receipts'].sum()
    
    pie_data = pd.DataFrame({
        'geo_label': top_receipts['geo_label'].tolist() + [other_label],
        'receipts': top_receipts['receipts'].tolist() + [other_receipts]
    })
    
    fig_pie = px.pie(
        pie_data, values="receipts", names="geo_label", 
        title=f"{t('tab_receipts', lang)} {title_suffix}",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_layout(height=500)
    st.plotly_chart(fig_pie, use_container_width=True)

with tab_alos:
    sort_alos = region_data.sort_values(by="alos", ascending=False)
    fig_bar_alos = px.bar(
        sort_alos, x="alos", y="geo_label",
        orientation='h',
        title=f"{t('tab_alos', lang)} {title_suffix}",
        labels={"alos": t("col_alos", lang), "geo_label": t("col_geo_label", lang)},
        color="alos",
        color_continuous_scale="Teal"
    )
    fig_bar_alos.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
    st.plotly_chart(fig_bar_alos, use_container_width=True)

with tab_yield:
    sort_yield = region_data.sort_values(by="daily_yield", ascending=False)
    fig_bar_yield = px.bar(
        sort_yield, x="daily_yield", y="geo_label",
        orientation='h',
        title=f"{t('tab_yield', lang)} {title_suffix}",
        labels={"daily_yield": t("col_yield", lang), "geo_label": t("col_geo_label", lang)},
        color="daily_yield",
        color_continuous_scale="Viridis"
    )
    fig_bar_yield.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
    st.plotly_chart(fig_bar_yield, use_container_width=True)

with tab4:
    st.subheader(t("tab_compare", lang))
    all_regions = sorted(df['geo_label'].unique().tolist())
    comp_col1, comp_col2 = st.columns(2)
    
    with comp_col1:
        reg_a = st.selectbox(t("select_region_a", lang), all_regions, index=0)
    with comp_col2:
        default_idx = 1 if len(all_regions) > 1 else 0
        reg_b = st.selectbox(t("select_region_b", lang), all_regions, index=default_idx)
        
    df_comp = df[df['geo_label'].isin([reg_a, reg_b])].groupby(['geo_label', 'year'])[['arrivals', 'overnights', 'receipts']].sum().reset_index()
    df_comp['alos'] = df_comp['overnights'] / df_comp['arrivals']
    df_comp['daily_yield'] = df_comp['receipts'] / df_comp['overnights']
    
    c_tab1, c_tab2, c_tab3 = st.tabs([t("tab_receipts", lang), t("tab_alos", lang), t("tab_yield", lang)])
    
    with c_tab1:
        st.markdown(f"#### {reg_a} vs {reg_b}")
        fig_comp_rec = px.bar(
            df_comp, x="year", y="receipts", color="geo_label", barmode="group",
            labels={"year": t("col_year", lang), "receipts": t("col_receipts", lang), "geo_label": t("col_geo_label", lang)},
            color_discrete_sequence=["#005BAE", "#ff7f0e"]
        )
        st.plotly_chart(fig_comp_rec, use_container_width=True)

    with c_tab2:
        fig_comp_alos = px.line(
            df_comp, x="year", y="alos", color="geo_label", markers=True,
            labels={"year": t("col_year", lang), "alos": t("col_alos", lang), "geo_label": t("col_geo_label", lang)},
            color_discrete_sequence=["#005BAE", "#9467bd"]
        )
        st.plotly_chart(fig_comp_alos, use_container_width=True)

    with c_tab3:
        fig_comp_yield = px.line(
            df_comp, x="year", y="daily_yield", color="geo_label", markers=True,
            labels={"year": t("col_year", lang), "daily_yield": t("col_yield", lang), "geo_label": t("col_geo_label", lang)},
            color_discrete_sequence=["#005BAE", "#e377c2"]
        )
        st.plotly_chart(fig_comp_yield, use_container_width=True)
