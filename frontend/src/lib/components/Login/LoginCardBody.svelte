<script lang="ts">
  type InputType = 'text' | 'password' | 'email' | 'number'

  interface Props {
    type: InputType
    title: string
    description: string
    value: string
    placeholder?: string
    onSubmit: () => void
    isValid: boolean,
    buttonText?: string,
    message?: string,
    onChange: (value: string) => void
  }

  let {
    type,
    title,
    description,
    value,
    placeholder = '',
    onSubmit,
    isValid,
    buttonText = 'Submit',
    message = '',
    onChange,
  }: Props = $props()

  const inputID = `login-input-${Math.random().toString(36).substring(2, 9)}`

  function handleInput(e: Event) {
    const value = (e.target as HTMLInputElement).value
    onChange(value)
  }
</script>

<h2 class="text-3xl font-bold">{title}</h2>
<p class="text-sm text-gray-500">{description}</p>
<label class="form-control w-full max-w-xs">
  <input
    type={type}
    id={inputID}
    oninput={handleInput}
    value={value}
    class="input input-bordered w-full max-w-xs"
    placeholder={placeholder}
  />
</label>
<div class="pt-2 text-center">
  <p>{ message }</p>
</div>
<div class="mt-4">
  <button
    class="btn btn-primary btn-block"
    onclick={() => {onSubmit()}}
    disabled={!isValid}
  >
    {buttonText}
  </button>
</div>