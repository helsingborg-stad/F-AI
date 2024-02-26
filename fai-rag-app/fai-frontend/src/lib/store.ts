import {writable} from "svelte/store";
import type {IComponentDef} from "./types";

export const pageDataStore = writable<IComponentDef[]>([])

