package main

import (
	"crypto/sha1"
	"fmt"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		os.Exit(1)
	}
	name := os.Args[1]
	h := sha1.Sum([]byte(name))
	// Ожидаемое значение (пример)
	if fmt.Sprintf("%x", h) == "c67844731b2414adf23945e1e92cf087cf46faf6" {
		os.Exit(0)
	}
	os.Exit(1)
}
