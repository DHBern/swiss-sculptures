/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
    const res = await fetch(`${base}/metadata.json`);
    
    if (!res.ok) {
        throw new Error('Failed to load metadata');
    }

    const metadata = await res.json();

    return {
        metadata: metadata.metadata
    };
}
