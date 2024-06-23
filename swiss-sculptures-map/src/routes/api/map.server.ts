import { PUBLIC_MAPTILER_API_KEY } from '$env/static/public';
import maplibregl from 'maplibre-gl';

export async function GET() {
    const map = new maplibregl.Map({
        container: 'map',
        style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${PUBLIC_MAPTILER_API_KEY}`,
        center: [7.25, 47.15], // Centered around Biel/Bienne
        zoom: 13
    });
    return  map;
}
