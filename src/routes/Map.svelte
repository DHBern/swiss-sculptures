<script src="https://unpkg.com/maplibre-gl@4.4.1/dist/maplibre-gl.js">
	import { preventDefault } from 'svelte/legacy';

	import { onMount } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import Popup from './Popup.svelte';
	import { queryCoordinates } from '../queryGeoJSON_coordinates';
	import { PUBLIC_MAPTILER_API_KEY } from '$env/static/public';
	import { isMapOChecked, isMapNChecked } from '../store.js';

	/**
	 * @type {maplibregl.Map}
	 */
	let map;

	/** @type {any} */
	let popup_id = $state();

	
	

	/** @type {{showLeft?: boolean, showRight?: boolean, a?: boolean}} */
	let { showLeft = $bindable(false), showRight = $bindable(false), a = true } = $props();

	/** @type {string | number | undefined | null} */
	let hoveredPointId = null;

	/** @type {string | number | undefined | null} */
	let hoveredLineId = null;

	// Calculate the width and left values based on the presence of the left and right pop-ups
	let mapWidth =
		$derived(showLeft && showRight
			? 'calc(100% - 52.08vw)'
			: showLeft || showRight
				? 'calc(100% - 26.04vw)'
				: '100%');
	let mapLeft = $derived(showLeft ? '26.04vw' : '0');

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
	/**
	 * @param {{ detail: { id: any; }; }} event
	 */
	function handleShowOldPopup(event) {
		const id = event.detail.id;
		if (id !== undefined) {
			popup_id = id;
			showLeft = true;
		}
	}
	/**
	 * @param {{ detail: { id: any; }; }} event
	 */
	function handleShowNewPopup(event) {
		const id = event.detail.id;
		if (id !== undefined) {
			popup_id = id;
			showRight = true;
		}
	}

	function resetZoom() {
		setTimeout(async () => {
			const coor = await queryCoordinates(popup_id);
			const padding = { top: 100, bottom: 50, left: 50, right: 50 };

			map.fitBounds(coor.arr, { padding, linear: false, animate: true, duration: 3000 });
		}, 500);
	}

	/**
	 * @type {number | undefined}
	 */
	let inactivityTimeout;

	// Function to reset the inactivity timer
	function resetInactivityTimeout() {
		clearTimeout(inactivityTimeout);
		inactivityTimeout = setTimeout(() => {
			resetMap();
		}, 120000); // 120 seconds
	}

	function setupInactivityListeners() {
		const events = ['mousemove', 'keydown', 'click', 'scroll'];

		events.forEach((event) => {
			document.addEventListener(event, resetInactivityTimeout);
		});

		resetInactivityTimeout();
	}

	onMount(() => {
		setupInactivityListeners();
	});

	onMount(async () => {
		map = new maplibregl.Map({
			container: 'map',
			style: `https://api.maptiler.com/maps/ch-swisstopo-lbm-dark/style.json?key=${PUBLIC_MAPTILER_API_KEY}`,
			center: [7.25, 47.15], // Centered around Biel/Bienne
			zoom: 13
		});
		map.dragRotate.disable();

		map.on('load', () => {
			map.addSource('sculptures', {
				type: 'geojson',
				data: '/data.geojson'
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
					'line-width': 8
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

							setTimeout(async () => {
								const coor = await queryCoordinates(id);
								// Zoom to fit the clicked point and its corresponding point
								const padding = { top: 100, bottom: 50, left: 50, right: 50 };

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
					console.log(image[0].replace(/\/large\//g, '/medium/'));
					// Create the popup HTML content
					const popupContent = `
						<div style="background-color: #d9d9d9; text-align: center;">
							<div style="display: inline-block; position: relative; max-width: 100%; max-height: 37.035vh; vertical-align: middle;">
								<img src="${image[0].replace(/\/large\//g, '/medium/')}" alt="${sculpture_name}" style="max-width: 100%; max-height: 100%; object-fit: contain; display: block; margin: 0 auto;" />
							</div>
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

	function resetMap() {
		if (map) {
			map.setCenter([7.25, 47.15]);
			map.setZoom(13);
			showLeft = false;
			showRight = false;
			map.setLayoutProperty('lines', 'visibility', 'none');
		}
	}

	// Handle checkbox state changes
	/**
	 * @param {MouseEvent & { currentTarget: EventTarget & HTMLInputElement; }} event
	 * @param {string} checkboxName
	 */
	function handleClick(event, checkboxName) {
		// Ensure that event.target is an HTMLInputElement
		const target = event.target;
		if (target instanceof HTMLInputElement) {
			const isCurrentlyChecked = target.checked;

			// Prevent unchecking if it's the only checkbox checked
			if (!isCurrentlyChecked) {
				if (checkboxName === 'MapO') {
					// If MapO is being unchecked, ensure MapN is checked
					if (!$isMapNChecked) {
						event.preventDefault(); // Prevent the checkbox from being unchecked
						return;
					}
				} else if (checkboxName === 'MapN') {
					// If MapN is being unchecked, ensure MapO is checked
					if (!$isMapOChecked) {
						event.preventDefault(); // Prevent the checkbox from being unchecked
						return;
					}
				}
			}

			// Update store based on the checkbox being clicked
			if (checkboxName === 'MapO') {
				isMapOChecked.set(isCurrentlyChecked ? true : false);
			} else if (checkboxName === 'MapN') {
				isMapNChecked.set(isCurrentlyChecked ? true : false);
			}
		}
	}
</script>

<div id="map-container" style="width: {mapWidth}; left: {mapLeft};">
	<div id="map">
		<div
			style="position: absolute; z-index:10; color:black; top:3vh; left:1vw; background-color: #d9d9d9;"
		>
			<label
				><input
					type="checkbox"
					bind:checked={$isMapOChecked}
					onclick={preventDefault((event) => handleClick(event, 'MapO'))}
				/>
				seuls emplacements <span style="color: red;">actuels</span> / nur
				<span style="color: red;">aktuelle</span> Standorte</label
			>

			<br />
			<label
				><input
					type="checkbox"
					bind:checked={$isMapNChecked}
					onclick={preventDefault((event) => handleClick(event, 'MapN'))}
				/>
				seuls emplacements <span style="color: blue;">d'origine</span> / nur
				<span style="color: blue;">ursprüngliche</span> Standorte</label
			>
			<br />
			<button onclick={resetMap} style="width: 100%;"
				>réinitialiser la carte / Karte zurücksetzen</button
			>
		</div>
	</div>
</div>

<div>
	<Popup
		on:closeL={handleCloseL}
		on:closeR={handleCloseR}
		{popup_id}
		{showLeft}
		{showRight}
		on:showOldPopup={handleShowOldPopup}
		on:showNewPopup={handleShowNewPopup}
		{a}
		on:showNewPopup={resetZoom}
		on:showOldPopup={resetZoom}
	/>
</div>
