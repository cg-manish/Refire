package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
)

func main() {
	fmt.Println("Hello, World!")

	ln, err := net.Listen("tcp", ":8080")

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Listeing in port 8080")

	connection, err := ln.Accept()
	if err != nil {
		log.Fatal(err)
	}

	for {
		message, err := bufio.NewReader(connection).ReadString('\n')
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println("Message received: ", string(message))

	}

}
