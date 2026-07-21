import streamlit as st
import pandas as pd
from sqlalchemy import text
import sys
import os

# Add the parent directory to sys.path so we can import from database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_engine
from app.components import apply_custom_css, render_sidebar, load_fallback_df, generate_pdf_report

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

total_arrivals = df["arrivals"].sum() if "arrivals" in df.columns else 0
total_overnights = df["overnights"].sum() if "overnights" in df.columns else 0
total_receipts = df["receipts"].sum() if "receipts" in df.columns else 0
avg_spend_per_tourist = total_receipts / total_arrivals if total_arrivals > 0 else 0

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
    st.markdown(f'<div class="metric-card"><div class="metric-label">Συνολικά Έσοδα (€)</div><div class="metric-value">{format_number(total_receipts)}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Δαπάνη / Αφιξη</div><div class="metric-value">{avg_spend_per_tourist:.0f} €</div></div>', unsafe_allow_html=True)

# --- TOP PERFORMING REGIONS HIGHLIGHTS ---
st.markdown("### 🏆 Κορυφαίες Περιφέρειες (Highlights)")

# Compute top region by receipts & arrivals
top_receipts_reg = df.groupby("geo_label")["receipts"].sum().idxmax() if "receipts" in df.columns else "N/A"
top_receipts_val = df.groupby("geo_label")["receipts"].sum().max() if "receipts" in df.columns else 0
top_receipts_pct = (top_receipts_val / total_receipts * 100) if total_receipts > 0 else 0

top_arrivals_reg = df.groupby("geo_label")["arrivals"].sum().idxmax() if "arrivals" in df.columns else "N/A"
top_arrivals_val = df.groupby("geo_label")["arrivals"].sum().max() if "arrivals" in df.columns else 0

h_col1, h_col2 = st.columns(2)
with h_col1:
    st.success(f"🥇 **Πρωταθλήτρια Περιφέρεια (Έσοδα):** **{top_receipts_reg}** με **{format_number(top_receipts_val)} €** (καλύπτει το **{top_receipts_pct:.1f}%** των συνολικών εσόδων της χώρας).")
with h_col2:
    st.info(f"🚀 **Πρώτη Περιφέρεια σε Αφίξεις:** **{top_arrivals_reg}** με **{format_number(top_arrivals_val)}** συνολικούς επισκέπτες.")

# --- EXECUTIVE DATA STORYTELLING & INSIGHTS ---
st.markdown("### 🧠 Σημαντικά Ευρήματα & Αναλυτικά Συμπεράσματα")

st.markdown(
    """
    <div style='background:#ffffff; padding:22px 28px; border-radius:14px; border:1px solid #e2e8f0; box-shadow:0 4px 12px rgba(0,0,0,0.03); margin-bottom:24px;'>
        <div style='margin-bottom:16px; padding-bottom:12px; border-bottom:1px solid #f1f5f9;'>
            <h4 style='color:#005BAE; margin:0 0 6px 0; font-size:1.15rem;'>📉 1. Ανάκαμψη COVID-19 (V-Shape Recovery)</h4>
            <p style='color:#475569; font-size:0.95rem; margin:0; line-height:1.5;'>
                Τα έσοδα υπέστησαν κάθετη πτώση (-70%) το 2020 λόγω πανδημίας (5.07B €), αλλά η αγορά επέδειξε ταχύτατη ανάκαμψη φτάνοντας σε <strong>ιστορικά ρεκόρ όλων των εποχών το 2023-2024 (25.34B €)</strong>.
            </p>
        </div>
        <div style='margin-bottom:16px; padding-bottom:12px; border-bottom:1px solid #f1f5f9;'>
            <h4 style='color:#2ca02c; margin:0 0 6px 0; font-size:1.15rem;'>⚖️ 2. Υψηλή Γεωγραφική Συγκέντρωση</h4>
            <p style='color:#475569; font-size:0.95rem; margin:0; line-height:1.5;'>
                Μόλις <strong>3 από τις 13 Περιφέρειες</strong> (<em>Νότιο Αιγαίο, Αττική, Κρήτη</em>) συγκεντρώνουν πάνω από το <strong>70% του συνολικού τουριστικού πλούτου</strong> της χώρας, αναδεικνύοντας επιτακτική ανάγκη περιφερειακής διασποράς.
            </p>
        </div>
        <div>
            <h4 style='color:#ff7f0e; margin:0 0 6px 0; font-size:1.15rem;'>💶 3. Ποιοτική Δαπάνη ανά Επισκέπτη</h4>
            <p style='color:#475569; font-size:0.95rem; margin:0; line-height:1.5;'>
                Η μέση δαπάνη ανά τουρίστη ανέρχεται στα <strong>~680 €</strong>. Περιφέρειες όπως το <em>Νότιο Αιγαίο</em> προσελκύουν τουρίστες υψηλής δαπάνης (~1.100 €/αφιξη), ενώ η <em>Στερεά Ελλάδα</em> καταγράφει χαμηλότερη δαπάνη (~300 €).
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

st.info("👈 Χρησιμοποιήστε το μενού στα αριστερά για να περιηγηθείτε στις αναλυτικές σελίδες **Τάσεων (Trends)** και **Περιοχών (Regions)**.")

st.subheader("Εξερεύνηση Δεδομένων")

# CSV Export Helper
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')

# Add layout for filters and exports
filter_col1, filter_col2, export_csv_col, export_pdf_col = st.columns([2, 2, 1, 1])

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

with export_csv_col:
    st.markdown("<br>", unsafe_allow_html=True)
    csv = convert_df(filtered_df)
    st.download_button(
        label="📥 CSV",
        data=csv,
        file_name='tourism_data.csv',
        mime='text/csv',
    )

with export_pdf_col:
    st.markdown("<br>", unsafe_allow_html=True)
    try:
        pdf_data = generate_pdf_report(filtered_df)
        st.download_button(
            label="📄 PDF Summary",
            data=pdf_data,
            file_name='tourism_summary_report.pdf',
            mime='application/pdf',
        )
    except Exception as e:
        print(f"PDF export error: {e}")

# Display the dataframe with clean business columns
drop_cols = ["id", "geo", "is_el_regional_unit", "country_code", "country_name", "nuts_level"]
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
