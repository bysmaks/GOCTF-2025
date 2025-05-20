package main

import (
	"holdem/config"
	"holdem/log"
	"net"
)

func main() {
	defer log.Flush()

	startServer(config.GetConfig().Addr)
}

func startServer(addr string) {
	log.Logger().Infof("listening on %s", addr)

	ln, err := net.Listen("tcp", addr)
	if err != nil {
		log.Logger().Fatalf("error starting server: %v", err)
	}
	defer ln.Close()

	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Logger().Infof("error accepting connection: %v", err)
			continue
		}
		go Handle(conn)
	}
}
