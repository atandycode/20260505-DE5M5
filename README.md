# Library System
A complete library data system to allow quality analysis using PowerBI Dashboards.

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation & Usage](#installation--usage)
- [Architecture](#architecture)
- [Dashboard](#dashboard)
- [Risks & Issues](#risks--issues)

## Overview
A containerised Python ETL pipeline that cleans and enriches library data 
and outputs metrics for analysis in PowerBI.

## Requirements
- Docker Desktop
- PowerBI Desktop
- Python 3.12

## Installation & Usage
1. Clone the repository
2. Navigate to the project folder
3. Build the Docker container
\```bash
docker build -t library-pipeline .
\```
4. Run the pipeline
\```bash
docker run -v $(pwd)/data:/app/data library-pipeline
\```
5. Open PowerBI and connect to the data folder

## Architecture
![Architecture](docs/library_system_architecture.png)

User uploads CSV file via web based application hosted in a Docker container.
Back end Docker container runs the ETL pipeline and outputs cleaned data.
PowerBI connects to the output folder and presents the dashboard.

## Dashboard
![PowerBI Dashboard](docs/demo_dashboard.png)

## Risks & Issues
| Risk | Impact | Mitigation |
|------|--------|------------|
| SQLite not suitable for concurrent users | High | Migrate to PostgreSQL |
| No pipeline scheduling | Medium | Add cron or Airflow |
# Library System
A complete library data system to allow quality analysis using PowerBI Dashboards.

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation & Usage](#installation--usage)
- [Architecture](#architecture)
- [Dashboard](#dashboard)
- [Risks & Issues](#risks--issues)

## Overview
A containerised Python ETL pipeline that cleans and enriches library data 
and outputs metrics for analysis in PowerBI.

## Requirements
- Docker Desktop
- PowerBI Desktop
- Python 3.12

## Installation & Usage
1. Clone the repository
2. Navigate to the project folder
3. Build the Docker container
\```bash
docker build -t library-pipeline .
\```
4. Run the pipeline
\```bash
docker run -v $(pwd)/data:/app/data library-pipeline
\```
5. Open PowerBI and connect to the data folder

## Architecture
![Architecture](docs/library_system_architecture.png)

User uploads CSV file via web based application hosted in a Docker container.
Back end Docker container runs the ETL pipeline and outputs cleaned data.
PowerBI connects to the output folder and presents the dashboard.

## Dashboard
![PowerBI Dashboard](docs/demo_dashboard.png)

## Risks & Issues
| Risk | Impact | Mitigation |
|------|--------|------------|
| SQLite not suitable for concurrent users | High | Migrate to PostgreSQL |
| No pipeline scheduling | Medium | Add cron or Airflow |
| Container fails mid pipeline run | High | Add restart policy in Dockerfile |