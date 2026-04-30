import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { query, state, start_year, end_year } = body;

    if (!query || !state || !start_year || !end_year) {
      return NextResponse.json({ error: 'Missing parameters' }, { status: 400 });
    }

    // Forward to FastAPI backend
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
    const res = await fetch(`${backendUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, state, start_year, end_year })
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      return NextResponse.json({ error: errorData.message || 'Backend error' }, { status: res.status });
    }

    const data = await res.json();
    return NextResponse.json({ response: data.response, context_used: true });
    
  } catch (error) {
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
