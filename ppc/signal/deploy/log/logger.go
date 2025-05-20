package log

import (
	"context"
	"go.uber.org/zap"
)

var (
	globalLogger *zap.SugaredLogger
)

func init() {
	l, _ := zap.NewProduction()
	globalLogger = l.Sugar()
	globalLogger.Infof("logger initialized")
}

func Flush() error {
	return globalLogger.Sync()
}

type loggerKey struct{}

func Logger(ctx ...context.Context) *zap.SugaredLogger {
	if len(ctx) == 0 {
		return globalLogger
	}

	l, ok := ctx[0].Value(loggerKey{}).(*zap.SugaredLogger)
	if !ok {
		return globalLogger
	}

	return l
}

func ContextWithLogger(ctx context.Context, logger *zap.SugaredLogger) context.Context {
	return context.WithValue(ctx, loggerKey{}, logger)
}
