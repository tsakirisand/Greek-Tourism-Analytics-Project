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
        "sidebar_status_active": "🟢 Κατάσταση Συστήματος: Ενεργό",
        "sidebar_pipeline": "⚡ Ροή Δεδομένων: Πολλαπλές Πηγές",
        "sidebar_scope": "📊 Εύρος: 13 Περιφέρειες Ελλάδας",
        "language_selector": "🌐 Γλώσσα / Language",

        # Main Dashboard Page
        "dash_title": "🇬🇷 Ελληνικός Τουρισμός - Κεντρική Σελίδα",
        "dash_subtitle": "Καλώς ήρθατε στην πλατφόρμα ανάλυσης του ελληνικού τουρισμού (2019-2024).",
        "kpi_section_title": "Συνολικά Στατιστικά Περιφερειών",
        "kpi_arrivals": "Συνολικές Αφίξεις",
        "kpi_overnights": "Διανυκτερεύσεις",
        "kpi_receipts": "Συνολικά Έσοδα (€)",
        "kpi_spend": "Δαπάνη ανά Επισκέπτη",
        "kpi_alos": "Μέση Διάρκεια Παραμονής",
        "kpi_yield": "Ημερήσιο Έσοδο ανά Νύχτα",
        "unit_days": "ημέρες",
        "unit_night": "€/νύχτα",

        # Highlights
        "highlights_title": "🏆 Κορυφαίες Περιφέρειες",
        "top_revenue_region": "🥇 **Πρώτη Περιφέρεια σε Έσοδα:** **{region}** με **{value} €** (καλύπτει το **{pct}%** των συνολικών εσόδων της χώρας).",
        "top_arrivals_region": "🚀 **Πρώτη Περιφέρεια σε Αφίξεις:** **{region}** με **{value}** επισκέπτες.",

        # Simple & Friendly Storytelling Insights Box
        "insights_summary_title": "🧠 Κύρια Συμπεράσματα με Απλά Λόγια",
        "insight_1_title": "📉 1. Μεγάλη Ανάκαμψη μετά την Πανδημία",
        "insight_1_body": "Το 2020 τα έσοδα έπεσαν στα {min_val} € λόγω των ταξιδιωτικών περιορισμών. Από τότε, ο τουρισμός αυξήθηκε κατά **{multiplier} φορές**, φτάνοντας στο ιστορικό ρεκόρ των **{max_val} € το 2023-2024**.",
        "insight_2_title": "⚖️ 2. Πού Πηγαίνουν τα Περισσότερα Χρήματα",
        "insight_2_body": "Μόλις **3 από τις {total_regions} Περιφέρειες** (**{top_regions_str}**) συγκεντρώνουν το **{top3_pct}% των συνολικών εσόδων** της χώρας ({top3_val} €), αφήνοντας το υπόλοιπο {rest_pct}% στις άλλες 10 περιφέρειες.",
        "insight_3_title": "💶 3. Πόσα Χρήματα Ξοδεύει Κάθε Τουρίστας",
        "insight_3_body": "Ο μέσος τουρίστας στην Ελλάδα ξοδεύει **{avg_spend} €**. Στο **{max_spend_region}** οι επισκέπτες ξοδεύουν τα περισσότερα (**{max_spend_val} €** ανά άτομο), δηλαδή **{disparity_ratio} φορές περισσότερα** από ό,τι στη **{min_spend_region}** ({min_spend_val} €).",

        # Filters & Exports
        "data_explore_title": "Εξερεύνηση Δεδομένων",
        "select_region": "Επιλογή Περιοχής:",
        "all_regions": "Όλες οι Περιοχές",
        "select_year": "Επιλογή Έτους:",
        "all_years": "Όλα τα Έτη",
        "download_csv": "📥 Λήψη CSV",
        "download_pdf": "📄 Λήψη PDF Αναφοράς",
        "showing_records": "Εμφάνιση {count} εγγραφών.",

        # Table Column Names
        "col_geo_label": "Περιφέρεια",
        "col_year": "Έτος",
        "col_arrivals": "Αφίξεις",
        "col_overnights": "Διανυκτερεύσεις",
        "col_receipts": "Έσοδα (€)",
        "col_turnover": "Τζίρος (€)",
        "col_alos": "Διάρκεια (Ημέρες)",
        "col_yield": "Έσοδο / Νύχτα (€)",

        # Trends Page
        "trends_title": "📈 Χρονολογική Ανάλυση (Τάσεις)",
        "trends_subtitle": "Πώς εξελίχθηκε ο τουρισμός στην Ελλάδα από το 2019 έως το 2024.",
        "chart_arrivals_title": "Συνολικές Αφίξεις ανά Έτος",
        "chart_receipts_title": "Συνολικά Έσοδα ανά Έτος (€)",
        "chart_alos_title": "Μέση Διάρκεια Παραμονής σε Ημέρες (2019-2024)",
        "chart_yield_title": "Ημερήσιο Έσοδο ανά Διανυκτέρευση (€/νύχτα)",
        "trends_storytelling_title": "💡 Τι Μας Δείχνουν τα Διαγράμματα",
        "trends_storytelling_body": (
            "📊 **Πώς Κινήθηκε ο Τουρισμός (2019 - 2024):**\n\n"
            "• **2019:** Η καλύτερη χρονιά προ πανδημίας με 31,9 εκατομμύρια αφίξεις και 20,27 δισεκατομμύρια € έσοδα.\n"
            "• **2020:** Μεγάλη πτώση λόγω COVID-19 (9,5 εκατομμύρια αφίξεις, 5,07 δισεκατομμύρια € έσοδα).\n"
            "• **2021-2022:** Ταχεία επανεκκίνηση με διπλασιασμό των επισκεπτών και αύξηση της διάρκειας παραμονής.\n"
            "• **2023-2024:** Ιστορικό ρεκόρ όλων των εποχών με **34,8 εκατομμύρια αφίξεις** και **25,34 δισεκατομμύρια € έσοδα**."
        ),

        # Regions Page
        "regions_title": "🗺️ Ανάλυση ανά Περιφέρεια",
        "regions_subtitle": "Σύγκριση των 13 περιφερειών της Ελλάδας.",
        "map_title": "Χάρτης Τουριστικών Αφίξεων στην Ελλάδα",
        "tab_arrivals": "📊 Αφίξεις",
        "tab_overnights": "🛏️ Διανυκτερεύσεις",
        "tab_receipts": "💶 Έσοδα",
        "tab_alos": "⏱️ Διάρκεια Παραμονής",
        "tab_yield": "💎 Έσοδο ανά Νύχτα",
        "tab_compare": "⚔️ Σύγκριση Περιφερειών",
        "select_region_a": "Επιλογή 1ης Περιφέρειας:",
        "select_region_b": "Επιλογή 2ης Περιφέρειας:",

        # Insights Page
        "insights_page_title": "💡 Στρατηγική Ανάλυση & Συμπεράσματα",
        "insights_page_subtitle": "Απλά συμπεράσματα και προτάσεις επενδύσεων βασισμένες στα δεδομένα.",
        "tab_covid": "📉 Ανάκαμψη COVID-19",
        "tab_conc": "⚖️ Κατανομή Εσόδων",
        "tab_spend": "💶 Δαπάνη ανά Τουρίστα",
        "tab_alos_yield": "⏱️ Διάρκεια & Απόδοση",
        "tab_rec": "📜 Επενδυτικές Προτάσεις",

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
            "Analytics & Data Storytelling system for Greek tourism (2019-2024).\n\n"
            "**🌐 Data Sources:**\n"
            "• Skillscapes API (Raw Metrics)\n"
            "• Eurostat Open Data (GeoJSON & NUTS 2)"
        ),
        "sidebar_status_active": "🟢 System Status: Active",
        "sidebar_pipeline": "⚡ Data Pipeline: Multi-Source",
        "sidebar_scope": "📊 Scope: 13 Regions of Greece",
        "language_selector": "🌐 Language / Γλώσσα",

        # Main Dashboard Page
        "dash_title": "🇬🇷 Greek Tourism - Executive Dashboard",
        "dash_subtitle": "Welcome to the analytics dashboard for Tourism in Greece (2019-2024).",
        "kpi_section_title": "Key Statistics by Region",
        "kpi_arrivals": "Total Arrivals",
        "kpi_overnights": "Overnights Spent",
        "kpi_receipts": "Total Revenue (€)",
        "kpi_spend": "Spend per Visitor",
        "kpi_alos": "Average Stay",
        "kpi_yield": "Daily Revenue per Night",
        "unit_days": "days",
        "unit_night": "€/night",

        # Highlights
        "highlights_title": "🏆 Top Performing Regions",
        "top_revenue_region": "🥇 **Top Region by Revenue:** **{region}** with **{value} €** (accounting for **{pct}%** of national tourism revenue).",
        "top_arrivals_region": "🚀 **Top Region by Visitors:** **{region}** with **{value}** total visitors.",

        # Simple & Friendly Storytelling Insights Box
        "insights_summary_title": "🧠 Key Takeaways in Simple Words",
        "insight_1_title": "📉 1. Strong Post-Pandemic Recovery",
        "insight_1_body": "In 2020, revenue dropped to {min_val} € due to pandemic travel restrictions. Since then, tourism revenue grew **{multiplier} times**, reaching an all-time record of **{max_val} € in 2023-2024**.",
        "insight_2_title": "⚖️ 2. Where the Revenue Goes",
        "insight_2_body": "Just **3 out of {total_regions} Regions** (**{top_regions_str}**) collect **{top3_pct}% of all tourism revenue** in the country ({top3_val} €), leaving the remaining {rest_pct}% for the other 10 regions.",
        "insight_3_title": "💶 3. How Much Each Tourist Spends",
        "insight_3_body": "The average tourist in Greece spends **{avg_spend} €**. In **{max_spend_region}**, visitors spend the most (**{max_spend_val} €** per person), which is **{disparity_ratio} times higher** than in **{min_spend_region}** ({min_spend_val} €).",

        # Filters & Exports
        "data_explore_title": "Data Exploration",
        "select_region": "Select Region:",
        "all_regions": "All Regions",
        "select_year": "Select Year:",
        "all_years": "All Years",
        "download_csv": "📥 Download CSV",
        "download_pdf": "📄 Download PDF Report",
        "showing_records": "Displaying {count} records.",

        # Table Column Names
        "col_geo_label": "Region Name",
        "col_year": "Year",
        "col_arrivals": "Arrivals",
        "col_overnights": "Overnights",
        "col_receipts": "Receipts (€)",
        "col_turnover": "Turnover (€)",
        "col_alos": "Stay Duration (Days)",
        "col_yield": "Revenue / Night (€)",

        # Trends Page
        "trends_title": "📈 Chronological Trends",
        "trends_subtitle": "How tourism in Greece evolved from 2019 to 2024.",
        "chart_arrivals_title": "Total Arrivals by Year",
        "chart_receipts_title": "Total Revenue by Year (€)",
        "chart_alos_title": "Average Length of Stay in Days (2019-2024)",
        "chart_yield_title": "Daily Revenue per Night (€/night)",
        "trends_storytelling_title": "💡 What the Charts Tell Us",
        "trends_storytelling_body": (
            "📊 **Tourism Performance (2019 - 2024):**\n\n"
            "• **2019:** Peak pre-pandemic year with 31.9M visitors and €20.27B revenue.\n"
            "• **2020:** Major COVID-19 decline (9.5M visitors, €5.07B revenue).\n"
            "• **2021-2022:** Rapid recovery with visitor numbers doubling and longer stays.\n"
            "• **2023-2024:** All-time record performance with **34.8M visitors** and **€25.34B revenue**."
        ),

        # Regions Page
        "regions_title": "🗺️ Regional Analysis",
        "regions_subtitle": "Comparing the 13 regions of Greece.",
        "map_title": "Greek Tourist Arrivals Map",
        "tab_arrivals": "📊 Arrivals",
        "tab_overnights": "🛏️ Overnights",
        "tab_receipts": "💶 Receipts",
        "tab_alos": "⏱️ Stay Duration",
        "tab_yield": "💎 Revenue / Night",
        "tab_compare": "⚔️ Region Comparison",
        "select_region_a": "Select 1st Region:",
        "select_region_b": "Select 2nd Region:",

        # Insights Page
        "insights_page_title": "💡 Strategic Insights & Takeaways",
        "insights_page_subtitle": "Simple data takeaways and investment suggestions.",
        "tab_covid": "📉 COVID-19 Recovery",
        "tab_conc": "⚖️ Revenue Distribution",
        "tab_spend": "💶 Visitor Spending",
        "tab_alos_yield": "⏱️ Stay & Revenue Yield",
        "tab_rec": "📜 Investment Suggestions",

        # PDF Report
        "pdf_title": "Greek Tourism Executive Summary Report",
        "pdf_subtitle": "Macroeconomic Performance Overview (2019 - 2024)",
        "pdf_section1": "1. Executive Key Performance Indicators (KPIs)",
        "pdf_section2": "2. Top 5 Greek Regions by Tourism Revenue",
        "pdf_footer": "Generated automatically by Greek Tourism Analytics Platform",
    }
}

def t(key: str, lang: str = "el", **kwargs) -> str:
    """Returns localized string for `key`. Fallback to Greek or key itself if missing."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["el"])
    text_template = lang_dict.get(key, TRANSLATIONS["el"].get(key, key))
    if kwargs:
        try:
            return text_template.format(**kwargs)
        except Exception as e:
            # Format failure fallback safely without crashing or leaking raw syntax
            return text_template
    return text_template
