# Architectural Plan: Physical AI & Humanoid Robotics - Embodied Intelligence in the Real World

## 1. Scope and Dependencies

### 1.1 In Scope:

*   Creation of a technical textbook for students of Computer Science, AI, and Robotics.
*   Content covering Physical AI, ROS 2, Gazebo, Unity, NVIDIA Isaac, and Vision-Language-Action.
*   Deployment of the book as a Docusaurus website on GitHub Pages.
*   Generation of a PDF version of the book with APA-style citations.

### 1.2 Out of Scope:

*   Development of actual robotic hardware.
*   In-depth coverage of specific AI algorithms beyond their application in robotics.
*   Maintenance of the deployed website beyond the initial deployment.
*   Translation of the book into other languages.

### 1.3 External Dependencies:

*   GitHub: For repository hosting and GitHub Pages deployment.
*   Docusaurus: For website generation.
*   Node.js: For running Docusaurus.
*   Citation management tools: To ensure proper formatting of academic citation.
*   Claude Code + Spec-Kit: For content generation and structure.

## 2. Key Decisions and Rationale

### 2.1 Docusaurus for Website Generation:

*   Options Considered: Jekyll, Hugo, GitBook, Docusaurus
*   Trade-offs: Docusaurus provides excellent documentation support, MDX support, and GitHub Pages integration. Other options lack some of these features.
*   Rationale: Docusaurus is well-suited for creating technical documentation and integrates seamlessly with GitHub Pages.

### 2.2 MDX for Content Creation:

*   Options Considered: Markdown, HTML, MDX
*   Trade-offs: MDX allows embedding React components within Markdown, enabling interactive examples and diagrams. Other options are limited to static content.
*   Rationale: MDX enhances the textbook with interactive elements, improving the learning experience.

### 2.3 GitHub Pages for Deployment:

*   Options Considered: Netlify, Vercel, AWS S3, GitHub Pages
*   Trade-offs: GitHub Pages offers simplicity and free hosting for static websites. Other options may provide more advanced features but require additional configuration.
*   Rationale: GitHub Pages simplifies deployment and provides a cost-effective solution.

### 2.4 Versioning Strategy:

*   Approach: Semantic Versioning (SemVer) for the book's content and structure.

### 2.5 Principles:

*   Measurable: Use automated tests to verify the Docusaurus build and link integrity.
*   Reversible: Store all content in Git, allowing easy rollback to previous versions.
*   Smallest Viable Change: Implement changes in small, incremental steps.

## 3. Interfaces and API Contracts

### 3.1 Public APIs:

*   N/A: This project does not involve creating public APIs.

### 3.2 Versioning Strategy:

*   N/A: No APIs are involved.

### 3.3 Idempotency, Timeouts, Retries:

*   N/A: Not applicable to a documentation project.

### 3.4 Error Taxonomy with status codes:

*   N/A: Not applicable to a documentation project.

## 4. Non-Functional Requirements (NFRs) and Budgets

### 4.1 Performance:

*   p95 latency: Website should load in under 3 seconds.
*   Throughput: Support at least 100 concurrent users.
*   Resource Caps: Minimize the use of large images or videos to reduce bandwidth consumption.

### 4.2 Reliability:

*   SLOs: GitHub Pages uptime SLO.
*   Error budgets: Minimize broken links and build errors.
*   Degradation strategy: Provide a static PDF version of the book if the website is unavailable.

### 4.3 Security:

*   AuthN/AuthZ: N/A, since contents are public
*   Data handling: Ensure any included code or examples are free from vulnerabilities
*   Secrets: No secrets should be stored in the codebase.
*   Auditing: Monitor website traffic and error logs.

### 4.4 Cost:

*   Unit economics: Utilize free hosting and open-source tools to minimize costs.

## 5. Data Management and Migration

### 5.1 Source of Truth:

*   Git repository will be the source of truth for all content.

### 5.2 Schema Evolution:

*   N/A: No database involved.

### 5.3 Migration and Rollback:

*   Use Git for version control, enabling easy rollback to previous versions.

### 5.4 Data Retention:

*   Retain all content and history in the Git repository.

## 6. Operational Readiness

### 6.1 Observability:

*   Logs: Monitor Docusaurus build logs and GitHub Pages traffic.
*   Metrics: Track website traffic using GitHub Pages analytics.
*   Traces: N/A

### 6.2 Alerting:

*   Set up alerts for broken links and build failures.

### 6.3 Runbooks for common tasks:

*   Document the process for updating content, generating the PDF, and deploying the website.

### 6.4 Deployment and Rollback strategies:

*   Use GitHub Actions for automated deployment to GitHub Pages. Rollback by reverting commits in Git.

### 6.5 Feature Flags and compatibility:

*   N/A: Not applicable to a documentation project.

## 7. Risk Analysis and Mitigation

### 7.1 Top 3 Risks:

*   Content Accuracy: Ensure all technical information is correct and up-to-date. Mitigation: Peer review, citation of sources.
*   Website Availability: GitHub Pages may experience downtime. Mitigation: Provide a static PDF version of the book.
*   Build Failures: Docusaurus build process may fail due to configuration issues or dependency conflicts. Mitigation: Implement automated tests and monitor build logs.

## 8. Evaluation and Validation

### 8.1 Definition of Done (tests, scans):

*   Automated tests to verify Docusaurus build success.
*   Link checker to identify broken links.
*   Manual review of content for accuracy and clarity.

### 8.2 Output Validation for format/requirements/safety:

*   Verify that the Docusaurus website renders correctly.
*   Ensure the PDF version is generated successfully and contains all content.
*   Check that all citations are properly formatted.

## 9. Architectural Decision Record (ADR)

*   For each significant decision, create an ADR and link it.

📋 Architectural decision detected: Use Docusaurus for website generation — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`

📋 Architectural decision detected: Use MDX for content creation — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`

📋 Architectural decision detected: Use GitHub Pages for deployment — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`
