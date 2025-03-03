package context

import (
	"context"
	"log/slog"
)

type ContextHandler struct {
	slog.Handler
}

func (h *ContextHandler) Handle(ctx context.Context, r slog.Record) error {
	if conID, ok := ConnectionIdFromContext(ctx); ok {
		r.AddAttrs(slog.Uint64("con_id", conID))
	}
	return h.Handler.Handle(ctx, r)
}
