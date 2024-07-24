<script>
	import { queryGeoJSON } from '../queryGeoJSON';
	import { createEventDispatcher } from 'svelte';
	import Slideshow from './Slideshow.svelte';
	import { Hr } from 'flowbite-svelte';

	/**
	 * @type {number | undefined}
	 */
	export let popup_id;
	export let showLeft = false;
	export let showRight = false;

	/**
	 * @type {import("../queryGeoJSON").GeoJSONFeature[] | { properties: { image: string[]; }; }[]}
	 */
	let qf;
	/**
	 * @type any
	 */
	let imgElementLeft;

	// Create an event dispatcher
	const dispatch = createEventDispatcher();

	// Close left
	function closeL() {
		dispatch('closeL', false);
	}

	// Close Right
	function closeR() {
		dispatch('closeR', false);
	}
	function showOldPopup() {
		dispatch('showOldPopup', { id: popup_id });
	}
	function showNewPopup() {
		dispatch('showNewPopup', { id: popup_id });
	}

	// Fetch queriedFeature whenever popup_id changes
	$: if (popup_id !== undefined) {
		(async () => {
			try {
				const { queriedFeatures } = await queryGeoJSON(popup_id);
				qf = queriedFeatures;
			} catch (error) {
				console.error('Error querying GeoJSON:', error);
			}
		})();
	}
</script>

{#if showLeft}
	<div class="left">
		<button class="close-btn" on:click={closeL}>x</button>
		{#if qf}
			{#each qf as queriedFeature}
				{#if queriedFeature.properties.period == 'old'}
					<div class="grid-item">
						<div class="popup_title">{queriedFeature.properties.sculpture_name}</div>
						<div
							style="position: relative; overflow: hidden; height: 37.035vh; width: 100%; min-height: 37.035vh; border-style: solid; border-color:red;"
							bind:this={imgElementLeft}
						>
							<Slideshow images={queriedFeature.properties.image} />
						</div>
						<div class="info">
							<a
								href="none"
								style="color:black; text-decoration: none;"
								on:click|preventDefault={showNewPopup}
							>
								<span style="font-size: 0.8vw;"
									>aller à l’emplacement actuel / zum aktuellen Standort</span
								>
								<span style="color: blue;">&#9654;</span>
							</a>
							<Hr classHr="my-8" />
							<h4>Künstler*in:</h4>
							<p>
								{queriedFeature.properties.sculptor} ({queriedFeature.properties.historic_year})
							</p>
							<Hr classHr="my-8" />
							<h4>Fotograf*in:</h4>
							<p>{queriedFeature.properties.photographer}</p>
							<Hr classHr="my-8" />
							<h4>Adresse:</h4>
							<p>{queriedFeature.properties.location}</p>
						</div>
					</div>
				{/if}
			{/each}
		{:else}
			<p>Loading...</p>
		{/if}
	</div>
{/if}

{#if showRight}
	<div class="right">
		<button class="close-btn" on:click={closeR}>x</button>
		{#if qf}
			{#each qf as queriedFeature}
				{#if queriedFeature.properties.period == 'new'}
					<div class="grid-item">
						<div class="popup_title">{queriedFeature.properties.sculpture_name}</div>
						<div
							style="position: relative; overflow: hidden; height: 37.035vh; width: 100%; min-height: 37.035vh; border-style: solid; border-color:blue;"
							bind:this={imgElementLeft}
						>
							<Slideshow images={queriedFeature.properties.image} />
						</div>
						<div class="info">
							<a
								href="none"
								style="color:black; text-decoration: none;"
								on:click|preventDefault={showOldPopup}
							>
								<span style="color: red;">&#9664;</span>
								<span style="font-size: 0.8vw;"
									>aller à l'emplacement d’origine / zum ursprünglichen Standort</span
								>
							</a>
							<Hr classHr="my-8" />
							<h4>Künstler*in:</h4>
							<p>
								{queriedFeature.properties.sculptor} ({queriedFeature.properties.historic_year})
							</p>
							<Hr classHr="my-8" />
							<h4>Fotograf*in:</h4>
							<p>{queriedFeature.properties.photographer}</p>
							<Hr classHr="my-8" />
							<h4>Adresse:</h4>
							<p>{queriedFeature.properties.location}</p>
						</div>
					</div>
				{/if}
			{/each}
		{:else}
			<p>Loading...</p>
		{/if}
	</div>
{/if}
