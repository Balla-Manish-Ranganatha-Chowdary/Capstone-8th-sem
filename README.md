# India Earth-Observation Intelligence System

A Streamlit-based web application providing environmental analysis, risk forecasting, and conversational intelligence for locations within India using ISRO satellite data.

## Application Workflow

1. **Location Selection**
   - Click a point on the interactive map of India or select a state from the dropdown menu.
   - The system captures the geographic coordinates for the selected region.

2. **Time Range Selection**
   - Specify a start and end year (between 2019 and 2024) to define the temporal scope of the analysis.

3. **Environmental Analysis**
   - Click the "Analyze" button.
   - The system processes the request to evaluate changes in vegetation, water bodies, and built-up areas for the specified timeline.
   - It generates risk forecasts for floods, heat stress, and land degradation, along with preventive action recommendations.

4. **Context-Aware Chat**
   - After the analysis is complete, a chat interface becomes available on the right side of the screen.
   - Users can ask specific questions about the environmental data.
   - The conversational AI answers using the context of the selected location, selected time range, and the analysis results.

## Setup Instructions

1. **Clone the repository and navigate to the directory**
   ```bash
   git clone <repository-url>
   cd india-eo-intelligence
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
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
