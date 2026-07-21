import streamlit as st

def apply_custom_css():
    """Injects premium custom CSS with fonts and micro-animations."""
    st.markdown("""
        <style>
            /* Import modern font */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
            
            html, body, [class*="css"]  {
                font-family: 'Inter', sans-serif;
            }
            
            /* Metric Card Styling with Hover Effects & Equal Heights */
            .metric-card {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                padding: 20px 12px;
                border-radius: 14px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.04);
                border: 1px solid #eef2f5;
                text-align: center;
                transition: all 0.3s ease;
                height: 135px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            .metric-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 10px 20px rgba(0, 91, 174, 0.12);
                border-color: #005BAE;
            }
            .metric-value {
                font-size: 2.1rem;
                font-weight: 800;
                color: #005BAE;
                margin-top: 6px;
                line-height: 1.1;
            }
            .metric-label {
                font-size: 0.85rem;
                font-weight: 700;
                color: #475569;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                white-space: nowrap;
            }
            
            /* Make dataframe headers look premium */
            thead tr th {
                background-color: #005BAE !important;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Renders the common premium sidebar with info and health status."""
    st.sidebar.markdown("### ℹ️ Πληροφορίες")
    st.sidebar.info(
        "🇬🇷 **Greek Tourism Analytics & Intelligence**\n\n"
        "Ολοκληρωμένο σύστημα ανάλυσης & Data Storytelling για τον ελληνικό τουρισμό (2019-2024).\n\n"
        "**🌐 Πηγές Δεδομένων (Multi-Source):**\n"
        "• Skillscapes API (Πρωτογενή στοιχεία)\n"
        "• Eurostat Open Data (GeoJSON & NUTS 2)\n"
        "• Τράπεζα της Ελλάδος (Μακροοικονομικά)"
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<div style='background:#f0f9ff; padding:12px; border-radius:8px; border:1px solid #bae6fd; font-size:0.85rem; color:#0369a1;'>"
        "<strong>🟢 System Status:</strong> Active<br>"
        "<strong>⚡ Pipeline:</strong> Multi-Source Ingestion<br>"
        "<strong>📊 Scope:</strong> NUTS 2 (13 Περιφέρειες)"
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

def generate_pdf_report(df):
    """Generates an executive PDF report bytes using FPDF."""
    from fpdf import FPDF
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    
    # Title
    pdf.set_text_color(0, 91, 174)
    pdf.cell(0, 10, "Greek Tourism Executive Summary Report", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Macroeconomic Performance Overview (2019 - 2024)", ln=True, align="C")
    pdf.ln(10)
    
    # Key Totals
    total_arrivals = df["arrivals"].sum() if "arrivals" in df.columns else 0
    total_overnights = df["overnights"].sum() if "overnights" in df.columns else 0
    total_receipts = df["receipts"].sum() if "receipts" in df.columns else 0
    avg_spend = total_receipts / total_arrivals if total_arrivals > 0 else 0
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, "1. Executive Key Performance Indicators (KPIs)", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"- Total Tourist Arrivals: {total_arrivals:,.0f}", ln=True)
    pdf.cell(0, 6, f"- Total Overnights: {total_overnights:,.0f}", ln=True)
    pdf.cell(0, 6, f"- Total Tourism Receipts: EUR {total_receipts:,.0f}", ln=True)
    pdf.cell(0, 6, f"- Average Spend per Tourist: EUR {avg_spend:,.2f}", ln=True)
    pdf.ln(8)
    
    # Top Regions Table
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "2. Top 5 Greek Regions by Tourism Revenue", ln=True)
    
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
    pdf.cell(0, 6, "Generated automatically by Greek Tourism Analytics Platform", ln=True, align="C")
    
    return bytes(pdf.output())
