<script src="https://unpkg.com/maplibre-gl@4.4.1/dist/maplibre-gl.js">
	import { onMount } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import Popup from './Popup.svelte';
	import { queryCoordinates } from '../queryGeoJSON_coordinates';
	import { PUBLIC_MAPTILER_API_KEY } from '$env/static/public';

	/** @type {string | number | undefined} */
	let popup_id;

	/**
	 * @type boolean
	 */
	export let showLeft = false;
	/**
	 * @type boolean
	 */
	export let showRight = false;

	/** @type {string | number | undefined | null} */
	let hoveredPointId = null;

	/** @type {string | number | undefined | null} */
	let hoveredLineId = null;

	// Calculate the width and left values based on the presence of the left and right pop-ups
	$: mapWidth =
		showLeft && showRight
			? 'calc(100% - 52.08vw)'
			: showLeft || showRight
				? 'calc(100% - 26.04vw)'
				: '100%';
	$: mapLeft = showLeft ? '26.04vw' : '0';

	// Functions to handle the custom events
	/**
	 * @param {{ detail: any; }} event
	 */
	function handleCloseL(event) {
		// Retrieve the value of showLeft from the event
		const sl = event.detail;
		showLeft = sl;
	}

	/**
	 * @param {{ detail: any; }} event
	 */
	function handleCloseR(event) {
		// Retrieve the value of showLeft from the event
		const sr = event.detail;
		showRight = sr;
	}

	onMount(async () => {
		const map = new maplibregl.Map({
			container: 'map',
			style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${PUBLIC_MAPTILER_API_KEY}`,
			center: [7.25, 47.15], // Centered around Biel/Bienne
			zoom: 13,
			minZoom: 8,
			maxZoom: 20
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
						'#007cbf' // Default color
					],
					'line-width': 2
				},
				layout: {
					visibility: 'none' // Initially hidden
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
						'old',
						'#FF0000', // red for old
						'new',
						'#0000FF', // blue for new
						'#000000' // default to black
					],
					'circle-stroke-width': ['case', ['boolean', ['feature-state', 'hover'], false], 2, 0],
					'circle-stroke-color': '#FFFF00' // Highlight color
				},
				filter: ['==', '$type', 'Point']
			});
			let popup = new maplibregl.Popup({
				closeButton: false,
				closeOnClick: false,
				maxWidth: 'none'
			});

			map.on('click', 'points', (e) => {
				const features = map.queryRenderedFeatures(e.point, { layers: ['points'] });
				if (features.length) {
					const clickedFeature = features[0];
					const id = clickedFeature.id;
					popup_id = id;

					// Open Popups
					if (clickedFeature.properties.period == 'new') {
						showLeft = false;
						showRight = true;
					} else if (clickedFeature.properties.period == 'old') {
						showRight = false;
						showLeft = true;
					}
					// Draw line and zoom
					const sculpture = clickedFeature.properties.sculpture_name;
					if (id !== undefined) {
						map.once('render', () => {
							// Turn the previous filter to none
							map.setLayoutProperty('lines', 'visibility', 'none');

							// Turn the filter at the clicked point to the opposite state
							map.setFilter('lines', ['==', ['get', 'sculpture_name'], sculpture]);

							const visibility = map.getLayoutProperty('lines', 'visibility');
							const vis = visibility === 'none' ? 'visible' : 'none';
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
								map.fitBounds(coor.arr, { padding, linear: false, animate: true, duration: 3000 });
							}, 500); // Adjust the timeout value as needed
						});
					}
				}
			});
			map.on('click', 'lines', async (e) => {
				const features = map.queryRenderedFeatures(e.point, { layers: ['lines'] });
				if (features.length) {
					const clickedFeature = features[0];
					const id = clickedFeature.id;
					popup_id = id;

					// Toggle both left and right popups
					showLeft = true;
					showRight = true;

					// Toggle line color between original and highlighted
					const isHighlighted = map.getFeatureState({
						source: 'sculptures',
						id: clickedFeature.id
					}).hover;
					map.setFeatureState(
						{ source: 'sculptures', id: clickedFeature.id },
						{ hover: !isHighlighted }
					);

					// Panning feature
					const coor = await queryCoordinates(id);
					const padding = { top: 50, bottom: 50, left: 50, right: 50 };
					map.fitBounds(coor.arr, { padding, linear: false, animate: true, duration: 3000 });
				}
			});

			map.on('mouseenter', 'points', (e) => {
				console.log('hovering...');
				console.log(e.lngLat);
				map.getCanvas().style.cursor = 'pointer';
				if (e.features && e.features.length) {
					hoveredPointId = e.features[0].id;
					const coordinates = e.lngLat;
					/**
					 * @type [number, number]
					 */
					const coordinatesArray = [coordinates.lng, coordinates.lat];

					const image = JSON.parse(e.features[0].properties.image);
					const sculpture_name = e.features[0].properties.sculpture_name;

					// Create the popup HTML content
					const popupContent = `
						<div style="background-color: #d9d9d9">
						<img src="${image[0]}" alt="${sculpture_name}" style="overflow: hidden; display: flex;" />
						<p>${sculpture_name}</p>
						</div>
					`;

					if (hoveredPointId !== null) {
						map.setFeatureState({ source: 'sculptures', id: hoveredPointId }, { hover: false });
					}

					map.setFeatureState({ source: 'sculptures', id: hoveredPointId }, { hover: true });

					while (Math.abs(e.lngLat.lng - coordinatesArray[0]) > 180) {
						coordinatesArray[0] += e.lngLat.lng > coordinatesArray[0] ? 360 : -360;
					}

					popup = new maplibregl.Popup()
						.setLngLat(coordinatesArray)
						.setHTML(popupContent)
						.addTo(map);

					console.log(popup.getLngLat());
				}
			});

			map.on('mouseleave', 'points', () => {
				map.getCanvas().style.cursor = '';
				if (hoveredPointId !== null) {
					map.setFeatureState({ source: 'sculptures', id: hoveredPointId }, { hover: false });
				}
				hoveredPointId = null;

				// Remove the popup
				popup.remove();
			});

			map.on('mouseenter', 'lines', (e) => {
				map.getCanvas().style.cursor = 'pointer';
				if (e.features && e.features.length) {
					hoveredLineId = e.features[0].id;
					if (hoveredLineId !== null) {
						map.setFeatureState({ source: 'sculptures', id: hoveredLineId }, { hover: false });
					}
					map.setFeatureState({ source: 'sculptures', id: hoveredLineId }, { hover: true });
				}
			});

			map.on('mouseleave', 'lines', () => {
				map.getCanvas().style.cursor = '';
				if (hoveredLineId !== null) {
					map.setFeatureState({ source: 'sculptures', id: hoveredLineId }, { hover: false });
				}
				hoveredLineId = null;
			});
		});
	});
</script>

<div id="map-container" style="width: {mapWidth}; left: {mapLeft};">
	<div id="map"></div>
</div>

<div>
	<Popup on:closeL={handleCloseL} on:closeR={handleCloseR} {popup_id} {showLeft} {showRight} />
</div>

<style>
	#map-container {
		position: absolute;
		overflow: hidden;
		height: 74.07vh;
		z-index: 100;
	}
	#map {
		width: 100%;
		height: 100%;
	}
</style>
