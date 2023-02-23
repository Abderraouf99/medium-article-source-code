import { writable, type Writable } from "svelte/store";
import type { UserData } from "../models/user-data";

export const userStore: Writable<UserData> = writable({
  id: "",
  name: "",
});
