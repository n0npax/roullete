package main

import (
	"os"

	app "github.com/n0npax/roullete/pkg/random/field"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	args = os.Args[1:]
	port = kingpin.Flag("port", "application port").Short('p').Default("8182").Int()
	rUrl = kingpin.Flag("random-api", "random-api url").Default("http://localhost:8181/api/v1/random/int/").String()
	cUrl = kingpin.Flag("colour-api", "colour-api url").Default("http://localhost:8183/api/v1/colour/%d/").String()
)

func main() {
	_, err := kingpin.CommandLine.Parse(args)
	if err != nil {
		panic("Arg parsing failed")
	}
	app.Run(*port, *rUrl, *cUrl)
}
