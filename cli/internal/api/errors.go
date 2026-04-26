package api

import "fmt"

// AetherSearchAPIError is returned when an AetherSearch API call fails.
type AetherSearchAPIError struct {
	StatusCode int
	Detail     string
}

func (e *AetherSearchAPIError) Error() string {
	return fmt.Sprintf("HTTP %d: %s", e.StatusCode, e.Detail)
}

// AuthError is returned when authentication or authorization fails.
type AuthError struct {
	Message string
}

func (e *AuthError) Error() string {
	return e.Message
}
