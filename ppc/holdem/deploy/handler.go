package main

import (
	"context"
	"github.com/segmentio/ksuid"
	"holdem/config"
	"holdem/log"
	"holdem/task"
	"holdem/timeoutrw"
	"net"
)

func Handle(conn net.Conn) {
	defer conn.Close()

	sessionId := ksuid.New().String()
	logger := log.Logger().With("session", sessionId)
	ctx := log.ContextWithLogger(context.Background(), logger)

	cfg := config.GetConfig()

	// TimeoutReaderWriter for closing idle connections after timeout
	rw := timeoutrw.NewTimeoutReadWriter(conn, cfg.Timeout, true)

	if _, err := rw.WriteStringf("SESSION ID: %s\nREAD/WRITE TIMEOUT: %s\n\n", sessionId, cfg.Timeout); err != nil {
		logger.Errorf("failed to write session id: %v", err)
		return
	}

	logger.Infof("connected")
	if err := task.Task(ctx, rw); err != nil {
		logger.Warnf("task exited with error: %v", err)
	}
}
