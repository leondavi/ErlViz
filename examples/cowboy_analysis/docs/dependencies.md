# Dependencies

## External Dependencies

This project depends on the following external libraries:

- **branch**
- **cowlib**
- **git**
- **ranch**
- **tag**

## Internal Module Dependencies

Dependencies between project modules:

- **cowboy** depends on: cowboy_http2, cowboy_constraints, cowboy_http, cowboy_http3
- **cowboy_app** depends on: cowboy_sup
- **cowboy_children** depends on: cowboy_stream
- **cowboy_clear** depends on: cowboy
- **cowboy_compress_h** depends on: cowboy, cowboy_stream, cowboy_req
- **cowboy_decompress_h** depends on: cowboy, cowboy_stream, cowboy_req
- **cowboy_handler** depends on: cowboy_req, cowboy_middleware
- **cowboy_http** depends on: cowboy_http2, cowboy_tracer_h, cowboy_req, cowboy_middleware, cowboy_stream, cowboy_children, cowboy, cowboy_metrics_h
- **cowboy_http2** depends on: cowboy_tracer_h, cowboy_req, cowboy_middleware, cowboy_stream, cowboy_children, cowboy, cowboy_metrics_h
- **cowboy_http3** depends on: cowboy_tracer_h, cowboy_req, cowboy_middleware, cowboy_stream, cowboy_quicer, cowboy_children, cowboy, cowboy_metrics_h
- **cowboy_loop** depends on: cowboy_req, cowboy_middleware, cowboy_handler, cowboy_children
- **cowboy_metrics_h** depends on: cowboy, cowboy_stream, cowboy_req
- **cowboy_middleware** depends on: cowboy_req
- **cowboy_req** depends on: cowboy_constraints, cowboy_router, cowboy_clock, cowboy_stream, cowboy
- **cowboy_rest** depends on: cowboy_clock, cowboy_req, cowboy_middleware, cowboy_handler
- **cowboy_router** depends on: cowboy_constraints, cowboy_req, cowboy_bstr, cowboy_middleware, cowboy
- **cowboy_static** depends on: cowboy_req
- **cowboy_stream** depends on: cowboy, cowboy_stream, cowboy_req
- **cowboy_stream_h** depends on: cowboy, cowboy_stream, cowboy_req, cowboy_middleware
- **cowboy_sub_protocol** depends on: cowboy_req, cowboy_middleware
- **cowboy_tls** depends on: cowboy
- **cowboy_tracer_h** depends on: cowboy, cowboy_stream, cowboy_req
- **cowboy_websocket** depends on: cowboy_req, cowboy_middleware, cowboy_bstr, cowboy_handler, cowboy_stream, cowboy_children
- **cowboy_webtransport** depends on: cowboy_req, cowboy_bstr, cowboy_middleware, cowboy_handler, cowboy_stream, cowboy_children

## Application Dependencies


