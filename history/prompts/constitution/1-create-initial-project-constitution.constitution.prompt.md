---
id: 1
title: Create initial project constitution
stage: constitution
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: unknown
command: /sp.constitution
labels: ["constitution", "project", "initial"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Create and publish an AI-powered textbook using Docusaurus for web and GitHub Pages deployment, developed with Spec-Kit Plus and Claude Code.

The book will focus on Physical AI & Humanoid Robotics, combining theory, implementation, code samples, and real-world applications for students and developers with a Computer Science background.

Core Principles

Accuracy: All technical concepts must be correct and verified using primary and reliable sources.

Clarity: Content must be understandable for university-level students in Computer Science, Robotics, or AI.

Reproducibility: Every claim and example must be traceable, testable, and verifiable.

Practicality: Include hands-on examples, diagrams, and code blocks where necessary.

AI-Enhanced: Claude Code will assist in drafting but human review is mandatory.

Open Knowledge: The book should be aligned with open-source and educational values.

Key Standards

All factual and technical claims must include citations.

APA citation format is required.

At least 50% of references must be peer-reviewed (journals, academic papers, research articles).

Include:

Diagrams (ASCII or Mermaid.js where possible)

Code examples

Use-cases

Algorithms

Writing level: Flesch-Kincaid Grade 10–12

Content must be suitable for:

University students

AI & Robotics beginners and intermediate learners

Technical practitioners

Structural Requirements

The textbook must contain:

Introduction to Physical AI

Fundamentals of Humanoid Robotics

History & Evolution of Robotics

Sensors & Actuators in Humanoids

Kinematics & Dynamics

Perception Systems (Vision, LIDAR, etc.)

Control Systems

Machine Learning in Robotics

Reinforcement Learning for Movement

Human-Robot Interaction

Path Planning & Navigation

Simulation Tools (ROS / Gazebo / PyBullet)

Ethics & Safety

Current Research & Case Studies

Future of Physical AI

All chapters must be modular and compatible with Docusaurus MD/MDX format.

Constraints

Total Word Count: 5,000 – 7,000 words

Minimum Sources: 15 academic/reliable sources

Platform: Docusaurus + GitHub Pages deployment

Output format:

Primary: Markdown (MD/MDX)

Secondary export: PDF with embedded citations

Success Criteria

✅ All claims verified and cited

✅ 0% plagiarism (must pass plagiarism checks)

✅ Compatible with Docusaurus structure

✅ Clean, structured, and modular format

✅ Successfully deployable to GitHub Pages

✅ Passes technical and academic review

## Response snapshot

Updated the project constitution based on the user input.

## Outcome

- ✅ Impact: The project now has an initial constitution.
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: Update templates to align with constitution.
- 🧠 Reflection: The template had a typo in the PRINCIPLE_DESCRIPTION placeholder.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none