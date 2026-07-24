import streamlit as st
from app.translations import t

def apply_custom_css():
    """Injects premium custom CSS with high-contrast fonts, rich card designs, and micro-animations."""
    st.markdown("""
        <style>
            /* Import modern font */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
            
            html, body, [class*="css"]  {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            
            /* Metric Card Styling with Rich Borders, High Contrast & Elevation */
            .metric-card {
                background: linear-gradient(145deg, #ffffff 0%, #f1f5f9 100%);
                padding: 18px 14px;
                border-radius: 12px;
                box-shadow: 0 4px 14px rgba(0, 91, 174, 0.08);
                border: 1px solid #cbd5e1;
                border-left: 5px solid #005BAE;
                text-align: center;
                transition: all 0.25s ease-in-out;
                min-height: 120px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                margin-bottom: 12px;
            }
            .metric-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 8px 22px rgba(0, 91, 174, 0.18);
                border-color: #005BAE;
                background: #ffffff;
            }
            .metric-value {
                font-size: 2.0rem;
                font-weight: 800;
                color: #005BAE;
                margin-top: 4px;
                line-height: 1.1;
                letter-spacing: -0.5px;
            }
            .metric-label {
                font-size: 0.82rem;
                font-weight: 800;
                color: #1e293b;
                text-transform: uppercase;
                letter-spacing: 0.6px;
                white-space: nowrap;
            }
            
            /* Make dataframe headers look premium */
            thead tr th {
                background-color: #005BAE !important;
                color: white !important;
                font-weight: 700 !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Renders the common premium sidebar with language toggle, info, and health status."""
    st.sidebar.markdown("### 🌐 Language / Γλώσσα")
    
    current_lang = st.session_state.get("lang", "el")
    default_index = 0 if current_lang == "el" else 1
    
    lang_choice = st.sidebar.selectbox(
        "Select Language / Επιλογή Γλώσσας",
        ["🇬🇷 Ελληνικά", "🇬🇧 English"],
        index=default_index,
        key="lang_selectbox"
    )
    
    new_lang = "el" if "Ελληνικά" in lang_choice else "en"
    if st.session_state.get("lang") != new_lang:
        st.session_state["lang"] = new_lang
        st.rerun()
        
    lang = st.session_state.get("lang", "el")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### {t('sidebar_info_title', lang)}")
    st.sidebar.info(t("sidebar_info_body", lang))
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"<div style='background:#f0f9ff; padding:12px; border-radius:8px; border:1px solid #bae6fd; font-size:0.85rem; color:#0369a1;'>"
        f"<strong>{t('sidebar_status_active', lang)}</strong><br>"
        f"<strong>{t('sidebar_pipeline', lang)}</strong><br>"
        f"<strong>{t('sidebar_scope', lang)}</strong>"
        "</div>",
        unsafe_allow_html=True
    )

def load_fallback_df():
    """Loads fallback data from local JSON file if database is unavailable."""
    import os
    import pandas as pd
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw_data.json")
    if not os.path.exists(json_path):
        return pd.DataFrame()
    try:
        df = pd.read_json(json_path)
        rename_map = {
            "hotels_total_arrivals": "arrivals",
            "hotels_total_overnights": "overnights",
            "hotels_occupancy": "occupancy",
            "turnover_total": "turnover"
        }
        df = df.rename(columns=rename_map)
        if 'receipts' in df.columns:
            df['receipts'] = df['receipts'] * 1_000_000
        if 'turnover' in df.columns:
            df['turnover'] = df['turnover'] * 1_000
        return df
    except Exception as e:
        print(f"Fallback load error: {e}")
        return pd.DataFrame()

def generate_pdf_report(df, lang="el"):
    """Generates an executive PDF report bytes using FPDF."""
    from fpdf import FPDF
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    
    title_text = t("pdf_title", lang)
    subtitle_text = t("pdf_subtitle", lang)
    sec1_text = t("pdf_section1", lang)
    sec2_text = t("pdf_section2", lang)
    footer_text = t("pdf_footer", lang)
    
    # Title
    pdf.set_text_color(0, 91, 174)
    pdf.cell(0, 10, title_text, ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, subtitle_text, ln=True, align="C")
    pdf.ln(10)
    
    # Key Totals
    total_arrivals = df["arrivals"].sum() if "arrivals" in df.columns else 0
    total_overnights = df["overnights"].sum() if "overnights" in df.columns else 0
    total_receipts = df["receipts"].sum() if "receipts" in df.columns else 0
    avg_spend = total_receipts / total_arrivals if total_arrivals > 0 else 0
    alos = total_overnights / total_arrivals if total_arrivals > 0 else 0
    daily_yield = total_receipts / total_overnights if total_overnights > 0 else 0
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, sec1_text, ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"- Total Tourist Arrivals: {total_arrivals:,.0f}", ln=True)
    pdf.cell(0, 6, f"- Total Overnights: {total_overnights:,.0f}", ln=True)
    pdf.cell(0, 6, f"- Total Tourism Receipts: EUR {total_receipts:,.0f}", ln=True)
    pdf.cell(0, 6, f"- Average Spend per Tourist: EUR {avg_spend:,.2f}", ln=True)
    pdf.cell(0, 6, f"- Average Length of Stay (ALOS): {alos:.2f} days/visitor", ln=True)
    pdf.cell(0, 6, f"- Daily Yield per Overnight: EUR {daily_yield:,.2f}/night", ln=True)
    pdf.ln(8)
    
    # Top Regions Table
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, sec2_text, ln=True)
    
    if "geo_label" in df.columns and "receipts" in df.columns:
        top_regions = df.groupby("geo_label")["receipts"].sum().reset_index().sort_values("receipts", ascending=False).head(5)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(110, 7, "Region Name", border=1)
        pdf.cell(70, 7, "Total Revenue (EUR)", border=1, ln=True)
        
        pdf.set_font("Helvetica", "", 10)
        for _, row in top_regions.iterrows():
            reg_name = str(row["geo_label"]).encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(110, 7, reg_name, border=1)
            pdf.cell(70, 7, f"EUR {row['receipts']:,.0f}", border=1, ln=True)
            
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 6, footer_text, ln=True, align="C")
    
    return bytes(pdf.output())

def export_clean_csv(df, lang="el"):
    """Transforms raw dataframe into a clean, localized CSV matching the dashboard table."""
    export_df = df.copy()
    
    # Calculate computed indicators if present
    if 'arrivals' in export_df.columns and 'overnights' in export_df.columns:
        export_df['alos'] = export_df['overnights'] / export_df['arrivals']
    if 'receipts' in export_df.columns and 'overnights' in export_df.columns:
        export_df['daily_yield'] = export_df['receipts'] / export_df['overnights']
        
    # Drop technical internal columns
    drop_cols = ["id", "geo", "is_el_regional_unit", "country_code", "country_name", "nuts_level"]
    if "occupancy" in export_df.columns and export_df["occupancy"].sum() == 0:
        drop_cols.append("occupancy")
    export_df = export_df.drop(columns=drop_cols, errors="ignore")
    
    # Rename headers to match localized column names
    rename_map = {
        "geo_label": t("col_geo_label", lang),
        "year": t("col_year", lang),
        "arrivals": t("col_arrivals", lang),
        "overnights": t("col_overnights", lang),
        "receipts": t("col_receipts", lang),
        "turnover": t("col_turnover", lang),
        "alos": t("col_alos", lang),
        "daily_yield": t("col_yield", lang)
    }
    export_df = export_df.rename(columns=rename_map)
    
    # Format decimals for clean Excel readability
    alos_header = t("col_alos", lang)
    yield_header = t("col_yield", lang)
    if alos_header in export_df.columns:
        export_df[alos_header] = export_df[alos_header].round(2)
    if yield_header in export_df.columns:
        export_df[yield_header] = export_df[yield_header].round(2)
        
    return export_df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')
