<script lang="ts">
  import Div from "./Div.svelte";
  import Button from "./Button.svelte";
  import ChatBubble from "./ChatBubble.svelte";
  import SvelteMarkdown from "svelte-markdown";

  interface SSEMessage {
    type: string;
    date: string;
    source: string | null;
    content: string | null;
  }

  interface ChatMessage {
    id: string;
    user: string;
    content: string;
    time: string;
    isSelf: boolean;
  }

  interface Assistant {
    id: string;
    name: string;
    project: string;
    description: string;
  }

  export let endpoint: string;
  export let assistants: Assistant[];

  let selectedAssistantId: string;
  let activeConversationId: string | null = null;
  let messages: ChatMessage[] = [];
  let currentMessageInput: string = "";
  let eventSource: EventSource | null = null;

  let contentScrollDiv: Element;
  let isContentAtBottom: Boolean = true;

  $: isContentAtBottom = messages.length == 0 || isContentAtBottom;

  function handleContentScroll() {
    const scrollPadding = 10;
    const isScrollable = contentScrollDiv.scrollHeight > contentScrollDiv.clientHeight || contentScrollDiv.scrollWidth > contentScrollDiv.clientWidth;
    isContentAtBottom = !isScrollable || (contentScrollDiv.scrollHeight - contentScrollDiv.scrollTop < contentScrollDiv.clientHeight + scrollPadding);
  }

  function scrollContentToBottom() {
    contentScrollDiv.scrollTop = contentScrollDiv.scrollHeight;
  }

  function addErrorMessage(message: string) {
    messages = [...messages, {
      id: `error${messages.length}`,
      user: "Error",
      content: message,
      time: new Date().toTimeString().split(" ")[0],
      isSelf: false
    }];
  }

  function toChatMessage(sse: SSEMessage): ChatMessage {
    return {
      id: sse.date,
      user: sse.source ?? "",
      content: sse.content ?? "",
      time: sse.date,
      isSelf: false
    };
  }

  function clearChat() {
    messages = [];
    activeConversationId = null;
  }

  function closeSSE() {
    eventSource?.close();
    eventSource = null;
  }

  function createSSE(question: string) {
    try {
      if (question.length == 0) return;
      currentMessageInput = "";

      messages = [...messages, {
        id: `self${messages.length}`,
        isSelf: true,
        user: "Me",
        content: question,
        time: new Date().toTimeString().split(" ")[0]
      }, {
        id: `placeholder${messages.length}`,
        isSelf: false,
        user: "",
        content: "",
        time: ""
      }];

      closeSSE();

      const selectedAssistant = assistants.find(a => a.id === selectedAssistantId)!;

      eventSource = new EventSource(`${endpoint}/${selectedAssistant.project}/${selectedAssistant.id}?question=${question}&conversation_id=${activeConversationId ?? ""}`);

      eventSource.onerror = (e) => {
        addErrorMessage(`unknown error / ${e}`);
        closeSSE();
      };

      eventSource.addEventListener("message_end", () => {
        closeSSE();
        return;
      });

      eventSource.addEventListener("conversation_id", (e) => {
        activeConversationId = e.data;
        console.log(`got conversation id ${e.data}`);
      });

      eventSource.addEventListener("message", (e) => {
        try {
          const bytes = Uint8Array.from(atob(e.data), (m) => m.codePointAt(0)!);
          const jsonString = new TextDecoder().decode(bytes);
          const messagePayload = JSON.parse(jsonString) as SSEMessage;
          const chatMessage = toChatMessage(messagePayload);

          messages = [...messages.slice(0, -1), {
            ...messages.at(-1),
            ...chatMessage,
            content: messages.at(-1)!.content + chatMessage.content
          }];
        } catch (ex) {
          console.error("Failed to parse raw message", ex, e);
          closeSSE();
        }
      });
    } catch (e) {
      closeSSE();
      console.error("createSSE error", e);
      addErrorMessage(e?.toString() ?? "unknown");
    }
  }

  function handleTextareaKeypress(event: KeyboardEvent) {
    if (event.key == "Enter" && !event.shiftKey) {
      event.preventDefault();
      createSSE(currentMessageInput);
    }
  }

  function formatMessageForMarkdown(content: string): string {
    return content
      .replace(/\n/g, `\n\n  `);
  }
</script>

<Div class="h-full relative">

  <!-- Document picker -->
  <Div class="h-24 p-4 absolute inset-x-0 top-0 flex flex-col gap-1 justify-center items-center">
    <select
      class="select select-bordered w-full max-w-xs"
      bind:value={selectedAssistantId}
      on:change={clearChat}
    >
      <option disabled selected value="">Choose assistant</option>
      {#each assistants as assistant (`${assistant.project}/${assistant.id}`)}
        <option value={assistant.id}>{assistant.name}</option>
      {/each}
    </select>
    <p class="text-sm" class:invisible={!activeConversationId}>conversation id: {activeConversationId}</p>
  </Div>

  <!-- Chat content -->
  <Div class="w-full grow flex flex-col gap-2 items-center justify-center absolute top-24 bottom-28">

    <!-- Chat bubbles -->
    <div
      class="grow w-full relative max-w-prose overflow-y-auto"
      bind:this={contentScrollDiv}
      on:scroll={handleContentScroll}
    >
      {#each messages as message (message.id)}
        <ChatBubble
          user={message.user}
          content={formatMessageForMarkdown(message.content)}
          time={message.time}
          isSelf={message.isSelf}
        />
      {:else}
        <div class="prose text-center">
          {#if selectedAssistantId}
            <SvelteMarkdown source={assistants.find(a => a.id === selectedAssistantId)?.description} />
          {:else}
            <p>Here you can chat with any specialized assistant that has been created for you.</p>
            <p>Choose an assistant from the dropdown to begin.</p>
          {/if}
        </div>
      {/each}

      <span class="loading loading-spinner" class:opacity-0={!eventSource} />
    </div>


    <div class="flex justify-center absolute inset-x-0 bottom-20"
         class:hidden={isContentAtBottom}
    >
      <Button
        onClick={scrollContentToBottom}
        label=""
        iconSrc="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWFycm93LWJpZy1kb3duLWRhc2giPjxwYXRoIGQ9Ik0xNSA1SDkiLz48cGF0aCBkPSJNMTUgOXYzaDRsLTcgNy03LTdoNFY5eiIvPjwvc3ZnPg=="
      />
    </div>

    <!-- Clear button -->
    {#if messages.length > 0}
      <Button
        onClick={clearChat}
        label="Rensa chat"
        state="secondary"
        disabled={!!eventSource} />
    {/if}
  </Div>

  <!-- Form controls -->
  <Div class="h-28 p-3 absolute inset-x-0 bottom-0">
    <form class="w-full h-full">
      <fieldset
        disabled={!selectedAssistantId}
        class="h-full"
      >
        <Div class="flex gap-2 w-full h-full items-end">
        <textarea
          name="message"
          bind:value={currentMessageInput}
          on:keydown={handleTextareaKeypress}
          class="textarea textarea-bordered grow h-full"
        />
          <Button
            onClick={()=>createSSE(currentMessageInput)}
            label=""
            iconSrc="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXNlbmQiPjxwYXRoIGQ9Im0yMiAyLTcgMjAtNC05LTktNFoiLz48cGF0aCBkPSJNMjIgMiAxMSAxMyIvPjwvc3ZnPg=="
          />
        </Div>
      </fieldset>
    </form>
  </Div>
</Div>
