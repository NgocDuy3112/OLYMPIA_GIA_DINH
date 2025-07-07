# 🏛️ OLYMPIA CUSTOM SERVICES

## Overview

Olympia Custom Services is a modular Python-based platform for scalable data processing, analysis, and automation.  
It uses **Docker** for containerization and **PostgreSQL** for data storage, providing APIs and services for media management, data analysis, and bot automation.

---

## ✨ Features

- **Modular Architecture** – Clear separation into `src`, `assistant`, and `ocbot` modules.
- **RESTful APIs** – Versioned API endpoints for maintainability.
- **Database Integration** – PostgreSQL with configuration and SQL scripts.
- **Media & Data Management** – Supports audio, video, images, PDFs, and tabular data.
- **Bot Automation** – Built-in bot framework for automated workflows.
- **Jupyter Notebooks** – Interactive analysis and prototyping.
- **Dockerized Deployment** – Consistent, portable environments using Docker Compose.

---

## 📦 Project Structure

```
├── src/              # Main application code: APIs, services, models, utils
├── assistant/        # Assistant services (chat, prompt management, etc.)
├── ocbot/            # Bot automation utilities
├── data/             # Media, PDFs, database files, tabular data
├── sql/              # SQL scripts for DB setup and migration
├── notebooks/        # Jupyter notebooks for data analysis
├── images/           # Project diagrams and images
├── sounds/           # Audio files for notifications/events
├── docker-compose.yaml
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- (Optional) PostgreSQL client tools

---

### ⚙️ Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NgocDuy3112/OLYMPIA_CUSTOM_SERVICES.git
   cd system
   ```

2. **Start services using Docker Compose:**
   ```bash
   docker-compose -f docker-compose.yaml -p gloryteam up --build
   ```

3. **Access the platform:**
   - API endpoints: [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)
   - Open `notebooks/analysis.ipynb` for data exploration.

---

## 🗄️ Database

- PostgreSQL data lives in `data/postgresql/`.
- SQL scripts for table creation and management are in `sql/`.

---

## 🛠 Development

Main application code is in `src/`.

To install dependencies for each service:
```bash
pip install -r <service>/requirements.txt
```
Where `<service>` can be **app**, **assistant**, or **glorybot**.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request.

---

## 📄 License

[MIT License](LICENSE)

---

## ✅ TODO

- Finalize the assistant service code.
- Add detailed documentation and examples.