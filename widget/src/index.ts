/**
 * AetherSearch Chat Widget - Entry Point
 * Exports the main web component
 */

import { AetherSearchChatWidget } from "./widget";

// Define the custom element
if (
  typeof customElements !== "undefined" &&
  !customElements.get("aethersearch-chat-widget")
) {
  customElements.define("aethersearch-chat-widget", AetherSearchChatWidget);
}

// Export for use in other modules
export { AetherSearchChatWidget };
export * from "./types/api-types";
export * from "./types/widget-types";
