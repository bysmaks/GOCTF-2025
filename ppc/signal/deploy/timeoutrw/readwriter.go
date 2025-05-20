package timeoutrw

import (
	"bufio"
	"fmt"
	"net"
	"time"
)

type TimeoutReadWriter struct {
	conn       net.Conn
	ReadWriter *bufio.ReadWriter
	timeout    time.Duration
	autoFlush  bool
}

func NewTimeoutReadWriter(conn net.Conn, timeout time.Duration, autoFlush bool) *TimeoutReadWriter {
	reader := bufio.NewReader(conn)
	writer := bufio.NewWriter(conn)
	rw := bufio.NewReadWriter(reader, writer)
	return &TimeoutReadWriter{
		conn:       conn,
		ReadWriter: rw,
		timeout:    timeout,
		autoFlush:  autoFlush,
	}
}

func (rw *TimeoutReadWriter) setDeadline() error {
	return rw.conn.SetDeadline(time.Now().Add(rw.timeout))
}

func (rw *TimeoutReadWriter) Write(p []byte) (int, error) {
	if err := rw.setDeadline(); err != nil {
		return 0, err
	}
	defer rw.conn.SetDeadline(time.Time{})

	n, err := rw.ReadWriter.Write(p)
	if err != nil {
		return n, err
	}

	if rw.autoFlush {
		if err := rw.Flush(); err != nil {
			return n, err
		}
	}
	return n, nil
}

func (rw *TimeoutReadWriter) WriteByte(c byte) error {
	if err := rw.setDeadline(); err != nil {
		return err
	}
	defer rw.conn.SetDeadline(time.Time{})

	err := rw.ReadWriter.WriteByte(c)
	if err != nil {
		return err
	}

	if rw.autoFlush {
		return rw.Flush()
	}
	return nil
}

func (rw *TimeoutReadWriter) WriteRune(r rune) (int, error) {
	if err := rw.setDeadline(); err != nil {
		return 0, err
	}
	defer rw.conn.SetDeadline(time.Time{})

	size, err := rw.ReadWriter.WriteRune(r)
	if err != nil {
		return size, err
	}

	if rw.autoFlush {
		if err := rw.Flush(); err != nil {
			return size, err
		}
	}
	return size, nil
}

func (rw *TimeoutReadWriter) WriteString(s string) (int, error) {
	if err := rw.setDeadline(); err != nil {
		return 0, err
	}
	defer rw.conn.SetDeadline(time.Time{})

	n, err := rw.ReadWriter.WriteString(s)
	if err != nil {
		return n, err
	}

	if rw.autoFlush {
		if err := rw.Flush(); err != nil {
			return n, err
		}
	}
	return n, nil
}

func (rw *TimeoutReadWriter) WriteStringf(tmplt string, args ...any) (int, error) {
	s := fmt.Sprintf(tmplt, args...)

	if err := rw.setDeadline(); err != nil {
		return 0, err
	}
	defer rw.conn.SetDeadline(time.Time{})

	n, err := rw.ReadWriter.WriteString(s)
	if err != nil {
		return n, err
	}

	if rw.autoFlush {
		if err := rw.Flush(); err != nil {
			return n, err
		}
	}
	return n, nil
}

func (rw *TimeoutReadWriter) Read(p []byte) (int, error) {
	if err := rw.setDeadline(); err != nil {
		return 0, err
	}
	defer rw.conn.SetDeadline(time.Time{})

	return rw.ReadWriter.Read(p)
}

func (rw *TimeoutReadWriter) ReadStringUntil(delim byte) (string, error) {
	if err := rw.setDeadline(); err != nil {
		return "", err
	}
	defer rw.conn.SetDeadline(time.Time{})

	return rw.ReadWriter.ReadString(delim)
}

func (rw *TimeoutReadWriter) ReadLine() ([]byte, bool, error) {
	if err := rw.setDeadline(); err != nil {
		return nil, false, err
	}
	defer rw.conn.SetDeadline(time.Time{})

	return rw.ReadWriter.ReadLine()
}

func (rw *TimeoutReadWriter) ReadByte() (byte, error) {
	if err := rw.setDeadline(); err != nil {
		return 0, err
	}
	defer rw.conn.SetDeadline(time.Time{})

	return rw.ReadWriter.ReadByte()
}

func (rw *TimeoutReadWriter) ReadBytes(delim byte) ([]byte, error) {
	if err := rw.setDeadline(); err != nil {
		return nil, err
	}
	defer rw.conn.SetDeadline(time.Time{})

	return rw.ReadWriter.ReadBytes(delim)
}

func (rw *TimeoutReadWriter) ReadRune() (rune, int, error) {
	if err := rw.setDeadline(); err != nil {
		return 0, 0, err
	}
	defer rw.conn.SetDeadline(time.Time{})

	return rw.ReadWriter.ReadRune()
}

func (rw *TimeoutReadWriter) Flush() error {
	if err := rw.setDeadline(); err != nil {
		return err
	}
	defer rw.conn.SetDeadline(time.Time{})

	return rw.ReadWriter.Flush()
}

func (rw *TimeoutReadWriter) SetAutoFlush(b bool) {
	rw.autoFlush = b
}
