import {
  DEFAULT_AETHERSEARCH_DOMAIN,
  CHROME_SPECIFIC_STORAGE_KEYS,
} from "./constants.js";

export async function getAetherSearchDomain() {
  const result = await chrome.storage.local.get({
    [CHROME_SPECIFIC_STORAGE_KEYS.AETHERSEARCH_DOMAIN]: DEFAULT_AETHERSEARCH_DOMAIN,
  });
  return result[CHROME_SPECIFIC_STORAGE_KEYS.AETHERSEARCH_DOMAIN];
}

export function setAetherSearchDomain(domain, callback) {
  chrome.storage.local.set(
    { [CHROME_SPECIFIC_STORAGE_KEYS.AETHERSEARCH_DOMAIN]: domain },
    callback,
  );
}

export function getAetherSearchDomainSync() {
  return new Promise((resolve) => {
    getAetherSearchDomain(resolve);
  });
}
