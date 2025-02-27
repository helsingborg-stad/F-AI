import type { RequestHandler } from './$types.ts';
import { json } from '@sveltejs/kit';
import { SECRET_API_URL } from '$env/static/private';

export const POST: RequestHandler = async ({ request }) => {
  try {
    const { message } = await request.json();

    // Send POST request to the back-end
    const response = await fetch(`${SECRET_API_URL}/chat/stream/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      const errorText = await response.text();
      return json({ error: `Back-end error: ${errorText}` }, { status: response.status });
    }

    const data = await response.json();

    // Return the response to the client
    return json({ response: data.response });
  } catch (error) {
    console.error('Server Error:', error);
    return json({ error: 'An error occurred on the server.' }, { status: 500 });
  }
};
