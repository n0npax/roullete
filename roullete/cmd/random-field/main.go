package main

import (
	"os"

	app "github.com/n0npax/roullete/pkg/random/field"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	args = os.Args[1:]
	port = kingpin.Flag("port", "application port").Short('p').Default("8182").Int()
	url  = kingpin.Flag("url", "random num url").Short('u').Default("http://localhost:8181/").String()
)

func main() {
	_, err := kingpin.CommandLine.Parse(args)
	if err != nil {
		panic("Arg parsing failed")
	}
	app.Run(*port, *url)
}
