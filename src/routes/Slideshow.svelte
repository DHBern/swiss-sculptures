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
			<div class="slide-container {index === currentIndex ? 'active' : ''}">
				<img src={image} alt="Sculptures" class="slide" />
			</div>
		{/if}
	{/each}
</div>

<style>
	.slideshow-container {
		position: relative;
		width: 100%;
		height: 100%;
		margin: 0;
		overflow: hidden;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.slide-container {
		position: absolute;
		width: 100%;
		height: 100%;
		display: none;
		justify-content: center;
		align-items: center;
	}

	.slide {
		max-width: 100%;
		object-fit: contain;
	}

	.active {
		display: flex;
	}
</style>
