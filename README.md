# 🇬🇷 Greek Tourism Analytics Dashboard (2019-2024)

Πλήρης enterprise εφαρμογή ανάλυσης και οπτικοποίησης δεδομένων ελληνικού τουρισμού (Αφίξεις, Διανυκτερεύσεις, Έσοδα) για την περίοδο 2019-2024. Η εφαρμογή είναι κατασκευασμένη με **Python**, **Streamlit**, **PostgreSQL**, **Plotly** και **Docker**.

---

## 🌟 Χαρακτηριστικά (Features)

* **📊 Κεντρικό Ταμπλό (KPIs):** Συνολικά στατιστικά στοιχεία (Αφίξεις, Διανυκτερεύσεις, Έσοδα σε Δισεκατομμύρια €) με διαδραστικά Metric Cards.
* **📈 Χρονολογική Ανάλυση (Trends):** Γραφήματα εξέλιξης του τουρισμού ανά έτος.
* **🗺️ Διαδραστικός Χάρτης Ελλάδας (Regions):** Χωροπληθικός χάρτης (Choropleth Map) των 13 Περιφερειών της Ελλάδας (NUTS 2) με GeoJSON και αναλυτικές καρτέλες (Tabs) για Αφίξεις, Διανυκτερεύσεις και Έσοδα.
* **📥 Εξαγωγή Δεδομένων (CSV Export):** Δυνατότητα λήψης των φιλτραρισμένων δεδομένων σε μορφή CSV, ειδικά διαμορφωμένη για το ελληνικό Excel (`UTF-8-SIG`, διαχωριστής `;`).
* **🐳 Dockerized Deployment:** Πλήρης υποστήριξη Docker & Docker Compose για άμεσο deployment σε οποιοδήποτε Cloud περιβάλλον.

---

## 🛠️ Τεχνολογικό Stack

* **Frontend / UI:** [Streamlit](https://streamlit.io/) με Custom CSS (Inter font, Hover effects, Navy Theme)
* **Visualizations:** [Plotly Express](https://plotly.com/python/)
* **Backend & ETL:** Python 3.10+, Pandas, SQLAlchemy
* **Database:** PostgreSQL
* **Containerization:** Docker & Docker Compose

---

## 🚀 Οδηγίες Εγκατάστασης & Λειτουργίας

### 1. Τοπική Εγκατάσταση (Local Run)

#### Προαπαιτούμενα:
* Python 3.10+
* PostgreSQL εγκατεστημένη και σε λειτουργία

#### Βήματα:
1. **Clone το Repository:**
   ```bash
   git clone https://github.com/your-username/GreekTourismProject.git
   cd GreekTourismProject
   ```

2. **Δημιουργία & Ενεργοποίηση Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Εγκατάσταση Εξαρτήσεων:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ρύθμιση Μεταβλητών Περιβάλλοντος (`.env`):**
   Δημιουργήστε ένα αρχείο `.env` στη ρίζα του project:
   ```env
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=greek_tourism
   ```

5. **Αρχικοποίηση Βάσης & Φόρτωση Δεδομένων:**
   ```bash
   # Δημιουργία πινάκων στη PostgreSQL
   python main.py --init-db

   # Φόρτωση δεδομένων από το API
   python main.py --load-data
   ```

6. **Εκκίνηση Εφαρμογής (Streamlit):**
   ```bash
   python main.py --dashboard
   ```
   Η εφαρμογή θα ανοίξει στη διεύθυνση `http://localhost:8501`.

---

### 2. Εκκίνηση με Docker Compose (Προτεινόμενο για Server / Production)

Δεν απαιτείται προεγκατεστημένη Python ή PostgreSQL!

```bash
# Εκκίνηση της Βάσης Δεδομένων και του Streamlit App
docker-compose up --build
```

Η εφαρμογή θα είναι διαθέσιμη στο `http://localhost:8501`.

---

## 📁 Δομή Project

```text
GreekTourismProject/
├── app/
│   ├── 🏛️_Dashboard.py        # Κεντρική Σελίδα Streamlit
│   ├── components.py           # Κοινά UI στοιχεία & CSS
│   └── pages/
│       ├── 1_📈_Trends.py      # Σελίδα Χρονολογικής Ανάλυσης
│       └── 2_🗺️_Regions.py     # Σελίδα Χάρτη & Περιφερειών
├── api_client.py               # Client για τη λήψη δεδομένων από το API
├── loader.py                   # ETL Pipeline (API -> PostgreSQL)
├── create_tables.py            # Σχήμα Βάσης Δεδομένων
├── database.py                 # SQLAlchemy Connection Engine
├── main.py                     # CLI Entry Point
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose orchestration
└── requirements.txt            # Python Dependencies
```

---

## 📄 Άδεια Χρήσης (License)

MIT License © 2026 Greek Tourism Analytics Project
# Greek-Tourism-Analytics-Project
