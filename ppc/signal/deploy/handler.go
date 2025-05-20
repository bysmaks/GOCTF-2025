package main

import (
	"context"
	"errors"
	"github.com/segmentio/ksuid"
	"net"
	"os"
	"signal/config"
	"signal/log"
	"signal/task"
	"signal/timeoutrw"
)

const (
	rwTimeoutExitMsgTmplt = "\n[ERROR] Read/Write timeout! (timeout = %v)\n"
)

func Handle(conn net.Conn) {
	defer conn.Close()

	sessionId := ksuid.New().String()
	logger := log.Logger().With("session", sessionId)
	ctx := log.ContextWithLogger(context.Background(), logger)

	logger.Infof("connected")

	cfg := config.GetConfig()

	// TimeoutReaderWriter for closing idle connections after timeout
	rw := timeoutrw.NewTimeoutReadWriter(conn, cfg.Timeout, true)

	if _, err := rw.WriteStringf("SESSION ID: %s\nREAD/WRITE TIMEOUT: %s\n\n", sessionId, cfg.Timeout); err != nil {
		logger.Errorf("failed to write session id: %v", err)

		if errors.Is(err, os.ErrDeadlineExceeded) {
			_, _ = rw.WriteStringf(rwTimeoutExitMsgTmplt, cfg.Timeout)
			return
		}

		return
	}

	if err := task.Task(ctx, rw); err != nil {
		logger.Warnf("task exited with error: %v", err)

		if errors.Is(err, os.ErrDeadlineExceeded) {
			_, _ = rw.WriteStringf(rwTimeoutExitMsgTmplt, cfg.Timeout)
			return
		}

		return
	}
}
