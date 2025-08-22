# API Reference

Public API functions in this project:

## cowboy

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `get_env/2`

---

#### `get_env/3`

---

#### `log/2`

**Arguments**: `Level, Format, Args, _`

**Description**: We use error_logger by default. Because error_logger does
%% not have all the levels we accept we have to do some
%% mapping to error_logger functions.

---

#### `log/4`

**Arguments**: `Level, Format, Args, _`

**Description**: We use error_logger by default. Because error_logger does
%% not have all the levels we accept we have to do some
%% mapping to error_logger functions.

---

#### `set_env/3`

---

#### `start_clear/3`

**Arguments**: `Ref, TransOpts0, ProtoOpts0`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy).

-export([start_clear/3]).
-export([start_tls/3]).
-export([start_quic/3]).
-export([stop_listener/1]).
-export([get_env/2]).
-export([get_env/3]).
-export([set_env/3]).

%% Internal.
-export([log/2]).
-export([log/4]).

%% Don't warn about the bad quicer specs.
-dialyzer([{nowarn_function, start_quic/3}]).

-type opts() :: cowboy_http:opts() | cowboy_http2:opts().
-export_type([opts/0]).

-type fields() :: [atom()
	| {atom(), cowboy_constraints:constraint() | [cowboy_constraints:constraint()]}
	| {atom(), cowboy_constraints:constraint() | [cowboy_constraints:constraint()], any()}].
-export_type([fields/0]).

-type http_headers() :: #{binary() => iodata()}.
-export_type([http_headers/0]).

-type http_status() :: non_neg_integer() | binary().
-export_type([http_status/0]).

-type http_version() :: 'HTTP/2' | 'HTTP/1.1' | 'HTTP/1.0'.
-export_type([http_version/0]).

-spec start_clear(ranch:ref(), ranch:opts(), opts())
	-> {ok, pid()} | {error, any()}.

---

#### `start_quic/3`

**Arguments**: `Ref, TransOpts, ProtoOpts`

**Description**: @todo Experimental function to start a barebone QUIC listener.
%%       This will need to be reworked to be closer to Ranch
%%       listeners and provide equivalent features.
%%
%% @todo Better type for transport options. Might require fixing quicer types.

-spec start_quic(ranch:ref(), #{socket_opts => [{atom(), _}]}, cowboy_http3:opts())
	-> {ok, pid()}.

%% @todo Implement dynamic_buffer for HTTP/3 if/when it applies.

---

#### `start_tls/3`

---

#### `stop_listener/1`

---


## cowboy_app

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `start/2`

**Arguments**: `_, _`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_app).
-behaviour(application).

-export([start/2]).
-export([stop/1]).

-spec start(_, _) -> {ok, pid()}.

---

#### `stop/1`

---


## cowboy_bstr

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `capitalize_token/1`

**Arguments**: `B`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_bstr).

%% Binary strings.
-export([capitalize_token/1]).
-export([to_lower/1]).
-export([to_upper/1]).

%% Characters.
-export([char_to_lower/1]).
-export([char_to_upper/1]).

%% The first letter and all letters after a dash are capitalized.
%% This is the form seen for header names in the HTTP/1.1 RFC and
%% others. Note that using this form isn't required, as header names
%% are case insensitive, and it is only provided for use with eventual
%% badly implemented clients.
-spec capitalize_token(B) -> B when B::binary().

---

#### `char_to_lower/1`

---

#### `char_to_upper/1`

---

#### `to_lower/1`

---

#### `to_upper/1`

---


## cowboy_children

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `down/2`

---

#### `handle_supervisor_call/4`

**Arguments**: `_, {From, Tag}, _, _`

**Description**: All other calls refer to children. We act in a similar way
%% to a simple_one_for_one so we never find those.

---

#### `init/0`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_children).

-export([init/0]).
-export([up/4]).
-export([down/2]).
-export([shutdown/2]).
-export([shutdown_timeout/3]).
-export([terminate/1]).
-export([handle_supervisor_call/4]).

-record(child, {
	pid :: pid(),
	streamid :: cowboy_stream:streamid() | undefined,
	shutdown :: timeout(),
	timer = undefined :: undefined | reference()
}).

-type children() :: [#child{}].
-export_type([children/0]).

-spec init() -> [].

---

#### `shutdown/2`

**Arguments**: `Children0, StreamID`

**Description**: We ask the processes to shutdown first. This gives
%% a chance to processes that are trapping exits to
%% shut down gracefully. Others will exit immediately.
%%
%% @todo We currently fire one timer per process being
%% shut down. This is probably not the most efficient.
%% A more efficient solution could be to maintain a
%% single timer and decrease the shutdown time of all
%% processes when it fires. This is however much more
%% complex, and there aren't that many processes that
%% will need to be shutdown through this function, so
%% this is left for later.
-spec shutdown(Children, cowboy_stream:streamid())
	-> Children when Children::children().

---

#### `shutdown_timeout/3`

---

#### `terminate/1`

---

#### `up/4`

---


## cowboy_clear

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `connection_process/4`

---

#### `start_link/3`

**Arguments**: `Ref, Transport, Opts`

**Description**: Ranch 2.
-spec start_link(ranch:ref(), module(), cowboy:opts()) -> {ok, pid()}.

---

#### `start_link/4`

**Arguments**: `Ref, Transport, Opts`

**Description**: Ranch 2.
-spec start_link(ranch:ref(), module(), cowboy:opts()) -> {ok, pid()}.

---


## cowboy_clock

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `code_change/3`

---

#### `handle_call/3`

---

#### `handle_cast/2`

---

#### `handle_info/2`

**Arguments**: `_Info, State`

**Description**: Cancel the timer in case an external process sent an update message.
	_ = erlang:cancel_timer(TRef0, [{async, true}, {info, false}]),
	T = erlang:universaltime(),
	B2 = update_rfc1123(B1, Prev, T),
	ets:insert(?MODULE, {rfc1123, B2}),
	TRef = erlang:send_after(1000, self(), update),
	{noreply, #state{universaltime=T, rfc1123=B2, tref=TRef}};

---

#### `init/1`

**Arguments**: `[]`

**Description**: gen_server.

-spec init([]) -> {ok, #state{}}.

---

#### `rfc1123/0`

**Description**: When the ets table doesn't exist, either because of a bug
%% or because Cowboy is being restarted, we perform in a
%% slightly degraded state and build a new timestamp for
%% every request.
-spec rfc1123() -> binary().

---

#### `rfc1123/1`

**Description**: When the ets table doesn't exist, either because of a bug
%% or because Cowboy is being restarted, we perform in a
%% slightly degraded state and build a new timestamp for
%% every request.
-spec rfc1123() -> binary().

---

#### `start_link/0`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

%% While a gen_server process runs in the background to update
%% the cache of formatted dates every second, all API calls are
%% local and directly read from the ETS cache table, providing
%% fast time and date computations.
-module(cowboy_clock).
-behaviour(gen_server).

%% API.
-export([start_link/0]).
-export([stop/0]).
-export([rfc1123/0]).
-export([rfc1123/1]).

%% gen_server.
-export([init/1]).
-export([handle_call/3]).
-export([handle_cast/2]).
-export([handle_info/2]).
-export([terminate/2]).
-export([code_change/3]).

-record(state, {
	universaltime = undefined :: undefined | calendar:datetime(),
	rfc1123 = <<>> :: binary(),
	tref = undefined :: undefined | reference()
}).

%% API.

-spec start_link() -> {ok, pid()}.

---

#### `stop/0`

---

#### `terminate/2`

---


## cowboy_compress_h

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `data/4`

---

#### `early_error/5`

**Arguments**: `StreamID, Reason, PartialReq, Resp, Opts`

**Description**: Clean the zlib:stream() in case something went wrong.
	%% In the normal scenario the stream is already closed.
	case Z of
		undefined -> ok;
		_ -> zlib:close(Z)
	end,
	cowboy_stream:terminate(StreamID, Reason, Next).

-spec early_error(cowboy_stream:streamid(), cowboy_stream:reason(),
	cowboy_stream:partial_req(), Resp, cowboy:opts()) -> Resp
	when Resp::cowboy_stream:resp_command().

---

#### `info/3`

---

#### `init/3`

**Arguments**: `StreamID, Req, Opts`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_compress_h).
-behavior(cowboy_stream).

-export([init/3]).
-export([data/4]).
-export([info/3]).
-export([terminate/3]).
-export([early_error/5]).

-record(state, {
	next :: any(),
	threshold :: non_neg_integer() | undefined,
	compress = undefined :: undefined | gzip,
	deflate = undefined :: undefined | zlib:zstream(),
	deflate_flush = sync :: none | sync
}).

-spec init(cowboy_stream:streamid(), cowboy_req:req(), cowboy:opts())
	-> {cowboy_stream:commands(), #state{}}.

---

#### `terminate/3`

---


## cowboy_constraints

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `format_error/1`

---

#### `reverse/2`

---

#### `validate/2`

**Arguments**: `Value, Constraints) when is_list(Constraints`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_constraints).

-export([validate/2]).
-export([reverse/2]).
-export([format_error/1]).

-type constraint() :: int | nonempty | fun().
-export_type([constraint/0]).

-type reason() :: {constraint(), any(), any()}.
-export_type([reason/0]).

-spec validate(binary(), constraint() | [constraint()])
	-> {ok, any()} | {error, reason()}.

---


## cowboy_decompress_h

Copyright (c) jdamanalo <joshuadavid.agustin@manalo.ph>
Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN

### Exported Functions

#### `data/4`

---

#### `early_error/5`

---

#### `info/3`

**Arguments**: `StreamID, Info, State=#state{next=Next0}`

**Description**: We can't change the enabled setting after we start reading,
	%% otherwise the data becomes garbage. Changing the setting
	%% is not treated as an error, it is just ignored.
	State = case IsReading of
		true -> State0;
		false -> State0#state{enabled=Enabled}
	end,
	fold(Commands, State#state{next=Next, ratio_limit=RatioLimit});

---

#### `init/3`

**Arguments**: `StreamID, Req0, Opts`

**Description**: Copyright (c) jdamanalo <joshuadavid.agustin@manalo.ph>
%% Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_decompress_h).
-behavior(cowboy_stream).

-export([init/3]).
-export([data/4]).
-export([info/3]).
-export([terminate/3]).
-export([early_error/5]).

-record(state, {
	next :: any(),
	enabled = true :: boolean(),
	ratio_limit :: non_neg_integer() | undefined,
	compress = undefined :: undefined | gzip,
	inflate = undefined :: undefined | zlib:zstream(),
	is_reading = false :: boolean(),

	%% We use a list of binaries to avoid doing unnecessary
	%% memory allocations when inflating. We convert to binary
	%% when we propagate the data. The data must be reversed
	%% before converting to binary or inflating: this is done
	%% via the buffer_to_binary/buffer_to_iovec functions.
	read_body_buffer = [] :: [binary()],
	read_body_is_fin = nofin :: nofin | {fin, non_neg_integer()}
}).

-spec init(cowboy_stream:streamid(), cowboy_req:req(), cowboy:opts())
	-> {cowboy_stream:commands(), #state{}}.

---

#### `terminate/3`

---


## cowboy_handler

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `execute/2`

**Arguments**: `Req, Env=#{handler := Handler, handler_opts := HandlerOpts}`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

%% Handler middleware.
%%
%% Execute the handler given by the <em>handler</em> and <em>handler_opts</em>
%% environment values. The result of this execution is added to the
%% environment under the <em>result</em> value.
-module(cowboy_handler).
-behaviour(cowboy_middleware).

-export([execute/2]).
-export([terminate/4]).

-callback init(Req, any())
	-> {ok | module(), Req, any()}
	| {module(), Req, any(), any()}
	when Req::cowboy_req:req().

-callback terminate(any(), map(), any()) -> ok.
-optional_callbacks([terminate/3]).

-spec execute(Req, Env) -> {ok, Req, Env}
	when Req::cowboy_req:req(), Env::cowboy_middleware:env().

---

#### `terminate/4`

---


## cowboy_http

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `init/6`

**Arguments**: `Parent, Ref, Socket, Transport, ProxyHeader, Opts`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

%% @todo Worth renaming to cowboy_http1.
%% @todo Change use of cow_http to cow_http1 where appropriate.
-module(cowboy_http).

-export([init/6]).
-export([loop/1]).

-export([system_continue/3]).
-export([system_terminate/4]).
-export([system_code_change/4]).

-type opts() :: #{
	active_n => pos_integer(),
	alpn_default_protocol => http | http2,
	chunked => boolean(),
	compress_buffering => boolean(),
	compress_threshold => non_neg_integer(),
	connection_type => worker | supervisor,
	dynamic_buffer => false | {pos_integer(), pos_integer()},
	dynamic_buffer_initial_average => non_neg_integer(),
	dynamic_buffer_initial_size => pos_integer(),
	env => cowboy_middleware:env(),
	hibernate => boolean(),
	http10_keepalive => boolean(),
	idle_timeout => timeout(),
	inactivity_timeout => timeout(),
	initial_stream_flow_size => non_neg_integer(),
	linger_timeout => timeout(),
	logger => module(),
	max_authority_length => non_neg_integer(),
	max_empty_lines => non_neg_integer(),
	max_header_name_length => non_neg_integer(),
	max_header_value_length => non_neg_integer(),
	max_headers => non_neg_integer(),
	max_keepalive => non_neg_integer(),
	max_method_length => non_neg_integer(),
	max_request_line_length => non_neg_integer(),
	metrics_callback => cowboy_metrics_h:metrics_callback(),
	metrics_req_filter => fun((cowboy_req:req()) -> map()),
	metrics_resp_headers_filter => fun((cowboy:http_headers()) -> cowboy:http_headers()),
	middlewares => [module()],
	protocols => [http | http2],
	proxy_header => boolean(),
	request_timeout => timeout(),
	reset_idle_timeout_on_send => boolean(),
	sendfile => boolean(),
	shutdown_timeout => timeout(),
	stream_handlers => [module()],
	tracer_callback => cowboy_tracer_h:tracer_callback(),
	tracer_flags => [atom()],
	tracer_match_specs => cowboy_tracer_h:tracer_match_specs(),
	%% Open ended because configured stream handlers might add options.
	_ => _
}.
-export_type([opts/0]).

-record(ps_request_line, {
	empty_lines = 0 :: non_neg_integer()
}).

-record(ps_header, {
	method = undefined :: binary(),
	authority = undefined :: binary() | undefined,
	path = undefined :: binary(),
	qs = undefined :: binary(),
	version = undefined :: cowboy:http_version(),
	headers = undefined :: cowboy:http_headers() | undefined,
	name = undefined :: binary() | undefined
}).

-record(ps_body, {
	length :: non_neg_integer() | undefined,
	received = 0 :: non_neg_integer(),
	transfer_decode_fun :: fun((binary(), cow_http_te:state()) -> cow_http_te:decode_ret()),
	transfer_decode_state :: cow_http_te:state()
}).

-record(stream, {
	id = undefined :: cowboy_stream:streamid(),
	%% Stream handlers and their state.
	state = undefined :: {module(), any()},
	%% Request method.
	method = undefined :: binary(),
	%% Client HTTP version for this stream.
	version = undefined :: cowboy:http_version(),
	%% Unparsed te header. Used to know if we can send trailers.
	te :: undefined | binary(),
	%% Expected body size.
	local_expected_size = undefined :: undefined | non_neg_integer(),
	%% Sent body size.
	local_sent_size = 0 :: non_neg_integer(),
	%% Commands queued.
	queue = [] :: cowboy_stream:commands()
}).

-type stream() :: #stream{}.

-record(state, {
	parent :: pid(),
	ref :: ranch:ref(),
	socket :: inet:socket(),
	transport :: module(),
	proxy_header :: undefined | ranch_proxy_header:proxy_info(),
	opts = #{} :: cowboy:opts(),
	buffer = <<>> :: binary(),

	%% Some options may be overriden for the current stream.
	overriden_opts = #{} :: cowboy:opts(),

	%% Remote address and port for the connection.
	peer = undefined :: {inet:ip_address(), inet:port_number()},

	%% Local address and port for the connection.
	sock = undefined :: {inet:ip_address(), inet:port_number()},

	%% Client certificate (TLS only).
	cert :: undefined | binary(),

	timer = undefined :: undefined | reference(),

	%% Whether we are currently receiving data from the socket.
	active = true :: boolean(),

	%% Identifier for the stream currently being read (or waiting to be received).
	in_streamid = 1 :: pos_integer(),

	%% Parsing state for the current stream or stream-to-be.
	in_state = #ps_request_line{} :: #ps_request_line{} | #ps_header{} | #ps_body{},

	%% Flow requested for the current stream.
	flow = infinity :: non_neg_integer() | infinity,

	%% Dynamic buffer moving average and current buffer size.
	dynamic_buffer_size :: pos_integer() | false,
	dynamic_buffer_moving_average :: non_neg_integer(),

	%% Identifier for the stream currently being written.
	%% Note that out_streamid =< in_streamid.
	out_streamid = 1 :: pos_integer(),

	%% Whether we finished writing data for the current stream.
	out_state = wait :: wait | chunked | streaming | done,

	%% The connection will be closed after this stream.
	last_streamid = undefined :: pos_integer(),

	%% Currently active HTTP/1.1 streams.
	streams = [] :: [stream()],

	%% Children processes created by streams.
	children = cowboy_children:init() :: cowboy_children:children()
}).

-include_lib("cowlib/include/cow_inline.hrl").
-include_lib("cowlib/include/cow_parse.hrl").

-spec init(pid(), ranch:ref(), inet:socket(), module(),
	ranch_proxy_header:proxy_info(), cowboy:opts()) -> ok.

---

#### `loop/1`

---

#### `system_code_change/4`

---

#### `system_continue/3`

**Arguments**: `_, _, State`

**Description**: System callbacks.

-spec system_continue(_, _, #state{}) -> ok.

---

#### `system_terminate/4`

---


## cowboy_http2

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `init/10`

**Arguments**: `Parent, Ref, Socket, Transport, ProxyHeader, Opts, Peer, Sock, Cert, Buffer,
		_Settings, Req=#{method := Method}`

**Description**: @todo Add an argument for the request body.
-spec init(pid(), ranch:ref(), inet:socket(), module(),
	ranch_proxy_header:proxy_info() | undefined, cowboy:opts(),
	{inet:ip_address(), inet:port_number()}, {inet:ip_address(), inet:port_number()},
	binary() | undefined, binary(), map() | undefined, cowboy_req:req()) -> no_return().

---

#### `init/12`

**Arguments**: `Parent, Ref, Socket, Transport, ProxyHeader, Opts, Peer, Sock, Cert, Buffer,
		_Settings, Req=#{method := Method}`

**Description**: @todo Add an argument for the request body.
-spec init(pid(), ranch:ref(), inet:socket(), module(),
	ranch_proxy_header:proxy_info() | undefined, cowboy:opts(),
	{inet:ip_address(), inet:port_number()}, {inet:ip_address(), inet:port_number()},
	binary() | undefined, binary(), map() | undefined, cowboy_req:req()) -> no_return().

---

#### `init/6`

**Arguments**: `Parent, Ref, Socket, Transport, ProxyHeader, Opts, Peer, Sock, Cert, Buffer,
		_Settings, Req=#{method := Method}`

**Description**: @todo Add an argument for the request body.
-spec init(pid(), ranch:ref(), inet:socket(), module(),
	ranch_proxy_header:proxy_info() | undefined, cowboy:opts(),
	{inet:ip_address(), inet:port_number()}, {inet:ip_address(), inet:port_number()},
	binary() | undefined, binary(), map() | undefined, cowboy_req:req()) -> no_return().

---

#### `loop/2`

---

#### `system_code_change/4`

---

#### `system_continue/3`

**Arguments**: `_, _, {State, Buffer}`

**Description**: System callbacks.

-spec system_continue(_, _, {#state{}, binary()}) -> no_return().

---

#### `system_terminate/4`

---


## cowboy_http3

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `init/4`

**Arguments**: `Parent, Ref, Conn, Opts`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

%% A key difference between cowboy_http2 and cowboy_http3
%% is that HTTP/3 streams are QUIC streams and therefore
%% much of the connection state is handled outside of
%% Cowboy.

-module(cowboy_http3).

-export([init/4]).

%% Temporary callback to do sendfile over QUIC.
-export([send/2]).

%% @todo Graceful shutdown? Linger? Timeouts? Frame rates? PROXY header?
-type opts() :: #{
	compress_buffering => boolean(),
	compress_threshold => non_neg_integer(),
	connection_type => worker | supervisor,
	enable_connect_protocol => boolean(),
	env => cowboy_middleware:env(),
	logger => module(),
	max_decode_blocked_streams => 0..16#3fffffffffffffff,
	max_decode_table_size => 0..16#3fffffffffffffff,
	max_encode_blocked_streams => 0..16#3fffffffffffffff,
	max_encode_table_size => 0..16#3fffffffffffffff,
	max_ignored_frame_size_received => non_neg_integer() | infinity,
	metrics_callback => cowboy_metrics_h:metrics_callback(),
	metrics_req_filter => fun((cowboy_req:req()) -> map()),
	metrics_resp_headers_filter => fun((cowboy:http_headers()) -> cowboy:http_headers()),
	middlewares => [module()],
	shutdown_timeout => timeout(),
	stream_handlers => [module()],
	tracer_callback => cowboy_tracer_h:tracer_callback(),
	tracer_flags => [atom()],
	tracer_match_specs => cowboy_tracer_h:tracer_match_specs(),
	%% Open ended because configured stream handlers might add options.
	_ => _
}.
-export_type([opts/0]).

%% HTTP/3 or WebTransport stream.
%%
%% WebTransport sessions involve one bidirectional CONNECT stream
%% that must stay open (and can be used for signaling using the
%% Capsule Protocol) and an application-defined number of
%% unidirectional and bidirectional streams, as well as datagrams.
%%
%% WebTransport sessions run in the CONNECT request process and
%% all events related to the session is sent there as a message.
%% The pid of the process is kept in the state.
-record(stream, {
	id :: cow_http3:stream_id(),

	%% Whether the stream is currently in a special state.
	status :: header | {unidi, control | encoder | decoder}
		| normal | {data | ignore, non_neg_integer()} | stopping
		| {webtransport_session, normal | {ignore, non_neg_integer()}}
		| {webtransport_stream, cow_http3:stream_id()},

	%% Stream buffer.
	buffer = <<>> :: binary(),

	%% Stream state.
	state = undefined :: undefined | {module(), any()}
}).

-record(state, {
	parent :: pid(),
	ref :: ranch:ref(),
	conn :: cowboy_quicer:quicer_connection_handle(),
	opts = #{} :: opts(),

	%% Remote address and port for the connection.
	peer = undefined :: {inet:ip_address(), inet:port_number()},

	%% Local address and port for the connection.
	sock = undefined :: {inet:ip_address(), inet:port_number()},

	%% Client certificate.
	cert :: undefined | binary(),

	%% HTTP/3 state machine.
	http3_machine :: cow_http3_machine:http3_machine(),

	%% Specially handled local unidi streams.
	local_control_id = undefined :: undefined | cow_http3:stream_id(),
	local_encoder_id = undefined :: undefined | cow_http3:stream_id(),
	local_decoder_id = undefined :: undefined | cow_http3:stream_id(),

	%% Bidirectional streams used for requests and responses,
	%% as well as unidirectional streams initiated by the client.
	streams = #{} :: #{cow_http3:stream_id() => #stream{}},

	%% Lingering streams that were recently reset. We may receive
	%% pending data or messages for these streams a short while
	%% after they have been reset.
	lingering_streams = [] :: [non_neg_integer()],

	%% Streams can spawn zero or more children which are then managed
	%% by this module if operating as a supervisor.
	children = cowboy_children:init() :: cowboy_children:children()
}).

-spec init(pid(), ranch:ref(), cowboy_quicer:quicer_connection_handle(), opts())
	-> no_return().

---

#### `send/2`

**Arguments**: `{Conn, StreamID}, IoData`

**Description**: Temporary callback to do sendfile over QUIC.
-spec send({cowboy_quicer:quicer_connection_handle(), cow_http3:stream_id()},
	iodata()) -> ok | {error, any()}.

---


## cowboy_loop

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `loop/5`

**Arguments**: `Req=#{pid := Parent}, Env, Handler, HandlerState, Timeout`

**Description**: @todo Handle system messages.

---

#### `system_code_change/4`

---

#### `system_continue/3`

**Arguments**: `_, _, {Req, Env, Handler, HandlerState, Timeout}`

**Description**: System callbacks.

-spec system_continue(_, _, {Req, Env, module(), any(), timeout()})
	-> {ok, Req, Env} | {suspend, ?MODULE, loop, [any()]}
	when Req::cowboy_req:req(), Env::cowboy_middleware:env().

---

#### `system_terminate/4`

---

#### `upgrade/4`

**Arguments**: `Req, Env, Handler, HandlerState`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_loop).
-behaviour(cowboy_sub_protocol).

-export([upgrade/4]).
-export([upgrade/5]).
-export([loop/5]).

-export([system_continue/3]).
-export([system_terminate/4]).
-export([system_code_change/4]).

%% From gen_server.
-define(is_timeout(X), ((X) =:= infinity orelse (is_integer(X) andalso (X) >= 0))).

-callback init(Req, any())
	-> {ok | module(), Req, any()}
	| {module(), Req, any(), any()}
	when Req::cowboy_req:req().

-callback info(any(), Req, State)
	-> {ok, Req, State}
	| {ok, Req, State, hibernate}
	| {stop, Req, State}
	when Req::cowboy_req:req(), State::any().

-callback terminate(any(), cowboy_req:req(), any()) -> ok.
-optional_callbacks([terminate/3]).

-spec upgrade(Req, Env, module(), any())
	-> {ok, Req, Env} | {suspend, ?MODULE, loop, [any()]}
	when Req::cowboy_req:req(), Env::cowboy_middleware:env().

---

#### `upgrade/5`

**Arguments**: `Req, Env, Handler, HandlerState`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_loop).
-behaviour(cowboy_sub_protocol).

-export([upgrade/4]).
-export([upgrade/5]).
-export([loop/5]).

-export([system_continue/3]).
-export([system_terminate/4]).
-export([system_code_change/4]).

%% From gen_server.
-define(is_timeout(X), ((X) =:= infinity orelse (is_integer(X) andalso (X) >= 0))).

-callback init(Req, any())
	-> {ok | module(), Req, any()}
	| {module(), Req, any(), any()}
	when Req::cowboy_req:req().

-callback info(any(), Req, State)
	-> {ok, Req, State}
	| {ok, Req, State, hibernate}
	| {stop, Req, State}
	when Req::cowboy_req:req(), State::any().

-callback terminate(any(), cowboy_req:req(), any()) -> ok.
-optional_callbacks([terminate/3]).

-spec upgrade(Req, Env, module(), any())
	-> {ok, Req, Env} | {suspend, ?MODULE, loop, [any()]}
	when Req::cowboy_req:req(), Env::cowboy_middleware:env().

---


## cowboy_metrics_h

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `data/4`

---

#### `early_error/5`

---

#### `info/3`

---

#### `init/3`

**Arguments**: `StreamID, Req=#{ref := Ref}, Opts=#{metrics_callback := Fun}`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_metrics_h).
-behavior(cowboy_stream).

-export([init/3]).
-export([data/4]).
-export([info/3]).
-export([terminate/3]).
-export([early_error/5]).

-type proc_metrics() :: #{pid() => #{
	%% Time at which the process spawned.
	spawn := integer(),

	%% Time at which the process exited.
	exit => integer(),

	%% Reason for the process exit.
	reason => any()
}}.

-type informational_metrics() :: #{
	%% Informational response status.
	status := cowboy:http_status(),

	%% Headers sent with the informational response.
	headers := cowboy:http_headers(),

	%% Time when the informational response was sent.
	time := integer()
}.

-type metrics() :: #{
	%% The identifier for this listener.
	ref := ranch:ref(),

	%% The pid for this connection.
	pid := pid(),

	%% The streamid also indicates the total number of requests on
	%% this connection (StreamID div 2 + 1).
	streamid := cowboy_stream:streamid(),

	%% The terminate reason is always useful.
	reason := cowboy_stream:reason(),

	%% A filtered Req object or a partial Req object
	%% depending on how far the request got to.
	req => cowboy_req:req(),
	partial_req => cowboy_stream:partial_req(),

	%% Response status.
	resp_status := cowboy:http_status(),

	%% Filtered response headers.
	resp_headers := cowboy:http_headers(),

	%% Start/end of the processing of the request.
	%%
	%% This represents the time from this stream handler's init
	%% to terminate.
	req_start => integer(),
	req_end => integer(),

	%% Start/end of the receiving of the request body.
	%% Begins when the first packet has been received.
	req_body_start => integer(),
	req_body_end => integer(),

	%% Start/end of the sending of the response.
	%% Begins when we send the headers and ends on the final
	%% packet of the response body. If everything is sent at
	%% once these values are identical.
	resp_start => integer(),
	resp_end => integer(),

	%% For early errors all we get is the time we received it.
	early_error_time => integer(),

	%% Start/end of spawned processes. This is where most of
	%% the user code lies, excluding stream handlers. On a
	%% default Cowboy configuration there should be only one
	%% process: the request process.
	procs => proc_metrics(),

	%% Informational responses sent before the final response.
	informational => [informational_metrics()],

	%% Length of the request and response bodies. This does
	%% not include the framing.
	req_body_length => non_neg_integer(),
	resp_body_length => non_neg_integer(),

	%% Additional metadata set by the user.
	user_data => map()
}.
-export_type([metrics/0]).

-type metrics_callback() :: fun((metrics()) -> any()).
-export_type([metrics_callback/0]).

-record(state, {
	next :: any(),
	callback :: fun((metrics()) -> any()),
	resp_headers_filter :: undefined | fun((cowboy:http_headers()) -> cowboy:http_headers()),
	req :: map(),
	resp_status :: undefined | cowboy:http_status(),
	resp_headers :: undefined | cowboy:http_headers(),
	ref :: ranch:ref(),
	req_start :: integer(),
	req_end :: undefined | integer(),
	req_body_start :: undefined | integer(),
	req_body_end :: undefined | integer(),
	resp_start :: undefined | integer(),
	resp_end :: undefined | integer(),
	procs = #{} :: proc_metrics(),
	informational = [] :: [informational_metrics()],
	req_body_length = 0 :: non_neg_integer(),
	resp_body_length = 0 :: non_neg_integer(),
	user_data = #{} :: map()
}).

-spec init(cowboy_stream:streamid(), cowboy_req:req(), cowboy:opts())
	-> {[{spawn, pid(), timeout()}], #state{}}.

---

#### `terminate/3`

---


## cowboy_quicer

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `handle/1`

**Arguments**: `{quic, transport_shutdown, _Conn, _Flags}`

**Description**: QUIC_CONNECTION_EVENT_SHUTDOWN_INITIATED_BY_TRANSPORT

---

#### `peercert/1`

---

#### `peername/1`

**Arguments**: `Conn`

**Description**: @todo Make quicer export these types.
-type quicer_connection_handle() :: reference().
-export_type([quicer_connection_handle/0]).

-type quicer_app_errno() :: non_neg_integer().

-include_lib("quicer/include/quicer.hrl").

%% Connection.

-spec peername(quicer_connection_handle())
	-> {ok, {inet:ip_address(), inet:port_number()}}
	| {error, any()}.

---

#### `send/3`

---

#### `send/4`

---

#### `send_datagram/2`

---

#### `shutdown/2`

---

#### `shutdown_stream/2`

**Arguments**: `_Conn, StreamID`

**Description**: @todo Fix/ignore the Dialyzer error instead of doing this.
	DataBin = iolist_to_binary(Data),
	Size = byte_size(DataBin),
	case quicer:send_dgram(Conn, DataBin) of
		{ok, Size} ->
			ok;
		%% @todo Handle error cases.
		Error ->
			Error
	end.

-spec shutdown_stream(quicer_connection_handle(), cow_http3:stream_id())
	-> ok.

---

#### `shutdown_stream/4`

**Arguments**: `_Conn, StreamID`

**Description**: @todo Fix/ignore the Dialyzer error instead of doing this.
	DataBin = iolist_to_binary(Data),
	Size = byte_size(DataBin),
	case quicer:send_dgram(Conn, DataBin) of
		{ok, Size} ->
			ok;
		%% @todo Handle error cases.
		Error ->
			Error
	end.

-spec shutdown_stream(quicer_connection_handle(), cow_http3:stream_id())
	-> ok.

---

#### `sockname/1`

---

#### `start_bidi_stream/2`

**Arguments**: `Conn, InitialData`

**Description**: Streams.

-spec start_bidi_stream(quicer_connection_handle(), iodata())
	-> {ok, cow_http3:stream_id()}
	| {error, any()}.

---

#### `start_unidi_stream/2`

---


## cowboy_req

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
Copyright (c) Anthony Ramine <nox@dev-extend.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN

### Exported Functions

#### `binding/2`

**Arguments**: `Name, Req`

**Description**: Disable individual components.
	<<"//localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{scheme => undefined})),
	<<"/path?dummy=2785">> = iolist_to_binary(uri(Req, #{host => undefined})),
	<<"http://localhost/path?dummy=2785">> = iolist_to_binary(uri(Req, #{port => undefined})),
	<<"http://localhost:8080?dummy=2785">> = iolist_to_binary(uri(Req, #{path => undefined})),
	<<"http://localhost:8080/path">> = iolist_to_binary(uri(Req, #{qs => undefined})),
	<<"http://localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{fragment => undefined})),
	<<"http://localhost:8080">> = iolist_to_binary(uri(Req, #{path => undefined, qs => undefined})),
	<<>> = iolist_to_binary(uri(Req, #{host => undefined, path => undefined, qs => undefined})),
	%% Empty values.
	<<"//localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{scheme => <<>>})),
	<<"//localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{scheme => ""})),
	<<"//localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{scheme => [<<>>]})),
	<<"/path?dummy=2785">> = iolist_to_binary(uri(Req, #{host => <<>>})),
	<<"/path?dummy=2785">> = iolist_to_binary(uri(Req, #{host => ""})),
	<<"/path?dummy=2785">> = iolist_to_binary(uri(Req, #{host => [<<>>]})),
	<<"http://localhost:8080?dummy=2785">> = iolist_to_binary(uri(Req, #{path => <<>>})),
	<<"http://localhost:8080?dummy=2785">> = iolist_to_binary(uri(Req, #{path => ""})),
	<<"http://localhost:8080?dummy=2785">> = iolist_to_binary(uri(Req, #{path => [<<>>]})),
	<<"http://localhost:8080/path">> = iolist_to_binary(uri(Req, #{qs => <<>>})),
	<<"http://localhost:8080/path">> = iolist_to_binary(uri(Req, #{qs => ""})),
	<<"http://localhost:8080/path">> = iolist_to_binary(uri(Req, #{qs => [<<>>]})),
	<<"http://localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{fragment => <<>>})),
	<<"http://localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{fragment => ""})),
	<<"http://localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{fragment => [<<>>]})),
	%% Port is integer() | undefined.
	{'EXIT', _} = (catch iolist_to_binary(uri(Req, #{port => <<>>}))),
	{'EXIT', _} = (catch iolist_to_binary(uri(Req, #{port => ""}))),
	{'EXIT', _} = (catch iolist_to_binary(uri(Req, #{port => [<<>>]}))),
	%% Update components.
	<<"https://localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{scheme => "https"})),
	<<"http://example.org:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{host => "example.org"})),
	<<"http://localhost:123/path?dummy=2785">> = iolist_to_binary(uri(Req, #{port => 123})),
	<<"http://localhost:8080/custom?dummy=2785">> = iolist_to_binary(uri(Req, #{path => "/custom"})),
	<<"http://localhost:8080/path?smart=42">> = iolist_to_binary(uri(Req, #{qs => "smart=42"})),
	<<"http://localhost:8080/path?dummy=2785#intro">> = iolist_to_binary(uri(Req, #{fragment => "intro"})),
	%% Interesting combinations.
	<<"http://localhost/path?dummy=2785">> = iolist_to_binary(uri(Req, #{port => 80})),
	<<"https://localhost/path?dummy=2785">> = iolist_to_binary(uri(Req, #{scheme => "https", port => 443})),
	ok.
-endif.

-spec binding(atom(), req()) -> any() | undefined.

---

#### `binding/3`

**Arguments**: `Name, Req`

**Description**: Disable individual components.
	<<"//localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{scheme => undefined})),
	<<"/path?dummy=2785">> = iolist_to_binary(uri(Req, #{host => undefined})),
	<<"http://localhost/path?dummy=2785">> = iolist_to_binary(uri(Req, #{port => undefined})),
	<<"http://localhost:8080?dummy=2785">> = iolist_to_binary(uri(Req, #{path => undefined})),
	<<"http://localhost:8080/path">> = iolist_to_binary(uri(Req, #{qs => undefined})),
	<<"http://localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{fragment => undefined})),
	<<"http://localhost:8080">> = iolist_to_binary(uri(Req, #{path => undefined, qs => undefined})),
	<<>> = iolist_to_binary(uri(Req, #{host => undefined, path => undefined, qs => undefined})),
	%% Empty values.
	<<"//localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{scheme => <<>>})),
	<<"//localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{scheme => ""})),
	<<"//localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{scheme => [<<>>]})),
	<<"/path?dummy=2785">> = iolist_to_binary(uri(Req, #{host => <<>>})),
	<<"/path?dummy=2785">> = iolist_to_binary(uri(Req, #{host => ""})),
	<<"/path?dummy=2785">> = iolist_to_binary(uri(Req, #{host => [<<>>]})),
	<<"http://localhost:8080?dummy=2785">> = iolist_to_binary(uri(Req, #{path => <<>>})),
	<<"http://localhost:8080?dummy=2785">> = iolist_to_binary(uri(Req, #{path => ""})),
	<<"http://localhost:8080?dummy=2785">> = iolist_to_binary(uri(Req, #{path => [<<>>]})),
	<<"http://localhost:8080/path">> = iolist_to_binary(uri(Req, #{qs => <<>>})),
	<<"http://localhost:8080/path">> = iolist_to_binary(uri(Req, #{qs => ""})),
	<<"http://localhost:8080/path">> = iolist_to_binary(uri(Req, #{qs => [<<>>]})),
	<<"http://localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{fragment => <<>>})),
	<<"http://localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{fragment => ""})),
	<<"http://localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{fragment => [<<>>]})),
	%% Port is integer() | undefined.
	{'EXIT', _} = (catch iolist_to_binary(uri(Req, #{port => <<>>}))),
	{'EXIT', _} = (catch iolist_to_binary(uri(Req, #{port => ""}))),
	{'EXIT', _} = (catch iolist_to_binary(uri(Req, #{port => [<<>>]}))),
	%% Update components.
	<<"https://localhost:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{scheme => "https"})),
	<<"http://example.org:8080/path?dummy=2785">> = iolist_to_binary(uri(Req, #{host => "example.org"})),
	<<"http://localhost:123/path?dummy=2785">> = iolist_to_binary(uri(Req, #{port => 123})),
	<<"http://localhost:8080/custom?dummy=2785">> = iolist_to_binary(uri(Req, #{path => "/custom"})),
	<<"http://localhost:8080/path?smart=42">> = iolist_to_binary(uri(Req, #{qs => "smart=42"})),
	<<"http://localhost:8080/path?dummy=2785#intro">> = iolist_to_binary(uri(Req, #{fragment => "intro"})),
	%% Interesting combinations.
	<<"http://localhost/path?dummy=2785">> = iolist_to_binary(uri(Req, #{port => 80})),
	<<"https://localhost/path?dummy=2785">> = iolist_to_binary(uri(Req, #{scheme => "https", port => 443})),
	ok.
-endif.

-spec binding(atom(), req()) -> any() | undefined.

---

#### `bindings/1`

---

#### `body_length/1`

**Arguments**: `#{body_length := Length}`

**Description**: The length may not be known if HTTP/1.1 with a transfer-encoding;
%% or HTTP/2 with no content-length header. The length is always
%% known once the body has been completely read.
-spec body_length(req()) -> undefined | non_neg_integer().

---

#### `cast/2`

**Arguments**: `Msg, #{pid := Pid, streamid := StreamID}`

**Description**: Stream handlers.

-spec cast(any(), req()) -> ok.

---

#### `cert/1`

---

#### `delete_resp_header/2`

**Arguments**: `_, Req`

**Description**: There are no resp headers so we have nothing to delete.

---

#### `filter_cookies/2`

---

#### `has_body/1`

**Arguments**: `#{has_body := HasBody}`

**Description**: Request body.

-spec has_body(req()) -> boolean().

---

#### `has_resp_body/1`

---

#### `has_resp_header/2`

---

#### `header/2`

---

#### `header/3`

---

#### `headers/1`

---

#### `host/1`

---

#### `host_info/1`

**Arguments**: `#{host_info := HostInfo}`

**Description**: @todo The host_info is undefined if cowboy_router isn't used. Do we want to crash?
-spec host_info(req()) -> cowboy_router:tokens() | undefined.

---

#### `inform/2`

---

#### `inform/3`

---

#### `match_cookies/2`

---

#### `match_qs/2`

---

#### `method/1`

**Arguments**: `#{method := Method}`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Copyright (c) Anthony Ramine <nox@dev-extend.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_req).

%% Request.
-export([method/1]).
-export([version/1]).
-export([peer/1]).
-export([sock/1]).
-export([cert/1]).
-export([scheme/1]).
-export([host/1]).
-export([host_info/1]).
-export([port/1]).
-export([path/1]).
-export([path_info/1]).
-export([qs/1]).
-export([parse_qs/1]).
-export([match_qs/2]).
-export([uri/1]).
-export([uri/2]).
-export([binding/2]).
-export([binding/3]).
-export([bindings/1]).
-export([header/2]).
-export([header/3]).
-export([headers/1]).
-export([parse_header/2]).
-export([parse_header/3]).
-export([filter_cookies/2]).
-export([parse_cookies/1]).
-export([match_cookies/2]).

%% Request body.
-export([has_body/1]).
-export([body_length/1]).
-export([read_body/1]).
-export([read_body/2]).
-export([read_urlencoded_body/1]).
-export([read_urlencoded_body/2]).
-export([read_and_match_urlencoded_body/2]).
-export([read_and_match_urlencoded_body/3]).

%% Multipart.
-export([read_part/1]).
-export([read_part/2]).
-export([read_part_body/1]).
-export([read_part_body/2]).

%% Response.
-export([set_resp_cookie/3]).
-export([set_resp_cookie/4]).
-export([resp_header/2]).
-export([resp_header/3]).
-export([resp_headers/1]).
-export([set_resp_header/3]).
-export([set_resp_headers/2]).
-export([has_resp_header/2]).
-export([delete_resp_header/2]).
-export([set_resp_body/2]).
%% @todo set_resp_body/3 with a ContentType or even Headers argument, to set content headers.
-export([has_resp_body/1]).
-export([inform/2]).
-export([inform/3]).
-export([reply/2]).
-export([reply/3]).
-export([reply/4]).
-export([stream_reply/2]).
-export([stream_reply/3]).
%% @todo stream_body/2 (nofin)
-export([stream_body/3]).
%% @todo stream_events/2 (nofin)
-export([stream_events/3]).
-export([stream_trailers/2]).
-export([push/3]).
-export([push/4]).

%% Stream handlers.
-export([cast/2]).

%% Internal.
-export([response_headers/2]).

-type read_body_opts() :: #{
	length => non_neg_integer() | infinity,
	period => non_neg_integer(),
	timeout => timeout()
}.
-export_type([read_body_opts/0]).

%% While sendfile allows a Len of 0 that means "everything past Offset",
%% Cowboy expects the real length as it is used as metadata.
-type resp_body() :: iodata()
	| {sendfile, non_neg_integer(), non_neg_integer(), file:name_all()}.
-export_type([resp_body/0]).

-type push_opts() :: #{
	method => binary(),
	scheme => binary(),
	host => binary(),
	port => inet:port_number(),
	qs => binary()
}.
-export_type([push_opts/0]).

-type req() :: #{
	%% Public interface.
	method := binary(),
	version := cowboy:http_version() | atom(),
	scheme := binary(),
	host := binary(),
	port := inet:port_number(),
	path := binary(),
	qs := binary(),
	headers := cowboy:http_headers(),
	peer := {inet:ip_address(), inet:port_number()},
	sock := {inet:ip_address(), inet:port_number()},
	cert := binary() | undefined,

	%% Private interface.
	ref := ranch:ref(),
	pid := pid(),
	streamid := cowboy_stream:streamid(),

	host_info => cowboy_router:tokens(),
	path_info => cowboy_router:tokens(),
	bindings => cowboy_router:bindings(),

	has_body := boolean(),
	body_length := non_neg_integer() | undefined,
	has_read_body => true,
	multipart => {binary(), binary()} | done,

	has_sent_resp => headers | true,
	resp_cookies => #{iodata() => iodata()},
	resp_headers => #{binary() => iodata()},
	resp_body => resp_body(),

	proxy_header => ranch_proxy_header:proxy_info(),
	media_type => {binary(), binary(), [{binary(), binary()}]},
	language => binary() | undefined,
	charset => binary() | undefined,
	range => {binary(), binary()
		| [{non_neg_integer(), non_neg_integer() | infinity} | neg_integer()]},
	websocket_version => 7 | 8 | 13,

	%% The user is encouraged to use the Req to store information
	%% when no better solution is available.
	_ => _
}.
-export_type([req/0]).

%% Request.

-spec method(req()) -> binary().

---

#### `parse_cookies/1`

---

#### `parse_header/2`

---

#### `parse_header/3`

---

#### `parse_qs/1`

**Arguments**: `#{qs := Qs}`

**Description**: @todo Might be useful to limit the number of keys.
-spec parse_qs(req()) -> [{binary(), binary() | true}].

---

#### `path/1`

---

#### `path_info/1`

**Arguments**: `#{path_info := PathInfo}`

**Description**: @todo The path_info is undefined if cowboy_router isn't used. Do we want to crash?
-spec path_info(req()) -> cowboy_router:tokens() | undefined.

---

#### `peer/1`

---

#### `port/1`

---

#### `push/3`

**Arguments**: `_, _, #{has_sent_resp := _}, _`

**Description**: @todo Optimization: don't send anything at all for HTTP/1.0 and HTTP/1.1.
%% @todo Path, Headers, Opts, everything should be in proper binary,
%% or normalized when creating the Req object.
-spec push(iodata(), cowboy:http_headers(), req(), push_opts()) -> ok.

---

#### `push/4`

**Arguments**: `_, _, #{has_sent_resp := _}, _`

**Description**: @todo Optimization: don't send anything at all for HTTP/1.0 and HTTP/1.1.
%% @todo Path, Headers, Opts, everything should be in proper binary,
%% or normalized when creating the Req object.
-spec push(iodata(), cowboy:http_headers(), req(), push_opts()) -> ok.

---

#### `qs/1`

---

#### `read_and_match_urlencoded_body/2`

---

#### `read_and_match_urlencoded_body/3`

---

#### `read_body/1`

---

#### `read_body/2`

---

#### `read_part/1`

**Arguments**: `Req`

**Description**: Multipart.

-spec read_part(Req)
	-> {ok, cowboy:http_headers(), Req} | {done, Req}
	when Req::req().

---

#### `read_part/2`

**Arguments**: `Req`

**Description**: Multipart.

-spec read_part(Req)
	-> {ok, cowboy:http_headers(), Req} | {done, Req}
	when Req::req().

---

#### `read_part_body/1`

**Arguments**: `Req`

**Description**: Reject multipart content containing duplicate headers.
			true = map_size(Headers) =:= length(Headers0),
			{ok, Headers, Req#{multipart => {Boundary, Rest}}};
		%% Ignore epilogue.
		{done, _} ->
			{done, Req#{multipart => done}}
	catch _:_:Stacktrace ->
		erlang:raise(exit, {request_error, {multipart, headers},
			'Malformed body; multipart expected.'
		}, Stacktrace)
	end.

-spec read_part_body(Req)
	-> {ok, binary(), Req} | {more, binary(), Req}
	when Req::req().

---

#### `read_part_body/2`

**Arguments**: `Req`

**Description**: Reject multipart content containing duplicate headers.
			true = map_size(Headers) =:= length(Headers0),
			{ok, Headers, Req#{multipart => {Boundary, Rest}}};
		%% Ignore epilogue.
		{done, _} ->
			{done, Req#{multipart => done}}
	catch _:_:Stacktrace ->
		erlang:raise(exit, {request_error, {multipart, headers},
			'Malformed body; multipart expected.'
		}, Stacktrace)
	end.

-spec read_part_body(Req)
	-> {ok, binary(), Req} | {more, binary(), Req}
	when Req::req().

---

#### `read_urlencoded_body/1`

---

#### `read_urlencoded_body/2`

---

#### `reply/2`

**Arguments**: `Status, Headers, Body, Req)
		when Status =:= 204; Status =:= 304 ->
	do_reply_ensure_no_body(Status, Headers, Body, Req);
reply(Status = <<"204",_/bits>>, Headers, Body, Req`

**Description**: 204 responses must not include content-length. 304 responses may
%% but only when set explicitly. (RFC7230 3.3.1, RFC7230 3.3.2)
%% Neither status code must include a response body. (RFC7230 3.3)

---

#### `reply/3`

**Arguments**: `Status, Headers, Body, Req)
		when Status =:= 204; Status =:= 304 ->
	do_reply_ensure_no_body(Status, Headers, Body, Req);
reply(Status = <<"204",_/bits>>, Headers, Body, Req`

**Description**: 204 responses must not include content-length. 304 responses may
%% but only when set explicitly. (RFC7230 3.3.1, RFC7230 3.3.2)
%% Neither status code must include a response body. (RFC7230 3.3)

---

#### `reply/4`

**Arguments**: `Status, Headers, Body, Req)
		when Status =:= 204; Status =:= 304 ->
	do_reply_ensure_no_body(Status, Headers, Body, Req);
reply(Status = <<"204",_/bits>>, Headers, Body, Req`

**Description**: 204 responses must not include content-length. 304 responses may
%% but only when set explicitly. (RFC7230 3.3.1, RFC7230 3.3.2)
%% Neither status code must include a response body. (RFC7230 3.3)

---

#### `resp_header/2`

---

#### `resp_header/3`

---

#### `resp_headers/1`

---

#### `response_headers/2`

**Arguments**: `Headers0, Req`

**Description**: Internal.

%% @todo What about set-cookie headers set through set_resp_header or reply?
-spec response_headers(Headers, req()) -> Headers when Headers::cowboy:http_headers().

---

#### `scheme/1`

---

#### `set_resp_body/2`

---

#### `set_resp_cookie/3`

**Arguments**: `Name, Value, Req, Opts`

**Description**: The cookie name cannot contain any of the following characters:
%%   =,;\s\t\r\n\013\014
%%
%% The cookie value cannot contain any of the following characters:
%%   ,; \t\r\n\013\014
-spec set_resp_cookie(binary(), iodata(), Req, cow_cookie:cookie_opts())
	-> Req when Req::req().

---

#### `set_resp_cookie/4`

**Arguments**: `Name, Value, Req, Opts`

**Description**: The cookie name cannot contain any of the following characters:
%%   =,;\s\t\r\n\013\014
%%
%% The cookie value cannot contain any of the following characters:
%%   ,; \t\r\n\013\014
-spec set_resp_cookie(binary(), iodata(), Req, cow_cookie:cookie_opts())
	-> Req when Req::req().

---

#### `set_resp_header/3`

**Arguments**: `<<"set-cookie">>, _, _`

**Description**: @todo We could add has_resp_cookie and unset_resp_cookie now.

-spec set_resp_header(binary(), iodata(), Req)
	-> Req when Req::req().

---

#### `set_resp_headers/2`

---

#### `sock/1`

---

#### `stream_body/3`

**Arguments**: `Msg, Req=#{pid := Pid}`

**Description**: @todo Do we need a timeout?

---

#### `stream_events/3`

---

#### `stream_reply/2`

**Arguments**: `Status, Headers=#{}, Req)
		when Status =:= 204; Status =:= 304 ->
	reply(Status, Headers, <<>>, Req);
stream_reply(Status = <<"204",_/bits>>, Headers=#{}, Req`

**Description**: 204 and 304 responses must NOT send a body. We therefore
%% transform the call to a full response and expect the user
%% to NOT call stream_body/3 afterwards. (RFC7230 3.3)

---

#### `stream_reply/3`

**Arguments**: `Status, Headers=#{}, Req)
		when Status =:= 204; Status =:= 304 ->
	reply(Status, Headers, <<>>, Req);
stream_reply(Status = <<"204",_/bits>>, Headers=#{}, Req`

**Description**: 204 and 304 responses must NOT send a body. We therefore
%% transform the call to a full response and expect the user
%% to NOT call stream_body/3 afterwards. (RFC7230 3.3)

---

#### `stream_trailers/2`

---

#### `uri/1`

---

#### `uri/2`

---

#### `version/1`

---


## cowboy_rest

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `upgrade/4`

**Arguments**: `Req, Env, Handler, HandlerState, _Opts`

**Description**: cowboy_rest takes no options.

---

#### `upgrade/5`

**Arguments**: `Req, Env, Handler, HandlerState, _Opts`

**Description**: cowboy_rest takes no options.

---


## cowboy_router

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `compile/1`

**Arguments**: `Routes`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

%% Routing middleware.
%%
%% Resolve the handler to be used for the request based on the
%% routing information found in the <em>dispatch</em> environment value.
%% When found, the handler module and associated data are added to
%% the environment as the <em>handler</em> and <em>handler_opts</em> values
%% respectively.
%%
%% If the route cannot be found, processing stops with either
%% a 400 or a 404 reply.
-module(cowboy_router).
-behaviour(cowboy_middleware).

-export([compile/1]).
-export([execute/2]).

-type bindings() :: #{atom() => any()}.
-type tokens() :: [binary()].
-export_type([bindings/0]).
-export_type([tokens/0]).

-type route_match() :: '_' | iodata().
-type route_path() :: {Path::route_match(), Handler::module(), Opts::any()}
	| {Path::route_match(), cowboy:fields(), Handler::module(), Opts::any()}.
-type route_rule() :: {Host::route_match(), Paths::[route_path()]}
	| {Host::route_match(), cowboy:fields(), Paths::[route_path()]}.
-type routes() :: [route_rule()].
-export_type([routes/0]).

-type dispatch_match() :: '_' | <<_:8>> | [binary() | '_' | '...' | atom()].
-type dispatch_path() :: {dispatch_match(), cowboy:fields(), module(), any()}.
-type dispatch_rule() :: {Host::dispatch_match(), cowboy:fields(), Paths::[dispatch_path()]}.
-opaque dispatch_rules() :: [dispatch_rule()].
-export_type([dispatch_rules/0]).

-spec compile(routes()) -> dispatch_rules().

---

#### `execute/2`

---


## cowboy_static

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
Copyright (c) Magnus Klaar <magnus.klaar@gmail.com>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN

### Exported Functions

#### `charsets_provided/2`

**Arguments**: `Req, State={Path, _, Extra}`

**Description**: Detect the charset of the file.

-spec charsets_provided(Req, State)
	-> {[binary()], Req, State} | no_call
	when State::state().

---

#### `content_types_provided/2`

**Arguments**: `Req, State={Path, _, Extra}) when is_list(Extra`

**Description**: Detect the mimetype of the file.

-spec content_types_provided(Req, State)
	-> {[{binary() | {binary(), binary(), '*' | [{binary(), binary()}]}, get_file}], Req, State}
	when State::state().

---

#### `forbidden/2`

**Arguments**: `Req, State={_, {_, #file_info{type=directory}}, _}`

**Description**: Directories, files that can't be accessed at all and
%% files with no read flag are forbidden.

-spec forbidden(Req, State)
	-> {boolean(), Req, State}
	when State::state().

---

#### `generate_etag/2`

**Arguments**: `Req, State={Path, {_, #file_info{size=Size, mtime=Mtime}},
		Extra}`

**Description**: Generate an etag for the file.

-spec generate_etag(Req, State)
	-> {{strong | weak, binary() | undefined}, Req, State}
	when State::state().

---

#### `get_file/2`

**Arguments**: `Req, State={Path, {direct, #file_info{size=Size}}, _}`

**Description**: Stream the file.

-spec get_file(Req, State)
	-> {{sendfile, 0, non_neg_integer(), binary()} | binary(), Req, State}
	when State::state().

---

#### `init/2`

**Arguments**: `Req, {Name, Path}`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Copyright (c) Magnus Klaar <magnus.klaar@gmail.com>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_static).

-export([init/2]).
-export([malformed_request/2]).
-export([forbidden/2]).
-export([content_types_provided/2]).
-export([charsets_provided/2]).
-export([ranges_provided/2]).
-export([resource_exists/2]).
-export([last_modified/2]).
-export([generate_etag/2]).
-export([get_file/2]).

-type extra_charset() :: {charset, module(), function()} | {charset, binary()}.
-type extra_etag() :: {etag, module(), function()} | {etag, false}.
-type extra_mimetypes() :: {mimetypes, module(), function()}
	| {mimetypes, binary() | {binary(), binary(), '*' | [{binary(), binary()}]}}.
-type extra() :: [extra_charset() | extra_etag() | extra_mimetypes()].
-type opts() :: {file | dir, string() | binary()}
	| {file | dir, string() | binary(), extra()}
	| {priv_file | priv_dir, atom(), string() | binary()}
	| {priv_file | priv_dir, atom(), string() | binary(), extra()}.
-export_type([opts/0]).

-include_lib("kernel/include/file.hrl").

-type state() :: {binary(), {direct | archive, #file_info{}}
	| {error, atom()}, extra()}.

%% Resolve the file that will be sent and get its file information.
%% If the handler is configured to manage a directory, check that the
%% requested file is inside the configured directory.

-spec init(Req, opts()) -> {cowboy_rest, Req, error | state()} when Req::cowboy_req:req().

---

#### `last_modified/2`

**Arguments**: `Req, State={_, {_, #file_info{mtime=Modified}}, _}`

**Description**: Return the time of last modification of the file.

-spec last_modified(Req, State)
	-> {calendar:datetime(), Req, State}
	when State::state().

---

#### `malformed_request/2`

**Arguments**: `Req, State`

**Description**: Reject requests that tried to access a file outside
%% the target directory, or used reserved characters.

-spec malformed_request(Req, State)
	-> {boolean(), Req, State}.

---

#### `ranges_provided/2`

**Arguments**: `Req, State`

**Description**: We simulate the callback not being exported.
		false ->
			no_call;
		{charset, Module, Function} ->
			{[Module:Function(Path)], Req, State};
		{charset, Charset} when is_binary(Charset) ->
			{[Charset], Req, State}
	end.

%% Enable support for range requests.

-spec ranges_provided(Req, State)
	-> {[{binary(), auto}], Req, State}
	when State::state().

---

#### `resource_exists/2`

**Arguments**: `Req, State={_, {_, #file_info{type=regular}}, _}`

**Description**: Assume the resource doesn't exist if it's not a regular file.

-spec resource_exists(Req, State)
	-> {boolean(), Req, State}
	when State::state().

---


## cowboy_stream

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `data/4`

**Arguments**: `_, _, _, undefined`

**Description**: We call the next handler and remove it from the list of
			%% stream handlers. This means that handlers that run after
			%% it have no knowledge it exists. Should user require this
			%% knowledge they can just define a separate option that will
			%% be left untouched.
			{Commands, State} = Handler:init(StreamID, Req, Opts#{stream_handlers => Tail}),
			{Commands, {Handler, State}}
	end.

-spec data(streamid(), fin(), binary(), {Handler, State} | undefined)
	-> {commands(), {Handler, State} | undefined}
	when Handler::module(), State::state().

---

#### `early_error/5`

---

#### `info/3`

---

#### `init/3`

**Arguments**: `StreamID, Req, Opts`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_stream).

-type state() :: any().
-type human_reason() :: atom().

-type streamid() :: any().
-export_type([streamid/0]).

-type fin() :: fin | nofin.
-export_type([fin/0]).

%% @todo Perhaps it makes more sense to have resp_body in this module?

-type resp_command()
	:: {response, cowboy:http_status(), cowboy:http_headers(), cowboy_req:resp_body()}.
-export_type([resp_command/0]).

-type commands() :: [{inform, cowboy:http_status(), cowboy:http_headers()}
	| resp_command()
	| {headers, cowboy:http_status(), cowboy:http_headers()}
	| {data, fin(), cowboy_req:resp_body()}
	| {trailers, cowboy:http_headers()}
	| {push, binary(), binary(), binary(), inet:port_number(),
		binary(), binary(), cowboy:http_headers()}
	| {flow, pos_integer()}
	| {spawn, pid(), timeout()}
	| {error_response, cowboy:http_status(), cowboy:http_headers(), iodata()}
	| {switch_protocol, cowboy:http_headers(), module(), state()}
	| {internal_error, any(), human_reason()}
	| {set_options, map()}
	| {log, logger:level(), io:format(), list()}
	| stop].
-export_type([commands/0]).

-type reason() :: normal | switch_protocol
	| {internal_error, timeout | {error | exit | throw, any()}, human_reason()}
	| {socket_error, closed | atom(), human_reason()}
	%% @todo Or cow_http3:error().
	| {stream_error, cow_http2:error(), human_reason()}
	| {connection_error, cow_http2:error(), human_reason()}
	| {stop, cow_http2:frame() | {exit, any()}, human_reason()}.
-export_type([reason/0]).

-type partial_req() :: map(). %% @todo Take what's in cowboy_req with everything? optional.
-export_type([partial_req/0]).

-callback init(streamid(), cowboy_req:req(), cowboy:opts()) -> {commands(), state()}.
-callback data(streamid(), fin(), binary(), State) -> {commands(), State} when State::state().
-callback info(streamid(), any(), State) -> {commands(), State} when State::state().
-callback terminate(streamid(), reason(), state()) -> any().
-callback early_error(streamid(), reason(), partial_req(), Resp, cowboy:opts())
	-> Resp when Resp::resp_command().

%% @todo To optimize the number of active timers we could have a command
%% that enables a timeout that is called in the absence of any other call,
%% similar to what gen_server does. However the nice thing about this is
%% that the connection process can keep a single timer around (the same
%% one that would be used to detect half-closed sockets) and use this
%% timer and other events to trigger the timeout in streams at their
%% intended time.
%%
%% This same timer can be used to try and send PING frames to help detect
%% that the connection is indeed unresponsive.

-export([init/3]).
-export([data/4]).
-export([info/3]).
-export([terminate/3]).
-export([early_error/5]).
-export([make_error_log/5]).

%% Note that this and other functions in this module do NOT catch
%% exceptions. We want the exception to go all the way down to the
%% protocol code.
%%
%% OK the failure scenario is not so clear. The problem is
%% that the failure at any point in init/3 will result in the
%% corresponding state being lost. I am unfortunately not
%% confident we can do anything about this. If the crashing
%% handler just created a process, we'll never know about it.
%% Therefore at this time I choose to leave all failure handling
%% to the protocol process.
%%
%% Note that a failure in init/3 will result in terminate/3
%% NOT being called. This is because the state is not available.

-spec init(streamid(), cowboy_req:req(), cowboy:opts())
	-> {commands(), {module(), state()} | undefined}.

---

#### `make_error_log/5`

**Arguments**: `init, [StreamID, Req, Opts], Class, Exception, Stacktrace`

**Description**: This is the same behavior as in init/3.
			Handler:early_error(StreamID, Reason,
				PartialReq, Resp, Opts#{stream_handlers => Tail})
	end.

-spec make_error_log(init | data | info | terminate | early_error,
	list(), error | exit | throw, any(), list())
	-> {log, error, string(), list()}.

---

#### `terminate/3`

---


## cowboy_stream_h

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `data/4`

**Arguments**: `StreamID, IsFin=nofin, Data, State=#state{
		read_body_length=ReadLen, read_body_buffer=Buffer, body_length=BodyLen})
		when byte_size(Data) + byte_size(Buffer) < ReadLen ->
	do_data(StreamID, IsFin, Data, [], State#state{
		expect=undefined,
		read_body_buffer= << Buffer/binary, Data/binary >>,
		body_length=BodyLen + byte_size(Data)
	});
%% Stream is waiting for data and we received enough to send.
data(StreamID, IsFin, Data, State=#state{read_body_pid=Pid, read_body_ref=Ref,
		read_body_timer_ref=TRef, read_body_buffer=Buffer, body_length=BodyLen0}`

**Description**: @todo This is wrong, it's missing byte_size(Data).
		body_length=BodyLen
	});
%% Stream is waiting for data but we didn't receive enough to send yet.

---

#### `early_error/5`

---

#### `info/3`

**Arguments**: `StreamID, Info, State`

**Description**: Unknown message, either stray or meant for a handler down the line.

---

#### `init/3`

**Arguments**: `StreamID, Req=#{ref := Ref}, Opts`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_stream_h).
-behavior(cowboy_stream).

-export([init/3]).
-export([data/4]).
-export([info/3]).
-export([terminate/3]).
-export([early_error/5]).

-export([request_process/3]).
-export([resume/5]).

-record(state, {
	next :: any(),
	ref = undefined :: ranch:ref(),
	pid = undefined :: pid(),
	expect = undefined :: undefined | continue,
	read_body_pid = undefined :: pid() | undefined,
	read_body_ref = undefined :: reference() | undefined,
	read_body_timer_ref = undefined :: reference() | undefined,
	read_body_length = 0 :: non_neg_integer() | infinity | auto,
	read_body_is_fin = nofin :: nofin | {fin, non_neg_integer()},
	read_body_buffer = <<>> :: binary(),
	body_length = 0 :: non_neg_integer(),
	stream_body_pid = undefined :: pid() | undefined,
	stream_body_status = normal :: normal | blocking | blocked
}).

-spec init(cowboy_stream:streamid(), cowboy_req:req(), cowboy:opts())
	-> {[{spawn, pid(), timeout()}], #state{}}.

---

#### `request_process/3`

**Arguments**: `Req, Env, Middlewares`

**Description**: Request process.

%% We add the stacktrace to exit exceptions here in order
%% to simplify the debugging of errors. The proc_lib library
%% already adds the stacktrace to other types of exceptions.
-spec request_process(cowboy_req:req(), cowboy_middleware:env(), [module()]) -> ok.

---

#### `resume/5`

---

#### `terminate/3`

---


## cowboy_sup

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `init/1`

---

#### `start_link/0`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_sup).
-behaviour(supervisor).

-export([start_link/0]).
-export([init/1]).

-spec start_link() -> {ok, pid()}.

---


## cowboy_tls

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `connection_process/4`

---

#### `start_link/3`

**Arguments**: `Ref, Transport, Opts`

**Description**: Ranch 2.
-spec start_link(ranch:ref(), module(), cowboy:opts()) -> {ok, pid()}.

---

#### `start_link/4`

**Arguments**: `Ref, Transport, Opts`

**Description**: Ranch 2.
-spec start_link(ranch:ref(), module(), cowboy:opts()) -> {ok, pid()}.

---


## cowboy_tracer_h

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `data/4`

---

#### `early_error/5`

---

#### `info/3`

---

#### `init/3`

**Arguments**: `StreamID, Req, Opts`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

-module(cowboy_tracer_h).
-behavior(cowboy_stream).

-export([init/3]).
-export([data/4]).
-export([info/3]).
-export([terminate/3]).
-export([early_error/5]).

-export([set_trace_patterns/0]).

-export([tracer_process/3]).
-export([system_continue/3]).
-export([system_terminate/4]).
-export([system_code_change/4]).

-type match_predicate()
	:: fun((cowboy_stream:streamid(), cowboy_req:req(), cowboy:opts()) -> boolean()).

-type tracer_match_specs() :: [match_predicate()
	| {method, binary()}
	| {host, binary()}
	| {path, binary()}
	| {path_start, binary()}
	| {header, binary()}
	| {header, binary(), binary()}
	| {peer_ip, inet:ip_address()}
].
-export_type([tracer_match_specs/0]).

-type tracer_callback() :: fun((init | terminate | tuple(), any()) -> any()).
-export_type([tracer_callback/0]).

-spec init(cowboy_stream:streamid(), cowboy_req:req(), cowboy:opts())
	-> {cowboy_stream:commands(), any()}.

---

#### `set_trace_patterns/0`

**Description**: API.

%% These trace patterns are most likely not suitable for production.
-spec set_trace_patterns() -> ok.

---

#### `system_code_change/4`

---

#### `system_continue/3`

**Arguments**: `Parent, _, {Opts, State}`

**Description**: System callbacks.

-spec system_continue(pid(), _, {cowboy:opts(), any()}) -> no_return().

---

#### `system_terminate/4`

---

#### `terminate/3`

---

#### `tracer_process/3`

**Arguments**: `StreamID, Req=#{pid := Parent}, Opts=#{tracer_callback := Fun}`

**Description**: The default flags are probably not suitable for production.
			Flags = maps:get(tracer_flags, Opts, [
				send, 'receive', call, return_to,
				procs, ports, monotonic_timestamp,
				%% The set_on_spawn flag is necessary to catch events
				%% from request processes.
				set_on_spawn
			]),
			erlang:trace(self(), true, [{tracer, TracerPid}|Flags]),
			ok;
		_ ->
			ok
	end.

%% Tracer process.

-spec tracer_process(_, _, _) -> no_return().

---


## cowboy_websocket

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `is_upgrade_request/1`

**Arguments**: `#{version := Version, method := <<"CONNECT">>, protocol := Protocol})
		when Version =:= 'HTTP/2'; Version =:= 'HTTP/3' ->
	<<"websocket">> =:= cowboy_bstr:to_lower(Protocol);
is_upgrade_request(Req=#{version := 'HTTP/1.1', method := <<"GET">>}`

**Description**: Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%%
%% Permission to use, copy, modify, and/or distribute this software for any
%% purpose with or without fee is hereby granted, provided that the above
%% copyright notice and this permission notice appear in all copies.
%%
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
%% WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
%% MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
%% ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
%% WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
%% ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
%% OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

%% Cowboy supports versions 7 through 17 of the Websocket drafts.
%% It also supports RFC6455, the proposed standard for Websocket.
-module(cowboy_websocket).
-behaviour(cowboy_sub_protocol).

-export([is_upgrade_request/1]).
-export([upgrade/4]).
-export([upgrade/5]).
-export([takeover/7]).
-export([loop/3]).

-export([system_continue/3]).
-export([system_terminate/4]).
-export([system_code_change/4]).

-type commands() :: [cow_ws:frame()
	| {active, boolean()}
	| {deflate, boolean()}
	| {set_options, map()}
	| {shutdown_reason, any()}
].
-export_type([commands/0]).

-type call_result(State) :: {commands(), State} | {commands(), State, hibernate}.

-type deprecated_call_result(State) :: {ok, State}
	| {ok, State, hibernate}
	| {reply, cow_ws:frame() | [cow_ws:frame()], State}
	| {reply, cow_ws:frame() | [cow_ws:frame()], State, hibernate}
	| {stop, State}.

-type terminate_reason() :: normal | stop | timeout
	| remote | {remote, cow_ws:close_code(), binary()}
	| {error, badencoding | badframe | closed | atom()}
	| {crash, error | exit | throw, any()}.

-callback init(Req, any())
	-> {ok | module(), Req, any()}
	| {module(), Req, any(), any()}
	when Req::cowboy_req:req().

-callback websocket_init(State)
	-> call_result(State) | deprecated_call_result(State) when State::any().
-optional_callbacks([websocket_init/1]).

-callback websocket_handle(ping | pong | {text | binary | ping | pong, binary()}, State)
	-> call_result(State) | deprecated_call_result(State) when State::any().
-callback websocket_info(any(), State)
	-> call_result(State) | deprecated_call_result(State) when State::any().

-callback terminate(any(), cowboy_req:req(), any()) -> ok.
-optional_callbacks([terminate/3]).

-type opts() :: #{
	active_n => pos_integer(),
	compress => boolean(),
	deflate_opts => cow_ws:deflate_opts(),
	dynamic_buffer => false | {pos_integer(), pos_integer()},
	dynamic_buffer_initial_average => non_neg_integer(),
	dynamic_buffer_initial_size => pos_integer(),
	idle_timeout => timeout(),
	max_frame_size => non_neg_integer() | infinity,
	req_filter => fun((cowboy_req:req()) -> map()),
	validate_utf8 => boolean()
}.
-export_type([opts/0]).

%% We don't want to reset the idle timeout too often,
%% so we don't reset it on data. Instead we reset the
%% number of ticks we have observed. We divide the
%% timeout value by a value and that value becomes
%% the number of ticks at which point we can drop
%% the connection. This value is the number of ticks.
-define(IDLE_TIMEOUT_TICKS, 10).

-record(state, {
	parent :: undefined | pid(),
	ref :: ranch:ref(),
	socket = undefined :: inet:socket() | {pid(), cowboy_stream:streamid()} | undefined,
	transport = undefined :: module() | undefined,
	opts = #{} :: opts(),
	active = true :: boolean(),
	handler :: module(),
	key = undefined :: undefined | binary(),
	timeout_ref = undefined :: undefined | reference(),
	timeout_num = 0 :: 0..?IDLE_TIMEOUT_TICKS,
	messages = undefined :: undefined | {atom(), atom(), atom()}
		| {atom(), atom(), atom(), atom()},

	%% Dynamic buffer moving average and current buffer size.
	dynamic_buffer_size = false :: pos_integer() | false,
	dynamic_buffer_moving_average = 0 :: non_neg_integer(),

	hibernate = false :: boolean(),
	frag_state = undefined :: cow_ws:frag_state(),
	frag_buffer = <<>> :: binary(),
	utf8_state :: cow_ws:utf8_state(),
	deflate = true :: boolean(),
	extensions = #{} :: map(),
	req = #{} :: map(),
	shutdown_reason = normal :: any()
}).

%% Because the HTTP/1.1 and HTTP/2 handshakes are so different,
%% this function is necessary to figure out whether a request
%% is trying to upgrade to the Websocket protocol.

-spec is_upgrade_request(cowboy_req:req()) -> boolean().

---

#### `loop/3`

---

#### `system_code_change/4`

**Arguments**: `Misc, _, _, _`

**Description**: @todo We should exit gracefully, if possible.
	terminate(State, HandlerState, Reason).

-spec system_code_change(Misc, _, _, _)
	-> {ok, Misc} when Misc::{#state{}, any(), parse_state()}.

---

#### `system_continue/3`

**Arguments**: `_, _, {State, HandlerState, ParseState}`

**Description**: System callbacks.

-spec system_continue(_, _, {#state{}, any(), parse_state()}) -> no_return().

---

#### `system_terminate/4`

---

#### `takeover/7`

**Arguments**: `Parent, Ref, Socket, Transport, Opts, Buffer,
		{State0=#state{opts=WsOpts, handler=Handler, req=Req}, HandlerState}`

**Description**: @todo We don't want date and server headers.
	Headers = cowboy_req:response_headers(#{}, Req),
	Pid ! {{Pid, StreamID}, {switch_protocol, Headers, ?MODULE, {State, HandlerState}}},
	takeover(Pid, Ref, {Pid, StreamID}, undefined, #{}, <<>>,
		{State, HandlerState}).

%% Connection process.

-record(ps_header, {
	buffer = <<>> :: binary()
}).

-record(ps_payload, {
	type :: cow_ws:frame_type(),
	len :: non_neg_integer(),
	mask_key :: cow_ws:mask_key(),
	rsv :: cow_ws:rsv(),
	close_code = undefined :: undefined | cow_ws:close_code(),
	unmasked = <<>> :: binary(),
	unmasked_len = 0 :: non_neg_integer(),
	buffer = <<>> :: binary()
}).

-type parse_state() :: #ps_header{} | #ps_payload{}.

-spec takeover(pid(), ranch:ref(), inet:socket() | {pid(), cowboy_stream:streamid()},
	module() | undefined, any(), binary(),
	{#state{}, any()}) -> no_return().

---

#### `upgrade/4`

**Arguments**: `Req0=#{version := Version}, Env, Handler, HandlerState, Opts`

**Description**: @todo Immediately crash if a response has already been sent.

---

#### `upgrade/5`

**Arguments**: `Req0=#{version := Version}, Env, Handler, HandlerState, Opts`

**Description**: @todo Immediately crash if a response has already been sent.

---


## cowboy_webtransport

Copyright (c) Loïc Hoguin <essen@ninenines.eu>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

### Exported Functions

#### `info/3`

**Arguments**: `StreamID, Msg, WTState=#{stream_state := StreamState0}`

**Description**: cowboy_stream callbacks.
%%
%% We shortcut stream handlers but still need to process some events
%% such as process exiting or termination. We implement the relevant
%% callbacks here. Note that as far as WebTransport is concerned,
%% receiving stream data here would be an error therefore the data
%% callback is not implemented.
%%
%% @todo Better type than map() for the cowboy_stream state.

-spec info(cowboy_stream:streamid(), any(), State)
	-> {cowboy_stream:commands(), State} when State::map().

---

#### `terminate/3`

---

#### `upgrade/4`

**Arguments**: `Req=#{version := 'HTTP/3', pid := Pid, streamid := StreamID}, Env, Handler, HandlerState, Opts`

**Description**: @todo Immediately crash if a response has already been sent.

---

#### `upgrade/5`

**Arguments**: `Req=#{version := 'HTTP/3', pid := Pid, streamid := StreamID}, Env, Handler, HandlerState, Opts`

**Description**: @todo Immediately crash if a response has already been sent.

---


