import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import text
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database import get_engine
from app.components import apply_custom_css, render_sidebar, load_fallback_df
from app.translations import t

st.set_page_config(page_title="Strategic Insights", page_icon="💡", layout="wide")
apply_custom_css()

# Render Sidebar with Language Toggle
render_sidebar()
lang = st.session_state.get("lang", "el")

st.title(t("insights_page_title", lang))
st.markdown(t("insights_page_subtitle", lang))

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
    except Exception:
        pass
        
    return load_fallback_df()

df = load_data()

if df.empty:
    st.warning("No data found.")
    st.stop()

# Filter df by NUTS length (Lock to NUTS 2)
df = df[df['geo'].str.len() == 4]

# Main Insights Tabs
tab_covid, tab_conc, tab_spend, tab_alos_yield, tab_rec = st.tabs([
    t("tab_covid", lang), 
    t("tab_conc", lang), 
    t("tab_spend", lang), 
    t("tab_alos_yield", lang),
    t("tab_rec", lang)
])

with tab_covid:
    st.subheader(t("insight_1_title", lang))
    
    yearly = df.groupby("year")[["arrivals", "receipts"]].sum().reset_index()
    yearly["receipts_billion"] = yearly["receipts"] / 1_000_000_000
    yearly["arrivals_million"] = yearly["arrivals"] / 1_000_000
    
    fig_rec = px.bar(
        yearly, x="year", y="receipts_billion",
        title=t("chart_receipts_title", lang),
        labels={"year": t("col_year", lang), "receipts_billion": "EUR (€ Billions)"},
        color="receipts_billion",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_rec, use_container_width=True)
    st.info(t("insight_1_body", lang))

with tab_conc:
    st.subheader(t("insight_2_title", lang))
    
    reg_summary = df.groupby("geo_label")["receipts"].sum().reset_index().sort_values("receipts", ascending=False)
    reg_summary["share_pct"] = (reg_summary["receipts"] / reg_summary["receipts"].sum()) * 100
    top3_share = reg_summary.head(3)["share_pct"].sum()
    
    fig_pie = px.pie(
        reg_summary, values="receipts", names="geo_label",
        title=t("tab_conc", lang),
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.warning(t("insight_2_body", lang))

with tab_spend:
    st.subheader(t("insight_3_title", lang))
    
    spend_df = df.groupby("geo_label")[["arrivals", "receipts"]].sum().reset_index()
    spend_df["spend_per_tourist"] = spend_df["receipts"] / spend_df["arrivals"]
    spend_df = spend_df.sort_values("spend_per_tourist", ascending=False)
    
    fig_spend = px.bar(
        spend_df, x="spend_per_tourist", y="geo_label", orientation="h",
        title=t("kpi_spend", lang),
        labels={"spend_per_tourist": t("kpi_spend", lang), "geo_label": t("col_geo_label", lang)},
        color="spend_per_tourist",
        color_continuous_scale="Magma"
    )
    fig_spend.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
    st.plotly_chart(fig_spend, use_container_width=True)
    st.success(t("insight_3_body", lang))

with tab_alos_yield:
    st.subheader(t("tab_alos_yield", lang))
    
    ay_df = df.groupby("geo_label")[["arrivals", "overnights", "receipts"]].sum().reset_index()
    ay_df["alos"] = ay_df["overnights"] / ay_df["arrivals"]
    ay_df["daily_yield"] = ay_df["receipts"] / ay_df["overnights"]
    
    fig_scatter = px.scatter(
        ay_df, x="alos", y="daily_yield", size="receipts", color="geo_label",
        hover_name="geo_label",
        title=f"ALOS vs Daily Yield",
        labels={"alos": t("col_alos", lang), "daily_yield": t("col_yield", lang), "geo_label": t("col_geo_label", lang)},
        size_max=40
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab_rec:
    st.subheader(t("tab_rec", lang))
    
    if lang == "en":
        st.markdown("""
        Based on data findings (2019-2024), 3 central strategic pillars are recommended:
        
        1. 🎯 **Regional Diversification:**
           - Incentivize tourism investments in lower-share regions (e.g. Epirus, Thessaly, Western Greece).
        
        2. 💎 **Focus on High-Value Tourism:**
           - Transition from counting total volume of arrivals to maximizing total yield per visitor.
        
        3. 📅 **Seasonality Extension:**
           - Develop thematic tourism (cultural, culinary, conference) for off-peak months.
        """)
    else:
        st.markdown("""
        Βάσει των ευρημάτων της ανάλυσης δεδομένων (2019-2024), προτείνονται 3 κεντρικοί στρατηγικοί πυλώνες:
        
        1. 🎯 **Περιφερειακή Διασπορά (Diversification):**
           - Παροχή κινήτρων για τουριστικές επενδύσεις σε περιφέρειες με χαμηλό μερίδιο (π.χ. Ηπειρος, Θεσσαλία, Δυτική Ελλάδα).
        
        2. 💎 **Ενίσχυση Ποιοτικού Τουρισμού (High-Value Tourism):**
           - Μετάβαση από τη μέτρηση 'αριθμού αφίξεων' στη μέτρηση 'συνολικής δαπάνης ανά επισκέπτη'.
        
        3. 📅 **Επιμήκυνση Τουριστικής Περιόδου (Seasonality Extension):**
           - Ανάπτυξη θεματικών μορφών τουρισμού (πολιτιστικός, γαστρονομικός, συνεδριακός) για τους μήνες εκτός αιχμής.
        """)
