# GLO System

## Overview

The GLO System is a modular Python-based platform designed for scalable data processing, analysis, and automation. It leverages Docker for containerization, PostgreSQL for data storage, and provides a suite of services and APIs for various applications, including data analysis, media management, and bot automation.

## Features

- **Modular Architecture:** Organized into `src`, `assistant`, and `glorybot` modules for clear separation of concerns.
- **RESTful APIs:** Versioned API endpoints for extensibility and backward compatibility.
- **Database Integration:** Uses PostgreSQL with ready-to-use configuration and initialization scripts.
- **Media & Data Management:** Handles audio, video, image, PDF, and tabular data.
- **Bot Automation:** Includes a bot framework for automation and interaction.
- **Jupyter Notebooks:** For data analysis and prototyping.
- **Dockerized Deployment:** Easy setup and consistent environments using Docker Compose.

## Project Structure

```
├── src/           # Main application code (APIs, models, services, utils)
├── assistant/     # Assistant services (chat, prompts, splitters, etc.)
├── glorybot/      # Bot automation and related utilities
├── data/          # Media, PDFs, database files, and tabular data
├── sql/           # SQL scripts for database setup and management
├── notebooks/     # Jupyter notebooks for analysis
├── images/        # Project images and diagrams
├── sounds/        # Audio files for notifications and events
├── docker-compose.yaml
├── README.md
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.8+
- (Optional) PostgreSQL client tools

### Setup

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd system
   ```

2. **Start services with Docker Compose:**
   ```sh
   docker-compose up --build
   ```

3. **Access the application:**
   - API endpoints: `http://localhost:<port>/api/v1/`
   - Jupyter Notebooks: Open `notebooks/analysis.ipynb` in your preferred environment.

### Database

- PostgreSQL data and configuration are stored in `data/postgresql/`.
- SQL scripts for table creation, insertion, and management are in `sql/`.

### Development

- Main application code is in `src/`.
- To install dependencies for a service:
  ```sh
  pip install -r <service>/requirements.txt
  ```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes.
4. Push to the branch and open a pull request.

## License

[MIT License](LICENSE)
