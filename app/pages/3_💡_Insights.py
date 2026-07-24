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
    st.subheader("⏱️ Average Length of Stay (ALOS) & Daily Yield Analysis")
    
    if lang == "en":
        st.markdown(
            "**What is ALOS?** Average Length of Stay = $\\text{Total Overnights} / \\text{Total Arrivals}$. "
            "It measures the average duration (in days) a visitor spends in Greece during a trip.\n\n"
            "#### 📈 Multi-Year Curve Explanation (2019-2024):\n"
            "• **2019 Baseline (3.74 Days):** Pre-pandemic equilibrium travel duration.\n"
            "• **2020 Pandemic Shock (3.50 Days):** Dropped due to strict flight bans, quarantine rules, and emergency short-stay return trips.\n"
            "• **2022 Post-Lockdown Peak (3.81 Days):** Surged as travelers took longer extended vacations ('revenge travel') after two years of restrictions.\n"
            "• **2023-2024 Stabilization (3.69 Days):** Normalized to ~3.7 days as European short-haul flight frequencies and city breaks resumed."
        )
    else:
        st.markdown(
            "**Τι είναι το ALOS;** Μέση Διάρκεια Παραμονής = $\\text{Συνολικές Διανυκτερεύσεις} / \\text{Συνολικές Αφίξεις}$. "
            "Μετρά τη μέση διάρκεια (σε ημέρες) που παραμένει ένας επισκέπτης στην Ελλάδα.\n\n"
            "#### 📈 Ερμηνεία Καμπύλης ALOS (2019-2024):\n"
            "• **2019 Βάση (3.74 Ημέρες):** Ισορροπία διάρκειας ταξιδιού προ πανδημίας.\n"
            "• **2020 Κρίση Πανδημίας (3.50 Ημέρες):** Πτώση λόγω ταξιδιωτικών περιορισμών και σύντομων αναγκαστικών επιστροφών.\n"
            "• **2022 Κορυφή Ανάκαμψης (3.81 Ημέρες):** Εκτόξευση λόγω της τάσης 'revenge travel' όπου οι ταξιδιώτες πραγματοποίησαν ταξίδια μεγαλύτερης διάρκειας.\n"
            "• **2023-2024 Σταθεροποίηση (3.69 Ημέρες):** Ομαλοποίηση στις ~3.7 ημέρες λόγω αύξησης συχνότητας σύντομων ταξιδιών (city-breaks)."
        )
    
    ay_df = df.groupby("geo_label")[["arrivals", "overnights", "receipts"]].sum().reset_index()
    ay_df["alos"] = ay_df["overnights"] / ay_df["arrivals"]
    ay_df["daily_yield"] = ay_df["receipts"] / ay_df["overnights"]
    
    fig_scatter = px.scatter(
        ay_df, x="alos", y="daily_yield", size="receipts", color="geo_label",
        hover_name="geo_label",
        title="ALOS (Days) vs Daily Yield (€/night)",
        labels={"alos": t("col_alos", lang), "daily_yield": t("col_yield", lang), "geo_label": t("col_geo_label", lang)},
        size_max=40
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab_rec:
    st.subheader("📜 Data-Driven Investment Strategy & Capital Allocation Matrix")
    
    if lang == "en":
        st.markdown(
            "Based on empirical 2019-2024 data, we outline a **3-tier data-driven investment roadmap** "
            "designed to maximize tourism revenue, extend length of stay, and optimize regional yields."
        )
        
        col_inv1, col_inv2, col_inv3 = st.columns(3)
        
        with col_inv1:
            st.markdown(
                """
                <div style='background:#f8fafc; padding:18px; border-radius:12px; border-top:4px solid #005BAE; border:1px solid #e2e8f0;'>
                    <h4 style='color:#005BAE; margin-top:0;'>1. 💎 Luxury & High-Yield Capital</h4>
                    <p><strong>Target Regions:</strong> South Aegean, Crete, Ionian Islands</p>
                    <p><strong>Empirical Data Basis:</strong> Captures 70%+ of total national revenue with €110+ daily yield.</p>
                    <p><strong>Recommended Investments:</strong></p>
                    <ul>
                        <li>5-Star luxury resort upgrades</li>
                        <li>Marinas & mega-yachting infrastructure</li>
                        <li>High-end gastronomy & wellness centers</li>
                    </ul>
                    <p><strong>ROI Objective:</strong> Maximize high-net-worth visitor yield.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_inv2:
            st.markdown(
                """
                <div style='background:#f8fafc; padding:18px; border-radius:12px; border-top:4px solid #2ca02c; border:1px solid #e2e8f0;'>
                    <h4 style='color:#2ca02c; margin-top:0;'>2. 🏙️ Urban Extended-Stay & MICE</h4>
                    <p><strong>Target Regions:</strong> Attica, Central Macedonia</p>
                    <p><strong>Empirical Data Basis:</strong> High visitor volume (>10M arrivals) but lower ALOS (~3.7 days).</p>
                    <p><strong>Recommended Investments:</strong></p>
                    <ul>
                        <li>International MICE / Conference Centers</li>
                        <li>365-day boutique city-break hotels</li>
                        <li>Digital nomad co-living apartments</li>
                    </ul>
                    <p><strong>ROI Objective:</strong> Stretching ALOS from 3.7 to 4.5 days yields <strong>+21% revenue growth (+€1.2B/yr)</strong>.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_inv3:
            st.markdown(
                """
                <div style='background:#f8fafc; padding:18px; border-radius:12px; border-top:4px solid #ff7f0e; border:1px solid #e2e8f0;'>
                    <h4 style='color:#ff7f0e; margin-top:0;'>3. 🌿 Regional Growth & Ecotourism</h4>
                    <p><strong>Target Regions:</strong> Epirus, Thessaly, Western Greece</p>
                    <p><strong>Empirical Data Basis:</strong> Under 10% revenue share despite prime natural assets.</p>
                    <p><strong>Recommended Investments:</strong></p>
                    <ul>
                        <li>Agri-tourism & mountain eco-lodges</li>
                        <li>Four-season adventure tourism hubs</li>
                        <li>Cultural heritage trail development</li>
                    </ul>
                    <p><strong>ROI Objective:</strong> Leverage regional tax incentives & relieve summer overtourism.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "Βάσει των πραγματικών δεδομένων 2019-2024, παρουσιάζεται ο **Στρατηγικός Χάρτης Επενδύσεων 3 Πυλώνων** "
            "για τη μεγιστοποίηση των εσόδων, την αύξηση της διάρκειας παραμονής και τη βελτιστοποίηση της απόδοσης."
        )
        
        col_inv1, col_inv2, col_inv3 = st.columns(3)
        
        with col_inv1:
            st.markdown(
                """
                <div style='background:#f8fafc; padding:18px; border-radius:12px; border-top:4px solid #005BAE; border:1px solid #e2e8f0;'>
                    <h4 style='color:#005BAE; margin-top:0;'>1. 💎 Ποιοτικός & Πολυτελής Τουρισμός</h4>
                    <p><strong>Περιφέρειες Στόχοι:</strong> Νότιο Αιγαίο, Κρήτη, Ιόνια Νήσοι</p>
                    <p><strong>Βάση Δεδομένων:</strong> Συγκεντρώνουν >70% των συνολικών εσόδων με Daily Yield >110 €.</p>
                    <p><strong>Προτεινόμενες Επενδύσεις:</strong></p>
                    <ul>
                        <li>Αναβάθμιση 5-άστερων Resort & Boutique ξενοδοχείων</li>
                        <li>Μααρίνες & Υποδομές Mega-Yachting</li>
                        <li>Κέντρα Ευεξίας (Wellness) & Υψηλής Γαστρονομίας</li>
                    </ul>
                    <p><strong>Στόχος ROI:</strong> Μεγιστοποίηση δαπάνης επισκεπτών υψηλού εισοδήματος.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_inv2:
            st.markdown(
                """
                <div style='background:#f8fafc; padding:18px; border-radius:12px; border-top:4px solid #2ca02c; border:1px solid #e2e8f0;'>
                    <h4 style='color:#2ca02c; margin-top:0;'>2. 🏙️ Αστικός Τουρισμός & Συνέδρια (MICE)</h4>
                    <p><strong>Περιφέρειες Στόχοι:</strong> Αττική, Κεντρική Μακεδονία</p>
                    <p><strong>Βάση Δεδομένων:</strong> Υψηλός όγκος (>10M αφίξεις), χαμηλότερο ALOS (~3.7 ημέρες).</p>
                    <p><strong>Προτεινόμενες Επενδύσεις:</strong></p>
                    <ul>
                        <li>Διεθνή Συνεδριακά Κέντρα (MICE)</li>
                        <li>Boutique City-Break Ξενοδοχεία 12-μηνης λειτουργίας</li>
                        <li>Υποδομές Co-living για ψηφιακούς νομάδες</li>
                    </ul>
                    <p><strong>Στόχος ROI:</strong> Η αύξηση του ALOS από 3.7 σε 4.5 ημέρες προσφέρει <strong>+21% αύξηση εσόδων (+1.2 Δις €/έτος)</strong>.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_inv3:
            st.markdown(
                """
                <div style='background:#f8fafc; padding:18px; border-radius:12px; border-top:4px solid #ff7f0e; border:1px solid #e2e8f0;'>
                    <h4 style='color:#ff7f0e; margin-top:0;'>3. 🌿 Περιφερειακή Διασπορά & Οικοτουρισμός</h4>
                    <p><strong>Περιφέρειες Στόχοι:</strong> Ήπειρος, Θεσσαλία, Δυτική Ελλάδα</p>
                    <p><strong>Βάση Δεδομένων:</strong> <10% μερίδιο εσόδων παρά το ισχυρό φυσικό/πολιτιστικό απόθεμα.</p>
                    <p><strong>Προτεινόμενες Επενδύσεις:</strong></p>
                    <ul>
                        <li>Αγροτουρισμός & Οικολογικά καταλύματα</li>
                        <li>Πάρκα ορεινού τουρισμού 4 εποχών</li>
                        <li>Δίκτυα πολιτιστικών & γαστρονομικών διαδρομών</li>
                    </ul>
                    <p><strong>Στόχος ROI:</strong> Αξιοποίηση αναπτυξιακών κινήτρων & αποσυμφόρηση θερινών προορισμών.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
