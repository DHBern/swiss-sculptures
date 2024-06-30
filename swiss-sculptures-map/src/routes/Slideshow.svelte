<script>
	import { onDestroy } from 'svelte';

	/**
	 * @type {string | any[]}
	 */
	export let images = [];
	export let delay = 3000;

	let currentIndex = 0;

	function nextSlide() {
		currentIndex = (currentIndex + 1) % images.length;
	}

	const interval = setInterval(nextSlide, delay);

	onDestroy(() => {
		clearInterval(interval);
	});
</script>

<div class="slideshow-container">
	{#each images as image, index}
		{#if image != '' || image != null}
			<img src={image} alt="Sculptures" class:active={index === currentIndex} class="slide" />
		{/if}
	{/each}
</div>

<style>
	.slideshow-container {
		position: relative;
		width: 100%;
		margin: 0;
		overflow: hidden;
	}

	.slide {
		display: none;
		width: 100%;
	}

	.active {
		display: block;
	}
</style>
