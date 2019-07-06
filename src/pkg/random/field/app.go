package randomNum

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/gin-contrib/cors"

	"github.com/gin-contrib/opengintracing"
	"github.com/gin-gonic/gin"
	"github.com/opentracing/opentracing-go"
	"github.com/uber/jaeger-client-go"
	"github.com/uber/jaeger-client-go/zipkin"
)

func Run(port int, url string) {
	propagator := zipkin.NewZipkinB3HTTPHeaderPropagator()
	trace, closer := jaeger.NewTracer(
		"api_gateway",
		jaeger.NewConstSampler(true),
		jaeger.NewNullReporter(),
		jaeger.TracerOptions.Injector(opentracing.HTTPHeaders, propagator),
		jaeger.TracerOptions.Extractor(opentracing.HTTPHeaders, propagator),
		jaeger.TracerOptions.ZipkinSharedRPCSpan(true),
	)
	defer closer.Close()
	opentracing.SetGlobalTracer(trace)
	var fn opengintracing.ParentSpanReferenceFunc
	fn = func(sc opentracing.SpanContext) opentracing.StartSpanOption {
		return opentracing.ChildOf(sc)
	}

	// Set up routes
	r := gin.Default()
	r.GET("/api/v1/random/field/",
		opengintracing.SpanFromHeadersHttpFmt(trace, "RandomField", fn, false),
		func(c *gin.Context) {
			n, err := randomNum(url)
			n %= 37
			if err != nil {
				c.JSON(500, gin.H{"error": err})
				return
			}
			c.JSON(200, gin.H{
				"int": n,
			})
		})
	r.Use(cors.Default())
	r.Run(fmt.Sprintf(":%d", port))
}

func randomNum(url string) (int, error) {
	n := &Num{}
	err := getJson(url, n)
	if err != nil {
		return 0, err
	}
	return n.Num, nil
}

var myClient = &http.Client{Timeout: 10 * time.Second}

func getJson(url string, target interface{}) error {
	r, err := myClient.Get(url)
	if err != nil {
		return err
	}
	defer r.Body.Close()

	return json.NewDecoder(r.Body).Decode(target)
}

type Num struct {
	Num int `json:"int"`
}
