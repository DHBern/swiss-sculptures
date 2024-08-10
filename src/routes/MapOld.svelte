<script src="https://unpkg.com/maplibre-gl@4.4.1/dist/maplibre-gl.js">
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
	let popup_id;

	/**
	 * @type boolean
	 */
	export let showLeft = false;
	/**
	 * @type boolean
	 */
	export let showRight = false;

	export let a = false;

	/** @type {string | number | undefined | null} */
	let hoveredPointId = null;

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
	 * @param {{ detail: { id: any; }; }} event
	 */
	function handleShowOldPopup(event) {
		const id = event.detail.id;
		if (id !== undefined) {
			popup_id = id;
			showLeft = true;
		}
	}

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
				data: '/old_points.geojson'
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

					// Open Popup
					showLeft = true;
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
						<div style="background-color: #d9d9d9; text-align: center;">
							<div style="display: inline-block; position: relative; max-width: 100%; max-height: 37.035vh; vertical-align: middle;">
								<img src="${image[0]}" alt="${sculpture_name}" style="max-width: 100%; max-height: 100%; object-fit: contain; display: block; margin: 0 auto;" />
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
		});
	});
	function resetMap() {
		if (map) {
			map.setCenter([7.25, 47.15]);
			map.setZoom(13);
			showLeft = false;
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
					on:click|preventDefault={(event) => handleClick(event, 'MapO')}
				/>
				seuls emplacements <span style="color: red;">actuels</span> / nur
				<span style="color: red;">aktuelle</span> Standorte</label
			>

			<br />
			<label
				><input
					type="checkbox"
					bind:checked={$isMapNChecked}
					on:click|preventDefault={(event) => handleClick(event, 'MapN')}
				/>
				seuls emplacements <span style="color: blue;">d'origine</span> / nur
				<span style="color: blue;">ursprüngliche</span> Standorte</label
			>
			<br />
			<button on:click={resetMap} style="width: 100%;"
				>réinitialiser la carte / Karte zurücksetzen</button
			>
		</div>
	</div>
</div>

<div>
	<Popup on:closeL={handleCloseL} {popup_id} {showLeft} on:showOldPopup={handleShowOldPopup} {a} />
</div>
