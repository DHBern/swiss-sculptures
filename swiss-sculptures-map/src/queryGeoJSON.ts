export type GeoJSONFeature = {
  id: number;
  geometry: {
    type: string;
  };
};
  
export async function queryGeoJSON(id: number): Promise<{ queriedFeatures: GeoJSONFeature[] }> {
  try {
      // Fetch the GeoJSON file
      const response = await fetch('src/data.geojson');
      if (!response.ok) {
          throw new Error('Failed to fetch GeoJSON file');
      }
      const geojsonObject = await response.json();

      // Filter features by the specified ID
      const queriedFeatures = geojsonObject.features.filter((feature: { id: number; geometry: { type: string }}) => feature.id === id && feature.geometry.type == 'Point');
      return { queriedFeatures };
  } catch (error) {
      console.error('Error fetching or parsing GeoJSON:', error);
      throw error;
  }
}


  // export async function queryGeoJSON(id: number) {
  //   const queriedFeature = id*2;
  //   return queriedFeature;
  // }