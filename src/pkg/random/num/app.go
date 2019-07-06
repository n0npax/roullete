package randomNum

import (
	"fmt"
	"math/rand"

	"github.com/gin-contrib/cors"

	"github.com/gin-contrib/opengintracing"
	"github.com/gin-gonic/gin"
	"github.com/opentracing/opentracing-go"
	"github.com/uber/jaeger-client-go"
	"github.com/uber/jaeger-client-go/zipkin"
)

func Run(port int) {
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
	r.GET("/api/v1/random/int",
		opengintracing.SpanFromHeadersHttpFmt(trace, "RandomNum", fn, false),
		func(c *gin.Context) {
			c.JSON(200, gin.H{
				"int": rand.Int(),
			})
		})
	r.Use(cors.Default())
	r.Run(fmt.Sprintf(":%d", port))
}
