<script lang="ts">
  import {
    Button,
    Modal,
    TextArea,
    TextInput,
    Tile,
  } from "carbon-components-svelte";
  import { Add } from "carbon-icons-svelte";
  import { onMount } from "svelte";
  import type { SnackbarMessage } from "../models/snackbar-message";
  import ChatBox from "./ChatBox.svelte";
  import Snackbar from "./Snackbar.svelte";
  import Spacer from "./Spacer.svelte";

  let open = false;
  let roomName: string = "";
  let roomDescription: string = "";
  let snackbarMessage: SnackbarMessage = {
    message: "",
    kind: "error",
    show: false,
    title: "",
  };
  let socket: WebSocket;
  onMount(() => {
    socket = new WebSocket("ws://localhost:8000/rooms");
    socket.onopen = () => {
      snackbarMessage = {
        message: "Connected to server",
        kind: "success",
        show: true,
        title: "Success",
      };
    };
    socket.onmessage = (event) => {
      console.log(event);
      console.log(event.data);
    };
  });
  async function handleCreateRoom() {
    if (roomName == "") return;
    try {
      await fetch(`http://localhost:8000/add-room`, {
        method: "POST",
        body: JSON.parse(
          JSON.stringify({
            name: roomName,
            description: roomDescription,
          })
        ),
      });
      snackbarMessage = {
        message: "Room created successfully",
        kind: "success",
        show: true,
        title: "Success",
      };
    } catch (e) {
      snackbarMessage = {
        message: "An error occured",
        kind: "error",
        show: true,
        title: "Error",
      };
    }
    roomName = "";
    open = false;
  }
</script>

<Tile>
  <div class="grid-2">
    <div class="rooms">
      <div class="rooms-header">
        <div style="display: flex">
          <img class="icon-small" src="/flash.svg" alt="Flash chat icon" />
          <h2>FlashChat</h2>
        </div>

        <Button kind="ghost" icon={Add} on:click={() => (open = true)}
          >Add a room</Button
        >
      </div>
      <Spacer space={20} orientation="vertical" />
      <div class="rooms-list">
        <Tile light>
          <h4>Main room</h4>
          <h5>Previews fidsjlksjgsgsfgklshjfdkdjsfjskdjffnklfnkds</h5>
          <p>2023-02-19</p>
        </Tile>
      </div>
    </div>

    <div class="discussion">
      <ChatBox />
    </div>
  </div>
</Tile>

<Modal
  bind:open
  modalHeading="Create a room"
  primaryButtonText="Create"
  primaryButtonIcon={Add}
  secondaryButtonText="Cancel"
  shouldSubmitOnEnter
  on:click:button--primary={handleCreateRoom}
  on:submit={handleCreateRoom}
  on:click:button--secondary={() => (open = false)}
>
  <TextInput
    label="Room name"
    placeholder="Wholesome conversation"
    bind:value={roomName}
  />
  <Spacer space={20} />
  <TextArea
    label="Room description"
    placeholder="Room description"
    bind:value={roomDescription}
  />
  <Spacer space={20} orientation="vertical" />
</Modal>
<Snackbar {snackbarMessage} />

<style>
  .icon-small {
    width: 2rem;
    height: 2rem;
    margin-right: 15px;
  }
  .rooms-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .grid-2 {
    display: grid;
    grid-template-columns: 2fr 3fr;
    grid-template-rows: 1fr;
    grid-template-areas: "rooms discussion";
    height: 600px;
    width: 1000px;
  }

  .rooms {
    grid-area: rooms;
  }

  .rooms-list {
    max-height: 500px;
    overflow-y: scroll;
    overflow-x: hidden;
  }

  .discussion {
    grid-area: discussion;
  }
</style>
