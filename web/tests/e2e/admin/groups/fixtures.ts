/**
 * Playwright fixtures for Admin Groups page tests.
 *
 * Provides:
 * - Authenticated admin page
 * - AetherSearchApiClient for API-level setup/teardown
 * - GroupsAdminPage page object
 */

import { test as base, expect, type Page } from "@playwright/test";
import { loginAs } from "@tests/e2e/utils/auth";
import { AetherSearchApiClient } from "@tests/e2e/utils/aethersearchApiClient";
import { GroupsAdminPage } from "./GroupsAdminPage";

export const test = base.extend<{
  adminPage: Page;
  api: AetherSearchApiClient;
  groupsPage: GroupsAdminPage;
}>({
  adminPage: async ({ page }, use) => {
    await page.context().clearCookies();
    await loginAs(page, "admin");
    await use(page);
  },

  api: async ({ adminPage }, use) => {
    const client = new AetherSearchApiClient(adminPage.request);
    await use(client);
  },

  groupsPage: async ({ adminPage }, use) => {
    const groupsPage = new GroupsAdminPage(adminPage);
    await use(groupsPage);
  },
});

export { expect };
