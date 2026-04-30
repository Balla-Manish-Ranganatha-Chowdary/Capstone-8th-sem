# India Earth-Observation Intelligence System

A full-stack geospatial intelligence platform for environmental risk assessment over the Indian subcontinent. The system ingests multispectral satellite imagery from ISRO constellations, runs land-cover segmentation through a fine-tuned NASA-IBM Prithvi-100M geospatial foundation model, and surfaces actionable flood, heat stress, and land degradation risk narratives through a DPO-aligned large language model — all accessible via an interactive web dashboard.

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Key Capabilities](#key-capabilities)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [API Reference](#api-reference)
- [Model Details](#model-details)
- [License](#license)

---

## Overview

Traditional disaster management in India relies on static hazard maps and manual interpretation of satellite imagery — workflows that cannot scale to the petabyte-level data streams produced by constellations like ISRO Resourcesat-2A and Cartosat. This platform addresses that gap by combining:

- **NASA-IBM Prithvi-100M** — a Vision Transformer pre-trained on 4.2 million global HLS time-series tiles, fine-tuned here as a four-class land-cover segmentation backbone using ISRO multispectral input (Green, Red, NIR, SWIR).
- **A DPO-aligned LLM** — a preference-optimized large language model grounded in satellite-derived physical quantities through a structured Geospatial Awareness Layer (GAL), which prevents hallucination by anchoring all reasoning to numerically verified perception scripts.
- **A Next.js web dashboard** — a responsive, map-first interface exposing geographic targeting, temporal bounding, environmental analysis, and a persistent conversational analyst.

No foundation model is trained from scratch. Prithvi-100M is used as a frozen pre-trained backbone; only the segmentation head and DPO alignment layers are fine-tuned for the Indian environmental context.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  SATELLITE DATA ACQUISITION                      │
│         ISRO Resourcesat-2A (LISS-3 / AWiFS)  +  Cartosat       │
│              Green · Red · NIR · SWIR bands                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              NASA-IBM PRITHVI-100M VISION ENCODER                │
│   Pre-trained ViT · Frozen backbone · Fine-tuned seg. head       │
│   Output: 4-class pixel mask                                     │
│   Classes: Vegetation · Water Bodies · Built-up · Barren Land    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              GEOSPATIAL AWARENESS LAYER  (GAL)                   │
│   Perception Script  S(R,T) = (L, M, H, E)                      │
│   L: land-cover fractions · M: LULC transition matrix            │
│   H: NDWI / SWIR moisture indices · E: exposure proxies          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DPO-ALIGNED LLM                                 │
│   Neuro-symbolic verification · Evidence-grounded narratives     │
│   Output: Low / Medium / High risk + natural-language report     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  NEXT.JS WEB DASHBOARD                           │
│   Interactive map · Temporal bounding · Chat analyst overlay     │
└─────────────────────────────────────────────────────────────────┘
```

### Repository Structure

```
india-eo-intelligence/
├── backend/
│   ├── main.py               # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   ├── prithvi/              # Prithvi-100M fine-tuning and inference
│   │   ├── model.py          # ViT encoder + segmentation head
│   │   ├── inference.py      # Perception script generation (GAL)
│   │   └── weights/          # Fine-tuned checkpoint (not tracked)
│   └── llm/                  # DPO-aligned LLM interface
│       ├── client.py         # API client for LLM inference
│       └── context.py        # Recursive context manager
├── nextjs-ui/                # Next.js 14 frontend
│   ├── app/
│   │   ├── api/
│   │   │   ├── analyze/      # Mock → real backend contract
│   │   │   └── chat/         # Mock → real backend contract
│   │   └── page.tsx
│   └── components/
├── .env                      # GEMINI_API_KEY and config
└── README.md
```

---

## Key Capabilities

### Geographic Targeting
Interactive fly-to mapping of India using CartoDB Dark Matter tiles via React Leaflet. Users can select any of the 28 states and 8 union territories or drop a custom coordinate pin anywhere on the subcontinent.

### Temporal Bounding
Precise filtering of historical satellite data spanning 2019 through 2024, enabling multi-year land-cover change analysis and trend detection.

### Environmental Analysis
- Percentage shifts in vegetation cover, water body extent, and urban built-up area computed from Prithvi-100M segmentation masks.
- Automated three-tier risk assessment (Low / Medium / High) for flood risk, heat stress, and land degradation, grounded in SWIR moisture indices and LULC transition matrices.
- Tabbed preventive action checklists — immediate, medium-term, and long-term — generated by the DPO-aligned LLM based on the region's physical risk profile.

### Conversational Intelligence
A persistent, context-aware analyst chat interface that answers ad-hoc queries about the selected geographic region and time window. The LLM operates under strict location and time-range context locks enforced by the GAL perception script, preventing it from reasoning outside the bounds of the current satellite observation.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Vision Encoder | NASA-IBM Prithvi-100M (ViT, HLS pre-trained) |
| Segmentation Head | Fine-tuned linear decoder (4-class) |
| LLM | DPO-aligned open-weight model (Gemini API) |
| Backend Framework | FastAPI (Python) |
| Frontend Framework | Next.js 14, React 18 |
| Styling | Tailwind CSS |
| Animations | Framer Motion |
| Maps | React Leaflet + CartoDB Dark Matter |
| Satellite Input | ISRO Resourcesat-2A (LISS-3, AWiFS), Cartosat |
| Reference Dataset | Harmonized Landsat Sentinel-2 (HLS) |

---

## Installation

> **Critical:** All backend commands must be run from the **project root directory** (`india-eo-intelligence/`), not from inside the `backend/` folder. Python resolves imports as `from backend.model import ...` relative to the root.

### Prerequisites

- Python 3.10 or higher
- Node.js v18 or higher
- npm or yarn
- A valid `GEMINI_API_KEY`

---

### Backend Setup

**1. Navigate to the project root:**
```bash
cd india-eo-intelligence
```

**2. Add your API key to the `.env` file at the project root:**
```
GEMINI_API_KEY=your_key_here
```

**3. Create and activate a virtual environment:**
```bash
python -m venv backend_venv

# Windows
backend_venv\Scripts\activate

# Unix / macOS
source backend_venv/bin/activate
```

**4. Install Python dependencies:**
```bash
pip install -r backend/requirements.txt
```

**5. Start the FastAPI server:**
```bash
uvicorn backend.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`. Keep this terminal running.

---

### Frontend Setup

**1. Open a new terminal and navigate to the UI directory:**
```bash
cd nextjs-ui
```

**2. Install dependencies:**
```bash
npm install
```

**3. Start the development server:**
```bash
npm run dev
```

The dashboard will be available at `http://localhost:3000`.

> The Next.js frontend currently uses seeded mock API endpoints at `/api/analyze` and `/api/chat` that emulate the Python backend responses. These routes serve as strict API contracts and will be replaced with live Prithvi-100M and LLM endpoints during final integration.

---

## API Reference

### `POST /api/analyze`

Triggers land-cover segmentation and risk assessment for a geographic coordinate over a specified time range.

**Request:**
```json
{
  "latitude": 28.6139,
  "longitude": 77.2090,
  "start_year": 2019,
  "end_year": 2024
}
```

**Response:**
```json
{
  "environmental_changes": {
    "vegetation_change": -4.2,
    "water_change": 2.1,
    "built_up_change": 6.8
  },
  "risk_forecast": {
    "flood_risk": "High",
    "heat_stress_risk": "Medium",
    "land_degradation_risk": "Low"
  },
  "preventive_actions": {
    "immediate": ["..."],
    "medium_term": ["..."],
    "long_term": ["..."]
  }
}
```

---

### `POST /api/chat`

Submits a natural-language query to the DPO-aligned LLM, locked to the geographic and temporal context of the current analysis session.

**Request:**
```json
{
  "query": "Which districts downstream of the Tista barrage show elevated moisture stress?",
  "state": "West Bengal",
  "start_year": 2021,
  "end_year": 2024
}
```

**Response:**
```json
{
  "response": "Based on SWIR moisture indices for West Bengal (2021–2024)...",
  "context_used": true
}
```

---

## Model Details

### Prithvi-100M Vision Encoder

| Property | Detail |
|---|---|
| Architecture | Vision Transformer (ViT) with 3D spatiotemporal tubelets |
| Pre-training | Masked Autoencoder (MAE) on 4.2M HLS global time-series tiles |
| Backbone | Frozen during fine-tuning |
| Fine-tuned component | Lightweight segmentation head (4-class) |
| Input bands | Green, Red, NIR, SWIR (Resourcesat-2A LISS-3 / AWiFS) |
| Output classes | Vegetation, Water Bodies, Built-up Area, Barren Land |
| Hardware requirement | 8 GB VRAM (QLoRA-optimized) |

### DPO-Aligned LLM

| Property | Detail |
|---|---|
| Alignment method | Direct Preference Optimization (DPO) |
| Fine-tuning strategy | QLoRA (4-bit, rank 32) |
| Grounding mechanism | GAL perception script S(R,T) = (L, M, H, E) |
| Verification | Neuro-symbolic constraint checking before output |
| Output schema | Three-tier risk (Low / Medium / High) + narrative |

---

## License

This system is developed exclusively for educational and research purposes, with a focus on accurate ingestion and analysis of ISRO satellite telemetry for humanitarian disaster management applications.