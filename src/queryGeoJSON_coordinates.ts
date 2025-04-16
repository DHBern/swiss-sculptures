import { base } from '$app/paths';

export async function queryCoordinates(
	id: number | string | undefined
): Promise<{ arr: [number, number, number, number] }> {
	try {
		// Fetch the GeoJSON file
		const response = await fetch(`${base}/data.geojson`);
		if (!response.ok) {
			throw new Error('Failed to fetch GeoJSON file');
		}
		const geojsonObject = await response.json();

		// Filter features by the specified ID
		const queriedFeatures = geojsonObject.features.filter(
			(feature: { id: number | string; geometry: { type: string } }) =>
				feature.id === id && feature.geometry.type == 'Point'
		);

		// Array to store coordinates
		let coordinates: number[][] = [];

		// Extract coordinates from queried features
		for (let qr of queriedFeatures) {
			coordinates.push(qr.geometry.coordinates);
		}

		// Ensure there are enough coordinates
		if (coordinates.length < 2) {
			throw new Error('Not enough coordinates available');
		}

		// Extract the first two coordinates
		let [lng1, lat1] = coordinates[0];
		let [lng2, lat2] = coordinates[1];

		// Create the bounding box array
		const arr: [number, number, number, number] = [lng1, lat1, lng2, lat2];

		// Return the bounding box array
		return { arr };
	} catch (error) {
		console.error('Error fetching or parsing GeoJSON:', error);
		throw error;
	}
}
