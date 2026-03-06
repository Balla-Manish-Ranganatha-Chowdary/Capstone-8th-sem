import { NextResponse } from 'next/server';
import seedrandom from 'seedrandom';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { latitude, longitude, start_year, end_year } = body;

    // Validate inputs
    if (!latitude || !longitude || !start_year || !end_year) {
      return NextResponse.json({ error: 'Missing required parameters' }, { status: 400 });
    }
    if (latitude < 6 || latitude > 37 || longitude < 68 || longitude > 97) {
      return NextResponse.json({ error: 'Coordinates outside India bounds' }, { status: 400 });
    }
    if (start_year < 2019 || end_year > 2024 || start_year > end_year) {
      return NextResponse.json({ error: 'Invalid time range' }, { status: 400 });
    }

    // Seed logic ported from mock_analysis.py
    const seedValue = (latitude * 1000) + (longitude * 100) + start_year + end_year;
    const rng = seedrandom(seedValue.toString());

    const time_span = end_year - start_year + 1;

    // Generates a mock percentage using seeded randomness
    const randomRange = (min: number, max: number) => min + rng() * (max - min);
    
    const vegetation_change = Number((randomRange(-15, 10) * (time_span / 5)).toFixed(2));
    const water_change = Number((randomRange(-8, 5) * (time_span / 5)).toFixed(2));
    const built_up_change = Number((randomRange(0, 20) * (time_span / 5)).toFixed(2));

    let flood_risk = 'Low';
    let heat_stress_risk = 'Low';
    let land_degradation_risk = 'Low';

    const levels = ['Low', 'Medium', 'High'];
    const pickRisk = (options: string[]) => options[Math.floor(rng() * options.length)];

    if (latitude > 28) {
      flood_risk = pickRisk(['Medium', 'High']);
      heat_stress_risk = pickRisk(['Low', 'Medium']);
      land_degradation_risk = pickRisk(['Low', 'Medium']);
    } else if (latitude < 15) {
      flood_risk = pickRisk(['Low', 'Medium']);
      heat_stress_risk = pickRisk(['Medium', 'High']);
      land_degradation_risk = pickRisk(['Low', 'Medium']);
    } else {
      flood_risk = pickRisk(['Low', 'Medium']);
      heat_stress_risk = pickRisk(['Medium', 'High']);
      land_degradation_risk = pickRisk(['Medium', 'High']);
    }

    const immediate = [];
    const medium_term = [];
    const long_term = [];

    if (['Medium', 'High'].includes(flood_risk)) {
      immediate.push('Monitor water levels and weather forecasts');
      medium_term.push('Improve drainage infrastructure');
      long_term.push('Develop flood-resistant urban planning');
    }
    if (['Medium', 'High'].includes(heat_stress_risk)) {
      immediate.push('Issue heat wave warnings to vulnerable populations');
      medium_term.push('Increase urban green cover');
      long_term.push('Implement climate-resilient building codes');
    }
    if (['Medium', 'High'].includes(land_degradation_risk)) {
      immediate.push('Restrict deforestation activities');
      medium_term.push('Promote soil conservation practices');
      long_term.push('Implement sustainable land management policies');
    }
    if (immediate.length === 0) {
      immediate.push('Continue environmental monitoring');
    }
    medium_term.push('Conduct detailed environmental impact assessments');
    long_term.push('Develop comprehensive climate adaptation strategy');

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    return NextResponse.json({
      environmental_changes: {
        vegetation_change,
        water_change,
        built_up_change
      },
      risk_forecast: {
        flood_risk,
        heat_stress_risk,
        land_degradation_risk
      },
      preventive_actions: {
        immediate,
        medium_term,
        long_term
      }
    });

  } catch (error) {
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
