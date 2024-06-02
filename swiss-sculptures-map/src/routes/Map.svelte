<script>
  import { onMount } from 'svelte';
  import maplibregl from 'maplibre-gl';

  onMount(() => {
    const map = new maplibregl.Map({
      container: 'map',
      style: 'https://api.maptiler.com/maps/streets-v2/style.json?key=nV6DhQQ3XsyCDE3mZxVq',
      center: [7.25, 47.15], // Centered around Biel/Bienne
      zoom: 13
    });

    map.on('load', () => {
      map.addSource('sculptures', {
        type: 'geojson',
        data: 'src/data.geojson'
      });

      map.addLayer({
        id: 'lines',
        type: 'line',
        source: 'sculptures',
        paint: {
          'line-color': '#007cbf',
          'line-width': 2
        },
        layout: {
          'visibility': 'none' // Initially hidden
        },
        filter: ['==', '$type', 'LineString']
      });

      map.addLayer({
        id: 'points',
        type: 'circle',
        source: 'sculptures',
        paint: {
          'circle-radius': 6,
          'circle-color': [
            'match',
            ['get', 'period'],
            'old', '#FF0000',    // red for old
            'new', '#0000FF',    // blue for new
            '#000000'            // default to black
          ]
        },
        filter: ['==', '$type', 'Point']
      });

      // Event listener on the map to show lines.
      map.on('click', (e) => {

        const point = e.point;
        const features = map.queryRenderedFeatures(point, { layers: ['points']});
        console.log(features);

        e.preventDefault();

        if (features.length) {
          const clickedFeature = features[0];
          const id = clickedFeature.id;
          console.log(id);

          const visibility = map.getLayoutProperty(
              'lines',
              'visibility'
          );

          // Toggle layer visibility by changing the layout object's visibility property.
          if (id !== undefined) {
            if (visibility === 'visible') {
                map.setLayoutProperty('lines', 'visibility', 'none');
            } else {
                map.setLayoutProperty(
                    'lines',
                    'visibility',
                    'visible'
                );
            }
          }
        }
      });


        map.on('mouseenter', 'points', (e) => {
            // Change the cursor style as a UI indicator.
            map.getCanvas().style.cursor = 'pointer';

        });

        map.on('mouseleave', 'points', () => {
            map.getCanvas().style.cursor = '';
        });

      
    });
  });
</script>

<style>
  #map {
    width: 100%;
    height: 700px;
  }
</style>

<div id="map"></div>
