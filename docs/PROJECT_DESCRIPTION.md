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

### 3. Node.js
**Description**: Node.js is an open-source, cross-platform JavaScript runtime built on Chrome's V8 engine that allows JavaScript to run outside the browser, powering server-side applications, build tooling, and package management via npm.

**Usage**: In RiskRadar, it is used as the runtime environment for the React front end, managing project dependencies through npm, running the development server, and executing the build toolchain that compiles and bundles the front-end application.
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

## IDEs
### 1. Android Studio
**Description**: Android Studio is Google's official integrated development environment (IDE) for Android application development, built on JetBrains' IntelliJ IDEA. It provides code editing, debugging, performance tooling, and a built-in Android Emulator for testing applications on virtual devices.

**Usage**: In RiskRadar, it is used as the development environment for testing the mobile application on Android, providing the Android Emulator for local device simulation and debugging of the Expo-based React Native build.

## CLIs
### 1. Expo
**Description**: Expo is an open-source platform and command-line interface for building universal React Native applications. It provides a managed workflow with pre-configured native modules, over-the-air updates, and streamlined build and deployment tooling for iOS and Android.

**Usage**: In RiskRadar, it is used to develop, build, and deploy the cross-platform mobile application from a single React-based codebase, and to manage push notification delivery to user devices via the device tokens stored in the database.