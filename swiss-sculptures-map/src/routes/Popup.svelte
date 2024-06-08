<script>
    import { onMount } from 'svelte';
    import { queryGeoJSON } from '../queryGeoJSON';

    export let popup_id;
    export let showLeft = false;
    export let showRight = false;

    /**
     * @type {import("../queryGeoJSON").GeoJSONFeature[]}
     */
    let qf;

    // Reactively fetch queriedFeature whenever popup_id changes
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

<style>
    .left, .right {
        position: absolute;
        top: 0;
        height: 800px;
        width: 500px;
        display: none; /* Initially hide both left and right pop-ups */
    }

    .left {
        left: 0;
        background-color: #D9D9D9;
    }

    .right {
        right: 0;
        background-color: #D9D9D9;
    }
</style>

{#if showLeft}
<div class="left flex flex-col justify-center items-center bg-gray-900 text-white fixed w-1/4">
    p id : {popup_id}
    {#if qf}
        {#each qf as queriedFeature}
            <h3>Queried Feature ID: {queriedFeature}</h3>
            <!-- Display other properties of queriedFeature as needed -->
        {/each}
    {:else}
        <p>Loading...</p>
    {/if}
</div>
{/if}

{#if showRight}
<div class="right flex flex-col justify-center items-center bg-gray-800 text-white fixed w-1/4">
    p id : {popup_id}
    {#if qf}
        {#each qf as queriedFeature}
            <h3>Queried Feature ID: {queriedFeature}</h3>
            <!-- Display other properties of queriedFeature as needed -->
        {/each}
    {:else}
        <p>Loading...</p>
    {/if}
</div>
{/if}
