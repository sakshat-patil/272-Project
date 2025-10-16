# 272-Project

##1. AgentMirror – A Real-Time Security Framework for Autonomous AI Agents
Project Summary: AgentMirror is a sophisticated security layer designed to ensure the safe operation of autonomous AI agents. It functions like a "conscience" for the AI, using a dual-agent architecture. Before an autonomous agent can perform any action in a live environment, its proposed action is intercepted and reviewed by a specialized "mirror" agent. This validation process ensures that the agent's behavior aligns with predefined safety protocols and ethical guidelines, effectively preventing unintended or malicious outcomes.

Key Features:

Dual-Agent Validation: A primary operational agent is supervised by a secondary validation agent, creating a system of checks and balances.

Hybrid Rules Engine: It combines a deterministic rules engine for straightforward, known-safe operations (e.g., "never delete a production database") with a more flexible Voyage AI-powered reasoning model.

Contextual Safety Analysis: The reasoning model analyzes nuanced situations where a simple rule isn't sufficient, assessing the context and potential consequences of an action.

Real-Time Threat Prevention: The framework is built to operate in real time, preventing prompt injection attacks, sensitive data leaks, and other harmful behaviors before they can be executed.

Tech Stack:

Reasoning: Voyage AI

Orchestration: A custom deterministic rules engine.

Core Logic: Python

Problem It Solves: As AI agents become more autonomous, the risk of them causing unintentional harm, leaking private data, or being manipulated by bad actors increases significantly. AgentMirror addresses the lack of a real-time safety net for these autonomous systems.

Target Audience: Developers, DevOps engineers, and organizations deploying autonomous AI agents in business-critical or public-facing applications where safety and reliability are paramount.

2. VidQuery – Interactive Video Question-Answering Platform
Project Summary: VidQuery is an intelligent video platform that transforms passive video consumption into an interactive Q&A session. Users can upload a video or link to one and ask specific, natural language questions about its content. The system analyzes both the visual frames and the audio transcript to provide precise, grounded answers. For example, a user could ask, "What was the key formula mentioned in the lecture?" or "Show me the part where the chef adds basil," and VidQuery would pinpoint the exact moment.

Key Features:

Natural Language Interaction: Users can query video content conversationally without needing to manually scrub through the timeline.

Multimodal Analysis: It integrates multimodal embeddings from Voyage AI to understand the visuals and uses Whisper to create an accurate, searchable transcript of the audio.

Fine-Grained Retrieval: The system can locate information with high precision, often linking directly to the relevant timestamp or video clip.

Context-Aware Answers: VidQuery doesn't just find keywords; it understands the context of the question to provide more relevant and accurate responses.

Tech Stack:

Embeddings: Voyage AI

Speech-to-Text: OpenAI's Whisper

ML Framework: PyTorch

Backend: Python, FastAPI

Problem It Solves: Videos contain vast amounts of information, but searching for specific details is incredibly tedious and inefficient. VidQuery solves this by making video content as easily searchable as a text document.

Target Audience: Students watching lectures, professionals reviewing training modules, researchers analyzing video data, and content creators looking to make their material more accessible.

3. AI-Powered Visual Support for Dementia Patients
Project Summary: This project is a compassionate AI assistant designed to support the cognitive needs of individuals with dementia. The system uses a visual interface (ideally smart glasses, but an MVP could use a laptop screen) to provide real-time memory cues and routine reminders. By accessing a secure, private database of the user's personal information—such as family members' names, photos, and daily schedules—the AI can generate gentle, empathetic prompts. For example, if the user looks at their daughter, the device could display "This is your daughter, Sarah."

Key Features:

Personalized Memory Retrieval: Uses Voyage AI's retrieval capabilities to pull relevant information from a MongoDB database containing personal photos, notes, and relationship graphs.

Empathetic Response Generation: An LLM reasoning layer is engineered to craft responses that are familiar, comforting, and emotionally supportive.

Privacy and Safety First: The architecture is designed as a closed loop to ensure sensitive personal data is never exposed externally.

Passive Visual Interface: Information is projected onto a screen or glasses, providing support without requiring complex interaction from the user.

Tech Stack:

Retrieval: Voyage AI

Database: MongoDB

Reasoning: LLM (e.g., OpenAI API, Llama)

Hardware: Meta Glasses (for final product), Laptop/Tablet screen (for MVP)

Problem It Solves: Dementia causes significant memory loss and confusion, which can lead to distress and a reduced quality of life. This tool aims to alleviate that burden by providing a constant, gentle source of memory support, empowering patients to maintain independence and connection.

Target Audience: Individuals with early-to-mid-stage dementia, their families, and in-home caregivers.
