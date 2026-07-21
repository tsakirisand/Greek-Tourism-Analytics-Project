import streamlit as st
import pandas as pd
from sqlalchemy import text
import sys
import os

# Add the parent directory to sys.path so we can import from database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_engine
from app.components import apply_custom_css, render_sidebar, load_fallback_df

st.set_page_config(
    page_title="Greek Tourism Dashboard",
    page_icon="🇬🇷",
    layout="wide"
)

# Apply Premium CSS
apply_custom_css()

st.title("🇬🇷 Ελληνικός Τουρισμός - Κεντρική Σελίδα")
st.markdown("Καλώς ήρθατε στο κεντρικό ταμπλό δεδομένων για τον Τουρισμό στην Ελλάδα (2019-2024).")

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

with st.spinner("Φόρτωση δεδομένων..."):
    df = load_data()

if df.empty:
    st.warning("Δεν βρέθηκαν δεδομένα. Παρακαλώ τρέξτε το ETL pipeline (`python main.py --load-data`).")
    st.stop()

# --- SIDEBAR FILTERS ---
render_sidebar()

# Filter df by NUTS length (Lock to NUTS 2 due to API bugs in NUTS 1/3)
df = df[df['geo'].str.len() == 4]

# Overall KPIs
st.subheader(f"Συνολικά Στατιστικά - Περιφέρειες (NUTS 2)")

total_arrivals = df["arrivals"].sum()
total_overnights = df["overnights"].sum()
avg_occupancy = df["occupancy"].mean()
total_receipts = df["receipts"].sum()

def format_number(num):
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{num:.0f}"

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Συνολικές Αφίξεις</div><div class="metric-value">{format_number(total_arrivals)}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Διανυκτερεύσεις</div><div class="metric-value">{format_number(total_overnights)}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Μέση Πληρότητα</div><div class="metric-value">{avg_occupancy:.1f}%</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Συνολικά Έσοδα (€)</div><div class="metric-value">{format_number(total_receipts)}</div></div>', unsafe_allow_html=True)

st.divider()

st.info("👈 Χρησιμοποιήστε το μενού στα αριστερά για να περιηγηθείτε στις αναλυτικές σελίδες **Τάσεων (Trends)** και **Περιοχών (Regions)**.")

st.subheader("Εξερεύνηση Δεδομένων")

# CSV Export Helper
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')

# Add some layout for filters
filter_col1, filter_col2, export_col = st.columns([2, 2, 1])

with filter_col1:
    regions = ["Όλες οι Περιοχές"] + sorted(df['geo_label'].unique().tolist())
    selected_region = st.selectbox("Επιλογή Περιοχής:", regions)

with filter_col2:
    years = ["Όλα τα Έτη"] + sorted(df['year'].unique().tolist())
    selected_year = st.selectbox("Επιλογή Έτους:", years)

# Filter the dataframe
filtered_df = df.copy()
if selected_region != "Όλες οι Περιοχές":
    filtered_df = filtered_df[filtered_df['geo_label'] == selected_region]
if selected_year != "Όλα τα Έτη":
    filtered_df = filtered_df[filtered_df['year'] == selected_year]

with export_col:
    st.markdown("<br>", unsafe_allow_html=True) # visual alignment
    csv = convert_df(filtered_df)
    st.download_button(
        label="📥 Λήψη (CSV)",
        data=csv,
        file_name='tourism_data.csv',
        mime='text/csv',
    )

# Display the dataframe with nice formatting
drop_cols = ["id", "geo"]
if "occupancy" in filtered_df.columns and filtered_df["occupancy"].sum() == 0:
    drop_cols.append("occupancy")

st.dataframe(
    filtered_df.drop(columns=drop_cols, errors="ignore").style.format({
        "arrivals": "{:,.0f}",
        "overnights": "{:,.0f}",
        "receipts": "{:,.0f} €",
        "turnover": "{:,.0f} €"
    }),
    use_container_width=True,
    hide_index=True,
    height=400
)

st.caption(f"Εμφάνιση {len(filtered_df)} εγγραφών με βάση τα φίλτρα σας.")
