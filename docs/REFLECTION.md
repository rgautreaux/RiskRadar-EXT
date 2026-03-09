# Reflection on AI Tool Usage in CMPS 357 Final Project

This document serves as a reflection on the use of AI tools in the CMPS 357 Final Project. It outlines the context in which the tool was used, the components of the project that benefited from its output, how the output was reviewed and verified, and what aspects worked well versus what required iteration or manual implementation.


## Project Proposal Brainstorming Session

### Session Summary
The session used **ChatGPT** to evaluate extension ideas for the RiskRadar project and identify the most feasible, high-impact final-project direction. The tool produced candidate extensions, compared their difficulty/fit, and then refined the result into a recommended architecture centered on a personalized environmental risk scoring engine.

### (1) Tool Used
- **Tool name:** ChatGPT

### (2) Components That Benefited
- **Project scoping and ideation:** Generated multiple extension options aligned with course requirements.
- **Feasibility analysis:** Compared options by implementation difficulty and compatibility with the existing RiskRadar codebase.
- **Architecture planning:** Proposed a system architecture diagram showing how a new risk engine layer fits between database and API.
- **Repository planning:** Identified likely new/updated backend and frontend files (risk engine modules, API route, schema, model updates, migration, and UI screen).

### (3) How Output Was Reviewed/Verified
- The recommendations were reviewed against the repository structure (existing scrapers, APIs, DB models, scheduler, and mobile app directories) to confirm technical fit.
- Suggested files and modules were checked for consistency with current naming/layout patterns in the codebase.
- The proposal was validated against assignment constraints (meaningful complexity beyond CRUD, architectural thinking, and full-stack impact).
- Meeting with the professor to discuss the proposed extension and receive feedback on its suitability and scope for the final project.

### (4) What Worked, What Needed Iteration, What Required Manual Implementation
- **Worked immediately:** High-level brainstorming and generation of several viable extension concepts; initial mapping to project requirements.
- **Required multiple iterations / improvement:** Narrowing from several ideas to one best-fit extension and refining architecture/file-level scope to match the exact repository context.
- **Required manual implementation:** Actual coding, database migration authoring/testing, endpoint integration, UI construction, and runtime verification (tests, debugging, and deployment checks) remained developer tasks.
