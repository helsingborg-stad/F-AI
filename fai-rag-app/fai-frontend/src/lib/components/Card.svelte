<script>
    export let title = "";
    export let description = "";
    export let imageSrc = "";
    export let imageAlt = "";
    export let compact = false;
    export let badge = "";
    export let actionText = "Buy Now";
    export let cardStyle = "";
    export let badgeStyle = "";
    export let centered = false;
    export let noImage = false;
    export let customColor = false;
    export let neutralColor = false;
    export let actionOnTop = false;
    export let glassStyle = false;
    export let imageOnSide = false;
    export let responsive = false;
</script>

<div class={`card w-96 bg-base-100 shadow-xl ${cardStyle} ${compact ? 'card-compact' : ''} ${centered ? 'items-center text-center' : ''} ${neutralColor ? 'bg-neutral text-neutral-content' : ''} ${customColor ? 'bg-primary text-primary-content' : ''} ${glassStyle ? 'glass' : ''} ${imageOnSide || responsive ? 'card-side' : ''} ${responsive ? 'lg:card-side' : ''}`}>
    {#if !noImage}
        <figure class={`${centered ? 'px-10 pt-10' : ''}`}>
            <img src={imageSrc} alt={imageAlt} class={`${centered ? 'rounded-xl' : ''}`}/>
        </figure>
    {/if}
    <div class="card-body">
        {#if actionOnTop}
            <!-- Place for top action button -->
        {/if}
        <h2 class="card-title">
            {title}
            {#if badge}
                <div class={`badge ${badgeStyle}`}>{badge}</div>
            {/if}
        </h2>
        <p>{description}</p>
        <div class={`justify-end card-actions ${centered ? '' : 'justify-end'}`}>
            <button class="btn btn-primary">{actionText}</button>
        </div>
    </div>
</div>
