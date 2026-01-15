# CA1 - Exam Viewer - Rubric

The following rubric will be used to grade your exam viewer application. In particular, you are encouraged to explore different technologies and push the boundaries of the basic requirements.

## Summary of Weighting

| Category | Weighting |
| :--- | :--- |
| [Functionality & Features](#functionality--features-40) | 30% |
| [Technical Implementation](#technical-implementation-30) | 20% |
| [User Interface & Experience (UI/UX)](#user-interface--experience-uiux-20) | 20% |
| [Innovation & Extension](#innovation--extension-10) | 30% |

---

## Detailed Criteria

### Functionality & Features (30%)

*Evaluates the core capabilities of the dashboard as a tool for exam preparation.*

| Level | Description |
| :--- | :--- |
| **Excellent (70-100%)** | Comprehensive search and filtering system. Advanced filters (topic, keyword, difficulty, etc.) work flawlessly. Shows detailed question information and metadata (e.g., year, mark breakdown). User intent is accurately reflected in results. |
| **Good (60-69%)** | Effective search and filtering for most common fields (topic, year). Filtering is reliable. Basic metadata is shown for each question. |
| **Satisfactory (40-59%)** | Basic search functionality. At least one type of filter (e.g., by topic) works. Displays matching questions but may lack detailed metadata. |
| **Needs Improvement (0-39%)** | Search or filtering is broken or non-existent. Minimal information displayed for questions. System is difficult to use for its intended purpose. |

### Technical Implementation (20%)

*Evaluates the robustness and efficiency of the code, specifically dashboard integration and PDF parsing.*

| Level | Description |
| :--- | :--- |
| **Excellent (70-100%)** | Highly efficient and accurate PDF parsing (e.g., using PyMuPDF) with robust handling of different layouts. Seamless integration with the dashboard framework (Streamlit, Gradio, etc.). Code is well-structured, modular, and optimized. |
| **Good (60-69%)** | Accurate PDF parsing for standard layouts. Smooth interaction between the parsing logic and the UI. Code is clean and readable. |
| **Satisfactory (40-59%)** | Basic PDF parsing works but may struggle with images or complex formatting. UI updates correctly but might have minor performance issues. Functional but less organized code. |
| **Needs Improvement (0-39%)** | Major issues with PDF parsing (missing text, incorrect mapping). UI is sluggish or frequently crashes. Poor code structure. |

### User Interface & Experience (UI/UX) (20%)

*Evaluates the design, aesthetics, and ease of use.*

| Level | Description |
| :--- | :--- |
| **Excellent (70-100%)** | Professional, modern, and aesthetically pleasing interface. Highly intuitive navigation. Layout is optimized for data exploration. Subtle micro-interactions enhance the experience. |
| **Good (60-69%)** | Clean and organized layout. Clear labeling and easy-to-use controls. Consistent design language throughout. |
| **Satisfactory (40-59%)** | Functional interface but lacks polish. Layout is usable but might be cluttered. Colors and typography are basic. |
| **Needs Improvement (0-39%)** | Confusing or broken layout. Interaction is difficult (e.g., non-responsive buttons). Poor visual hierarchy makes data hard to read. |

### Innovation & Extension (30%)

*Evaluates extra effort and creative additions beyond the basic brief.*

| Level | Description |
| :--- | :--- |
| **Excellent (70-100%)** | Significant extensions such as: AI-powered question classification, performance tracking, export features (e.g., customized practice sets), or exceptionally creative UI solutions. |
| **Good (60-69%)** | Useful extra features like a "favorites" system, better-than-required metadata extraction, or unique visualization of exam trends. |
| **Satisfactory (40-59%)** | A few small additions that go slightly beyond the minimum requirements (e.g., very thorough topic tagging). |
| **Needs Improvement (0-39%)** | Only implements the minimum requirements with no attempt to explore beyond the provided examples. |
