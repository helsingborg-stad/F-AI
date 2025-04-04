<script lang="ts">
  interface Props {
    initialId: string
    initialIsIdSubmitted: boolean
    errorMessage: string
    requestId: string
  }

  let {
    initialId,
    initialIsIdSubmitted,
    errorMessage,
    requestId,
  }: Props = $props()

  let id = $state(initialId)
  let isIdSubmitted = $state(initialIsIdSubmitted)
  let otp = $state('')
  let processingForm = $state(false)

  let isIdValidEmail = $derived.by(() => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    return emailRegex.test(id)
  })

  let isOtpCodeValid = $derived.by(() => {
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
    {#if !isIdSubmitted}
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
          <div class="mb-4">
            <p>{errorMessage}</p>
          </div>
          <button
            class="btn btn-primary btn-block"
            disabled={!isIdValidEmail || processingForm}
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
        <input type="hidden" name="request_id" value={requestId}>
        <input type="hidden" name="email" value={id}>
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
          <div class="mb-4">
            <p>{errorMessage}</p>
          </div>
          <button
            class="btn btn-primary btn-block"
            disabled={!isOtpCodeValid || processingForm}
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