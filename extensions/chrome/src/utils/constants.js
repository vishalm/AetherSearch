export const THEMES = {
  LIGHT: "light",
  DARK: "dark",
};

export const DEFAULT_AETHERSEARCH_DOMAIN = "http://localhost:3000";

export const SIDE_PANEL_PATH = "/nrf/side-panel";

export const ACTIONS = {
  GET_SELECTED_TEXT: "getSelectedText",
  GET_CURRENT_AETHERSEARCH_DOMAIN: "getCurrentAetherSearchDomain",
  UPDATE_PAGE_URL: "updatePageUrl",
  SEND_TO_AETHERSEARCH: "sendToAetherSearch",
  OPEN_SIDE_PANEL: "openSidePanel",
  TOGGLE_NEW_TAB_OVERRIDE: "toggleNewTabOverride",
  OPEN_SIDE_PANEL_WITH_INPUT: "openSidePanelWithInput",
  OPEN_AETHERSEARCH_WITH_INPUT: "openAetherSearchWithInput",
  CLOSE_SIDE_PANEL: "closeSidePanel",
  TAB_URL_UPDATED: "tabUrlUpdated",
  TAB_READING_ENABLED: "tabReadingEnabled",
  TAB_READING_DISABLED: "tabReadingDisabled",
};

export const CHROME_SPECIFIC_STORAGE_KEYS = {
  AETHERSEARCH_DOMAIN: "aethersearchExtensionDomain",
  USE_AETHERSEARCH_AS_DEFAULT_NEW_TAB: "aethersearchExtensionDefaultNewTab",
  THEME: "aethersearchExtensionTheme",
  BACKGROUND_IMAGE: "aethersearchExtensionBackgroundImage",
  DARK_BG_URL: "aethersearchExtensionDarkBgUrl",
  LIGHT_BG_URL: "aethersearchExtensionLightBgUrl",
  ONBOARDING_COMPLETE: "aethersearchExtensionOnboardingComplete",
};

export const CHROME_MESSAGE = {
  PREFERENCES_UPDATED: "PREFERENCES_UPDATED",
  AETHERSEARCH_APP_LOADED: "AETHERSEARCH_APP_LOADED",
  SET_DEFAULT_NEW_TAB: "SET_DEFAULT_NEW_TAB",
  LOAD_NEW_CHAT_PAGE: "LOAD_NEW_CHAT_PAGE",
  LOAD_NEW_PAGE: "LOAD_NEW_PAGE",
  AUTH_REQUIRED: "AUTH_REQUIRED",
  TAB_READING_ENABLED: "TAB_READING_ENABLED",
  TAB_READING_DISABLED: "TAB_READING_DISABLED",
  TAB_URL_UPDATED: "TAB_URL_UPDATED",
};

export const WEB_MESSAGE = {
  PAGE_CHANGE: "PAGE_CHANGE",
};
