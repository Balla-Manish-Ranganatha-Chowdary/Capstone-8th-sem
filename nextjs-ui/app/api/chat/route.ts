import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { query, state, start_year, end_year } = body;

    if (!query || !state || !start_year || !end_year) {
      return NextResponse.json({ error: 'Missing parameters' }, { status: 400 });
    }

    // TODO: Later replace this logic with actual LLM API call (Anthropic/OpenAI) using the system prompt context.

    const time_range = start_year === end_year ? `in ${start_year}` : `between ${start_year} and ${end_year}`;
    const queryLower = query.toLowerCase();

    const context_keywords = ['state', 'location', 'area', 'region', 'here', 'year', 'time', state.toLowerCase()];
    const context_used = context_keywords.some(k => queryLower.includes(k));

    let response = "";

    if (['vegetation', 'forest', 'green', 'tree'].some(k => queryLower.includes(k))) {
      response = context_used 
        ? `Based on satellite data for ${state} ${time_range}, vegetation patterns show significant changes. Forest cover in ${state} has been affected by both natural and anthropogenic factors during this period.`
        : `Vegetation monitoring uses multispectral satellite imagery to track changes in forest cover and agricultural health.`;
    } else if (['water', 'river', 'lake', 'flood'].some(k => queryLower.includes(k))) {
      response = context_used
        ? `Water body analysis for ${state} ${time_range} shows variations in surface water extent. Rivers and lakes in ${state} have experienced changes due to rainfall patterns.`
        : `Water body monitoring uses radar and optical satellite data to track changes in rivers, lakes, and reservoirs.`;
    } else if (['urban', 'city', 'built'].some(k => queryLower.includes(k))) {
      response = context_used
        ? `Urban development in ${state} ${time_range} has been tracked through satellite imagery. Built-up areas in ${state} have expanded.`
        : `Urban growth monitoring uses satellite imagery to track expansion of built-up areas.`;
    } else {
      response = context_used
        ? `Based on the analysis for ${state} ${time_range}, the India EO Intelligence System uses satellite data to analyze specific conditions and changes in this area.`
        : `The India Earth-Observation Intelligence System provides environmental analysis, risk forecasting, and insights based on ISRO satellite data.`;
    }

    // Simulate LLM delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    return NextResponse.json({ response, context_used });
  } catch (error) {
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
