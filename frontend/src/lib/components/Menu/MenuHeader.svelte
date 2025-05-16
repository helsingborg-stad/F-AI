<script lang="ts">
  import Icon from '$lib/components/Icon/Icon.svelte'
  import { icons } from '$lib/components/Icon/icons.js'

  interface Props {
    title: string;
    iconName: keyof typeof icons;
    onClick?: () => void;
  }

  const { title, iconName, onClick = () => {} }: Props = $props()
</script>

<ul class="menu">
  <li>
    <button onclick={onClick}>
      {#if iconName && icons[iconName]}
        <Icon icon={ icons[iconName] } />
      {/if}
      <span class="uppercase">{title}</span>
    </button>
  </li>
</ul>