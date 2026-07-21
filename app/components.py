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
            
            /* Metric Card Styling with Hover Effects */
            .metric-card {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                padding: 24px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                border: 1px solid #eef2f5;
                text-align: center;
                transition: all 0.3s ease;
                margin-bottom: 20px;
            }
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 15px rgba(0, 91, 174, 0.15);
                border-color: #005BAE;
            }
            .metric-value {
                font-size: 2.5rem;
                font-weight: 800;
                color: #005BAE;
                margin-top: 10px;
            }
            .metric-label {
                font-size: 1.1rem;
                font-weight: 600;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            /* Make dataframe headers look premium */
            thead tr th {
                background-color: #005BAE !important;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Renders the common premium sidebar with info."""
    st.sidebar.markdown("### ℹ️ Πληροφορίες")
    st.sidebar.info(
        "🇬🇷 **Greek Tourism Dashboard**\n\n"
        "Η εφαρμογή παρουσιάζει επίσημα στοιχεία τουρισμού (Αφίξεις, Διανυκτερεύσεις, Έσοδα) "
        "για την Ελλάδα την περίοδο 2019-2024.\n\n"
        "**Δεδομένα:** Skillscapes API"
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
