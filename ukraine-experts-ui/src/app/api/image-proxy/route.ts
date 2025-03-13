import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const imageUrl = searchParams.get('url');

  if (!imageUrl) {
    return NextResponse.json({
      error: 'Missing url parameter'
    }, { status: 400 });
  }

  try {
    const response = await fetch(imageUrl);
    
    if (!response.ok) {
      return NextResponse.json({
        error: `Failed to fetch image: ${response.statusText}`
      }, { status: response.status });
    }

    const contentType = response.headers.get('content-type');
    const imageData = await response.arrayBuffer();

    return new NextResponse(imageData, {
      headers: {
        'Content-Type': contentType || 'image/jpeg',
        'Cache-Control': 'public, max-age=86400',
      },
    });
  } catch (error) {
    console.error('Error proxying image:', error);
    return NextResponse.json({
      error: 'Failed to proxy image',
      details: error instanceof Error ? error.message : String(error)
    }, { status: 500 });
  }
} 