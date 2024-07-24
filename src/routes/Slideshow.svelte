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
	{#if images.length === 0}
		<div class="slide-container active">
			<img
				src="/default-img.png"
				alt="Sculptures"
				style="object-fit: contain; width:100%; height:100%;"
			/>
		</div>
	{/if}
	{#each images as image, index}
		{#if image && image !== ''}
			<div class="slide-container {index === currentIndex ? 'active' : ''}">
				<img src={image} alt="Sculptures" class="slide" />
			</div>
		{/if}
	{/each}
</div>
