package main

import (
	"fmt"
)

func main() {

	var xorKey = []byte{7, 42, 19, 101, 99, 11, 88, 250, 17, 1, 3, 15, 40, 62, 25, 57, 71, 9, 88, 101, 102, 11, 8, 17, 29, 54, 90, 1, 5, 67, 32, 10, 19, 99, 70, 61, 35, 11, 77, 6, 80, 66, 88, 29, 12}
	
	var encryptedFlag = []byte{64, 26, 76, 84, 86, 84, 108, 165, 118, 49, 51, 107, 119, 15, 45, 87, 113, 124, 108, 83, 85, 84, 110, 33, 111, 105, 40, 50, 115, 112, 82, 63, 32, 60, 117, 83, 21, 58, 35, 53, 99, 48, 105, 115, 58}

	result := make([]byte, len(encryptedFlag))

	for i := range encryptedFlag{
		result[i] = encryptedFlag[i] ^ xorKey[i]
	}
	fmt.Println(string(result))
}


