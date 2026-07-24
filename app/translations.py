"""
Translations dictionary and localization helper for Greek Tourism Analytics.
Supports Greek (el) and English (en).
"""

TRANSLATIONS = {
    "el": {
        # Navigation & Sidebar
        "sidebar_info_title": "ℹ️ Πληροφορίες",
        "sidebar_info_body": (
            "🇬🇷 **Greek Tourism Analytics & Intelligence**\n\n"
            "Ολοκληρωμένο σύστημα ανάλυσης & Data Storytelling για τον ελληνικό τουρισμό (2019-2024).\n\n"
            "**🌐 Πηγές Δεδομένων:**\n"
            "• Skillscapes API (Πρωτογενή στοιχεία)\n"
            "• Eurostat Open Data (GeoJSON & NUTS 2)"
        ),
        "sidebar_status_active": "🟢 System Status: Active",
        "sidebar_pipeline": "⚡ Pipeline: Multi-Source Ingestion",
        "sidebar_scope": "📊 Scope: NUTS 2 (13 Περιφέρειες)",
        "language_selector": "🌐 Γλώσσα / Language",

        # Main Dashboard Page
        "dash_title": "🇬🇷 Ελληνικός Τουρισμός - Κεντρική Σελίδα",
        "dash_subtitle": "Καλώς ήρθατε στο κεντρικό ταμπλό δεδομένων για τον Τουρισμό στην Ελλάδα (2019-2024).",
        "kpi_section_title": "Συνολικά Στατιστικά - Περιφέρειες (NUTS 2)",
        "kpi_arrivals": "Συνολικές Αφίξεις",
        "kpi_overnights": "Διανυκτερεύσεις",
        "kpi_receipts": "Συνολικά Έσοδα (€)",
        "kpi_spend": "Δαπάνη / Αφιξη",
        "kpi_alos": "Μέση Διάρκεια (ALOS)",
        "kpi_yield": "Ημερήσιο Yield",
        "unit_days": "ημ.",
        "unit_night": "€/νύχτα",

        # Highlights
        "highlights_title": "🏆 Κορυφαίες Περιφέρειες (Highlights)",
        "top_revenue_region": "🥇 **Πρωταθλήτρια Περιφέρεια (Έσοδα):** **{region}** με **{value} €** (καλύπτει το **{pct:.1f}%** των συνολικών εσόδων της χώρας).",
        "top_arrivals_region": "🚀 **Πρώτη Περιφέρεια σε Αφίξεις:** **{region}** με **{value}** συνολικούς επισκέπτες.",

        # Storytelling Insights Box (Dynamically Computed Metrics)
        "insights_summary_title": "🧠 Σημαντικά Ευρήματα & Αναλυτικά Συμπεράσματα",
        "insight_1_title": "📉 1. Ανάκαμψη COVID-19 (V-Shape Recovery)",
        "insight_1_body": "Τα έσοδα υπέστησαν κάθετη πτώση το 2020 λόγω πανδημίας ({min_val} €), αλλά η αγορά επέδειξε ταχύτατη ανάκαμψη πολλαπλασιάζοντας τα έσοδα κατά <strong>{multiplier:.1f}x</strong> και φτάνοντας σε <strong>ιστορικά ρεκόρ το 2023-2024 ({max_val} €)</strong>.",
        "insight_2_title": "⚖️ 2. Υψηλή Γεωγραφική Συγκέντρωση (Pareto Distribution)",
        "insight_2_body": "Μόλις <strong>3 από τις {total_regions} Περιφέρειες</strong> (<em>{top_regions_str}</em>) συγκεντρώνουν το <strong>{top3_pct:.1f}% του συνολικού τουριστικού εισοδήματος</strong> ({top3_val} €), ενώ οι υπόλοιπες 10 περιφέρειες μοιράζονται μόλις το {rest_pct:.1f}%.",
        "insight_3_title": "💶 3. Ποιοτική Δαπάνη & Ανισότητα Απόδοσης",
        "insight_3_body": "Η μέση εθνική δαπάνη ανά τουρίστη ανέρχεται στα <strong>{avg_spend:.0f} €</strong>. Η περιφέρεια <em>{max_spend_region}</em> ηγείται με <strong>{max_spend_val:.0f} €/επισκέπτη</strong>, καταγράφοντας <strong>{disparity_ratio:.1f}x υψηλότερη δαπάνη</strong> σε σύγκριση με την περιφέρεια <em>{min_spend_region}</em> ({min_spend_val:.0f} €/επισκέπτη).",

        # Filters & Exports
        "data_explore_title": "Εξερεύνηση Δεδομένων",
        "select_region": "Επιλογή Περιοχής:",
        "all_regions": "Όλες οι Περιοχές",
        "select_year": "Επιλογή Έτους:",
        "all_years": "Όλα τα Έτη",
        "download_csv": "📥 CSV",
        "download_pdf": "📄 PDF Summary",
        "showing_records": "Εμφάνιση {count} εγγραφών με βάση τα φίλτρα σας.",

        # Table Column Names
        "col_geo_label": "Περιφέρεια",
        "col_year": "Έτος",
        "col_arrivals": "Αφίξεις",
        "col_overnights": "Διανυκτερεύσεις",
        "col_receipts": "Έσοδα (€)",
        "col_turnover": "Τζίρος (€)",
        "col_alos": "ALOS (Ημέρες)",
        "col_yield": "Yield (€/νύχτα)",

        # Trends Page
        "trends_title": "📈 Χρονολογική Ανάλυση (Trends)",
        "trends_subtitle": "Ανάλυση της εξέλιξης του τουρισμού στην Ελλάδα μέσα στο χρόνο.",
        "chart_arrivals_title": "Συνολικές Αφίξεις ανά Έτος",
        "chart_receipts_title": "Συνολικά Έσοδα ανά Έτος (€)",
        "chart_alos_title": "ALOS: Ημέρες ανά Επισκέπτη (2019-2024)",
        "chart_yield_title": "Daily Yield: Έσοδα ανά Νύχτα (€/Διανυκτέρευση)",
        "trends_storytelling_title": "💡 Ερμηνεία Διαγραμμάτων & Τάσεων (Storytelling)",
        "trends_storytelling_body": (
            "📊 **Βασικά Συμπεράσματα Χρονοσειράς (2019 - 2024):**\n\n"
            "• **2019 (Βάση Αναφοράς):** Η χρονιά-σταθμός προ COVID-19 με 31.9M αφίξεις, 20.27B € έσοδα και μέσο daily yield **~92 €/νύχτα**.\n"
            "• **2020 (Κρίση Πανδημίας):** Δραματική πτώση λόγω ταξιδιωτικών περιορισμών (9.5M αφίξεις, 5.07B € έσοδα).\n"
            "• **2021-2022 (Στάδιο Ανάκαμψης):** Σταδιακή επανεκκίνηση με διπλασιασμό των αφίξεων (29.2M το 2022) και αύξηση της μέσης διάρκειας παραμονής (ALOS ~ 7.3 ημέρες).\n"
            "• **2023-2024 (Ιστορικό Ρεκόρ):** Πλήρης υπέρβαση επιδόσεων. Το 2024 καταγράφονται **34.8M αφίξεις**, **25.34B € έσοδα** και daily yield πάνω από **110 €/νύχτα**."
        ),

        # Regions Page
        "regions_title": "🗺️ Γεωγραφική Ανάλυση (Regions)",
        "regions_subtitle": "Σύγκριση της τουριστικής κίνησης ανά περιφέρεια.",
        "map_title": "Χάρτης Τουριστικών Αφίξεων Ελλάδα",
        "tab_arrivals": "📊 Αφίξεις",
        "tab_overnights": "🛏️ Διανυκτερεύσεις",
        "tab_receipts": "💶 Έσοδα",
        "tab_alos": "⏱️ ALOS (Διάρκεια)",
        "tab_yield": "💎 Daily Yield (€)",
        "tab_compare": "⚔️ Σύγκριση Περιφερειών",
        "select_region_a": "Επιλογή Περιφέρειας Α:",
        "select_region_b": "Επιλογή Περιφέρειας Β:",

        # Insights Page
        "insights_page_title": "💡 Στρατηγική Ανάλυση & Data Insights",
        "insights_page_subtitle": "Επιχειρησιακά συμπεράσματα, τάσεις και στρατηγικές προτάσεις βασισμένες στα δεδομένα.",
        "tab_covid": "📉 Ανάκαμψη COVID-19",
        "tab_conc": "⚖️ Γεωγραφική Συγκέντρωση",
        "tab_spend": "💶 Ποιοτική Δαπάνη / Τουρίστη",
        "tab_alos_yield": "⏱️ Διάρκεια & Yield",
        "tab_rec": "📜 Στρατηγικές Προτάσεις",

        # PDF Report
        "pdf_title": "Greek Tourism Executive Summary Report",
        "pdf_subtitle": "Macroeconomic Performance Overview (2019 - 2024)",
        "pdf_section1": "1. Executive Key Performance Indicators (KPIs)",
        "pdf_section2": "2. Top 5 Greek Regions by Tourism Revenue",
        "pdf_footer": "Generated automatically by Greek Tourism Analytics Platform",
    },

    "en": {
        # Navigation & Sidebar
        "sidebar_info_title": "ℹ️ Information",
        "sidebar_info_body": (
            "🇬🇷 **Greek Tourism Analytics & Intelligence**\n\n"
            "Enterprise-grade analytics & Data Storytelling system for Greek tourism (2019-2024).\n\n"
            "**🌐 Data Sources:**\n"
            "• Skillscapes API (Raw Metrics)\n"
            "• Eurostat Open Data (GeoJSON & NUTS 2)"
        ),
        "sidebar_status_active": "🟢 System Status: Active",
        "sidebar_pipeline": "⚡ Pipeline: Multi-Source Ingestion",
        "sidebar_scope": "📊 Scope: NUTS 2 (13 Regions)",
        "language_selector": "🌐 Language / Γλώσσα",

        # Main Dashboard Page
        "dash_title": "🇬🇷 Greek Tourism - Executive Dashboard",
        "dash_subtitle": "Welcome to the central analytics dashboard for Tourism in Greece (2019-2024).",
        "kpi_section_title": "Key Statistics - Greek Regions (NUTS 2)",
        "kpi_arrivals": "Total Arrivals",
        "kpi_overnights": "Overnights Spent",
        "kpi_receipts": "Total Revenue (€)",
        "kpi_spend": "Spend / Tourist",
        "kpi_alos": "Avg Stay (ALOS)",
        "kpi_yield": "Daily Yield",
        "unit_days": "days",
        "unit_night": "€/night",

        # Highlights
        "highlights_title": "🏆 Top Performing Regions (Highlights)",
        "top_revenue_region": "🥇 **Top Revenue Region:** **{region}** with **EUR {value}** (accounting for **{pct:.1f}%** of national tourism receipts).",
        "top_arrivals_region": "🚀 **Top Region by Arrivals:** **{region}** with **{value}** total visitors.",

        # Storytelling Insights Box (Dynamically Computed Metrics)
        "insights_summary_title": "🧠 Strategic Takeaways & Analytics Storytelling",
        "insight_1_title": "📉 1. COVID-19 V-Shaped Recovery",
        "insight_1_body": "Revenue experienced a severe shock in 2020 due to pandemic bans (€{min_val}), but demonstrated a **{multiplier:.1f}x recovery multiplier** to reach **all-time record highs in 2023-2024 (€{max_val})**.",
        "insight_2_title": "⚖️ 2. High Regional Concentration (Pareto Distribution)",
        "insight_2_body": "Only **3 out of {total_regions} Regions** (<em>{top_regions_str}</em>) command **{top3_pct:.1f}% of total national revenue** (€{top3_val}), leaving the remaining 10 regions to share just {rest_pct:.1f}%.",
        "insight_3_title": "💶 3. Tourist Spending Efficiency & Yield Disparity",
        "insight_3_body": "Average national spend per visitor stands at **€{avg_spend:.0f}**. **{max_spend_region}** leads with **€{max_spend_val:.0f}/visitor**, recording a **{disparity_ratio:.1f}x higher spending yield** compared to **{min_spend_region}** (€{min_spend_val:.0f}/visitor).",

        # Filters & Exports
        "data_explore_title": "Data Exploration",
        "select_region": "Select Region:",
        "all_regions": "All Regions",
        "select_year": "Select Year:",
        "all_years": "All Years",
        "download_csv": "📥 CSV",
        "download_pdf": "📄 PDF Summary",
        "showing_records": "Displaying {count} records based on your selected filters.",

        # Table Column Names
        "col_geo_label": "Region Name",
        "col_year": "Year",
        "col_arrivals": "Arrivals",
        "col_overnights": "Overnights",
        "col_receipts": "Receipts (€)",
        "col_turnover": "Turnover (€)",
        "col_alos": "ALOS (Days)",
        "col_yield": "Yield (€/night)",

        # Trends Page
        "trends_title": "📈 Chronological Trends",
        "trends_subtitle": "Multi-year evolution of Greek tourism indicators.",
        "chart_arrivals_title": "Total Arrivals by Year",
        "chart_receipts_title": "Total Revenue by Year (€)",
        "chart_alos_title": "ALOS: Days per Visitor (2019-2024)",
        "chart_yield_title": "Daily Yield: Revenue per Night (€/Overnight)",
        "trends_storytelling_title": "💡 Trend Analysis & Data Insights",
        "trends_storytelling_body": (
            "📊 **Key Time-Series Findings (2019 - 2024):**\n\n"
            "• **2019 (Pre-Pandemic Baseline):** Milestone benchmark with 31.9M arrivals, €20.27B revenue, and daily yield of **~€92/night**.\n"
            "• **2020 (Pandemic Shock):** Sharp decline due to global travel bans (9.5M arrivals, €5.07B revenue).\n"
            "• **2021-2022 (Recovery Phase):** Rapid rebound doubling arrivals (29.2M in 2022) with increased average length of stay (ALOS ~7.3 days).\n"
            "• **2023-2024 (Record Performance):** All-time peak records. 2024 logged **34.8M arrivals**, **€25.34B revenue**, and daily yields exceeding **€110/night**."
        ),

        # Regions Page
        "regions_title": "🗺️ Regional Analysis",
        "regions_subtitle": "Geographic breakdown and regional performance comparison.",
        "map_title": "Greek Tourist Arrivals Map",
        "tab_arrivals": "📊 Arrivals",
        "tab_overnights": "🛏️ Overnights",
        "tab_receipts": "💶 Receipts",
        "tab_alos": "⏱️ ALOS (Stay)",
        "tab_yield": "💎 Daily Yield (€)",
        "tab_compare": "⚔️ Region Comparison",
        "select_region_a": "Select Region A:",
        "select_region_b": "Select Region B:",

        # Insights Page
        "insights_page_title": "💡 Strategic Insights & Data Intelligence",
        "insights_page_subtitle": "Data-driven takeaways, regional dynamics, and executive policy recommendations.",
        "tab_covid": "📉 COVID-19 Recovery",
        "tab_conc": "⚖️ Regional Concentration",
        "tab_spend": "💶 Spending Efficiency",
        "tab_alos_yield": "⏱️ Stay & Yield",
        "tab_rec": "📜 Policy Action Plan",

        # PDF Report
        "pdf_title": "Greek Tourism Executive Summary Report",
        "pdf_subtitle": "Macroeconomic Performance Overview (2019 - 2024)",
        "pdf_section1": "1. Executive Key Performance Indicators (KPIs)",
        "pdf_section2": "2. Top 5 Greek Regions by Tourism Revenue",
        "pdf_footer": "Generated automatically by Greek Tourism Analytics Platform",
    }
}

def t(key: str, lang: str = "el", **kwargs) -> str:
    """Returns the localized string for `key`. Fallback to Greek or key itself if missing."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["el"])
    text_template = lang_dict.get(key, TRANSLATIONS["el"].get(key, key))
    if kwargs:
        try:
            return text_template.format(**kwargs)
        except Exception:
            return text_template
    return text_template
