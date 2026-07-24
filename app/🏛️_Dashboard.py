import streamlit as st
import pandas as pd
from sqlalchemy import text
import sys
import os

# Add the parent directory to sys.path so we can import from database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_engine
from app.components import apply_custom_css, render_sidebar, load_fallback_df, generate_pdf_report
from app.translations import t

st.set_page_config(
    page_title="Greek Tourism Dashboard",
    page_icon="🇬🇷",
    layout="wide"
)

# Apply Premium CSS
apply_custom_css()

# Render Sidebar with Language Toggle
render_sidebar()
lang = st.session_state.get("lang", "el")

st.title(t("dash_title", lang))
st.markdown(t("dash_subtitle", lang))

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

with st.spinner("Loading / Φόρτωση..."):
    df = load_data()

if df.empty:
    st.warning("No data found. Please run ETL pipeline (`python main.py --load-data`).")
    st.stop()

# Filter df by NUTS length (Lock to NUTS 2 due to API bugs in NUTS 1/3)
df = df[df['geo'].str.len() == 4]

# Overall KPIs
st.subheader(t("kpi_section_title", lang))

total_arrivals = df["arrivals"].sum() if "arrivals" in df.columns else 0
total_overnights = df["overnights"].sum() if "overnights" in df.columns else 0
total_receipts = df["receipts"].sum() if "receipts" in df.columns else 0
avg_spend_per_tourist = total_receipts / total_arrivals if total_arrivals > 0 else 0
alos = total_overnights / total_arrivals if total_arrivals > 0 else 0
daily_yield = total_receipts / total_overnights if total_overnights > 0 else 0

def format_number(num):
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{num:.0f}"

# 2 Rows of 3 Columns for optimal width and high visual contrast
row1_col1, row1_col2, row1_col3 = st.columns(3)
with row1_col1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">{t("kpi_arrivals", lang)}</div><div class="metric-value">{format_number(total_arrivals)}</div></div>', unsafe_allow_html=True)
with row1_col2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">{t("kpi_overnights", lang)}</div><div class="metric-value">{format_number(total_overnights)}</div></div>', unsafe_allow_html=True)
with row1_col3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">{t("kpi_receipts", lang)}</div><div class="metric-value">{format_number(total_receipts)} €</div></div>', unsafe_allow_html=True)

row2_col1, row2_col2, row2_col3 = st.columns(3)
with row2_col1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">{t("kpi_spend", lang)}</div><div class="metric-value">{avg_spend_per_tourist:.0f} €</div></div>', unsafe_allow_html=True)
with row2_col2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">{t("kpi_alos", lang)}</div><div class="metric-value">{alos:.2f} {t("unit_days", lang)}</div></div>', unsafe_allow_html=True)
with row2_col3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">{t("kpi_yield", lang)}</div><div class="metric-value">{daily_yield:.1f} {t("unit_night", lang)}</div></div>', unsafe_allow_html=True)

# --- TOP PERFORMING REGIONS HIGHLIGHTS ---
st.markdown(f"### {t('highlights_title', lang)}")

top_receipts_reg = df.groupby("geo_label")["receipts"].sum().idxmax() if "receipts" in df.columns else "N/A"
top_receipts_val = df.groupby("geo_label")["receipts"].sum().max() if "receipts" in df.columns else 0
top_receipts_pct = (top_receipts_val / total_receipts * 100) if total_receipts > 0 else 0

top_arrivals_reg = df.groupby("geo_label")["arrivals"].sum().idxmax() if "arrivals" in df.columns else "N/A"
top_arrivals_val = df.groupby("geo_label")["arrivals"].sum().max() if "arrivals" in df.columns else 0

h_col1, h_col2 = st.columns(2)
with h_col1:
    st.success(t("top_revenue_region", lang, region=top_receipts_reg, value=format_number(top_receipts_val), pct=top_receipts_pct))
with h_col2:
    st.info(t("top_arrivals_region", lang, region=top_arrivals_reg, value=format_number(top_arrivals_val)))

# --- DYNAMIC ANALYTICS CALCULATIONS ---
yearly_rec = df.groupby("year")["receipts"].sum()
min_year_val = yearly_rec.min() if not yearly_rec.empty else 0
max_year_val = yearly_rec.max() if not yearly_rec.empty else 0
rec_multiplier = (max_year_val / min_year_val) if min_year_val > 0 else 1.0

reg_rec = df.groupby("geo_label")["receipts"].sum().sort_values(ascending=False)
total_reg_count = len(reg_rec)
top3_regions_list = reg_rec.head(3).index.tolist()
top3_regions_str = ", ".join(top3_regions_list)
top3_sum = reg_rec.head(3).sum()
total_rec_sum = reg_rec.sum()
top3_pct_val = (top3_sum / total_rec_sum * 100) if total_rec_sum > 0 else 0
rest_pct_val = 100.0 - top3_pct_val

reg_spend = df.groupby("geo_label").apply(lambda g: g["receipts"].sum() / g["arrivals"].sum() if g["arrivals"].sum() > 0 else 0).sort_values(ascending=False)
max_spend_reg_name = reg_spend.index[0] if not reg_spend.empty else "N/A"
max_spend_reg_val = reg_spend.iloc[0] if not reg_spend.empty else 0
min_spend_reg_name = reg_spend.index[-1] if not reg_spend.empty else "N/A"
min_spend_reg_val = reg_spend.iloc[-1] if not reg_spend.empty else 1.0
disp_ratio = (max_spend_reg_val / min_spend_reg_val) if min_spend_reg_val > 0 else 1.0

# --- EXECUTIVE DATA STORYTELLING & INSIGHTS ---
st.markdown(f"### {t('insights_summary_title', lang)}")

ins1_body = t("insight_1_body", lang, min_val=format_number(min_year_val), max_val=format_number(max_year_val), multiplier=rec_multiplier)
ins2_body = t("insight_2_body", lang, total_regions=total_reg_count, top_regions_str=top3_regions_str, top3_pct=top3_pct_val, top3_val=format_number(top3_sum), rest_pct=rest_pct_val)
ins3_body = t("insight_3_body", lang, avg_spend=avg_spend_per_tourist, max_spend_region=max_spend_reg_name, max_spend_val=max_spend_reg_val, disparity_ratio=disp_ratio, min_spend_region=min_spend_reg_name, min_spend_val=min_spend_reg_val)

st.markdown(
    f"""
    <div style='background:#ffffff; padding:22px 28px; border-radius:14px; border:1px solid #e2e8f0; box-shadow:0 4px 12px rgba(0,0,0,0.03); margin-bottom:24px;'>
        <div style='margin-bottom:16px; padding-bottom:12px; border-bottom:1px solid #f1f5f9;'>
            <h4 style='color:#005BAE; margin:0 0 6px 0; font-size:1.15rem;'>{t('insight_1_title', lang)}</h4>
            <p style='color:#475569; font-size:0.95rem; margin:0; line-height:1.5;'>
                {ins1_body}
            </p>
        </div>
        <div style='margin-bottom:16px; padding-bottom:12px; border-bottom:1px solid #f1f5f9;'>
            <h4 style='color:#2ca02c; margin:0 0 6px 0; font-size:1.15rem;'>{t('insight_2_title', lang)}</h4>
            <p style='color:#475569; font-size:0.95rem; margin:0; line-height:1.5;'>
                {ins2_body}
            </p>
        </div>
        <div>
            <h4 style='color:#ff7f0e; margin:0 0 6px 0; font-size:1.15rem;'>{t('insight_3_title', lang)}</h4>
            <p style='color:#475569; font-size:0.95rem; margin:0; line-height:1.5;'>
                {ins3_body}
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

st.subheader(t("data_explore_title", lang))

# CSV Export Helper
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')

# Add layout for filters and exports
filter_col1, filter_col2, export_csv_col, export_pdf_col = st.columns([2, 2, 1, 1])

with filter_col1:
    regions = [t("all_regions", lang)] + sorted(df['geo_label'].unique().tolist())
    selected_region = st.selectbox(t("select_region", lang), regions)

with filter_col2:
    years = [t("all_years", lang)] + sorted(df['year'].unique().tolist())
    selected_year = st.selectbox(t("select_year", lang), years)

# Filter the dataframe
filtered_df = df.copy()
if selected_region != t("all_regions", lang):
    filtered_df = filtered_df[filtered_df['geo_label'] == selected_region]
if selected_year != t("all_years", lang):
    filtered_df = filtered_df[filtered_df['year'] == selected_year]

with export_csv_col:
    st.markdown("<br>", unsafe_allow_html=True)
    csv = convert_df(filtered_df)
    st.download_button(
        label=t("download_csv", lang),
        data=csv,
        file_name='tourism_data.csv',
        mime='text/csv',
    )

with export_pdf_col:
    st.markdown("<br>", unsafe_allow_html=True)
    try:
        pdf_data = generate_pdf_report(filtered_df, lang=lang)
        st.download_button(
            label=t("download_pdf", lang),
            data=pdf_data,
            file_name='tourism_summary_report.pdf',
            mime='application/pdf',
        )
    except Exception as e:
        print(f"PDF export error: {e}")

# Display the dataframe with clean business columns
display_df = filtered_df.copy()
display_df['alos'] = display_df['overnights'] / display_df['arrivals']
display_df['daily_yield'] = display_df['receipts'] / display_df['overnights']

drop_cols = ["id", "geo", "is_el_regional_unit", "country_code", "country_name", "nuts_level"]
if "occupancy" in display_df.columns and display_df["occupancy"].sum() == 0:
    drop_cols.append("occupancy")

st.dataframe(
    display_df.drop(columns=drop_cols, errors="ignore").rename(columns={
        "geo_label": t("col_geo_label", lang),
        "year": t("col_year", lang),
        "arrivals": t("col_arrivals", lang),
        "overnights": t("col_overnights", lang),
        "receipts": t("col_receipts", lang),
        "turnover": t("col_turnover", lang),
        "alos": t("col_alos", lang),
        "daily_yield": t("col_yield", lang)
    }).style.format({
        t("col_arrivals", lang): "{:,.0f}",
        t("col_overnights", lang): "{:,.0f}",
        t("col_receipts", lang): "{:,.0f} €",
        t("col_turnover", lang): "{:,.0f} €",
        t("col_alos", lang): "{:.2f}",
        t("col_yield", lang): "{:,.2f} €"
    }),
    use_container_width=True,
    hide_index=True,
    height=400
)

st.caption(t("showing_records", lang, count=len(filtered_df)))
