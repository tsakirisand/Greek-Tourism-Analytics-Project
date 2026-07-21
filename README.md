# 🇬🇷 Greek Tourism Analytics Dashboard (2019-2024)

An enterprise-grade data analytics and visualization application for Greek tourism statistics (Arrivals, Overnights, Receipts) covering the 2019-2024 period. Built with **Python**, **Streamlit**, **PostgreSQL**, **Plotly**, and **Docker**.

---

## 🌟 Key Features

* **📊 Executive Dashboard (KPIs):** Macroeconomic overview tracking Arrivals, Overnights, and Receipts (in Billions of Euros) with custom interactive metric cards.
* **📈 Chronological Trends:** Interactive multi-year trend charts powered by Plotly.
* **🗺️ Interactive Map of Greece (Regions):** GeoJSON-powered Choropleth map covering all 13 Greek NUTS 2 regions with dedicated tabs for Arrivals, Overnights, and Receipts.
* **📥 Excel-Optimized CSV Export:** Download filtered datasets formatted specifically for European/Greek Excel environments (`UTF-8-SIG` encoding with `;` delimiter).
* **🐳 Production Ready (Docker):** Full Docker and Docker Compose setup for seamless containerized deployment on any cloud provider.

---

## 🛠️ Tech Stack

* **Frontend / UI:** [Streamlit](https://streamlit.io/) with Custom CSS (Inter font, Glassmorphism hover effects, Navy Theme)
* **Visualizations:** [Plotly Express](https://plotly.com/python/)
* **Backend & ETL:** Python 3.10+, Pandas, SQLAlchemy
* **Database:** PostgreSQL
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
│       └── 2_🗺️_Regions.py     # Regional Analysis & Interactive Map
├── api_client.py               # API Client for data extraction
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
