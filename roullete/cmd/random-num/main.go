package main

import (
	app "github.com/n0npax/roullete/pkg/random/num"
	"gopkg.in/alecthomas/kingpin.v2"
	"os"

)
var (
	args                    = os.Args[1:]
	port           = kingpin.Flag("port", "application port").Short('p').Default("8181").Int()
)


func main() {
	_, err := kingpin.CommandLine.Parse(args)
	if err != nil {
		panic("Arg parsing failed")
	}
	app.Run(*port)
}
