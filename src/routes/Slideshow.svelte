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
		<div class="slide-container active">
			<img
				src="{base}/default-img.png"
				alt="Sculptures"
				style="max-width: 100%; max-height: 100%; object-fit: cover;"
			/>
		</div>
	{/if}
	{#each images as image, index}
			<div class="slide-container {index === currentIndex ? 'active' : ''}">
				<img src={image.image_url} alt="Sculptures" class="slide" />
			</div>
				<p>
					<span style="font-weight: bold;">Photographe / Fotograf*in:</span>
					{image.image_credits}
				</p>
	{/each}
</div>
