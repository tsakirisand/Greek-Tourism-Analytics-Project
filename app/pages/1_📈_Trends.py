import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database import get_engine
from app.components import apply_custom_css, render_sidebar, load_fallback_df
from app.translations import t

st.set_page_config(page_title="Trends Analysis", page_icon="📈", layout="wide")
apply_custom_css()

# Render Sidebar with Language Toggle
render_sidebar()
lang = st.session_state.get("lang", "el")

st.title(t("trends_title", lang))
st.markdown(t("trends_subtitle", lang))

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

# Filter df by NUTS length (Lock to NUTS 2)
df = df[df['geo'].str.len() == 4]

# Aggregate data by year
yearly_data = df.groupby('year')[['arrivals', 'overnights', 'receipts', 'occupancy']].sum().reset_index()

# Compute Industry Advanced KPIs
yearly_data['alos'] = yearly_data['overnights'] / yearly_data['arrivals']
yearly_data['daily_yield'] = yearly_data['receipts'] / yearly_data['overnights']

# Note: Occupancy is an average, so we should take the mean.
yearly_data['occupancy'] = df.groupby('year')['occupancy'].mean().values

has_occupancy = yearly_data['occupancy'].sum() > 0

col1, col2 = st.columns(2)

with col1:
    fig_arrivals = px.line(
        yearly_data, x="year", y="arrivals", 
        markers=True, 
        title=t("chart_arrivals_title", lang),
        labels={"year": t("col_year", lang), "arrivals": t("col_arrivals", lang)}
    )
    fig_arrivals.update_traces(line_color="#005BAE", line_width=3)
    st.plotly_chart(fig_arrivals, use_container_width=True)

with col2:
    fig_receipts = px.line(
        yearly_data, x="year", y="receipts", 
        markers=True, 
        title=t("chart_receipts_title", lang),
        labels={"year": t("col_year", lang), "receipts": t("col_receipts", lang)}
    )
    fig_receipts.update_traces(line_color="#2ca02c", line_width=3)
    st.plotly_chart(fig_receipts, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig_alos = px.line(
        yearly_data, x="year", y="alos",
        markers=True,
        title=t("chart_alos_title", lang),
        labels={"year": t("col_year", lang), "alos": t("col_alos", lang)}
    )
    fig_alos.update_traces(line_color="#9467bd", line_width=3)
    st.plotly_chart(fig_alos, use_container_width=True)

with col4:
    fig_yield = px.line(
        yearly_data, x="year", y="daily_yield",
        markers=True,
        title=t("chart_yield_title", lang),
        labels={"year": t("col_year", lang), "daily_yield": t("col_yield", lang)}
    )
    fig_yield.update_traces(line_color="#e377c2", line_width=3)
    st.plotly_chart(fig_yield, use_container_width=True)

st.divider()

st.markdown(f"### {t('trends_storytelling_title', lang)}")
st.info(t("trends_storytelling_body", lang))

st.divider()
st.subheader("Data Table")
display_data = yearly_data.drop(columns=['occupancy']) if not has_occupancy else yearly_data
st.dataframe(
    display_data.rename(columns={
        "year": t("col_year", lang),
        "arrivals": t("col_arrivals", lang),
        "overnights": t("col_overnights", lang),
        "receipts": t("col_receipts", lang),
        "alos": t("col_alos", lang),
        "daily_yield": t("col_yield", lang)
    }).style.format({
        t("col_arrivals", lang): "{:,.0f}",
        t("col_overnights", lang): "{:,.0f}",
        t("col_receipts", lang): "{:,.0f} €",
        t("col_alos", lang): "{:.2f}",
        t("col_yield", lang): "{:,.2f} €"
    }),
    use_container_width=True,
    hide_index=True
)
