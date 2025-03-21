<script lang="ts">
  let { form } = $props()

  let id = $state(form?.email || '')
  let isIDSubmitted = $state(form?.isIDSubmitted || false)
  let otp = $state('')
  let processingForm = $state(false)

  let isIDValidEmail = $derived.by(() => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    return emailRegex.test(id)
  })

  let isOTPCodeValid = $derived.by(() => {
    return otp.length > 0
  })

  function handleEmailChange(e: Event) {
    id = (e.target as HTMLInputElement).value
  }

  function handleOTPChange(e: Event) {
    otp = (e.target as HTMLInputElement).value
  }

  function handleForm() {
    processingForm = true
  }
</script>

<div class="card w-96 bg-base-100 shadow-sm">
  <div class="card-body">
    {#if !isIDSubmitted}
      <form method="POST" action="?/initiateOTP" onsubmit={handleForm}>
        <h2 class="text-3xl font-bold">Login to your account</h2>
        <p class="mt-4 mb-2 text-sm text-gray-500">Enter your email address</p>
        <label class="form-control w-full max-w-xs">
          <input
            type="email"
            name="email"
            value={id}
            oninput={handleEmailChange}
            class="input input-bordered w-full max-w-xs"
            placeholder="your-email@helsingborg.se"
          />
        </label>
        <div class="mt-6">
          <button
            class="btn btn-primary btn-block"
            disabled={!isIDValidEmail || processingForm}
          >
            Continue with email
            {#if processingForm}
              <span class="loading loading-spinner"></span>
            {/if}
          </button>
        </div>
      </form>
    {:else}
      <form method="POST" action="?/confirmOTP" onsubmit={handleForm}>
        <input type="hidden" name="request_id" value={form?.request_id}>
        <h2 class="text-3xl font-bold">Enter verification code</h2>
        <p class="mt-4 mb-2 text-sm text-gray-500">Enter the code sent to your email {id}</p>
        <label class="form-control w-full max-w-xs">
          <input
            type="text"
            name="OTPCode"
            value={otp}
            oninput={handleOTPChange}
            class="input input-bordered w-full max-w-xs"
            placeholder="1234"
          />
        </label>

        <div class="mt-6">
          <button
            class="btn btn-primary btn-block"
            disabled={!isOTPCodeValid || processingForm}
          >
            Verify email address
            {#if processingForm}
              <span class="loading loading-spinner"></span>
            {/if}
          </button>
        </div>
      </form>
    {/if}
  </div>
</div>
