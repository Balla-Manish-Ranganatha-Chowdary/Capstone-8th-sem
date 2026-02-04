# India Earth-Observation Intelligence System

A Streamlit-based web application providing environmental analysis, risk forecasting, and conversational intelligence for locations within India using ISRO satellite data.

## Features

- **Interactive India Map**: Click anywhere on the map or select from a dropdown of all 28 states and 8 union territories
- **Environmental Analysis**: Track vegetation, water body, and built-up area changes over time (2019-2024)
- **Risk Forecasting**: Get flood, heat stress, and land degradation risk assessments
- **Context-Aware Chat**: Ask questions about environmental data with location and time-specific responses
- **Clean UI**: High-contrast design with white boundaries on black background for optimal visibility
- **Mock Backend**: Ready-to-replace mock services that simulate ML model responses

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Application                    │
│                         (app.py)                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  UI Layer    │    │  Services    │    │  Data Layer  │
│              │    │              │    │              │
│ - india_map  │    │ - mock_      │    │ - india_     │
│ - chat_panel │◄───┤   analysis   │    │   states.json│
│ - output_    │    │ - mock_chat  │    │              │
│   panels     │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd india-eo-intelligence
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   
   The application will automatically open in your default browser at `http://localhost:8501`

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run only unit tests
pytest tests/test_services.py tests/test_ui_basic.py

# Run property-based tests
pytest tests/test_validation.py
```

## Deployment to Streamlit Community Cloud

### Prerequisites

- GitHub account
- Streamlit Community Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Deployment Checklist

Follow this comprehensive checklist to ensure successful deployment:

#### Phase 1: GitHub Repository Setup

- [ ] **Create GitHub Repository**
  - Create a new repository on GitHub (public or private)
  - Initialize with or without README (will be overwritten)
  - Note the repository URL for later use

- [ ] **Verify Local Repository Structure**
  - [ ] Confirm `app.py` is at repository root
  - [ ] Confirm `requirements.txt` exists with all dependencies
  - [ ] Confirm `.streamlit/config.toml` exists with proper configuration
  - [ ] Confirm all required directories exist: `ui/`, `services/`, `data/`, `tests/`
  - [ ] Confirm `data/india_states.json` contains all 36 states/UTs

- [ ] **Push Code to GitHub**
  ```bash
  git init
  git add .
  git commit -m "Initial commit: India EO Intelligence System"
  git branch -M main
  git remote add origin <your-github-repo-url>
  git push -u origin main
  ```

- [ ] **Verify GitHub Push**
  - Visit your GitHub repository in browser
  - Confirm all files are present
  - Confirm `app.py` is visible at root level

#### Phase 2: Streamlit Community Cloud Connection

- [ ] **Sign Up / Log In to Streamlit Cloud**
  - Go to [share.streamlit.io](https://share.streamlit.io)
  - Sign in with your GitHub account
  - Authorize Streamlit to access your repositories

- [ ] **Create New App**
  - Click "New app" button
  - Select your GitHub repository from the dropdown
  - Choose the branch: `main`
  - Set main file path: `app.py`
  - Set app URL (optional custom subdomain)

- [ ] **Configure Advanced Settings** (if needed)
  - Python version: 3.9 or higher (auto-detected from requirements.txt)
  - Click "Advanced settings" if you need to customize

#### Phase 3: Environment Variable Configuration

- [ ] **Configure COMMIT_SHA Variable** (optional but recommended)
  - In Streamlit Cloud app dashboard, click "⋮" menu
  - Select "Settings"
  - Go to "Secrets" section
  - Add environment variable:
    ```toml
    COMMIT_SHA = "abc1234"
    ```
  - This enables version tracking in the app footer
  - Update this value after each significant deployment

- [ ] **Configure Future ML API Keys** (when ready)
  - Add API keys for ML model services
  - Add database connection strings
  - Add any other sensitive configuration
  - Format in TOML:
    ```toml
    [api_keys]
    ml_service = "your-api-key-here"
    ```

#### Phase 4: Deploy and Verify

- [ ] **Initiate Deployment**
  - Click "Deploy!" button
  - Wait for deployment to complete (typically 2-5 minutes)
  - Monitor build logs for any errors

- [ ] **Verify Deployment Success**
  - [ ] App loads without errors
  - [ ] Map displays correctly with black background and white boundaries
  - [ ] State dropdown shows all 36 states/UTs
  - [ ] Time range selector displays years 2019-2024
  - [ ] "Analyze" button is functional
  - [ ] Analysis results display correctly
  - [ ] Chat interface is accessible
  - [ ] Footer shows version and commit hash

- [ ] **Test Core Functionality**
  - [ ] Select a state from dropdown → Verify coordinates update
  - [ ] Click on map → Verify location selection works
  - [ ] Select time range → Click Analyze → Verify results display
  - [ ] Submit chat query → Verify context-aware response
  - [ ] Test error handling: Select invalid time range (start > end)

#### Phase 5: Auto-Deploy Verification

- [ ] **Test Auto-Deploy Workflow**
  - Make a small change to README.md locally
  - Commit and push to main branch:
    ```bash
    git add README.md
    git commit -m "Test auto-deploy"
    git push origin main
    ```
  - Go to Streamlit Cloud dashboard
  - Verify "Reboot" or "Deploying" status appears
  - Wait for redeployment to complete
  - Verify change is reflected in deployed app

- [ ] **Configure Branch Protection** (optional)
  - In GitHub repository settings
  - Enable branch protection for `main`
  - Require pull request reviews before merging
  - Require status checks to pass (if CI/CD configured)

#### Phase 6: Monitoring and Maintenance

- [ ] **Set Up Monitoring**
  - Bookmark Streamlit Cloud dashboard URL
  - Enable email notifications for deployment failures
  - Monitor app logs regularly for errors

- [ ] **Document Deployment Details**
  - Record deployed app URL
  - Record GitHub repository URL
  - Record any custom configuration
  - Share URLs with team members

- [ ] **Plan for Updates**
  - Establish branching strategy (feature branches → main)
  - Define testing requirements before merging to main
  - Schedule regular dependency updates
  - Plan for ML model integration timeline

### Quick Deployment Steps (Summary)

For experienced users, here's the condensed version:

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select repository, branch (`main`), and main file (`app.py`)
   - Click "Deploy"

3. **Configure Environment Variables** (optional)
   - Add `COMMIT_SHA` in app settings → Secrets
   - Format: `COMMIT_SHA = "abc1234"`

4. **Verify Auto-Deploy**
   - Push a change to main branch
   - Confirm automatic redeployment in Streamlit Cloud dashboard

### Troubleshooting Deployment Issues

**Issue**: App fails to deploy with "ModuleNotFoundError"
- **Solution**: Verify all dependencies are listed in `requirements.txt` with correct versions

**Issue**: Map doesn't display correctly
- **Solution**: Check browser console for errors; verify `folium` and `streamlit-folium` versions are compatible

**Issue**: "File not found" error for `data/india_states.json`
- **Solution**: Verify file is committed to GitHub and path is correct (case-sensitive)

**Issue**: Environment variables not working
- **Solution**: Verify TOML format in Secrets section; restart app after adding secrets

**Issue**: Auto-deploy not triggering
- **Solution**: Check GitHub webhook settings; verify Streamlit has repository access permissions

## Usage Guide

### 1. Select a Location

**Option A: Click on the Map**
- Click anywhere on the interactive India map
- Coordinates will be captured automatically

**Option B: Use State Dropdown**
- Select a state or union territory from the dropdown
- Representative coordinates will be used

### 2. Choose Time Range

- Select start year (2019-2024)
- Select end year (2019-2024)
- System validates that start year ≤ end year

### 3. Analyze

- Click the "Analyze" button
- View environmental changes (vegetation, water, built-up areas)
- Review risk forecasts (flood, heat stress, land degradation)
- Read preventive action recommendations

### 4. Ask Questions

- Type questions in the chat interface
- Responses are context-aware (include your selected location and time range)
- Chat history is maintained during your session

## API Contract Documentation

The system uses well-defined API contracts to enable seamless replacement of mock services with ML models.

### Analysis Service

**Endpoint**: POST /analyze

**Request**:
```json
{
  "latitude": 28.6139,
  "longitude": 77.2090,
  "start_year": 2019,
  "end_year": 2024
}
```

**Response**:
```json
{
  "environmental_changes": {
    "vegetation_change": -12.5,
    "water_change": 8.3,
    "built_up_change": 15.7
  },
  "risk_forecast": {
    "flood_risk": "High",
    "heat_stress_risk": "Medium",
    "land_degradation_risk": "Low"
  },
  "preventive_actions": {
    "immediate": [
      "Implement flood early warning systems",
      "Establish emergency response protocols"
    ],
    "medium_term": [
      "Develop urban drainage infrastructure",
      "Create green buffer zones"
    ],
    "long_term": [
      "Implement sustainable urban planning",
      "Develop climate adaptation strategies"
    ]
  }
}
```

### Chat Service

**Endpoint**: POST /chat

**Request**:
```json
{
  "query": "What are the main environmental concerns?",
  "state": "Delhi",
  "start_year": 2019,
  "end_year": 2024
}
```

**Response**:
```json
{
  "response": "Based on analysis of Delhi from 2019 to 2024, the main environmental concerns include...",
  "context_used": true
}
```

### Replacing Mock Services with ML Models

To integrate real ML models:

1. **Replace `services/mock_analysis.py`**
   - Keep the same `analyze()` function signature
   - Call your ML model instead of generating mock data
   - Return data matching the exact response schema

2. **Replace `services/mock_chat.py`**
   - Keep the same `chat()` function signature
   - Call your LLM with India-specific context
   - Return data matching the exact response schema

**No UI changes required** - the UI depends only on API contracts, not implementations.

## Project Structure

```
india-eo-intelligence/
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── ui/
│   ├── __init__.py
│   ├── india_map.py         # Interactive map component
│   ├── chat_panel.py        # Chat interface
│   └── output_panels.py     # Analysis output display
├── services/
│   ├── __init__.py
│   ├── mock_analysis.py     # Mock analysis service
│   └── mock_chat.py         # Mock chat service
├── utils/
│   ├── __init__.py
│   └── validation.py        # Input validation utilities
├── data/
│   └── india_states.json    # State/UT coordinates
├── tests/
│   ├── __init__.py
│   ├── test_services.py     # Service unit tests
│   ├── test_ui_basic.py     # UI component tests
│   └── test_validation.py   # Validation tests
├── app.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
├── pytest.ini              # Pytest configuration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Data Source Attribution

This system is designed to use satellite data from the **Indian Space Research Organisation (ISRO)**. The current implementation uses mock data that simulates the structure and format of real satellite observations.

### ISRO Data Sources

- **Bhuvan**: ISRO's geoportal providing satellite imagery and geospatial data
- **NRSC**: National Remote Sensing Centre datasets
- **Resourcesat**: Multi-spectral satellite imagery
- **Cartosat**: High-resolution terrain mapping

### Future Integration

The system architecture supports integration with:
- ISRO's Bhuvan API for real satellite imagery
- India Meteorological Department (IMD) for weather data
- State-level environmental monitoring agencies

## Technology Stack

- **Frontend**: Streamlit 1.28+
- **Mapping**: Folium 0.14+ with streamlit-folium
- **Testing**: pytest 7.4+ with Hypothesis 6.90+ for property-based testing
- **Python**: 3.9+

## Development

### Code Quality

- All functions include docstrings and type hints
- Code follows PEP 8 style guidelines
- Property-based tests validate correctness properties
- Unit tests cover specific scenarios and edge cases

### Testing Strategy

The project uses a dual testing approach:

1. **Unit Tests**: Verify specific examples and edge cases
2. **Property-Based Tests**: Verify universal properties across randomized inputs

Run tests before committing:
```bash
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is designed for educational and research purposes.

## Contact

For questions or support, please open an issue in the GitHub repository.

## Acknowledgments

- **ISRO** for satellite data and earth observation capabilities
- **Streamlit** for the excellent web framework
- **Folium** for interactive mapping capabilities
- **Hypothesis** for property-based testing framework

---

**Version**: 1.0.0 | **Data Source**: ISRO
