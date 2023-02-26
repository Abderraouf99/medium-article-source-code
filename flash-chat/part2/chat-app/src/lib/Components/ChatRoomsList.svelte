<script lang="ts">
  import {
    Button,
    Modal,
    TextArea,
    TextInput,
    Tile,
  } from "carbon-components-svelte";
  import { Add } from "carbon-icons-svelte";
  import { createEventDispatcher, onDestroy, onMount } from "svelte";
  import type { Room } from "../models/room";
  import type { SnackbarMessage } from "../models/snackbar-message";
  import Snackbar from "./Snackbar.svelte";
  import Spacer from "./Spacer.svelte";

  let roomsSockets: WebSocket;
  let rooms: Room[] = [];
  let activeRoomName: string = "";
  let open = false;

  let roomName: string = "";
  let roomDescription: string = "";

  let snackbarMessage: SnackbarMessage = {
    message: "",
    kind: "error",
    show: false,
    title: "",
  };

  onMount(handleOnMount);
  onDestroy(handleOnDestroy);

  const roomsDispatcher = createEventDispatcher();

  function handleOnMount() {
    roomsSockets = new WebSocket("ws://localhost:8000/rooms");
    roomsSockets.onopen = () => {
      snackbarMessage = {
        message: "Connected to server",
        kind: "success",
        show: true,
        title: "Success",
      };
    };
    roomsSockets.onmessage = (event) => {
      const roomRaw = JSON.parse(event.data);
      rooms = [
        ...rooms,
        {
          id: roomRaw.__id,
          name: roomRaw.name,
          description: roomRaw.description,
        },
      ];
      // making sure that the first room is selected by default
      if (activeRoomName == "" && rooms.length > 0) {
        activeRoomName = rooms[0].name;
        roomsDispatcher("room", { room: activeRoomName });
      }
    };

    roomsSockets.onclose = () => {
      snackbarMessage = {
        message: "Disconnected from server",
        kind: "error",
        show: true,
        title: "Error",
      };
    };
  }

  function handleOnDestroy() {
    roomsSockets.close();
  }

  async function handleRoomSelect(id: string) {
    activeRoomName = id;
    roomsDispatcher("room", { room: activeRoomName });
  }

  async function handleCreateRoom() {
    try {
      if (roomName == "") throw new Error("Name cannot be empty");
      const response = await fetch(`http://localhost:8000/add-room/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: roomName,
          description: roomDescription,
        }),
      });
      if (response.status != 201) throw new Error("Error creating room");
      snackbarMessage = {
        message: "Room created successfully",
        kind: "success",
        show: true,
        title: "Success",
      };
    } catch (error) {
      snackbarMessage = {
        message: error.message,
        kind: "error",
        show: true,
        title: "Error",
      };
    }
    roomName = "";
    open = false;
  }
</script>

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
  {#each rooms as room}
    <div class="room-tile" class:selected={activeRoomName === room.name}>
      <Tile light on:click={() => handleRoomSelect(room.name)}>
        <h4 class="room-header">{room.name}</h4>
        <p class="room-description">{room.description}</p>
      </Tile>
    </div>
    <Spacer space={20} orientation="vertical" />
  {/each}
</div>

<Modal
  bind:open
  modalHeading="Create a room"
  primaryButtonText="Create"
  primaryButtonIcon={Add}
  secondaryButtonText="Cancel"
  shouldSubmitOnEnter
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
  .rooms-list {
    max-height: 500px;
    overflow-y: scroll;
    overflow-x: hidden;
  }
  .room-tile {
    cursor: pointer;
    width: 98%;
    border: 1px solid transparent;
  }

  .selected {
    border: 1px solid #0062ff;
  }
  .room-header {
    font-weight: bold;
  }
  .room-description {
    opacity: 0.8;
  }
</style>
