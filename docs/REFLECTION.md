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


## Reflection Update

### Session Summary
This session used **GitHub Copilot** to see how effective it would be in summarizing the Transcript entries to create a cohesive reflection document. The tool was prompted to extract key information about the AI tool usage, project components that benefited, review/verification processes, and reflections on what worked versus what required iteration or manual implementation.

### (1) Tool Used
- **Tool name:** GitHub Copilot

### (2) Components That Benefited
- **Session Summarization:** Was able to read through the Transcript entries and extract relevant information to create a structured reflection document.
- **Information Extraction:** Identified key points about the AI tool usage, project components that benefited, review/verification processes, and reflections on what worked versus what required iteration or manual implementation.
- **Criteria Meeting:** Constructed its Reflection entry based on the criteria outlined in the course syllabus for what is expected from a transcript reflection
  
### (3) How Output Was Reviewed/Verified
- The response was reviewed for accuracy and completeness by the students working on the project.
- Suggested files and modules were checked for consistency to inform the formatting and contents.

### (4) What Worked, What Needed Iteration, What Required Manual Implementation
- **Worked immediately:** Cohesive summarization of AI tool usage session from Transcript and reflection on the impacts this tool use for the project.
- **Required multiple iterations / improvement:** Reviewing the output for accuracy and completeness and making edits to ensure it met the criteria outlined in the course syllabus for a transcript reflection.
- **Required manual implementation:** Small Editing adjustments to reflect the required criteria and ensure the reflection was comprehensive and well-structured.


---

## STAGES.md Construction Session

### Session Summary
This session used **GitHub Copilot** to build and refine project-planning documentation by updating `docs/STAGES.md` to match `INSTRUCTIONS.md` requirements and `EXAMPLE_STAGES.md` formatting, then synchronizing related tracking content in `README.md`. The interaction included iterative edits: creating a full stage roadmap, replacing placeholders, adding a stage-status table and legend, and aligning status vocabulary across files.

### (1) Tool Used
- **Tool name:** GitHub Copilot

### (2) Components That Benefited
- **Documentation structure and quality:** `docs/STAGES.md` was rewritten into a professional, stage-based format with clear objectives, tasks, verification checklists, deliverables, and progress sections.
- **Requirements alignment:** Stage content was mapped directly to project expectations in `docs/INSTRUCTIONS.md`.
- **Repository consistency:** `README.md` and `docs/STAGES.md` were aligned using shared status terms (`Not Started`, `In Progress`, `Completed`) and a consistent legend.
- **Project tracking clarity:** A current stage status table and synchronized legend improved progress visibility and update discipline.

### (3) How Output Was Reviewed/Verified
- Copilot outputs were reviewed against source documents (`docs/INSTRUCTIONS.md`, `EXAMPLE_STAGES.md`) to verify completeness and formatting consistency.
- The updated `README.md` and `docs/STAGES.md` were compared to confirm synchronized terminology and matching status values.
- Verification was iterative: after each change request (placeholder replacement, table addition, legend addition, synchronization), the resulting documents were checked and then refined.

### (4) What Worked, What Needed Iteration, What Required Manual Implementation
- **Worked immediately:** Rapid drafting/reformatting of `docs/STAGES.md` into a complete, structured roadmap and quick insertion of requested `README.md` elements.
- **Required multiple iterations / improvement:** Cross-file consistency required multiple passes (adding legend, then synchronizing status language between files).
- **Required manual implementation:** Final human decisions on wording, stage status accuracy, and ongoing maintenance of progress updates remained manual responsibilities.


## Follow-Up Reflection: REFLECTION.md Update Request

### Session Summary
This follow-up request used **GitHub Copilot** to continue documentation continuity by replacing the placeholder section in `docs/REFLECTION.md` with a formal reflection on the STAGES construction session and adding an additional reflection entry for the current update action.

### (1) Tool Used
- **Tool name:** GitHub Copilot

### (2) Components That Benefited
- **Continuity of AI usage records:** Ensured each major transcript session has a corresponding reflection entry.
- **Documentation completeness:** Removed placeholder text and replaced it with actionable, rubric-aligned content.
- **Standardized reflection format:** Preserved the same four-component structure used in earlier entries.

### (3) How Output Was Reviewed/Verified
- The new reflection content was checked against `docs/TRANSCRIPT.md` (specifically the STAGES construction interaction) to ensure factual alignment.
- The formatting and section order were validated against the existing reflection template in this file for consistency.

### (4) What Worked, What Needed Iteration, What Required Manual Implementation
- **Worked immediately:** Converting the placeholder into complete reflection sections using the established template.
- **Required multiple iterations / improvement:** Minor wording refinement to keep tone, detail level, and structure consistent with prior entries.
- **Required manual implementation:** Final author review for voice/style preferences and future updates as additional AI-assisted sessions are added.

---

## Documentation Continuity and Clarity + Follow-Up Session

### Session Summary
This session used **GitHub Copilot** to complete a documentation continuity pass focused on keeping project records synchronized, accurate, and easy to audit. Building on the transcript’s **Documentation Continuity and Clarity** entry, the work expanded from filling empty docs to full alignment of language, formatting, and grammar across the documentation set, including both root and frontend README files.

### (1) Tool Used
- **Tool name:** GitHub Copilot

### (2) Components That Benefited
- **Project description quality:** `docs/PROJECT_DESCRIPTION.md` was expanded with a complete overview of purpose, architecture direction, goals, and intended outcomes.
- **Current-state technical documentation:** Empty/underdeveloped docs were rewritten to reflect implemented system behavior:
	- `docs/ARCHITECTURE.md`
	- `docs/DATA_MODEL.md`
	- `docs/DATA_SETS.md`
- **Planning-document consistency:** `docs/EXAMPLES.md` and `docs/INSTRUCTIONS.md` were reformatted and normalized to match the style and terminology used across the docs set.
- **Cross-file wording alignment:** `README.md` and `docs/PROJECT_DESCRIPTION.md` were aligned for stage naming, assistant naming, and project-scope language.
- **Grammar and readability cleanup:** Grammar passes were completed for `README.md`, top-level docs in `docs/`, and frontend readmes:
	- `frontend/README.md`
	- `frontend/RiskRadar/README.md`

### (3) How Output Was Reviewed/Verified
- The updates were verified against implemented backend code and configuration (models, scrapers, scheduler, API routes, schemas, settings, and migration notes) to ensure documentation reflected actual runtime behavior rather than planned-only features.
- Terminology and stage names were cross-checked between `README.md`, `docs/INSTRUCTIONS.md`, `docs/STAGES.md`, and `docs/PROJECT_DESCRIPTION.md` to confirm consistency.
- Follow-up searches and file reads were used to confirm typo removal and wording normalization (for example, spelling fixes and consistent use of “RiskRadar AI Assistant” and “24-48 hour”).
- Transcript integrity was preserved by avoiding grammar edits that would alter quoted historical dialogue.

### (4) What Worked, What Needed Iteration, What Required Manual Implementation
- **Worked immediately:** Structured rewriting of empty documents and conversion to a consistent, sectioned format with clear headings, checklists, and examples.
- **Required multiple iterations / improvement:** Cross-file alignment required multiple passes (first technical-content completion, then naming/terminology normalization, then grammar and readability cleanup).
- **Required manual implementation:** Final judgment on wording tone, what to preserve verbatim in transcript records, and how much to standardize legacy narrative sections remained human decisions.

---

## PROJECT_PROPOSAL.md Creation Session

### Session Summary
This session used **GitHub Copilot** to create a new `PROJECT_PROPOSAL.md` file that summarizes the project premise, objectives, and goals using the existing documentation set (`README.md`, `docs/PROJECT_DESCRIPTION.md`, and `docs/STAGES.md`) as source context. The result was a structured proposal document in the repository root aligned with the project’s staged roadmap and course expectations.

### (1) Tool Used
- **Tool name:** GitHub Copilot

### (2) Components That Benefited
- **Proposal documentation:** Added `PROJECT_PROPOSAL.md` as a dedicated, easy-to-reference summary artifact for project premise/objectives/goals.
- **Cross-document synthesis:** Consolidated overlapping content from multiple project docs into one concise proposal format.
- **Stage communication clarity:** Reframed the four-stage plan into proposal language suitable for quick review and reporting.

### (3) How Output Was Reviewed/Verified
- The generated proposal content was checked for consistency with `README.md`, `docs/PROJECT_DESCRIPTION.md`, and `docs/STAGES.md`.
- Stage ordering and scope coverage were verified to ensure all required areas (web extension, scoring/prioritization, map UX, forecasting + assistant) were represented.
- Wording was reviewed to confirm that implemented/in-progress versus planned work was communicated accurately.

### (4) What Worked, What Needed Iteration, What Required Manual Implementation
- **Worked immediately:** Fast conversion of existing project documentation into a clean proposal structure with clear headings and staged goals.
- **Required multiple iterations / improvement:** Minor refinement of phrasing to keep scope language precise and avoid over-claiming completion state.
- **Required manual implementation:** Final human validation of narrative tone, course-fit framing, and whether additional links/references should be added in `README.md`.

---

## Follow-Up Reflection: Reflection Entry Update Command

### Session Summary
This follow-up command used **GitHub Copilot** to append reflection coverage for the proposal-writing session and explicitly document this update action itself. The purpose was to maintain continuity between transcript activity and reflection records by ensuring the latest documentation actions were captured in the same standardized format.

### (1) Tool Used
- **Tool name:** GitHub Copilot

### (2) Components That Benefited
- **Reflection continuity:** Ensured the proposal-creation activity is now represented in `docs/REFLECTION.md`.
- **Auditability:** Improved traceability of AI-assisted actions by pairing the original task and this follow-up update with explicit reflection entries.
- **Template consistency:** Preserved the established four-part reflection structure used throughout the file.

### (3) How Output Was Reviewed/Verified
- The new sections were checked to confirm they match the existing heading hierarchy and formatting style.
- Content was reviewed for factual alignment with the immediately preceding command history (proposal creation, then reflection-update request).
- Terminology was validated for consistency with existing project naming (for example, stage language and RiskRadar feature naming).

### (4) What Worked, What Needed Iteration, What Required Manual Implementation
- **Worked immediately:** Appending a properly structured reflection entry and follow-up entry in one pass.
- **Required multiple iterations / improvement:** Minor wording adjustments may still be needed to match preferred voice/style across older entries.
- **Required manual implementation:** Final editorial review and any instructor-specific phrasing adjustments remain team responsibilities.
