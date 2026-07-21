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

st.set_page_config(page_title="Data Insights", page_icon="💡", layout="wide")
apply_custom_css()

st.title("💡 Στρατηγική Ανάλυση & Data Insights")
st.markdown("Επιχειρησιακά συμπεράσματα, τάσεις και στρατηγικές προτάσεις βασισμένες στα δεδομένα (Data-Driven Intelligence).")

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
    st.warning("Δεν βρέθηκαν δεδομένα.")
    st.stop()

# --- SIDEBAR ---
render_sidebar()

# Filter df by NUTS length (Lock to NUTS 2)
df = df[df['geo'].str.len() == 4]

# Main Insights Tabs
tab_covid, tab_conc, tab_spend, tab_rec = st.tabs([
    "📉 Ανάκαμψη COVID-19", 
    "⚖️ Γεωγραφική Συγκέντρωση", 
    "💶 Ποιοτική Δαπάνη / Τουρίστη", 
    "📜 Στρατηγικές Προτάσεις"
])

with tab_covid:
    st.subheader("📉 Η Κατάρρευση του COVID-19 & η Ταχύτατη Ανάκαμψη (V-Shape Recovery)")
    st.markdown(
        "Η πανδημία του 2020 προκάλεσε την πιο βίαιη προσαρμογή στην ιστορία του ελληνικού τουρισμού. "
        "Ωστόσο, η αγορά επέδειξε πρωτοφανή ανθεκτικότητα."
    )
    
    yearly = df.groupby("year")[["arrivals", "receipts"]].sum().reset_index()
    yearly["receipts_billion"] = yearly["receipts"] / 1_000_000_000
    yearly["arrivals_million"] = yearly["arrivals"] / 1_000_000
    
    fig_rec = px.bar(
        yearly, x="year", y="receipts_billion",
        title="Εξέλιξη Συνολικών Εσόδων (Δισεκατομμύρια €)",
        labels={"year": "Έτος", "receipts_billion": "Έσοδα (€ Δις)"},
        color="receipts_billion",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_rec, use_container_width=True)
    
    st.info(
        "💡 **Data Takeaway:** Από τα **20.27 Δις €** το 2019, τα έσοδα υποχώρησαν στα **5.07 Δις €** το 2020 (-75%). "
        "Μέχρι το 2024, τα έσοδα εκτοξεύθηκαν στα **25.34 Δις €**, ξεπερνώντας τα προ-πανδημικά επίπεδα κατά **25%**!"
    )

with tab_conc:
    st.subheader("⚖️ Υψηλή Γεωγραφική Συγκέντρωση Τουριστικού Πλούτου")
    st.markdown("Ανάλυση της κατανομής των τουριστικών εσόδων στις 13 Περιφέρειες της Ελλάδας.")
    
    reg_summary = df.groupby("geo_label")["receipts"].sum().reset_index().sort_values("receipts", ascending=False)
    reg_summary["share_pct"] = (reg_summary["receipts"] / reg_summary["receipts"].sum()) * 100
    
    top3_share = reg_summary.head(3)["share_pct"].sum()
    
    fig_pie = px.pie(
        reg_summary, values="receipts", names="geo_label",
        title="Μερίδιο Εσόδων ανά Περιφέρεια (2019-2024)",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.warning(
        f"⚠️ **Data Takeaway:** Μόλις **3 Περιφέρειες** (*Νότιο Αιγαίο*, *Αττική*, *Κρήτη*) "
        f"συγκεντρώνουν το **{top3_share:.1f}%** του συνολικού τουριστικού εισοδήματος της Ελλάδας, "
        "αναδεικνύοντας έντονο πρόβλημα γεωγραφικής ανισότητας."
    )

with tab_spend:
    st.subheader("💶 Ποιοτικός Τουρισμός: Μέση Δαπάνη ανά Επισκέπτη (€)")
    st.markdown("Αξιολόγηση των Περιφερειών με βάση την οικονομική απόδοση κάθε τουρίστα.")
    
    spend_df = df.groupby("geo_label")[["arrivals", "receipts"]].sum().reset_index()
    spend_df["spend_per_tourist"] = spend_df["receipts"] / spend_df["arrivals"]
    spend_df = spend_df.sort_values("spend_per_tourist", ascending=False)
    
    fig_spend = px.bar(
        spend_df, x="spend_per_tourist", y="geo_label", orientation="h",
        title="Μέση Δαπάνη ανά Επισκέπτη ανά Περιφέρεια (€/Αφιξη)",
        labels={"spend_per_tourist": "Δαπάνη (€/τουρίστη)", "geo_label": "Περιφέρεια"},
        color="spend_per_tourist",
        color_continuous_scale="Magma"
    )
    fig_spend.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
    st.plotly_chart(fig_spend, use_container_width=True)
    
    st.success(
        "💡 **Data Takeaway:** Το *Νότιο Αιγαίο* ηγείται στην ποιοτική δαπάνη (~1.100 € ανά τουρίστη), "
        "ενώ η *Στερεά Ελλάδα* και η *Δυτική Ελλάδα* καταγράφουν χαμηλότερη δαπάνη (~300 €), "
        "υποδεικνύοντας ευκαιρίες ανάπτυξης τουρισμού υψηλής προστιθέμενης αξίας."
    )

with tab_rec:
    st.subheader("📜 Στρατηγικές Προτάσεις Πολιτικής (Executive Action Plan)")
    
    st.markdown("""
    Βάσει των ευρημάτων της ανάλυσης δεδομένων (2019-2024), προτείνονται 3 κεντρικοί στρατηγικοί πυλώνες:
    
    1. 🎯 **Περιφερειακή Διασπορά (Diversification):**
       - Παροχή κινήτρων για τουριστικές επενδύσεις σε περιφέρειες με χαμηλό μερίδιο (π.χ. Ηπειρος, Θεσσαλία, Δυτική Ελλάδα).
    
    2. 💎 **Ενίσχυση Ποιοτικού Τουρισμού (High-Value Tourism):**
       - Μετάβαση από τη μέτρηση 'αριθμού αφίξεων' στη μέτρηση 'συνολικής δαπάνης ανά επισκέπτη'.
    
    3. 📅 **Επιμήκυνση Τουριστικής Περιόδου (Seasonality Extension):**
       - Ανάπτυξη θεματικών μορφών τουρισμού (πολιτιστικός, γαστρονομικός, συνεδριακός) για τους μήνες εκτός αιχμής.
    """)
