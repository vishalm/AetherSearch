package cmd

import (
	tea "github.com/charmbracelet/bubbletea"
	"github.com/aethersearch-dot-app/aethersearch/cli/internal/config"
	"github.com/aethersearch-dot-app/aethersearch/cli/internal/onboarding"
	"github.com/aethersearch-dot-app/aethersearch/cli/internal/starprompt"
	"github.com/aethersearch-dot-app/aethersearch/cli/internal/tui"
	"github.com/spf13/cobra"
)

func newChatCmd() *cobra.Command {
	var noStreamMarkdown bool

	cmd := &cobra.Command{
		Use:   "chat",
		Short: "Launch the interactive chat TUI (default)",
		Long: `Launch the interactive terminal UI for chatting with your AetherSearch agent.
This is the default command when no subcommand is specified. On first run,
an interactive setup wizard will guide you through configuration.`,
		Example: `  aethersearch-cli chat
  aethersearch-cli`,
		RunE: func(cmd *cobra.Command, args []string) error {
			cfg := config.Load()

			// First-run: onboarding
			if !config.ConfigExists() || !cfg.IsConfigured() {
				result := onboarding.Run(&cfg)
				if result == nil {
					return nil
				}
				cfg = *result
			}

			// CLI flag overrides config/env
			if cmd.Flags().Changed("no-stream-markdown") {
				v := !noStreamMarkdown
				cfg.Features.StreamMarkdown = &v
			}

			starprompt.MaybePrompt()

			m := tui.NewModel(cfg)
			p := tea.NewProgram(m, tea.WithAltScreen(), tea.WithMouseCellMotion())
			_, err := p.Run()
			return err
		},
	}

	cmd.Flags().BoolVar(&noStreamMarkdown, "no-stream-markdown", false, "Disable progressive markdown rendering during streaming")

	return cmd
}
