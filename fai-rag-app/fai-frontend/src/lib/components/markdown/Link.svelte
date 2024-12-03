<script>
  export let href = ''
  export let title = undefined

  const isExternalLink = (href) => {
    try {
      const url = new URL(href, window.location.origin)
      return url.origin !== window.location.origin
    } catch (e) {
      return false
    }
  }

  $: target = isExternalLink(href) ? '_blank' : null
</script>

<a {href} {title} {target}><slot></slot></a>
