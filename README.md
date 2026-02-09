Student Internship Path Optimizer
Overview

Finding the right path to secure an internship can feel overwhelming. Students often hear the same advice over and over:

Join clubs

Attend workshops

Fix your CV

Apply on LinkedIn daily

But every student is different. What works for a social student may feel impossible for a shy student. There is no single “magic path.”

Our project helps students follow a personalized, efficient path toward internships, taking into account their personality, skills, and preferences.

Problem Statement

Goal: Identify the most effective sequence of actions a student at TBS should take during their 4-year journey to maximize their chance of getting an internship while matching their personality.

Challenges:

Students have different personalities and energy levels.

Actions like networking or attending workshops vary in difficulty and value for each student.

Real-life journeys are not linear — students may skip steps, take shortcuts, or do multiple actions simultaneously.

Approach
1. Modeling the Student Journey

We modeled the journey as a network graph:

Nodes: Actions students can take (e.g., join a club, update CV, attend a career fair).

Edges: Connections between actions.

Weights for each node were calculated from survey data:

Difficulty: How hard the action is for a student personally.

Value: How much the action helps in securing an internship.

Weight: Difficulty ÷ Value (higher ROI = better action).

2. Personality Types

Students were grouped into three types:

Shy: Prefer low-pressure actions

Neutral: Balanced approach

Social: Comfortable with networking

Optimal paths are personalized for each personality type.

3. Graph Structure

The graph is layered into four stages:

Learning Activities — skills, courses, workshops

Profile Building — CV, LinkedIn, clubs

Application Methods — career fairs, job platforms, alumni networking

Interview & Final Steps — interviews and offer negotiation

We added shortcuts (skip layers) and cross-layer edges (parallel actions) to reflect real-life flexibility.

4. Finding the Optimal Path

We use Dijkstra’s algorithm to find the lowest-weight path from “Student” to “Internship Offer,” producing:

Step-by-step, personalized roadmap

Adaptation to personality type

Efficient, realistic guidance without guesswork

Implementation

Language: Python

Libraries: pandas, networkx, matplotlib (for graph visualization)

Input: Survey data with difficulty, value, personality, and student info

Output: Optimal path per personality type, visualized as a network graph

Features

Personalized internship roadmap for different personalities

Flexible graph structure with shortcuts and cross-layer actions

Data-driven decision-making using real student survey responses
