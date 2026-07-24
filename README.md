# 🇬🇷 Greek Tourism Analytics Dashboard (2019-2024)

An enterprise-grade data analytics and visualization application for Greek tourism statistics (Arrivals, Overnights, Receipts) covering the 2019-2024 period. Built with **Python**, **Streamlit**, **PostgreSQL**, **Plotly**, and **Docker**.

---

## 🌐 Live Demo
🔗 **Public Application URL:** [greek-tourism-analytics-project.onrender.com](https://greek-tourism-analytics-project.onrender.com)

---

## 🌟 Key Features

* **📊 Executive Dashboard (KPIs):** Macroeconomic overview tracking Arrivals, Overnights, Receipts, Spend per Tourist (€), **Average Length of Stay (ALOS - Days/Visitor)**, and **Daily Yield (€/Night)** with custom interactive metric cards.
* **🧠 Data Storytelling & Automated Insights:** Automated domain analysis quantifying COVID-19 V-shaped recovery, 70%+ regional revenue concentration, tourist spending efficiency, and ALOS/Yield scatter matrices.
* **💡 Standalone Insights Page (`3_💡_Insights.py`):** Dedicated page featuring in-depth analysis on pandemic shock, regional economic disparities, tourist spending rankings, ALOS/Yield dynamics, and executive action plans.
* **🌐 Multi-Source Data Architecture:** Data pipeline integrating Skillscapes API (raw metrics) and Eurostat Open Data API (NUTS 2 GeoJSON boundaries).
* **📈 Chronological Trends:** Interactive multi-year trend charts powered by Plotly tracking Arrivals, Receipts, ALOS, and Daily Yield with automated trend explanations.
* **🗺️ Interactive Map & Regional Comparison:** GeoJSON-powered Choropleth map covering all 13 Greek NUTS 2 regions with dedicated tabs for Arrivals, Overnights, Receipts, ALOS, Daily Yield, and **Side-by-Side Regional Comparisons**.
* **📄 Executive PDF & CSV Export:** Download auto-generated executive PDF summary reports (including ALOS & Yield metrics) and Excel-optimized CSV datasets (`UTF-8-SIG` encoding with `;` delimiter).
* **🐳 Production Ready (Docker):** Full Docker and Docker Compose setup for seamless containerized deployment.

---

## 🛠️ Tech Stack

* **Frontend / UI:** [Streamlit](https://streamlit.io/) with Custom CSS (Inter font, Glassmorphism hover effects, Navy Theme)
* **Visualizations:** [Plotly Express](https://plotly.com/python/)
* **Backend & ETL:** Python 3.10+, Pandas, SQLAlchemy
* **Database:** PostgreSQL (with automatic local JSON fallback for zero-downtime cloud hosting)
* **Containerization:** Docker & Docker Compose

---

## 🚀 Setup & Installation

### 1. Local Run

#### Prerequisites:
* Python 3.10+
* Running PostgreSQL instance

#### Steps:
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/tsakirisand/Greek-Tourism-Analytics-Project.git
   cd Greek-Tourism-Analytics-Project
   ```

2. **Create & Activate Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables (`.env`):**
   Create a `.env` file in the project root directory:
   ```env
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=greek_tourism
   ```

5. **Initialize Database & Load Data:**
   ```bash
   # Create database tables
   python main.py --init-db

   # Extract from API and load into PostgreSQL
   python main.py --load-data
   ```

6. **Launch Dashboard:**
   ```bash
   python main.py --dashboard
   ```
   Access the dashboard at `http://localhost:8501`.

---

### 2. Run with Docker Compose (Recommended for Cloud Hosting)

No local Python or PostgreSQL installation required!

```bash
docker-compose up --build
```

Access the dashboard at `http://localhost:8501`.

---

## 📁 Project Structure

```text
GreekTourismProject/
├── app/
│   ├── 🏛️_Dashboard.py        # Streamlit Main Dashboard
│   ├── components.py           # Shared UI components & Custom CSS
│   └── pages/
│       ├── 1_📈_Trends.py      # Chronological Trends Page
│       ├── 2_🗺️_Regions.py     # Regional Analysis & Interactive Map
│       └── 3_💡_Insights.py    # Dedicated Data Insights & Storytelling
├── api_client.py               # API Client for data extraction (Skillscapes & Eurostat)
├── loader.py                   # ETL Pipeline (API -> PostgreSQL)
├── create_tables.py            # Database Schema definition
├── database.py                 # SQLAlchemy Connection Engine
├── main.py                     # CLI Entry Point
├── Dockerfile                  # Container build instructions
├── docker-compose.yml          # Container orchestration
└── requirements.txt            # Python Dependencies
```

---

## 📄 License

MIT License © 2026 Greek Tourism Analytics Project
