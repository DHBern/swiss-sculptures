<script>
  import { onMount } from 'svelte';
  import maplibregl from 'maplibre-gl';
  import Popup from './Popup.svelte';
  import { queryCoordinates } from '../queryGeoJSON_coordinates';

  /** @type {string | number | undefined} */
  let popup_id;
  export let showLeft = false;
  export let showRight = false;

  /** @type {string | number | undefined | null} */
  let hoveredPointId = null;

  /** @type {string | number | undefined | null} */
  let hoveredLineId = null;

  // Calculate the width and left values based on the presence of the left and right pop-ups
  $: mapWidth = showLeft && showRight ? 'calc(100% - 1000px)' : showLeft || showRight ? 'calc(100% - 520px)' : '100%';
  $: mapLeft = showLeft ? '520px' : '0';


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
          'line-color': [
            'case',
            ['boolean', ['feature-state', 'hover'], false],
            '#FFFF00', // Highlight color
            '#007cbf'  // Default color
          ],
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
          ],
          'circle-stroke-width': [
            'case',
            ['boolean', ['feature-state', 'hover'], false],
            2,
            0
          ],
          'circle-stroke-color': '#FFFF00' // Highlight color
        },
        filter: ['==', '$type', 'Point']
      });

      map.on('click', 'points', (e) => {
        const features = map.queryRenderedFeatures(e.point, { layers: ['points'] });
        if (features.length) {
          const clickedFeature = features[0];
          const id = clickedFeature.id;
          popup_id = id;
          const sculpture = clickedFeature.properties.sculpture_name;
          if (id !== undefined ){
            map.once('render', () => {

              // Turn the previous filter to none
              map.setLayoutProperty('lines', 'visibility', 'none');

              // Turn the filter at the clicked point to the opposite state
              map.setFilter('lines', ['==', ['get', 'sculpture_name'], sculpture]);

              const visibility = map.getLayoutProperty('lines', 'visibility');
              const vis = visibility === 'none' ? 'visible' : 'none';;
              map.setLayoutProperty('lines', 'visibility', vis);

              /**
               * @type any
               */
              let filteredPoints;
              setTimeout(async () => {
                const coor = await queryCoordinates(id);
                // Zoom to fit the clicked point and its corresponding point
                const padding = { top: 50, bottom: 50, left: 50, right: 50 };

                // Fit the map to the bounding box with the specified padding
                map.fitBounds(coor.arr, { padding , linear: false, animate: true, duration: 3000});

                    
                }, 500); // Adjust the timeout value as needed

            });


          }
        }
      
      });

      map.on('mouseenter', 'points', (e) => {
        map.getCanvas().style.cursor = 'pointer';
        if (e.features && e.features.length) {
          hoveredPointId = e.features[0].id;
          if (hoveredPointId !== null) {
            map.setFeatureState(
              { source: 'sculptures', id: hoveredPointId },
              { hover: false }
            );
          }
          
          map.setFeatureState(
            { source: 'sculptures', id: hoveredPointId },
            { hover: true }
          );
        }
      });

      map.on('mouseleave', 'points', () => {
        map.getCanvas().style.cursor = '';
        if (hoveredPointId !== null) {
          map.setFeatureState(
            { source: 'sculptures', id: hoveredPointId },
            { hover: false }
          );
        }
        hoveredPointId = null;
      });

      map.on('mouseenter', 'lines', (e) => {
        map.getCanvas().style.cursor = 'pointer';
        if (e.features && e.features.length) {
          hoveredLineId = e.features[0].id;
          if (hoveredLineId !== null) {
            map.setFeatureState(
              { source: 'sculptures', id: hoveredLineId },
              { hover: false }
            );
          }
          map.setFeatureState(
            { source: 'sculptures', id: hoveredLineId },
            { hover: true }
          );
        }
      });

      map.on('mouseleave', 'lines', () => {
        map.getCanvas().style.cursor = '';
        if (hoveredLineId !== null) {
          map.setFeatureState(
            { source: 'sculptures', id: hoveredLineId },
            { hover: false }
          );
        }
        hoveredLineId = null;
      });
    });
  });
</script>

<div id="map" class="z-0" style="position: absolute; width: {mapWidth}; height: 800px; left: {mapLeft};"></div>

<div class="z-10">
  <Popup {popup_id}/>
</div>
