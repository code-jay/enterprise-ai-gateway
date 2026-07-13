
# Enterprise AI Gateway

> A production-ready Enterprise AI Gateway that provides a unified interface for multiple Large Language Model (LLM) providers with intelligent model routing, recommendation, telemetry, cost tracking, and governance.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# Overview

Enterprise AI applications rarely use a single LLM.

Different workloads require different models based on:

- Response Quality
- Latency
- Cost
- Context Window
- Privacy
- Provider Availability
- Enterprise Policies

Instead of hardcoding applications to one provider, this project introduces an **Enterprise AI Gateway** that intelligently recommends and routes requests to the most appropriate model.

Think of it as an **API Gateway for LLMs**.

---

# Current Features

## Multi-Provider Architecture

Supports multiple providers through a common abstraction.

- OpenAI
- Anthropic Claude (Coming Soon)
- Google Gemini (Coming Soon)
- Ollama (Coming Soon)
- Azure OpenAI (Planned)

---

## Recommendation Engine

Automatically recommends the best model based on:

- Task
- Context Length
- Budget
- Privacy
- Response Speed
- Required Capabilities

Example:

```
Task: Chat

↓

Budget: Low

↓

Need Fast Response

↓

Recommended Model:

GPT-4o Mini
```

---

## Rule Engine

Filters unsupported models before scoring.

Example:

- Context exceeds model limit
- Vision not supported
- Privacy policy violation
- Provider unavailable

---

## Scoring Engine

Uses weighted scoring.

| Criterion | Weight |
|-----------|---------|
| Task | 30% |
| Quality | 20% |
| Speed | 15% |
| Cost | 15% |
| Privacy | 10% |
| Context | 5% |
| Capability | 5% |

---

## Provider Abstraction Layer

Applications never communicate directly with providers.

```
Application

↓

Gateway

↓

Provider

↓

OpenAI
Claude
Gemini
Ollama
```

---

## Unified API

Every provider returns the same response format.

```json
{
    "provider":"openai",
    "model":"gpt-4o-mini",
    "content":"Hello!",
    "input_tokens":20,
    "output_tokens":50,
    "latency_ms":430
}
```

---

## Explainable Recommendations

Instead of returning only the selected model:

```json
{
  "recommended_model":"gpt-4o-mini",
  "score":91.4,
  "reason":[
      "Fast",
      "Low Cost",
      "Supports Chat"
  ]
}
```

---

## Enterprise Ready

- Configuration Driven
- Strong Typing
- Pydantic Validation
- Provider Factory
- Dependency Injection
- Layered Architecture
- Unit Tests

---

# Project Architecture

```
                        Client
                           │
                           ▼
                 FastAPI REST API
                           │
                           ▼
                  Gateway Service
                           │
                           ▼
                    Model Router
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
 Recommendation Engine            Provider Selector
            │                             │
            ▼                             ▼
      Scoring Engine               Provider Factory
            │                             │
            ▼                             ▼
      Model Catalog             OpenAI / Claude /
                                Gemini / Ollama
```

---

# Project Structure

```
enterprise-ai-gateway/

app/

├── api/
│   └── v1/
│
├── core/
│   ├── gateway/
│   ├── recommendation/
│   └── router/
│
├── providers/
│
├── domain/
│   ├── contracts/
│   ├── enums/
│   └── models/
│
├── telemetry/
│
├── services/
│
├── config/
│
├── utils/
│
└── tests/
```

---

# Technology Stack

- Python 3.13
- FastAPI
- Pydantic v2
- AsyncIO
- Pytest
- OpenAI SDK
- Uvicorn

Future

- Redis
- PostgreSQL
- Prometheus
- Grafana
- Docker
- Kubernetes

---

# Getting Started

## Clone

```bash
git clone https://github.com/<username>/enterprise-ai-gateway.git

cd enterprise-ai-gateway
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Mac/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create

```
.env
```

Example

```env
APP_NAME=Enterprise AI Gateway

APP_VERSION=1.0.0

APP_ENV=development

API_PREFIX=/api

API_VERSION=v1

OPENAI_API_KEY=xxxxxxxx

DEFAULT_PROVIDER=openai

DEFAULT_MODEL=gpt-4o-mini
```

---

## Run

```bash
uvicorn app.main:app --reload
```

Swagger

```
http://localhost:8000/docs
```

---

# API Endpoints

## Health

```
GET /

GET /health
```

---

## Recommendation

```
POST

/api/v1/recommendations
```

Example Request

```json
{
    "task":"chat",
    "context_length":12000,
    "budget":"low",
    "privacy":"public",
    "response_speed":"fast"
}
```

Example Response

```json
{
    "provider":"openai",
    "model":"gpt-4o-mini",
    "score":91.4,
    "alternatives":[
        "gemini-pro",
        "claude-sonnet"
    ]
}
```

---

## Chat (Coming Next)

```
POST

/api/v1/chat
```

The gateway will

- Recommend Model
- Route Request
- Call Provider
- Return Response

---

# Testing

Run all tests

```bash
pytest
```

Run coverage

```bash
pytest --cov=app
```

---

# Current Development Progress

## Completed

- Configuration Management
- Health API
- Domain Models
- Request / Response Contracts
- Provider Abstraction Layer
- Mock Provider
- OpenAI Provider
- Provider Factory
- Model Catalog
- Recommendation Engine
- Rule Engine
- Scoring Engine
- Recommendation API
- Gateway Service

---

## In Progress

- Model Router
- Intelligent Routing
- Chat Endpoint
- Provider Failover
- Streaming Responses

---

## Planned

- Claude Provider
- Gemini Provider
- Ollama Provider
- Azure OpenAI
- Telemetry Dashboard
- Rate Limiting
- Authentication
- API Keys
- Multi-Tenant Support
- Prompt Templates
- Semantic Cache
- Redis
- PostgreSQL
- Docker
- Kubernetes
- Grafana
- Prometheus
- OpenTelemetry
- Admin Dashboard

---

# Enterprise Roadmap

## Phase 1

Gateway Foundation

- FastAPI
- Providers
- Recommendation Engine

---

## Phase 2

Enterprise Routing

- Intelligent Routing
- Provider Failover
- Retry Policies

---

## Phase 3

Enterprise Telemetry

- Request Logging
- Cost Tracking
- Token Tracking
- Latency Dashboard

---

## Phase 4

Enterprise Governance

- RBAC
- API Keys
- Multi-Tenant
- Audit Logs
- Rate Limiting

---

## Phase 5

Enterprise Platform

- Admin UI
- Analytics
- Monitoring
- Billing
- Usage Reports

---

# Why this Project?

This project demonstrates production-grade Enterprise AI Architecture patterns including:

- Clean Architecture
- Domain Driven Design
- Strategy Pattern
- Factory Pattern
- Dependency Injection
- Provider Abstraction
- Enterprise Routing
- Explainable AI Recommendations
- Observability
- Governance

The goal is to provide a reference implementation for building scalable, maintainable, and vendor-neutral AI platforms.

---

# Author

**Jay Ram Singh**

Enterprise AI Architect (Learning Journey)

18+ years in Software Engineering, Technical Leadership, and Enterprise Solutions.

Currently building enterprise-grade AI systems focused on:

- AI Gateways
- RAG Platforms
- LLM Infrastructure
- Multi-Agent Systems
- Enterprise AI Architecture

LinkedIn: https://linkedin.com/in/jayram

GitHub: https://github.com/code-jay

---

# License

MIT License
<!--
Configuration and application bootstrap
Health API
Domain enums and request/response contracts
Provider abstraction
OpenAI provider
Provider factory
Model catalog
Recommendation and scoring engine
Router
Gateway orchestration
Telemetry and request logging
Retry and fallback
Security and guardrails
Redis cache and persistence
Tests and Docker
-->