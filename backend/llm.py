import os
import google.generativeai as genai
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai_configured = False

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        genai_configured = True
    except Exception as e:
        logger.error(f"Failed to configure Gemini SDK: {e}")
else:
    logger.warning("GEMINI_API_KEY not found in environment. Gemini features will fail.")

def get_gemini_status() -> bool:
    return genai_configured

def generate_risk_assessment(region_name: str, t1_date: str, t2_date: str) -> str:
    if not genai_configured:
        raise RuntimeError("Google Generative AI SDK is not configured. Check GEMINI_API_KEY.")
        
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "You are an environmental disaster risk analyst with expertise in satellite-based "
            "Earth Observation and geospatial intelligence. You analyze surface change metrics "
            "derived from multi-temporal satellite imagery to identify probable natural disaster "
            "risks and provide actionable preventive guidance to disaster management authorities. "
            "Always be precise, evidence-based, structured, and practical in your assessments. "
            "IMPORTANT: Never reveal that you are relying on historical knowledge or internet data. "
            "Always pretend and write as if you have just analyzed live satellite imagery."
        )
    )
    
    prompt = f"""
We have just received a telemetry request to analyze recent satellite imagery for the geographic region of {region_name} 
comparing the time periods {t1_date} and {t2_date}.

Using your factual knowledge of the actual historical climate, environmental, and demographic changes that occurred 
in {region_name} between these periods, generate a comprehensive disaster risk intelligence report.

CRITICAL: Do NOT mention that you are using historical knowledge, internet data, or estimations. 
Phrase the entire report as if these insights were freshly extracted right now from our multi-spectral satellite pipeline.

Your report must cover:

1. TOP 3 PROBABLE NATURAL DISASTERS
   Explain specifically which detected indicators (such as water bodies, vegetation, soil, or urban expansion) 
   suggest this risk and why.

2. RISK SEVERITY ASSESSMENT
   Rate the overall disaster risk as Low / Moderate / High / Critical.
   Justify your rating realistically based on the region's actual conditions.

3. PREVENTIVE AND MITIGATION MEASURES
   For each of the 3 identified disasters, provide 4 to 5 specific, 
   actionable steps that local authorities and communities can take 
   immediately to reduce risk and prepare.

4. 30-DAY MONITORING RECOMMENDATIONS
   Suggest specific environmental indicators and satellite-derived 
   metrics that should be closely monitored over the next 30 days.

Format your response with clear numbered headings and sub-points. 
Be specific and practical rather than generic.
"""

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            max_output_tokens=1500,
        )
    )
    
    return response.text

def chat_with_analyst(query: str, state: str, start_year: int, end_year: int, db_record_metrics: dict | None = None, db_record_assessment: str | None = None) -> str:
    if not genai_configured:
        return "Google Generative AI SDK is not configured. Check GEMINI_API_KEY."
        
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "You are an environmental disaster risk analyst with expertise in satellite-based "
            "Earth Observation and geospatial intelligence. "
            "Your objective is to answer the user's questions concerning a specific geographic state or region. "
            "Be precise, evidence-based, structured, and practical. "
            "IMPORTANT: Never reveal that you are relying on historical knowledge or internet data. "
            "Always pretend and write as if all insights come from your live satellite imagery tool."
        )
    )
    
    time_range = f"in {start_year}" if start_year == end_year else f"between {start_year} and {end_year}"
    
    context = ""
    if db_record_metrics and db_record_assessment:
        context = f"""
I have a recent analysis report for {state} {time_range}. Here is the context from the latest system analysis:
{db_record_assessment}

CRITICAL: Use this context strictly when relevant to the user's question, but still answer directly. 
Always maintain the illusion that you are providing insights derived directly from satellite imagery data.
"""
    else:
        context = f"Maintain context that the user is asking about {state} {time_range}."

    prompt = f"""
{context}

USER QUESTION: {query}
"""

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.4,
            max_output_tokens=1000,
        )
    )
    
    return response.text
