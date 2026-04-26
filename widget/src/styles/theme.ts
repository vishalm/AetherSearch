import { css } from "lit";
import { colors } from "./colors";

/**
 * AetherSearch Design System - Theme
 * Typography, spacing, and layout tokens from Figma
 */
export const theme = css`
  ${colors}

  :host {
    /* Typography - Hanken Grotesk */
    --aethersearch-font-family: "Hanken Grotesk", -apple-system, BlinkMacSystemFont,
      "Segoe UI", sans-serif;
    --aethersearch-font-family-mono: "DM Mono", "Monaco", "Menlo", monospace;

    /* Font Sizes */
    --aethersearch-font-size-small: 10px;
    --aethersearch-font-size-secondary: 12px;
    --aethersearch-font-size-sm: 13px;
    --aethersearch-font-size-main: 14px;
    --aethersearch-font-size-label: 16px;

    /* Line Heights */
    --aethersearch-line-height-small: 12px;
    --aethersearch-line-height-secondary: 16px;
    --aethersearch-line-height-main: 20px;
    --aethersearch-line-height-label: 24px;
    --aethersearch-line-height-section: 28px;
    --aethersearch-line-height-headline: 36px;

    /* Font Weights */
    --aethersearch-weight-regular: 400;
    --aethersearch-weight-medium: 500;
    --aethersearch-weight-semibold: 600;

    /* Content Heights */
    --aethersearch-height-content-secondary: 12px;
    --aethersearch-height-content-main: 16px;
    --aethersearch-height-content-label: 18px;
    --aethersearch-height-content-section: 24px;

    /* Border Radius - from Figma */
    --aethersearch-radius-04: 4px;
    --aethersearch-radius-08: 8px;
    --aethersearch-radius-12: 12px;
    --aethersearch-radius-16: 16px;
    --aethersearch-radius-round: 1000px;

    /* Spacing - Block */
    --aethersearch-space-block-1x: 4px;
    --aethersearch-space-block-2x: 8px;
    --aethersearch-space-block-3x: 12px;
    --aethersearch-space-block-4x: 16px;
    --aethersearch-space-block-6x: 24px;

    /* Spacing - Inline */
    --aethersearch-space-inline-0: 0px;
    --aethersearch-space-inline-0_5x: 2px;
    --aethersearch-space-inline-1x: 4px;

    /* Legacy spacing aliases (for compatibility) */
    --aethersearch-space-2xs: var(--aethersearch-space-block-1x);
    --aethersearch-space-xs: var(--aethersearch-space-block-2x);
    --aethersearch-space-sm: var(--aethersearch-space-block-3x);
    --aethersearch-space-md: var(--aethersearch-space-block-4x);
    --aethersearch-space-lg: var(--aethersearch-space-block-6x);

    /* Padding */
    --aethersearch-padding-icon-0: 0px;
    --aethersearch-padding-icon-0_5x: 2px;
    --aethersearch-padding-text-0_5x: 2px;
    --aethersearch-padding-text-1x: 4px;

    /* Icon Weights (stroke-width) */
    --aethersearch-icon-weight-secondary: 1px;
    --aethersearch-icon-weight-main: 1.5px;
    --aethersearch-icon-weight-section: 2px;

    /* Z-index */
    --aethersearch-z-launcher: 9999;
    --aethersearch-z-widget: 10000;

    /* Transitions */
    --aethersearch-transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
    --aethersearch-transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
  }

  * {
    box-sizing: border-box;
  }
`;
