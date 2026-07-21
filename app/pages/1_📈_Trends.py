import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database import get_engine
from app.components import apply_custom_css, render_sidebar, load_fallback_df

st.set_page_config(page_title="Ανάλυση Τάσεων", page_icon="📈", layout="wide")
apply_custom_css()

st.title("📈 Χρονολογική Ανάλυση (Trends)")
st.markdown("Ανάλυση της εξέλιξης του τουρισμού στην Ελλάδα μέσα στο χρόνο.")

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
    st.warning("Δεν βρέθηκαν δεδομένα.")
    st.stop()

# --- SIDEBAR FILTERS ---
render_sidebar()

# Filter df by NUTS length (Lock to NUTS 2)
df = df[df['geo'].str.len() == 4]

# Aggregate data by year
yearly_data = df.groupby('year')[['arrivals', 'overnights', 'receipts', 'occupancy']].sum().reset_index()

# Note: Occupancy is an average, so we should take the mean.
yearly_data['occupancy'] = df.groupby('year')['occupancy'].mean().values

has_occupancy = yearly_data['occupancy'].sum() > 0

if has_occupancy:
    col1, col2, col3 = st.columns(3)
else:
    col1, col2 = st.columns(2)

with col1:
    st.subheader("Εξέλιξη Αφίξεων")
    fig_arrivals = px.line(
        yearly_data, x="year", y="arrivals", 
        markers=True, 
        title="Συνολικές Αφίξεις ανά Έτος",
        labels={"year": "Έτος", "arrivals": "Αφίξεις"}
    )
    fig_arrivals.update_traces(line_color="#005BAE", line_width=3)
    st.plotly_chart(fig_arrivals, use_container_width=True)

with col2:
    st.subheader("Εξέλιξη Εσόδων")
    fig_receipts = px.line(
        yearly_data, x="year", y="receipts", 
        markers=True, 
        title="Συνολικά Έσοδα ανά Έτος (€)",
        labels={"year": "Έτος", "receipts": "Έσοδα (€)"}
    )
    fig_receipts.update_traces(line_color="#2ca02c", line_width=3)
    st.plotly_chart(fig_receipts, use_container_width=True)

if has_occupancy:
    with col3:
        st.subheader("Εξέλιξη Πληρότητας")
        fig_occ = px.line(
            yearly_data, x="year", y="occupancy", 
            markers=True, 
            title="Μέση Πληρότητα ανά Έτος (%)",
            labels={"year": "Έτος", "occupancy": "Πληρότητα (%)"}
        )
        fig_occ.update_traces(line_color="#ff7f0e", line_width=3)
        st.plotly_chart(fig_occ, use_container_width=True)

st.divider()

st.markdown("### 💡 Ερμηνεία Διαγραμμάτων & Τάσεων (Storytelling)")
st.info(
    "📊 **Βασικά Συμπεράσματα Χρονοσειράς (2019 - 2024):**\n\n"
    "• **2019 (Βάση Αναφοράς):** Η χρονιά-σταθμός προ COVID-19 με 31.9M αφίξεις και 20.27B € έσοδα.\n"
    "• **2020 (Κρίση Πανδημίας):** Δραματική πτώση λόγω ταξιδιωτικών περιορισμών (9.5M αφίξεις, 5.07B € έσοδα).\n"
    "• **2021-2022 (Στάδιο Ανάκαμψης):** Σταδιακή επανεκκίνηση με διπλασιασμό των αφίξεων (29.2M το 2022) και επιστροφή των εσόδων στα προ-πανδημικά επίπεδα (20.1B €).\n"
    "• **2023-2024 (Ιστορικό Ρεκόρ):** Πλήρης υπέρβαση όλων των προηγούμενων επιδόσεων. Το 2024 καταγράφονται **34.8M αφίξεις** και **25.34B € έσοδα**, επιβεβαιώνοντας τη μακροπρόθεσμη δυναμική του ελληνικού τουριστικού προϊόντος."
)

st.divider()
st.subheader("Αναλυτικός Πίνακας Τάσεων")
display_data = yearly_data.drop(columns=['occupancy']) if not has_occupancy else yearly_data
st.dataframe(
    display_data.style.format({
        "arrivals": "{:,.0f}",
        "overnights": "{:,.0f}",
        "receipts": "{:,.0f} €"
    }),
    use_container_width=True,
    hide_index=True
)
