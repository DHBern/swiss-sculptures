<script>
	import { base } from '$app/paths';
	import { onDestroy } from 'svelte';

	let { images = [], delay = 3000 } = $props();

	let currentIndex = $state(0);

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
		<div class="slide active">
			<img
				src="{base}/default-img.png"
				alt="Sculptures"
				class="slide-image"
			/>
		</div>
	{/if}
	{#each images as image, index}
			<div class="slide {index === currentIndex ? 'active' : ''}">
				<img src={image.image_url} alt="Sculptures" class="slide-image" />
				<p style="font-size: 7pt; text-align: center;">
					<span style="font-weight: bold;">Photo:</span>
					{image.image_credits}
				</p>
			</div>
	{/each}
</div>
