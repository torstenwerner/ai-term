const REST_ENDPOINT = import.meta.env.VITE_REST_ENDPOINT;
const REST_API_KEY = import.meta.env.VITE_REST_API_KEY;

/**
 * Sends a prompt to the AI chat service and returns the response
 * @param {string} prompt_type - The user's selection of prompt type
 * @param {string} term - The user's search term'
 * @returns {Promise<string>} The AI's response
 */
export async function askAi(prompt_type, term) {
    const response = await fetch(REST_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': REST_API_KEY,
        },
        body: JSON.stringify({prompt_type, term})
    });

    if (!response.ok) {
        return `**Error communicating with the AI service.** (${response.status})`
    }

    return (await response.json()).result;
} 