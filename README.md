📋 Overview
Supply Chain Risk Monitor transforms supply chain disruption response from a days-long manual process into a 15-30 second automated analysis powered by AI agents. The system uses Google Gemini AI to coordinate six specialized agents that analyze incidents, identify affected suppliers, calculate risks, recommend alternatives, and generate complete incident response playbooks.
Key Stats:

⚡ 95% faster analysis time (days → seconds)
🤖 6 AI agents working collaboratively
📊 Quantified risk scores (0-100 scale)
💰 ROI tracking with financial impact estimates
🌍 Multi-tier supplier dependency tracking


🎯 Problem & Solution
The Problem

Global supply chain disruptions cost businesses $184B annually
Traditional risk assessment takes 2-5 days
93% of companies experienced disruptions in 2023
Manual analysis can't keep pace with modern supply chains

Our Solution
An intelligent platform that:

✅ Analyzes incidents in 15-30 seconds using AI
✅ Identifies affected suppliers across multiple tiers
✅ Calculates quantified risk scores (0-100)
✅ Recommends ranked alternative suppliers
✅ Generates actionable incident response playbooks
✅ Predicts future risks (30/60/90 days)


🏗️ Architecture
Multi-Agent System
User Input → [Event Parser] → [Supplier Matcher] → [Risk Analyzer]
                                                          ↓
             [Playbook Generator] ← [Recommendation Generator]
6 Specialized AI Agents:
AgentFunctionAI UsageEvent ParserUnderstands incident contextHigh (Gemini)Supplier MatcherIdentifies affected suppliersLogic-basedRisk AnalyzerCalculates impact scoresMedium (Gemini summary)Recommendation GeneratorFinds alternativesHigh (Gemini)Playbook GeneratorCreates action plansLogic-basedFuture Risk PredictorForecasts risksMedium (Gemini)
Tech Stack
Frontend:

React 18.2 + Vite 5.0
Tailwind CSS 3.3
TanStack Query (React Query)
Axios + React Router

Backend:

FastAPI 0.104 (Python 3.11+)
SQLAlchemy 2.0 ORM
SQLite/PostgreSQL
LangChain 0.1

AI/ML:

Google Gemini 2.5 Flash
Multi-agent orchestration
Natural language processing

