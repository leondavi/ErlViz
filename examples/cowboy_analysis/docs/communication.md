# Communication Patterns

This project uses the following communication patterns:

## Gen Server

Synchronous request-response pattern with state management. Clients send requests and wait for responses.

**Modules using this pattern** (1):

- **cowboy_clock**: cowboy_clock handles synchronous gen_server calls

---

## Http Handler

HTTP request-response pattern. Handles incoming HTTP requests and returns responses.

**Modules using this pattern** (24):

- **cowboy**: cowboy handles HTTP requests
- **cowboy_app**: cowboy_app handles HTTP requests
- **cowboy_children**: cowboy_children handles HTTP requests
- **cowboy_clear**: cowboy_clear handles HTTP requests
- **cowboy_compress_h**: cowboy_compress_h handles HTTP requests
- **cowboy_decompress_h**: cowboy_decompress_h handles HTTP requests
- **cowboy_handler**: cowboy_handler handles HTTP requests
- **cowboy_http**: cowboy_http handles HTTP requests
- **cowboy_http2**: cowboy_http2 handles HTTP requests
- **cowboy_http3**: cowboy_http3 handles HTTP requests
- **cowboy_loop**: cowboy_loop handles HTTP requests
- **cowboy_metrics_h**: cowboy_metrics_h handles HTTP requests
- **cowboy_middleware**: cowboy_middleware handles HTTP requests
- **cowboy_req**: cowboy_req handles HTTP requests
- **cowboy_rest**: cowboy_rest handles HTTP requests
- **cowboy_router**: cowboy_router handles HTTP requests
- **cowboy_static**: cowboy_static handles HTTP requests
- **cowboy_stream**: cowboy_stream handles HTTP requests
- **cowboy_stream_h**: cowboy_stream_h handles HTTP requests
- **cowboy_sub_protocol**: cowboy_sub_protocol handles HTTP requests
- **cowboy_tls**: cowboy_tls handles HTTP requests
- **cowboy_tracer_h**: cowboy_tracer_h handles HTTP requests
- **cowboy_websocket**: cowboy_websocket handles HTTP requests
- **cowboy_webtransport**: cowboy_webtransport handles HTTP requests

---

