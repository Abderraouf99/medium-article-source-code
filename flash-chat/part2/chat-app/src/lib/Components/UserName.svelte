<script lang="ts">
  import { Button, Modal, TextInput } from "carbon-components-svelte";
  import { createEventDispatcher } from "svelte";
  import type { SnackbarMessage } from "../models/snackbar-message";
  import { userStore } from "../stores/user-store";
  import Snackbar from "./Snackbar.svelte";

  let open: boolean = false;
  let userName: string = "";
  let snackbarMessage: SnackbarMessage = {
    kind: "success",
    title: "Success",
    message: "User name set successfully",
    show: false,
  };

  const userNameDispatcher = createEventDispatcher();

  function handleUserNameChange(event: CustomEvent<string>) {
    userName = event.detail;
  }

  async function handleUserNameSubmit() {
    try {
      userStore.update((user) => {
        user.name = userName;
        return user;
      });

      snackbarMessage = {
        kind: "success",
        title: "Success",
        message: "User name set successfully",
        show: true,
      };
    } catch (e) {
      snackbarMessage = {
        kind: "error",
        title: "Error",
        message: "Failed to set user name",
        show: true,
      };
    }
    open = false;
    userNameDispatcher("username", { userName });
  }
</script>

<div>
  <img
    class="about-yourself-illustration"
    src="/undraw_tell_us_about_yourself.svg"
    alt="tell about yourself illustration"
  />
  <div class="spacer" />
  <h2>We need to know who you are !</h2>
  <div class="spacer" />

  <p>Let us know how you want us to call you</p>
  <div class="spacer" />

  <Button on:click={() => (open = true)}>Set your name</Button>
</div>

<Modal
  bind:open
  modalHeading="New user"
  primaryButtonText="Send"
  secondaryButtonText="Cancel"
  shouldSubmitOnEnter
  on:submit={handleUserNameSubmit}
>
  <p>Enter a user name that we will use to refer to you in the application</p>
  <TextInput
    labelText="User name"
    placeholder="Awesome John"
    on:input={handleUserNameChange}
  />
</Modal>

<Snackbar {snackbarMessage} />

<style>
  .about-yourself-illustration {
    width: 100%;
    max-width: 400px;
  }
  .spacer {
    height: 20px;
  }
</style>
