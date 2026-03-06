# India Earth-Observation Intelligence System

A full-stack web application designed to analyze satellite imagery from the Indian Space Research Organisation (ISRO). The system provides environmental analysis, risk forecasting, and conversational intelligence through a context-aware interface.

## System Architecture

The project is structured into independent frontend and backend services:

### Frontend (`nextjs-ui/`)
A responsive, high-performance web dashboard built with Next.js 14 App Router.
- **Framework:** Next.js 14, React 18
- **Styling:** Tailwind CSS
- **Animations:** Framer Motion
- **Maps:** React Leaflet with CartoDB Dark Matter tiles
- **Components:** Glassmorphism UI, interactive charts, and a sliding chat overlay
- **State Management:** React Hooks and local state

### Backend Models
The intelligence layer currently consists of the following components available in the root directory:
- **CNN (`cnn/`):** A custom DeepLabV3+ model utilizing a ResNet50 backbone, modified to accept 4-channel inputs (RGB + SWIR) for precise land cover segmentation (Vegetation, Water Bodies, Built-up Area, Barren Land).
- **LLM (`llm/`):** An API client and recursive context manager designed to interface with an open-weight large language model (e.g., 120B parameters) for generating complex environmental reports and maintaining chat context across large temporal bounds.

*Note: The Next.js frontend currently utilizes seeded mock API endpoints (`/api/analyze` and `/api/chat`) that emulate the python backend logic. These routes serve as strict API contracts ready to be replaced with the actual CNN/LLM endpoints during final integration.*

## Capabilities

1. **Geographic Targeting**
   - Interactive fly-to mapping of India using CartoDB dark theme tiles.
   - Users can select any of the 28 states and 8 union territories, or drop a custom pin.

2. **Temporal Bounding**
   - Precise filtering of historical satellite data covering the years 2019 through 2024.

3. **Environmental Analysis**
   - Calculates percentage shifts in environmental markers (vegetation growth, water body variation, and urban expansion).
   - Generates automated risk assessments (Low/Medium/High) for immediate threats including flood risk, heat stress, and land degradation.
   - Provides an automated, tabbed checklist of recommended immediate, medium-term, and long-term preventive actions based on geographic risk profiles.

4. **Conversational Intelligence**
   - A persistent, context-aware analyst chat interface capable of answering ad-hoc queries about the specific geographic region bounding the analysis.
   - Operates with strict location and time-range context locks.

## Installation and Execution

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn

### Setup the Frontend
1. Clone the repository and navigate into the UI directory:
   ```bash
   git clone <repository-url>
   cd "india-eo-intelligence/nextjs-ui"
   ```

2. Install dependencies:
   ```bash
   npm install
   ```
   *Required packages include: `next`, `react`, `react-dom`, `tailwindcss`, `framer-motion`, `leaflet`, `react-leaflet`, `lucide-react`.*

3. Start the Next.js development server:
   ```bash
   npm run dev
   ```

4. The application will be available locally at `http://localhost:3000`.

## API Contracts (Frontend to Backend Integration)

The Next.js application exposes two primary endpoints designed to interface with the Python models:

### `POST /api/analyze`
**Request Payload:**
```json
{
  "latitude": 28.6139,
  "longitude": 77.2090,
  "start_year": 2019,
  "end_year": 2024
}
```

**Expected Response Schema:**
```json
{
  "environmental_changes": {
    "vegetation_change": number,
    "water_change": number,
    "built_up_change": number
  },
  "risk_forecast": {
    "flood_risk": "Low" | "Medium" | "High",
    "heat_stress_risk": "Low" | "Medium" | "High",
    "land_degradation_risk": "Low" | "Medium" | "High"
  },
  "preventive_actions": {
    "immediate": ["..."],
    "medium_term": ["..."],
    "long_term": ["..."]
  }
}
```

### `POST /api/chat`
**Request Payload:**
```json
{
  "query": "string",
  "state": "string",
  "start_year": 2019,
  "end_year": 2024
}
```

**Expected Response Schema:**
```json
{
  "response": "string",
  "context_used": boolean
}
```

## License
This architecture is developed exclusively for educational and research purposes prioritizing accurate ingestion and modeling of ISRO satellite telemetry.
