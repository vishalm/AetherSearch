package tui

import "github.com/aethersearch-dot-app/aethersearch/cli/internal/config"

// experimentsText returns the formatted experiments list for the current config.
func (m Model) experimentsText() string {
	return config.ExperimentsText(m.config.Features)
}
