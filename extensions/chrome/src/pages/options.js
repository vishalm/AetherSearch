import {
  CHROME_SPECIFIC_STORAGE_KEYS,
  DEFAULT_AETHERSEARCH_DOMAIN,
} from "../utils/constants.js";

document.addEventListener("DOMContentLoaded", function () {
  const domainInput = document.getElementById("aethersearchDomain");
  const useAetherSearchAsDefaultToggle = document.getElementById("useAetherSearchAsDefault");
  const statusContainer = document.getElementById("statusContainer");
  const statusElement = document.getElementById("status");
  const newTabButton = document.getElementById("newTab");
  const themeToggle = document.getElementById("themeToggle");
  const themeIcon = document.getElementById("themeIcon");

  let currentTheme = "dark";

  function updateThemeIcon(theme) {
    if (!themeIcon) return;

    if (theme === "light") {
      themeIcon.innerHTML = `
        <circle cx="12" cy="12" r="4"></circle>
        <path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"></path>
      `;
    } else {
      themeIcon.innerHTML = `
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
      `;
    }
  }

  function loadStoredValues() {
    chrome.storage.local.get(
      {
        [CHROME_SPECIFIC_STORAGE_KEYS.AETHERSEARCH_DOMAIN]: DEFAULT_AETHERSEARCH_DOMAIN,
        [CHROME_SPECIFIC_STORAGE_KEYS.USE_AETHERSEARCH_AS_DEFAULT_NEW_TAB]: false,
        [CHROME_SPECIFIC_STORAGE_KEYS.THEME]: "dark",
      },
      (result) => {
        if (domainInput)
          domainInput.value = result[CHROME_SPECIFIC_STORAGE_KEYS.AETHERSEARCH_DOMAIN];
        if (useAetherSearchAsDefaultToggle)
          useAetherSearchAsDefaultToggle.checked =
            result[CHROME_SPECIFIC_STORAGE_KEYS.USE_AETHERSEARCH_AS_DEFAULT_NEW_TAB];

        currentTheme = result[CHROME_SPECIFIC_STORAGE_KEYS.THEME] || "dark";
        updateThemeIcon(currentTheme);

        document.body.className = currentTheme === "light" ? "light-theme" : "";
      },
    );
  }

  function saveSettings() {
    const domain = domainInput.value.trim();
    const useAetherSearchAsDefault = useAetherSearchAsDefaultToggle
      ? useAetherSearchAsDefaultToggle.checked
      : false;

    chrome.storage.local.set(
      {
        [CHROME_SPECIFIC_STORAGE_KEYS.AETHERSEARCH_DOMAIN]: domain,
        [CHROME_SPECIFIC_STORAGE_KEYS.USE_AETHERSEARCH_AS_DEFAULT_NEW_TAB]:
          useAetherSearchAsDefault,
        [CHROME_SPECIFIC_STORAGE_KEYS.THEME]: currentTheme,
      },
      () => {
        showStatusMessage(
          useAetherSearchAsDefault
            ? "Settings updated. Open a new tab to test it out. Click on the extension icon to bring up AetherSearch from any page."
            : "Settings updated.",
        );
      },
    );
  }

  function showStatusMessage(message) {
    if (statusElement) {
      const useAetherSearchAsDefault = useAetherSearchAsDefaultToggle
        ? useAetherSearchAsDefaultToggle.checked
        : false;

      statusElement.textContent =
        message ||
        (useAetherSearchAsDefault
          ? "Settings updated. Open a new tab to test it out. Click on the extension icon to bring up AetherSearch from any page."
          : "Settings updated.");

      if (newTabButton) {
        newTabButton.style.display = useAetherSearchAsDefault ? "block" : "none";
      }
    }

    if (statusContainer) {
      statusContainer.classList.add("show");
    }

    setTimeout(hideStatusMessage, 5000);
  }

  function hideStatusMessage() {
    if (statusContainer) {
      statusContainer.classList.remove("show");
    }
  }

  function toggleTheme() {
    currentTheme = currentTheme === "light" ? "dark" : "light";
    updateThemeIcon(currentTheme);

    document.body.className = currentTheme === "light" ? "light-theme" : "";

    chrome.storage.local.set({
      [CHROME_SPECIFIC_STORAGE_KEYS.THEME]: currentTheme,
    });
  }

  function openNewTab() {
    chrome.tabs.create({});
  }

  if (domainInput) {
    domainInput.addEventListener("input", () => {
      clearTimeout(domainInput.saveTimeout);
      domainInput.saveTimeout = setTimeout(saveSettings, 1000);
    });
  }

  if (useAetherSearchAsDefaultToggle) {
    useAetherSearchAsDefaultToggle.addEventListener("change", saveSettings);
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
  }

  if (newTabButton) {
    newTabButton.addEventListener("click", openNewTab);
  }

  loadStoredValues();
});
