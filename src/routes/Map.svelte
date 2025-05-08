<script>
	import { onMount } from 'svelte';
	import maplibregl from 'maplibre-gl';
	import Popup from './Popup.svelte';
	import { queryCoordinates } from '../queryGeoJSON_coordinates';
	import { PUBLIC_MAPTILER_API_KEY } from '$env/static/public';
	import { base } from '$app/paths';

	let map;
	let checkedShowHist = $state(true);
	let checkedShowToday = $state(true);
	let showLeft = $state(false);
	let showRight = $state(false);

	let popup_id = $state();
	let { metadata } = $props();

	let mdrow = $derived.by(() => {
		const idx = metadata.findIndex((m) => m.id === popup_id);
		return metadata[idx];
	});

	let hoveredPointId = null;
	let hoveredLineId = null;

	// Calculate the width and left values based on the presence of the left and right pop-ups
	let mapWidth = $derived(
		showLeft && showRight
			? 'calc(100% - 52.08vw)'
			: showLeft || showRight
				? 'calc(100% - 26.04vw)'
				: '100%'
	);
	let mapLeft = $derived(showLeft ? '26.04vw' : '0');

	onMount(async () => {
		map = new maplibregl.Map({
			container: 'map',
			// style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
			style: `https://api.maptiler.com/maps/ch-swisstopo-lbm-dark/style.json?key=${PUBLIC_MAPTILER_API_KEY}`,
			center: [7.25, 47.15], // Centered around Biel/Bienne
			zoom: 13
		});
		map.dragRotate.disable();

		map.on('load', () => {
			map.addSource('sculptures', { type: 'geojson', data: `${base}/features.geojson` });

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
				filter: ['==', ['get', 'today_hist'], 'line']
			});

			map.addLayer({
				id: 'hist-points',
				type: 'circle',
				source: 'sculptures',
				paint: {
					'circle-radius': 6,
					'circle-color': '#FF0000', // red
					'circle-stroke-width': ['case', ['boolean', ['feature-state', 'hover'], false], 2, 0],
					'circle-stroke-color': '#FFFF00' // Highlight color
				},
				filter: ['==', ['get', 'today_hist'], 'hist']
			});
			map.addLayer({
				id: 'today-points',
				type: 'circle',
				source: 'sculptures',
				paint: {
					'circle-radius': 6,
					'circle-color': '#0000FF', // blue
					'circle-stroke-width': ['case', ['boolean', ['feature-state', 'hover'], false], 2, 0],
					'circle-stroke-color': '#FFFF00' // Highlight color
				},
				filter: ['==', ['get', 'today_hist'], 'today']
			});
			let popup;

			function handlePointClicked(e) {
				const features = map.queryRenderedFeatures(e.point, {
					layers: ['hist-points', 'today-points']
				});
				if (features.length > 0) {
					popup_id = features[0].properties.id;

					// Open Popups
					switch (features[0].properties.today_hist) {
						case 'today':
							showLeft = false;
							showRight = true;
							break;
						case 'hist':
							showRight = false;
							showLeft = true;
							break;
					}
					// Draw line and zoom
					if (popup_id !== undefined) {
						map.once('render', () => {
							// Make all lines invisible
							map.setLayoutProperty('lines', 'visibility', 'none');

							// Turn the filter at the clicked point to the opposite state
							map.setFilter('lines', ['==', ['get', 'id'], popup_id]);

							let visibility = map.getLayoutProperty('lines', 'visibility');
							visibility = visibility === 'none' ? 'visible' : 'none';
							map.setLayoutProperty('lines', 'visibility', visibility);

							setTimeout(async () => {
								resetZoom();
							}, 500);
						});
					}
				}
			}

			map.on('click', 'today-points', (e) => {
				handlePointClicked(e);
			});
			map.on('click', 'hist-points', (e) => {
				handlePointClicked(e);
			});

			map.on('click', 'lines', async (e) => {
				const features = map.queryRenderedFeatures(e.point, { layers: ['lines'] });
				if (features.length) {
					const id = features[0].properties.id;
					popup_id = id;

					// Toggle both left and right popups
					showLeft = true;
					showRight = true;

					// Toggle line color between original and highlighted
					const isHighlighted = map.getFeatureState({
						source: 'sculptures',
						id: id
					}).hover;
					map.setFeatureState({ source: 'sculptures', id: id }, { hover: !isHighlighted });

					// Panning feature
					const coor = await queryCoordinates(id);
					const padding = { top: 50, bottom: 50, left: 50, right: 50 };
					map.fitBounds(coor.arr, { padding, linear: false, animate: true, duration: 3000 });
				}
			});

			function handleMouseEnter(e, popup) {
				map.getCanvas().style.cursor = 'pointer';
				if (e.features && e.features.length) {
					const coordinates = e.lngLat;
					/**
					 * @type [number, number]
					 */
					const coordinatesArray = [coordinates.lng, coordinates.lat];
					const id = e.features[0].properties.id;
					const idx = metadata.findIndex((m) => m.id === id);
					let image = metadata[idx].images_hist[0].image_url;
					image = image.replace(/\/large\//g, '/medium/');
					const name = metadata[idx].title;
					// Create the popup HTML content
					const popupContent = `
					<div style="background-color: #d9d9d9; text-align: center;">
						<div style="display: inline-block; position: relative; max-width: 100%; max-height: 37.035vh; vertical-align: middle;">
							<img src="${image}" alt="${name}" style="max-width: 100%; max-height: 100%; object-fit: contain; display: block; margin: 0 auto;" />
						</div>
						<p>${name}</p>
					</div>
					`;

					hoveredPointId = e.features[0].properties.id;
					if (hoveredPointId !== null) {
						map.setFeatureState({ source: 'sculptures', id: hoveredPointId }, { hover: false });
					}

					map.setFeatureState({ source: 'sculptures', id: hoveredPointId }, { hover: true });

					while (Math.abs(e.lngLat.lng - coordinatesArray[0]) > 180) {
						coordinatesArray[0] += e.lngLat.lng > coordinatesArray[0] ? 360 : -360;
					}
					if (popup) {
						popup.remove();
					}
					popup = new maplibregl.Popup({
						closeButton: false,
						closeOnClick: false,
						maxWidth: '300px'
					})
						.setLngLat(coordinatesArray)
						.setHTML(popupContent)
						.addTo(map);
				}
				return popup;
			}

			function handleMouseLeave(e, popup) {
				map.getCanvas().style.cursor = '';
				hoveredPointId = null;
				popup.remove();
				popup = null;
				return popup;
			}

			map.on('mouseenter', 'today-points', (e) => {
				popup = handleMouseEnter(e, popup);
			});
			map.on('mouseenter', 'hist-points', (e) => {
				popup = handleMouseEnter(e, popup);
			});
			map.on('mouseleave', 'today-points', (e) => {
				popup = handleMouseLeave(e, popup);
			});
			map.on('mouseleave', 'hist-points', (e) => {
				popup = handleMouseLeave(e, popup);
			});

			map.on('mouseenter', 'lines', (e) => {
				map.getCanvas().style.cursor = 'pointer';
				if (e.features && e.features.length) {
					hoveredLineId = e.features[0].properties.id;
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

	function resetZoom() {
		console.log('Resetting zoom...');
		setTimeout(() => {
			const lon_min = Math.min(mdrow.lon_today, mdrow.lon_hist);
			const lon_max = Math.max(mdrow.lon_today, mdrow.lon_hist);
			const lat_min = Math.min(mdrow.lat_today, mdrow.lat_hist);
			const lat_max = Math.max(mdrow.lat_today, mdrow.lat_hist);
			const bbox = [lon_min, lat_min, lon_max, lat_max];
			console.log(bbox);
			const padding = { top: 100, bottom: 50, left: 50, right: 50 };
			map.fitBounds(bbox, { padding, linear: false, animate: true, duration: 3000 });
		}, 500);
	}

	function resetMap() {
		if (map) {
			map.setCenter([7.25, 47.15]);
			map.setZoom(13);
			showLeft = false;
			showRight = false;
			map.setLayoutProperty('lines', 'visibility', 'none');
		}
	}

	$effect(() => {
		checkedShowHist = checkedShowHist;
		checkedShowToday = checkedShowToday;
		if (map && map.loaded()) {
			map.setLayoutProperty('hist-points', 'visibility', checkedShowHist ? 'visible' : 'none');
			map.setLayoutProperty('today-points', 'visibility', checkedShowToday ? 'visible' : 'none');
		}
	});
</script>

<div id="map-container" style="width: {mapWidth}; left: {mapLeft};">
	<div id="map">
		<div
			style="position: absolute; z-index:10; color:black; top:3vh; left:1vw; background-color: #d9d9d9;"
		>
			<label
				><input type="checkbox" bind:checked={checkedShowHist} />
				seuls emplacements <span style="color: red;">d'origine</span> / nur
				<span style="color: red;">ursprüngliche</span> Standorte</label
			>

			<br />
			<label
				><input type="checkbox" bind:checked={checkedShowToday} />
				seuls emplacements <span style="color: blue;">actuels</span> / nur
				<span style="color: blue;">aktuelle</span> Standorte</label
			>
			<br />
			<button onclick={resetMap} style="width: 100%;"
				>réinitialiser la carte / Karte zurücksetzen</button
			>
		</div>
	</div>
</div>

<div>
	{#if showLeft}
		<Popup {metadata} bind:popup_id side="left" bind:showLeft bind:showRight {resetZoom} />
	{/if}

	{#if showRight}
		<Popup {metadata} bind:popup_id side="right" bind:showLeft bind:showRight {resetZoom} />
	{/if}
</div>
