Task: AI-Powered Content SEO Optimization App
Overview
Build a small web application (“SEO Assistant Agent”) that lets authenticated users
interact with an AI-powered agent via a conversational UI to get recommendations for
optimizing page title, content, and meta information for SEO.
The exercise is designed to evaluate your full-stack proficiency (frontend, backend,
database, auth) and your ability to integrate AI services or write basic AI logic.
Functional Requirements
1. Authentication & Multi-User Sessions
o Users must be able to register and log in.
o Each user has their own session history; separate users cannot see each
other’s data.
o Using an external Identity management system is preferred.
2. Conversational UI (Chat Interface)
o A single-page application where users:
• Can enter a message about “page title” and “page content” in the
input area at the bottom of the screen.
• New messages, both user and AI should be appended at the bottom
of a scrollable chat area.
3. AI Agent for SEO Recommendations (Commented [MS1]: imo this should be extended a bit to be more descriptive that we expect to be able to have a
back-and-forth conversation with the agent) 
o Given the provided title & content, the agent should:
• Suggest improvements to title & content (inline or rewritten).
• Make recommendations for title tag and meta description
Non-Functional Requirements
• Front-end and back-end should be different applications.
• The back-end should be RESTful API.
• You should choose the front-end and back-end technologies.
• Use an agentic framework to implement the AI Agent.
• Use a popular LLM that is easily accessible like the models of OpenAI, Anthropic,
etc.
Deliverables
• A Git repository (public or private) containing all source code.
• A README explaining:
o How to install dependencies and start front-end & back-end.
o How to configure the model used.
o What model/models were used and why.
o Provide any configuration and credentials for third party used.
o The app should be runnable at our side.
o Any assumptions or shortcuts taken.
• (Optional) Deployed demo link.