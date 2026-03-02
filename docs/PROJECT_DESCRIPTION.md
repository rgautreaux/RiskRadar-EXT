# RiskRadar Description

---

## APIs

### 1. OpenAI API

**Description**: OpenAI provides a suite of large language model APIs (e.g., GPT-4) that enable natural language understanding, text generation, and code analysis via simple REST calls.

**Usage**: In RiskRadar, it is used for natural language processing, data analysis, and generating insights from collected data—summarizing large datasets, extracting key information, and providing recommendations.

### 2. Firecrawl API

**Description**: Firecrawl is a web scraping and crawling service that turns websites into clean, structured, LLM-ready data without requiring manual selector configuration.

**Usage**: In RiskRadar, it is used to gather real-time data from websites, social media platforms, and other online sources relevant to the chosen problem domain.

### 3. RabbitMQ API

**Description**: RabbitMQ is an open-source message broker that implements the Advanced Message Queuing Protocol (AMQP), enabling applications to send, receive, and queue messages between distributed services.

**Usage**: In RiskRadar, it is used for message queuing and handling asynchronous tasks, managing the flow of data between components so that processing and analysis do not block the main application thread.

### 4. Docker Engine API

**Description**: The Docker Engine API is a RESTful API that allows programmatic interaction with the Docker daemon to build, run, and manage containers—lightweight, portable units that package an application with all its dependencies.

**Usage**: In RiskRadar, it is used for containerization and deployment, ensuring the application runs consistently across different platforms and environments.

### 5. Antimatter API

**Description**: Antimatter is a data security platform that provides a control plane for governing how data is accessed, encrypted, and shared across multiple storage systems and clients. It separates data control (policy, access rules, encryption) from the data plane (storage and transport).

**Usage**: In RiskRadar, it is used to manage data consistently and securely, enforcing access policies independent of the underlying storage infrastructure.

---

## Languages & Frameworks

### 1. Python

**Description**: Python is a high-level, general-purpose programming language known for its readability, extensive standard library, and rich ecosystem of third-party packages for web development, data processing, and machine learning.

**Usage**: In RiskRadar, it is used as the primary back-end language to handle web scraping orchestration, data processing pipelines, AI-driven summarization of articles and alerts, and interaction with external APIs such as OpenAI and Firecrawl.

### 2. React

**Description**: React is an open-source JavaScript library developed by Meta for building user interfaces through reusable, component-based architectures that efficiently update and render in response to data changes.

**Usage**: In RiskRadar, it is used to build the front-end user interface, providing an interactive and responsive dashboard for visualizing risk data, displaying analysis results, and enabling users to interact with the system's features.

---

## Database

### MySQL (MariaDB)

**Description**: MySQL is an open-source relational database management system that uses Structured Query Language (SQL) for defining, querying, and manipulating data in tabular form with support for indexing, transactions, and referential integrity.

**Usage**: In RiskRadar, it is used (via MariaDB) as the primary data store for the `riskradar_db` database, persisting users, articles, alerts, sources, scrape logs, AI-generated summaries, notification settings, and user preferences across 13 interconnected tables.

For full schema documentation, normalization analysis, and known issues, see [DATA_MODEL.md](DATA_MODEL.md).

---

## Infrastructure

### Apache HTTP Server

**Description**: Apache HTTP Server is an open-source, cross-platform web server maintained by the Apache Software Foundation, widely used to serve web content and proxy requests between clients and back-end applications.

**Usage**: In RiskRadar, it is used (via XAMPP alongside PHP and phpMyAdmin) as the local web server during development, serving the application and providing database administration through phpMyAdmin.