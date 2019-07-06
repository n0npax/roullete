package randomNum

import (
	"fmt"
	"strconv"

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
	r.GET("/api/v1/colour/:id/",
		opengintracing.SpanFromHeadersHttpFmt(trace, "RandomNum", fn, false),
		func(c *gin.Context) {
			id, err := strconv.Atoi(c.Param("id"))
			var colour string
			switch id {
			case 0:
				colour = "green"
			case 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35:
				colour = "black"
			case 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36:
				colour = "red"
			default:
				colour = "unknown"
			}
			if err != nil {
				c.JSON(400, gin.H{
					"error": "id should be a number",
				})
				return
			}
			c.JSON(200, gin.H{
				"colour": colour,
			})
		})
	r.Use(cors.Default())
	r.Run(fmt.Sprintf(":%d", port))
}
