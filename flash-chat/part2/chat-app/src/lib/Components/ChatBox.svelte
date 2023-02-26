<script lang="ts">
  import { Tile, TextInput, Button, Loading } from "carbon-components-svelte";

  import Send from "carbon-icons-svelte/lib/Send.svelte";
  import { afterUpdate, onDestroy, onMount } from "svelte";
  import type Message from "../models/message";
  import Spacer from "./Spacer.svelte";

  export let roomId: string;
  export let userName: string;

  let messageText: string = "";

  let messages: Message[] = [];

  let messageSockets: WebSocket;

  let wrapperContainer = undefined;

  $: {
    connectToRoomWith(roomId);
  }

  afterUpdate(() => {
    if (wrapperContainer !== undefined) {
      scrollToBottom(wrapperContainer);
    }
  });

  const scrollToBottom = async (node) => {
    node.scroll({ top: node.scrollHeight, behavior: "smooth" });
  };

  function forceDisconnect() {
    try {
      messageSockets.send(JSON.stringify({ type: "close" }));
      messageSockets.close(1000, "Closing socket");
    } catch (e) {
      console.log("Failed to close socket");
    }
  }
  function connectToRoomWith(id: string) {
    if (roomId == "") return;

    if (messageSockets !== null && messageSockets !== undefined) {
      forceDisconnect();
    }

    messages = [];

    messageSockets = new WebSocket("ws://localhost:8000/connect-rooms/" + id);
    messageSockets.onopen = () => {};
    messageSockets.onmessage = (event) => {
      const data = JSON.parse(event.data);

      messages = [
        ...messages,
        {
          message: data.message,
          userId: data.user_id,
          roomId: data.room_id,
        },
      ];

      scrollToBottom(wrapperContainer);
    };
    messageSockets.onerror = (event) => {
      messages = [];
    };
    messageSockets.close = (event) => {
      messages = [];
    };
  }

  onMount(() => connectToRoomWith(roomId));

  onDestroy(forceDisconnect);

  function handleSendMessage() {
    if (messageText === "" || roomId === "") return;
    console.log(userName);
    messageSockets.send(
      JSON.stringify({
        message: messageText,
        user_id: userName,
        room_id: roomId,
      })
    );

    messageText = "";
  }
</script>

{#if roomId !== ""}
  <Tile>
    <div class="wrapper" bind:this={wrapperContainer}>
      <div class="message-list">
        {#if messages.length > 0}
          {#each messages as message}
            <div
              class="message"
              class:sent-message={message.userId === userName}
              class:received-message={message.userId !== userName}
            >
              <p class="message-text">{message.message}</p>
              <p class="message-sender">{message.userId}</p>
            </div>
          {/each}
        {:else}
          <div class="no-messages">No messages</div>
        {/if}
      </div>
    </div>
    <div class="tile-actions">
      <TextInput
        labelText="Message"
        placeholder="Enter a message..."
        bind:value={messageText}
      />
      <Button type="submit" icon={Send} on:click={handleSendMessage}
        >Send</Button
      >
    </div>
  </Tile>
{:else}
  <div class="centered-loader">
    <Loading withOverlay={false} />
    <Spacer space={10} />
    <p>We are waiting for rooms to load</p>
  </div>
{/if}

<style>
  .wrapper {
    overflow-y: scroll;
    overflow-x: hidden;
    height: 500px;
    width: 600px;
    min-height: 500px;
    min-width: 600px;
  }

  .message-list {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 10px;
    height: 100%;
  }

  .message {
    padding: 10px;
    margin-top: 10px;
    width: 50%;
    max-width: 50%;
    min-width: 50%;
  }
  .message-text {
    word-wrap: break-word;
  }
  .sent-message {
    align-self: flex-end;
    background-color: #0062ff;
  }
  .received-message {
    align-self: flex-start;
    background-color: grey;
  }
  .tile-actions {
    display: flex;
    align-items: flex-end;
    padding: 10px;
  }
  .no-messages {
    text-align: center;
    padding: 10px;
  }
  .centered-loader {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
  }
  .message-sender {
    font-size: 12px;
    text-align: right;
  }
</style>
