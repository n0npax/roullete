package main

import (
	"os"

	app "github.com/n0npax/roullete/pkg/colour"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	args = os.Args[1:]
	port = kingpin.Flag("port", "application port").Short('p').Default("8183").Int()
)

func main() {
	_, err := kingpin.CommandLine.Parse(args)
	if err != nil {
		panic("Arg parsing failed")
	}
	app.Run(*port)
}
