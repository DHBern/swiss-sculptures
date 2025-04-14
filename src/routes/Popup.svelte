<script>
	import { run, preventDefault } from 'svelte/legacy';

	import { queryGeoJSON } from '../queryGeoJSON';
	import { createEventDispatcher } from 'svelte';
	import Slideshow from './Slideshow.svelte';
	import { Hr } from 'flowbite-svelte';

	/** @type {{popup_id: number | undefined, showLeft?: boolean, showRight?: boolean, a?: boolean}} */
	let { popup_id, showLeft = false, showRight = false, a = false } = $props();

	/**
	 * @type {import("../queryGeoJSON").GeoJSONFeature[] | { properties: { image: string[]; }; }[]}
	 */
	let qf = $state();
	/**
	 * @type any
	 */
	let imgElementLeft = $state();

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
	run(() => {
		if (popup_id !== undefined) {
			(async () => {
				try {
					const { queriedFeatures } = await queryGeoJSON(popup_id);
					qf = queriedFeatures;
				} catch (error) {
					console.error('Error querying GeoJSON:', error);
				}
			})();
		}
	});
</script>

{#if showLeft}
	<div class="left">
		<button class="close-btn" onclick={closeL}>x</button>
		{#if qf}
			{#each qf as queriedFeature}
				{#if queriedFeature.properties.period == 'old'}
					<div class="grid-item">
						<div class="popup_title">{queriedFeature.properties.sculpture_name}</div>
						<div
							style="position: relative; overflow: hidden; height: 37.035vh; width: auto; max-height: 37.035vh; border-style: solid; border-color:red;"
							bind:this={imgElementLeft}
						>
							<Slideshow images={queriedFeature.properties.image} />
						</div>
						<div class="info">
							{#if a}
								<a
									href="none"
									style="color:black; text-decoration: none;"
									onclick={preventDefault(showNewPopup)}
								>
									<span style="font-size: 0.8vw;"
										>aller à l’emplacement actuel / zum aktuellen Standort</span
									>
									<span style="color: blue;">&#9654;</span>
								</a>
							{/if}
							<Hr classHr="my-8" />
							<h4>Artiste / Künstler*in:</h4>
							<p>
								{queriedFeature.properties.sculptor} ({queriedFeature.properties.historic_year})
							</p>
							<Hr classHr="my-8" />
							<h4>Photographe / Fotograf*in:</h4>
							<p>{queriedFeature.properties.photographer}</p>
							<Hr classHr="my-8" />
							<h4>Lieu / Ort:</h4>
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
		<button class="close-btn" onclick={closeR}>x</button>
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
							{#if a}
								<a
									href="none"
									style="color:black; text-decoration: none;"
									onclick={preventDefault(showOldPopup)}
								>
									<span style="color: red;">&#9664;</span>
									<span style="font-size: 0.8vw;"
										>aller à l'emplacement d’origine / zum ursprünglichen Standort</span
									>
								</a>
							{/if}
							<Hr classHr="my-8" />
							<h4>Artiste / Künstler*in:</h4>
							<p>
								{queriedFeature.properties.sculptor} ({queriedFeature.properties.historic_year})
							</p>
							<Hr classHr="my-8" />
							<h4>Photographe / Fotograf*in:</h4>
							<p>{queriedFeature.properties.photographer}</p>
							<Hr classHr="my-8" />
							<h4>Lieu / Ort:</h4>
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
