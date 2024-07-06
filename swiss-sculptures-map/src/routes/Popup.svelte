<script>
	import { queryGeoJSON } from '../queryGeoJSON';
	import { createEventDispatcher } from 'svelte';
	import Slideshow from './Slideshow.svelte';

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

	/**
	 * @type any
	 */
	let imgElementRight;

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

	// Fetch queriedFeature whenever popup_id changes
	$: if (popup_id !== undefined) {
		(async () => {
			try {
				const { queriedFeatures } = await queryGeoJSON(popup_id);
				qf = queriedFeatures;
				// Start the slideshow when data is fetched
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
						<div
							style="position: relative; overflow: hidden; height: 37.035vh; width: 100%; min-height: 37.035vh;"
							bind:this={imgElementLeft}
						>
							<Slideshow images={queriedFeature.properties.image} />
						</div>
						<div class="info">
							<h4>Künstler*in:</h4>
							<p>{queriedFeature.properties.scuptor}</p>
							<h4>Fotograf*in:</h4>
							<p>{queriedFeature.properties.photographer}</p>
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
						<div
							style="position: relative; overflow: hidden; height: 37.035vh; width: 100%; min-height: 37.035vh;"
							bind:this={imgElementLeft}
						>
							<Slideshow images={queriedFeature.properties.image} />
						</div>
						<div class="info">
							<h4>Künstler*in:</h4>
							<p>{queriedFeature.properties.scuptor}</p>
							<h4>Fotograf*in:</h4>
							<p>{queriedFeature.properties.photographer}</p>
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

<style>
	.left,
	.right {
		position: absolute;
		top: 0;
		height: 74.07vh;
		width: 26.04vw;
		padding: 0;
		margin: 0;
	}

	.left {
		left: 0;
		background-color: #d9d9d9;
	}

	.right {
		right: 0;
		background-color: #d9d9d9;
	}

	.grid-item {
		padding: 1rem;
		display: flex;
		flex-direction: column;
	}

	.info h4 {
		margin-bottom: 0;
		font-weight: bold;
	}

	.close-btn {
		position: absolute;
		top: 0;
		right: 0;
		background-color: transparent;
		border: 1px solid black;
		cursor: pointer;
		font-size: 1.5rem;
		z-index: 100;
	}
</style>
