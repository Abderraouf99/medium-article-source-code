<script lang="ts">
  import { Button, Tile } from "carbon-components-svelte";
  import { Add } from "carbon-icons-svelte";
  import ChatBox from "./ChatBox.svelte";
  import ChatRoomsList from "./ChatRoomsList.svelte";
  import Spacer from "./Spacer.svelte";

  export let userName: string;

  let open = false;
  let activeRoomID = "";

  function handleRoomChange(event: CustomEvent) {
    console.log("[ChatView]: room changed");
    activeRoomID = event.detail.room;
  }
</script>

<Tile>
  <div class="grid-2">
    <div class="rooms">
      <ChatRoomsList on:room={handleRoomChange} />
    </div>

    <div class="discussion">
      <ChatBox roomId={activeRoomID} {userName} />
    </div>
  </div>
</Tile>

<style>
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

  .discussion {
    grid-area: discussion;
  }
</style>
