# Module Documentation

## Module Modules

### cowboy

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy.erl`

**Description**:
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

**Exported Functions**: start_clear/3, start_tls/3, start_quic/3, stop_listener/1, get_env/2, get_env/3, set_env/3, log/2, log/4

**Functions**:

- `start_clear(Ref, TransOpts0, ProtoOpts0)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `start_quic(Ref, TransOpts, ProtoOpts)` - @todo Experimental function to start a barebone QUIC listener.
%%       This will need to be reworked to be closer to Ranch
%%       listeners and provide equivalent features.
%%
%% @todo Better type for transport options. Might require fixing quicer types.

-spec start_quic(ranch:ref(), #{socket_opts => [{atom(), _}]}, cowboy_http3:opts())
	-> {ok, pid()}.

%% @todo Implement dynamic_buffer for HTTP/3 if/when it applies.
- `port_0()` - @todo Why not binary?
		%% We only need 3 for control and QPACK enc/dec,
		%% but we need more for WebTransport. %% @todo Use 3 if WT is disabled.
		{peer_unidi_stream_count, 100},
		{peer_bidi_stream_count, 100},
		%% For WebTransport.
		%% @todo We probably don't want it enabled if WT isn't used.
		{datagram_send_enabled, 1},
		{datagram_receive_enabled, 1}
	|SocketOpts2],
	_ListenerPid = spawn(fun() ->
		{ok, Listener} = quicer:listen(Port, SocketOpts),
		Parent ! {ok, Listener},
		_AcceptorPid = [spawn(fun AcceptLoop() ->
			{ok, Conn} = quicer:accept(Listener, []),
			Pid = spawn(fun() ->
				receive go -> ok end,
				%% We have to do the handshake after handing control of
				%% the connection otherwise streams may come in before
				%% the controlling process is changed and messages will
				%% not be sent to the correct process.
				{ok, Conn} = quicer:handshake(Conn),
				process_flag(trap_exit, true), %% @todo Only if supervisor though.
				try cowboy_http3:init(Parent, Ref, Conn, ProtoOpts)
				catch
					exit:{shutdown,_} -> ok;
					C:E:S -> log(error, "CRASH ~p:~p:~p", [C,E,S], ProtoOpts)
				end
			end),
			ok = quicer:controlling_process(Conn, Pid),
			Pid ! go,
			AcceptLoop()
		end) || _ <- lists:seq(1, 20)],
		%% Listener process must not terminate.
		receive after infinity -> ok end
	end),
	receive
		{ok, Listener} ->
			{ok, Listener}
	end.

%% Select a random UDP port using gen_udp because quicer
%% does not provide equivalent functionality. Taken from
%% quicer test suites.
- `ensure_alpn(TransOpts)` - Apparently macOS doesn't free the port immediately.
			timer:sleep(500);
		_ ->
			ok
	end,
	Port.
- `ensure_dynamic_buffer(TransOpts=#{socket_opts := SocketOpts}, _)` - Dynamic buffer was not set; define default dynamic buffer
%% only if 'buffer' size was not configured. In that case we
%% set the 'buffer' size to the lowest value.
- `log(Level, Format, Args, _)` - We use error_logger by default. Because error_logger does
%% not have all the levels we accept we have to do some
%% mapping to error_logger functions.

**Dependencies**: application, cowboy_http, os, error_logger, cowboy_constraints, cowboy_http3, proplists, quicer, gen_udp, inet, timer, ranch, logger, Logger, maps, cowboy_http2

---

### cowboy_bstr

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_bstr.erl`

**Description**:
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

**Exported Functions**: capitalize_token/1, to_lower/1, to_upper/1, char_to_lower/1, char_to_upper/1

**Functions**:

- `capitalize_token(B)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `capitalize_token_test_()` - Tests.

-ifdef(TEST).

---

### cowboy_children

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_children.erl`

**Description**:
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

**Exported Functions**: init/0, up/4, down/2, shutdown/2, shutdown_timeout/3, terminate/1, handle_supervisor_call/4

**Functions**:

- `init()` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `shutdown(Children0, StreamID)` - We ask the processes to shutdown first. This gives
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
- `before_terminate_loop([])` - For each child, either ask for it to shut down,
	%% or cancel its shutdown timer if it already is.
	%%
	%% We do not need to flush stray timeout messages out because
	%% we are either terminating or switching protocols,
	%% and in the latter case we flush all messages.
	_ = [case TRef of
		undefined -> exit(Pid, shutdown);
		_ -> erlang:cancel_timer(TRef, [{async, true}, {info, false}])
	end || #child{pid=Pid, timer=TRef} <- Children],
	before_terminate_loop(Children).
- `terminate_loop(Children, TRef)` - Don't forget to cancel the timer, if any!
	case TRef of
		undefined ->
			ok;
		_ ->
			_ = erlang:cancel_timer(TRef, [{async, true}, {info, false}]),
			ok
	end;
- `longest_shutdown_time([], Time)` - We delayed the creation of the timer. If a process with
			%% infinity shutdown just ended, we might have to start that timer.
			case Shutdown of
				infinity -> before_terminate_loop(Children1);
				_ -> terminate_loop(Children1, TRef)
			end;
		{'EXIT', Pid, _} ->
			terminate_loop(lists:keydelete(Pid, #child.pid, Children), TRef);
		{timeout, TRef, terminate} ->
			%% Brutally kill any remaining children.
			_ = [exit(Pid, kill) || #child{pid=Pid} <- Children],
			ok
	end.
- `handle_supervisor_call(_, {From, Tag}, _, _)` - All other calls refer to children. We act in a similar way
%% to a simple_one_for_one so we never find those.

**Dependencies**: cowboy_stream

---

### cowboy_clear

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_clear.erl`

**Behaviors**: ranch_protocol

**Description**:
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

**Exported Functions**: start_link/3, start_link/4, connection_process/4

**Functions**:

- `start_link(Ref, Transport, Opts)` - Ranch 2.
-spec start_link(ranch:ref(), module(), cowboy:opts()) -> {ok, pid()}.
- `init(Parent, Ref, Socket, Transport, ProxyInfo, Opts, Protocol)` - Use cowboy_http2 directly only when 'http' is missing.
	Protocol = case maps:get(protocols, Opts, [http2, http]) of
		[http2] -> cowboy_http2;
		[_|_] -> cowboy_http
	end,
	init(Parent, Ref, Socket, Transport, ProxyInfo, Opts, Protocol).

**Dependencies**: Protocol, proc_lib, cowboy, inet, ranch, maps

---

### cowboy_compress_h

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_compress_h.erl`

**Behaviors**: cowboy_stream

**Description**:
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

**Exported Functions**: init/3, data/4, info/3, terminate/3, early_error/5

**Functions**:

- `init(StreamID, Req, Opts)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `early_error(StreamID, Reason, PartialReq, Resp, Opts)` - Clean the zlib:stream() in case something went wrong.
	%% In the normal scenario the stream is already closed.
	case Z of
		undefined -> ok;
		_ -> zlib:close(Z)
	end,
	cowboy_stream:terminate(StreamID, Reason, Next).

-spec early_error(cowboy_stream:streamid(), cowboy_stream:reason(),
	cowboy_stream:partial_req(), Resp, cowboy:opts()) -> Resp
	when Resp::cowboy_stream:resp_command().
- `check_req(Req)` - Internal.

%% Check if the client supports decoding of gzip responses.
%%
%% A malformed accept-encoding header is ignored (no compression).
- `check_resp_headers(#{<<"etag">> := _}, State)` - Do not compress responses that contain the etag header.
- `fold([Command|Tail], State, Acc)` - Otherwise, we have an unrelated command or compression is disabled.
- `gzip_headers({headers, Status, Headers0}, State)` - We can't call zlib:gzip/1 because it does an
	%% iolist_to_binary(GzBody) at the end to return
	%% a binary(). Therefore the code here is largely
	%% a duplicate of the code of that function.
	Z = zlib:open(),
	GzBody = try
		%% 31 = 16+?MAX_WBITS from zlib.erl
		%% @todo It might be good to allow them to be configured?
		zlib:deflateInit(Z, default, deflated, 31, 8, default),
		Gz = zlib:deflate(Z, Body, finish),
		zlib:deflateEnd(Z),
		Gz
	after
		zlib:close(Z)
	end,
	{{response, Status, Headers#{
		<<"content-length">> => integer_to_binary(iolist_size(GzBody)),
		<<"content-encoding">> => <<"gzip">>
	}, GzBody}, State}.
- `vary_response({response, Status, Headers, Body})` - We use the same arguments as when compressing the body fully.
	%% @todo It might be good to allow them to be configured?
	zlib:deflateInit(Z, default, deflated, 31, 8, default),
	Headers = maps:remove(<<"content-length">>, Headers0),
	{{headers, Status, Headers#{
		<<"content-encoding">> => <<"gzip">>
	}}, State#state{deflate=Z}}.
- `vary(Headers)` - The vary header is invalid. Probably empty. We replace it with ours.
		Headers#{<<"vary">> => <<"accept-encoding">>}
	end;
- `gzip_data({data, nofin, Sendfile={sendfile, _, _, _}},
		State=#state{deflate=Z, deflate_flush=Flush})` - It is not possible to combine zlib and the sendfile
%% syscall as far as I can tell, because the zlib format
%% includes a checksum at the end of the stream. We have
%% to read the file in memory, making this not suitable for
%% large files.

**Dependencies**: cowboy_stream, file, cow_http_hd, cowboy, zlib, maps, cowboy_req

---

### cowboy_constraints

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_constraints.erl`

**Description**:
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

**Exported Functions**: validate/2, reverse/2, format_error/1

**Functions**:

- `validate(Value, Constraints) when is_list(Constraints)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `apply_constraint(Type, Value, int)` - @todo {int, From, To}, etc.
- `int(forward, Value)` - Constraint functions.
- `reverse_test()` - Value, Constraints, Result.
	Tests = [
		{<<>>, [], <<>>},
		{<<"123">>, int, 123},
		{<<"123">>, [int], 123},
		{<<"123">>, [nonempty, int], 123},
		{<<"123">>, [int, nonempty], 123},
		{<<>>, nonempty, error},
		{<<>>, [nonempty], error},
		{<<"hello">>, F, hello},
		{<<"hello">>, [F], hello},
		{<<"123">>, [F, int], error},
		{<<"123">>, [int, F], error},
		{<<"hello">>, [nonempty, F], hello},
		{<<"hello">>, [F, nonempty], hello}
	],
	[{lists:flatten(io_lib:format("~p, ~p", [V, C])), fun() ->
		case R of
			error -> {error, _} = validate(V, C);
			_ -> {ok, R} = validate(V, C)
		end
	end} || {V, C, R} <- Tests].
- `int_format_error_test()` - Value, Constraints, Result.
	Tests = [
		{<<>>, [], <<>>},
		{123, int, <<"123">>},
		{123, [int], <<"123">>},
		{123, [nonempty, int], <<"123">>},
		{123, [int, nonempty], <<"123">>},
		{<<>>, nonempty, error},
		{<<>>, [nonempty], error},
		{hello, F, <<"hello">>},
		{hello, [F], <<"hello">>},
		{123, [F, int], error},
		{123, [int, F], error},
		{hello, [nonempty, F], <<"hello">>},
		{hello, [F, nonempty], <<"hello">>}
	],
	[{lists:flatten(io_lib:format("~p, ~p", [V, C])), fun() ->
		case R of
			error -> {error, _} = reverse(V, C);
			_ -> {ok, R} = reverse(V, C)
		end
	end} || {V, C, R} <- Tests].

**Dependencies**: io_lib

---

### cowboy_decompress_h

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_decompress_h.erl`

**Behaviors**: cowboy_stream

**Description**:
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

**Exported Functions**: init/3, data/4, info/3, terminate/3, early_error/5

**Functions**:

- `init(StreamID, Req0, Opts)` - Copyright (c) jdamanalo <joshuadavid.agustin@manalo.ph>
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
- `info(StreamID, Info, State=#state{next=Next0})` - We can't change the enabled setting after we start reading,
	%% otherwise the data becomes garbage. Changing the setting
	%% is not treated as an error, it is just ignored.
	State = case IsReading of
		true -> State0;
		false -> State0#state{enabled=Enabled}
	end,
	fold(Commands, State#state{next=Next, ratio_limit=RatioLimit});
- `check_and_update_req(Req=#{headers := Headers})` - Internal.

%% Check whether the request needs content decoding, and if it does
%% whether it fits our criteria for decoding. We also update the
%% Req to indicate whether content was decoded.
%%
%% We always set the content_decoded value in the Req because it
%% indicates whether content decoding was attempted.
%%
%% A malformed content-encoding header results in no decoding.
- `buffer_to_iovec(Buffer)` - We only automatically decompress when gzip is the only
		%% encoding used. Since it's the only encoding used, we
		%% can remove the header entirely before passing the Req
		%% forward.
		[<<"gzip">>] ->
			{Req#{
				headers => maps:remove(<<"content-encoding">>, Headers),
				content_decoded => [<<"gzip">>|ContentDecoded]
			}, #state{compress=gzip}};
		_ ->
			{Req#{content_decoded => ContentDecoded},
				#state{compress=undefined}}
	catch _:_ ->
		{Req#{content_decoded => ContentDecoded},
			#state{compress=undefined}}
	end.
- `add_accept_encoding(Headers)` - gzip is excluded but this handler is enabled; we replace.
				{_, 0} ->
					Replaced = lists:keyreplace(<<"gzip">>, 1, List, {<<"gzip">>, 1000}),
					Codings = build_accept_encoding(Replaced),
					Headers#{<<"accept-encoding">> => Codings};
				{_, _} ->
					Headers;
				false ->
					case lists:keyfind(<<"*">>, 1, List) of
						%% Others are excluded along with gzip; we add.
						{_, 0} ->
							WithGzip = [{<<"gzip">>, 1000} | List],
							Codings = build_accept_encoding(WithGzip),
							Headers#{<<"accept-encoding">> => Codings};
						{_, _} ->
							Headers;
						false ->
							Headers#{<<"accept-encoding">> => [AcceptEncoding, <<", gzip">>]}
					end
			end
	catch _:_ ->
		%% The accept-encoding header is invalid. Probably empty. We replace it with ours.
		Headers#{<<"accept-encoding">> => <<"gzip">>}
	end;
- `qvalue_to_iodata(0)` - @todo From cowlib, maybe expose?
- `build_accept_encoding([{ContentCoding, Q}|Tail])` - @todo Should be added to Cowlib.

**Dependencies**: cowboy_stream, cow_http_hd, cowboy, zlib, cow_deflate, maps, cowboy_req

---

### cowboy_handler

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_handler.erl`

**Behaviors**: cowboy_middleware

**Description**:
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

**Exported Functions**: execute/2, terminate/4

**Functions**:

- `execute(Req, Env=#{handler := Handler, handler_opts := HandlerOpts})` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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

**Dependencies**: cowboy_middleware, Handler, Mod, cowboy_req

---

### cowboy_http

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_http.erl`

**Description**:
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

**Exported Functions**: init/6, loop/1, system_continue/3, system_terminate/4, system_code_change/4

**Functions**:

- `init(Parent, Ref, Socket, Transport, ProxyHeader, Opts)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `before_loop(State=#state{opts=#{hibernate := true}})` - Hardcoded for compatibility with Ranch 1.x.
				Passive =:= tcp_passive; Passive =:= ssl_passive ->
			flush_passive(Socket, Messages)
	after 0 ->
		ok
	end.
- `set_timeout(State=#state{streams=[], in_state=InState}, idle_timeout)
		when element(1, InState) =/= ps_body ->
	State;
%% Otherwise we can set the timeout.
%% @todo Don't do this so often, use a strategy similar to Websocket/H2 if possible.
set_timeout(State0=#state{opts=Opts, overriden_opts=Override}, Name)` - We do not set idle_timeout if there are no active streams,
%% unless when we are skipping a body.
- `maybe_reset_idle_timeout(State=#state{opts=Opts})` - The timeout may have been overriden for the current stream.
		#{Name := Timeout0} -> Timeout0;
		_ -> maps:get(Name, Opts, Default)
	end,
	TimerRef = case Timeout of
		infinity -> undefined;
		Timeout -> erlang:start_timer(Timeout, self(), Name)
	end,
	State#state{timer=TimerRef}.
- `timeout(State=#state{in_state=#ps_request_line{}}, request_timeout)` - Do a synchronous cancel and remove the message if any
			%% to avoid receiving stray messages.
			_ = erlang:cancel_timer(TimerRef, [{async, false}, {info, false}]),
			receive
				{timeout, TimerRef, _} -> ok
			after 0 ->
				ok
			end
	end,
	State#state{timer=undefined}.

-spec timeout(_, _) -> no_return().
- `parse(_, State=#state{in_streamid=InStreamID, in_state=#ps_request_line{},
		last_streamid=LastStreamID}) when InStreamID > LastStreamID ->
	before_loop(State#state{buffer= <<>>});
parse(Buffer, State=#state{in_state=#ps_request_line{empty_lines=EmptyLines}})` - Do not process requests that come in after the last request
%% and discard the buffer if any to save memory.
- `after_parse({data, _, IsFin, _, State=#state{buffer=Buffer}})` - @todo Should call parse after this.
		stream_terminate(State0, StreamID, {internal_error, {Class, Exception},
			'Unhandled exception in cowboy_stream:data/4.'})
	end;
%% No corresponding stream. We must skip the body of the previous request
%% in order to process the next one.
- `update_flow(nofin, Data, State0=#state{flow=Flow0})` - This function is only called after parsing, therefore we
	%% are expecting to be in active mode already.
	State#state{flow=infinity};
- `parse_request(Buffer, State=#state{opts=Opts, in_streamid=InStreamID}, EmptyLines)` - We limit the length of the Request-line to MaxLength to avoid endlessly
%% reading from the socket and eventually crashing.
- `match_eol(<< $\n, _/bits >>, N)` - @todo * is only for server-wide OPTIONS request (RFC7230 5.3.4); tests
				<< "OPTIONS * ", Rest/bits >> ->
					parse_version(Rest, State, <<"OPTIONS">>, undefined, <<"*">>, <<>>);
				<<"CONNECT ", _/bits>> ->
					error_terminate(501, State, {connection_error, no_error,
						'The CONNECT method is currently not implemented. (RFC7231 4.3.6)'});
				<<"TRACE ", _/bits>> ->
					error_terminate(501, State, {connection_error, no_error,
						'The TRACE method is currently not implemented. (RFC7231 4.3.8)'});
				%% Accept direct HTTP/2 only at the beginning of the connection.
				<< "PRI * HTTP/2.0\r\n", _/bits >> when InStreamID =:= 1 ->
					case lists:member(http2, maps:get(protocols, Opts, [http2, http])) of
						true ->
							http2_upgrade(State, Buffer);
						false ->
							error_terminate(501, State, {connection_error, no_error,
								'Prior knowledge upgrade to HTTP/2 is disabled by configuration.'})
					end;
				_ ->
					parse_method(Buffer, State, <<>>,
						maps:get(max_method_length, Opts, 32))
			end
	end.
- `parse_uri_authority(Rest, State=#state{opts=Opts}, Method)` - @todo We probably want to apply max_authority_length also
%% to the host header and to document this option. It might
%% also be useful for HTTP/2 requests.
- `parse_header(Rest, State=#state{in_state=PS}, Headers) when byte_size(Rest) < 2 ->
	{more, State#state{buffer=Rest, in_state=PS#ps_header{headers=Headers}}};
parse_header(<< $\r, $\n, Rest/bits >>, S, Headers)` - Headers.

%% We need two or more bytes in the buffer to continue.
- `match_colon(<< $:, _/bits >>, N)` - We don't have a colon but we might have an invalid header line,
			%% so check if we have an LF and abort with an error if we do.
			case match_eol(Buffer, 0) of
				nomatch ->
					{more, State#state{buffer=Buffer, in_state=PS#ps_header{headers=Headers}}};
				_ ->
					error_terminate(400, State#state{in_state=PS#ps_header{headers=Headers}},
						{connection_error, protocol_error,
							'A header line is missing a colon separator. (RFC7230 3.2.4)'})
			end;
		_ ->
			parse_hd_name(Buffer, State, Headers, <<>>)
	end.
- `parse_hd_value(<< C, Rest/bits >>, S, H, N, SoFar)` - The cookie header does not use proper HTTP header lists.
		Value0 when Name =:= <<"cookie">> -> Headers0#{Name => << Value0/binary, "; ", Value/binary >>};
		Value0 -> Headers0#{Name => << Value0/binary, ", ", Value/binary >>}
	end,
	parse_header(Rest, S, Headers);
- `request_parse_host(Buffer, State=#state{transport=Transport, in_state=PS}, Headers, RawHost)` - @todo Might want to not close the connection on this and next one.
			error_terminate(400, State#state{in_state=PS#ps_header{headers=Headers}},
				{stream_error, protocol_error,
					'HTTP/1.1 requests must include a host header. (RFC7230 5.4)'});
		undefined ->
			request(Buffer, State, Headers, <<>>, default_port(Transport:secure()));
		%% @todo When CONNECT requests come in we need to ignore the RawHost
		%% and instead use the Authority as the source of host.
		RawHost when Authority =:= undefined; Authority =:= RawHost ->
			request_parse_host(Buffer, State, Headers, RawHost);
		%% RFC7230 does not explicitly ask us to reject requests
		%% that have a different authority component and host header.
		%% However it DOES ask clients to set them to the same value,
		%% so we enforce that.
		_ ->
			error_terminate(400, State#state{in_state=PS#ps_header{headers=Headers}},
				{stream_error, protocol_error,
					'The host header is different than the absolute-form authority component. (RFC7230 5.4)'})
	end.
- `request(Buffer, State0=#state{ref=Ref, transport=Transport, peer=Peer, sock=Sock, cert=Cert,
		opts=Opts, proxy_header=ProxyHeader, in_streamid=StreamID, in_state=
			PS=#ps_header{method=Method, path=Path, qs=Qs, version=Version}},
		Headers, Host, Port)` - End of request parsing.
- `is_http2_upgrade(#{<<"connection">> := Conn, <<"upgrade">> := Upgrade,
		<<"http2-settings">> := HTTP2Settings}, 'HTTP/1.1', Opts)` - We are transparently taking care of transfer-encodings so
		%% the user code has no need to know about it.
		headers => maps:remove(<<"transfer-encoding">>, Headers),
		has_body => HasBody,
		body_length => BodyLength
	},
	%% We add the PROXY header information if any.
	Req = case ProxyHeader of
		undefined -> Req0;
		_ -> Req0#{proxy_header => ProxyHeader}
	end,
	case is_http2_upgrade(Headers, Version, Opts) of
		false ->
			State = case HasBody of
				true ->
					State0#state{in_state=#ps_body{
						length = BodyLength,
						transfer_decode_fun = TDecodeFun,
						transfer_decode_state = TDecodeState
					}};
				false ->
					State0#state{in_streamid=StreamID + 1, in_state=#ps_request_line{}}
			end,
			{request, Req, State#state{buffer=Buffer}};
		{true, HTTP2Settings} ->
			%% We save the headers in case the upgrade will fail
			%% and we need to pass them to cowboy_stream:early_error.
			http2_upgrade(State0#state{in_state=PS#ps_header{headers=Headers}},
				Buffer, HTTP2Settings, Req)
	end.

%% HTTP/2 upgrade.
- `http2_upgrade(State=#state{parent=Parent, ref=Ref, socket=Socket, transport=Transport,
		proxy_header=ProxyHeader, peer=Peer, sock=Sock, cert=Cert},
		Buffer, HTTP2Settings, Req)` - Upgrade via an HTTP/1.1 request.
- `opts_for_upgrade(#state{opts=Opts, dynamic_buffer_size=false})` - @todo
			%% However if the client sent a body, we need to read the body in full
			%% and if we can't do that, return a 413 response. Some options are in order.
			%% Always half-closed stream coming from this side.
			try cow_http_hd:parse_http2_settings(HTTP2Settings) of
				Settings ->
					_ = cancel_timeout(State),
					cowboy_http2:init(Parent, Ref, Socket, Transport, ProxyHeader,
						opts_for_upgrade(State), Peer, Sock, Cert, Buffer, Settings, Req)
			catch _:_ ->
				error_terminate(400, State, {connection_error, protocol_error,
					'The HTTP2-Settings header must contain a base64 SETTINGS payload. (RFC7540 3.2, RFC7540 3.2.1)'})
			end;
		true ->
			error_terminate(400, State, {connection_error, protocol_error,
				'Clients that support HTTP/2 over TLS MUST use ALPN. (RFC7540 3.4)'})
	end.
- `parse_body(Buffer, State=#state{in_streamid=StreamID, in_state=
		PS=#ps_body{received=Received, transfer_decode_fun=TDecode,
			transfer_decode_state=TState0}})` - Request body parsing.
- `down(State=#state{opts=Opts, children=Children0}, Pid, Msg)` - @todo Proper trailers.
	try TDecode(Buffer, TState0) of
		more ->
			{more, State#state{buffer=Buffer}};
		{more, Data, TState} ->
			{data, StreamID, nofin, Data, State#state{buffer= <<>>,
				in_state=PS#ps_body{received=Received + byte_size(Data),
					transfer_decode_state=TState}}};
		{more, Data, _Length, TState} when is_integer(_Length) ->
			{data, StreamID, nofin, Data, State#state{buffer= <<>>,
				in_state=PS#ps_body{received=Received + byte_size(Data),
					transfer_decode_state=TState}}};
		{more, Data, Rest, TState} ->
			{data, StreamID, nofin, Data, State#state{buffer=Rest,
				in_state=PS#ps_body{received=Received + byte_size(Data),
					transfer_decode_state=TState}}};
		{done, _HasTrailers, Rest} ->
			{data, StreamID, fin, <<>>,
				State#state{buffer=Rest, in_streamid=StreamID + 1, in_state=#ps_request_line{}}};
		{done, Data, _HasTrailers, Rest} ->
			{data, StreamID, fin, Data,
				State#state{buffer=Rest, in_streamid=StreamID + 1, in_state=#ps_request_line{}}}
	catch _:_ ->
		Reason = {connection_error, protocol_error,
			'Failure to decode the content. (RFC7230 4)'},
		terminate(stream_terminate(State, StreamID, Reason), Reason)
	end.

%% Message handling.
- `info(State=#state{opts=Opts, streams=Streams0}, StreamID, Msg)` - The stream was terminated already.
		{ok, undefined, Children} ->
			State#state{children=Children};
		%% The stream is still running.
		{ok, StreamID, Children} ->
			info(State#state{children=Children}, StreamID, Msg);
		%% The process was unknown.
		error ->
			cowboy:log(warning, "Received EXIT signal ~p for unknown process ~p.~n",
				[Msg, Pid], Opts),
			State
	end.
- `commands(State, StreamID, [{push, _, _, _, _, _, _, _}|Tail])` - HTTP/1.1 does not support push; ignore.
- `headers_to_list(Headers0=#{<<"set-cookie">> := SetCookies})` - The set-cookie header is special; we can only send one cookie per header.
- `sendfile(State=#state{socket=Socket, transport=Transport, opts=Opts},
		{sendfile, Offset, Bytes, Path})` - We wrap the sendfile call into a try/catch because on OTP-20
%% and earlier a few different crashes could occur for sockets
%% that were closing or closed. For example a badarg in
%% erlang:port_get_data(#Port<...>) or a badmatch like
%% {{badmatch,{error,einval}},[{prim_file,sendfile,8,[]}...
%%
%% OTP-21 uses a NIF instead of a port so the implementation
%% and behavior has dramatically changed and it is unclear
%% whether it will be necessary in the future.
%%
%% This try/catch prevents some noisy logs to be written
%% when these errors occur.
- `flush(Parent)` - When sendfile is disabled we explicitly use the fallback.
		{ok, _} = maybe_socket_error(State,
			case maps:get(sendfile, Opts, true) of
				true -> Transport:sendfile(Socket, Path, Offset, Bytes);
				false -> ranch_transport:sendfile(Transport, Socket, Path, Offset, Bytes, [])
			end
		),
		ok
	catch _:_ ->
		terminate(State, {socket_error, sendfile_crash,
			'An error occurred when using the sendfile function.'})
	end.

%% Flush messages specific to cowboy_http before handing over the
%% connection to another protocol.
- `maybe_terminate(State, StreamID, _Tail)` - @todo Reason ok?
- `stream_next(State0=#state{opts=Opts, active=Active, out_streamid=OutStreamID, streams=Streams})` - Send a response or terminate chunks depending on the current output state.
	State1 = #state{streams=Streams1} = case OutState of
		wait when element(1, Reason) =:= internal_error ->
			info(State0, StreamID, {response, 500, #{<<"content-length">> => <<"0">>}, <<>>});
		wait when element(1, Reason) =:= connection_error ->
			info(State0, StreamID, {response, 400, #{<<"content-length">> => <<"0">>}, <<>>});
		wait ->
			info(State0, StreamID, {response, 204, #{}, <<>>});
		chunked when Version =:= 'HTTP/1.1' ->
			info(State0, StreamID, {data, fin, <<>>});
		streaming when SentSize < ExpectedSize ->
			terminate(State0, response_body_too_small);
		_ -> %% done or Version =:= 'HTTP/1.0'
			State0
	end,
	%% Stop the stream, shutdown children and reset overriden options.
	{value, #stream{state=StreamState}, Streams}
		= lists:keytake(StreamID, #stream.id, Streams1),
	stream_call_terminate(StreamID, Reason, StreamState, State1),
	Children = cowboy_children:shutdown(Children0, StreamID),
	State = State1#state{overriden_opts=#{}, streams=Streams, children=Children},
	%% We want to drop the connection if the body was not read fully
	%% and we don't know its length or more remains to be read than
	%% configuration allows.
	MaxSkipBodyLength = maps:get(max_skip_body_length, Opts, 1000000),
	case InState of
		#ps_body{length=undefined}
				when InStreamID =:= OutStreamID ->
			terminate(State, skip_body_unknown_length);
		#ps_body{length=Len, received=Received}
				when InStreamID =:= OutStreamID, Received + MaxSkipBodyLength < Len ->
			terminate(State, skip_body_too_large);
		#ps_body{} when InStreamID =:= OutStreamID ->
			stream_next(State#state{flow=infinity});
		_ ->
			stream_next(State)
	end.
- `stream_call_terminate(StreamID, Reason, StreamState, #state{opts=Opts})` - Enable active mode again if it was disabled.
	State1 = case Active of
		true -> State0;
		false -> active(State0)
	end,
	NextOutStreamID = OutStreamID + 1,
	case lists:keyfind(NextOutStreamID, #stream.id, Streams) of
		false ->
			State = State1#state{out_streamid=NextOutStreamID, out_state=wait},
			%% There are no streams remaining. We therefore can
			%% and want to switch back to the request_timeout.
			set_timeout(State, request_timeout);
		#stream{queue=Commands} ->
			%% @todo Remove queue from the stream.
			%% We set the flow to the initial flow size even though
			%% we might have sent some data through already due to pipelining.
			Flow = maps:get(initial_stream_flow_size, Opts, 65535),
			commands(State1#state{flow=Flow, out_streamid=NextOutStreamID, out_state=wait},
				NextOutStreamID, Commands)
	end.
- `connection(State, Headers, _, 'HTTP/1.0')` - @todo Here we need to set keep-alive only if it wasn't set before.
		false -> {State, Headers}
	end;
- `stream_te(_, #stream{te=undefined})` - No TE header was sent.
- `error_terminate(StatusCode, State=#state{ref=Ref, peer=Peer, in_state=StreamState}, Reason)` - If we can't parse the TE header, assume we can't send trailers.
		no_trailers
	end.

%% This function is only called when an error occurs on a new stream.
-spec error_terminate(cowboy:http_status(), #state{}, _) -> no_return().
- `initiate_closing(State=#state{streams=[]}, Reason)` - @todo We shouldn't send the body when the method is HEAD.
					%% @todo Technically we allow the sendfile tuple.
					RespBody
				])
			)
	catch Class:Exception:Stacktrace ->
		cowboy:log(cowboy_stream:make_error_log(early_error,
			[StreamID, Reason, PartialReq, Resp, Opts],
			Class, Exception, Stacktrace), Opts),
		%% We still need to send an error response, so send what we initially
		%% wanted to send. It's better than nothing.
		ok = maybe_socket_error(State,
			Transport:send(Socket, cow_http:response(StatusCode0,
				'HTTP/1.1', maps:to_list(RespHeaders1)))
		)
	end.
- `maybe_socket_error(State, {error, closed})` - Function replicated in cowboy_http2.
- `terminate_linger_loop(State=#state{socket=Socket}, TimerRef, Messages)` - We may already be in active mode when we do this
	%% but it's OK because we are shutting down anyway.
	%%
	%% We specially handle the socket error to terminate
	%% when an error occurs.
	case setopts_active(State) of
		ok ->
			terminate_linger_loop(State, TimerRef, Messages);
		{error, _} ->
			ok
	end.
- `system_continue(_, _, State)` - System callbacks.

-spec system_continue(_, _, #state{}) -> ok.

**Dependencies**: Protocol, Transport, binary, sys, cowboy_children, horse, cowboy, cowboy_req, cow_http, cowboy_tracer_h, inet, ranch_transport, cowboy_middleware, maps, cowboy_http2, cowboy_stream, cowboy_metrics_h, proc_lib, cow_http_hd, ranch_proxy_header, ssl, cow_http_te, ranch

---

### cowboy_http2

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_http2.erl`

**Description**:
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

**Exported Functions**: init/6, init/10, init/12, loop/2, system_continue/3, system_terminate/4, system_code_change/4

**Functions**:

- `init(Parent, Ref, Socket, Transport, ProxyHeader, Opts, Peer, Sock, Cert, Buffer,
		_Settings, Req=#{method := Method})` - @todo Add an argument for the request body.
-spec init(pid(), ranch:ref(), inet:socket(), module(),
	ranch_proxy_header:proxy_info() | undefined, cowboy:opts(),
	{inet:ip_address(), inet:port_number()}, {inet:ip_address(), inet:port_number()},
	binary() | undefined, binary(), map() | undefined, cowboy_req:req()) -> no_return().
- `init_rate_limiting(State0)` - Send the preface before doing all the init in case we get a socket error.
	ok = maybe_socket_error(undefined, Transport:send(Socket, Preface)),
	State = set_idle_timeout(init_rate_limiting(#state{parent=Parent, ref=Ref, socket=Socket,
		transport=Transport, proxy_header=ProxyHeader,
		opts=Opts, peer=Peer, sock=Sock, cert=Cert,
		dynamic_buffer_size=DynamicBuffer,
		dynamic_buffer_moving_average=maps:get(dynamic_buffer_initial_average, Opts, 0),
		http2_status=sequence, http2_machine=HTTP2Machine}), 0),
	safe_setopts_active(State),
	case Buffer of
		<<>> -> before_loop(State, Buffer);
		_ -> parse(State, Buffer)
	end.
- `setopts_active(#state{socket=Socket, transport=Transport, opts=Opts})` - We assume that the upgrade will be applied. A stream handler
	%% must not prevent the normal operations of the server.
	State2 = info(State1, 1, {switch_protocol, #{
		<<"connection">> => <<"Upgrade">>,
		<<"upgrade">> => <<"h2c">>
	}, ?MODULE, undefined}), %% @todo undefined or #{}?
	State = set_idle_timeout(init_rate_limiting(State2#state{http2_status=sequence}), 0),
	%% In the case of HTTP/1.1 Upgrade we cannot send the Preface
	%% until we send the 101 response.
	ok = maybe_socket_error(State, Transport:send(Socket, Preface)),
	safe_setopts_active(State),
	case Buffer of
		<<>> -> before_loop(State, Buffer);
		_ -> parse(State, Buffer)
	end.

-include("cowboy_dynamic_buffer.hrl").

%% Because HTTP/2 has flow control and Cowboy has other rate limiting
%% mechanisms implemented, a very large active_n value should be fine,
%% as long as the stream handlers do their work in a timely manner.
%% However large active_n values reduce the impact of dynamic_buffer.
- `tick_idle_timeout(State=#state{idle_timeout_num=?IDLE_TIMEOUT_TICKS}, _)` - Socket messages.
		{OK, Socket, Data} when OK =:= element(1, Messages) ->
			State1 = maybe_resize_buffer(State, Data),
			parse(State1#state{idle_timeout_num=0}, << Buffer/binary, Data/binary >>);
		{Closed, Socket} when Closed =:= element(2, Messages) ->
			Reason = case State#state.http2_status of
				closing -> {stop, closed, 'The client is going away.'};
				_ -> {socket_error, closed, 'The socket has been closed.'}
			end,
			terminate(State, Reason);
		{Error, Socket, Reason} when Error =:= element(3, Messages) ->
			terminate(State, {socket_error, Reason, 'An error has occurred on the socket.'});
		{Passive, Socket} when Passive =:= element(4, Messages);
				%% Hardcoded for compatibility with Ranch 1.x.
				Passive =:= tcp_passive; Passive =:= ssl_passive ->
			safe_setopts_active(State),
			before_loop(State, Buffer);
		%% System messages.
		{'EXIT', Parent, shutdown} ->
			Reason = {stop, {exit, shutdown}, 'Parent process requested shutdown.'},
			before_loop(initiate_closing(State, Reason), Buffer);
		{'EXIT', Parent, Reason} ->
			terminate(State, {stop, {exit, Reason}, 'Parent process terminated.'});
		{system, From, Request} ->
			sys:handle_system_msg(Request, From, Parent, ?MODULE, [], {State, Buffer});
		%% Timeouts.
		{timeout, TimerRef, idle_timeout} ->
			tick_idle_timeout(State, Buffer);
		{timeout, Ref, {shutdown, Pid}} ->
			cowboy_children:shutdown_timeout(Children, Ref, Pid),
			before_loop(State, Buffer);
		{timeout, TRef, {cow_http2_machine, Name}} ->
			before_loop(timeout(State, Name, TRef), Buffer);
		{timeout, TimerRef, {goaway_initial_timeout, Reason}} ->
			before_loop(closing(State, Reason), Buffer);
		{timeout, TimerRef, {goaway_complete_timeout, Reason}} ->
			terminate(State, {stop, stop_reason(Reason),
				'Graceful shutdown timed out.'});
		%% Messages pertaining to a stream.
		{{Pid, StreamID}, Msg} when Pid =:= self() ->
			before_loop(info(State, StreamID, Msg), Buffer);
		%% Exit signal from children.
		Msg = {'EXIT', Pid, _} ->
			before_loop(down(State, Pid, Msg), Buffer);
		%% Calls from supervisor module.
		{'$gen_call', From, Call} ->
			cowboy_children:handle_supervisor_call(Call, From, Children, ?MODULE),
			before_loop(State, Buffer);
		Msg ->
			cowboy:log(warning, "Received stray message ~p.", [Msg], Opts),
			before_loop(State, Buffer)
	after InactivityTimeout ->
		terminate(State, {internal_error, timeout, 'No message or data received before timeout.'})
	end.
- `parse(State=#state{http2_status=sequence}, Data)` - HTTP/2 protocol parsing.
- `frame_rate(State0=#state{frame_rate_num=Num0, frame_rate_time=Time}, Frame)` - Terminate the connection if we are closing and all streams have completed.
		more when Status =:= closing, Streams =:= #{} ->
			terminate(State, {stop, normal, 'The connection is going away.'});
		more ->
			before_loop(State, Data)
	end.

%% Frame rate flood protection.
- `frame(State=#state{http2_machine=HTTP2Machine0}, Frame)` - When the option has a period of infinity we cannot reach this clause.
					{ok, init_frame_rate_limiting(State0, CurrentTime)}
			end;
		Num ->
			{ok, State0#state{frame_rate_num=Num}}
	end,
	case {Result, Frame} of
		{ok, ignore} -> ignored_frame(State);
		{ok, _} -> frame(State, Frame);
		{error, _} -> terminate(State, {connection_error, enhance_your_calm,
			'Frame rate larger than configuration allows. Flood? (CVE-2019-9512, CVE-2019-9515, CVE-2019-9518)'})
	end.

%% Frames received.

%% We do nothing when receiving a lingering DATA frame.
%% We already removed the stream flow from the connection
%% flow and are therefore already accounting for the window
%% being reduced by these frames.
- `maybe_ack(State=#state{socket=Socket, transport=Transport}, Frame)` - We do not reset the idle timeout on send here because we are
%% sending data as a consequence of receiving data, which means
%% we already resetted the idle timeout.
- `headers_frame(State=#state{opts=Opts, streams=Streams}, StreamID, Req)` - The cookie header does not use proper HTTP header lists.
		#{Name := Value0} when Name =:= <<"cookie">> ->
			Acc0#{Name => << Value0/binary, "; ", Value/binary >>};
		#{Name := Value0} ->
			Acc0#{Name => << Value0/binary, ", ", Value/binary >>};
		_ ->
			Acc0#{Name => Value}
	end,
	headers_to_map(Tail, Acc).
- `ensure_port(<<"http">>, undefined)` - We add the PROXY header information if any.
					Req1 = case ProxyHeader of
						undefined -> Req0;
						_ -> Req0#{proxy_header => ProxyHeader}
					end,
					%% We add the protocol information for extended CONNECTs.
					Req = case PseudoHeaders of
						#{protocol := Protocol} -> Req1#{protocol => Protocol};
						_ -> Req1
					end,
					headers_frame(State, StreamID, Req)
			catch _:_ ->
				reset_stream(State, StreamID, {stream_error, protocol_error,
					'The :path pseudo-header is invalid. (RFC7540 8.1.2.3)'})
			end
	catch _:_ ->
		reset_stream(State, StreamID, {stream_error, protocol_error,
			'The :authority pseudo-header is invalid. (RFC7540 8.1.2.3)'})
	end.
- `headers_to_map([], Acc)` - This function is necessary to properly handle duplicate headers
%% and the special-case cookie header.
- `rst_stream_frame(State=#state{streams=Streams0, children=Children0}, StreamID, Reason)` - We automatically terminate the stream but it is not an error
	%% per se (at least not in the first implementation).
	Reason = {stream_error, no_error, HumanReadable},
	%% The partial Req is minimal for now. We only have one case
	%% where it can be called (when a method is completely disabled).
	%% @todo Fill in the other elements.
	PartialReq = #{
		ref => Ref,
		peer => Peer,
		method => Method,
		headers => headers_to_map(Headers, #{})
	},
	Resp = {response, StatusCode0, RespHeaders0=#{<<"content-length">> => <<"0">>}, <<>>},
	try cowboy_stream:early_error(StreamID, Reason, PartialReq, Resp, Opts) of
		{response, StatusCode, RespHeaders, RespBody} ->
			send_response(State0, StreamID, StatusCode, RespHeaders, RespBody)
	catch Class:Exception:Stacktrace ->
		cowboy:log(cowboy_stream:make_error_log(early_error,
			[StreamID, Reason, PartialReq, Resp, Opts],
			Class, Exception, Stacktrace), Opts),
		%% We still need to send an error response, so send what we initially
		%% wanted to send. It's better than nothing.
		send_headers(State0, StreamID, fin, StatusCode0, RespHeaders0)
	end.
- `ignored_frame(State=#state{http2_machine=HTTP2Machine0})` - When the option has a period of infinity we cannot reach this clause.
					init_cancel_rate_limiting(State0, CurrentTime)
			end;
		Num ->
			State0#state{cancel_rate_num=Num}
	end.
- `timeout(State=#state{http2_machine=HTTP2Machine0}, Name, TRef)` - HTTP/2 timeouts.
- `down(State0=#state{opts=Opts, children=Children0}, Pid, Msg)` - Erlang messages.
- `info(State=#state{opts=Opts, http2_machine=HTTP2Machine, streams=Streams}, StreamID, Msg)` - The stream was terminated already.
		{ok, undefined, Children} ->
			State0#state{children=Children};
		%% The stream is still running.
		{ok, StreamID, Children} ->
			info(State0#state{children=Children}, StreamID, Msg);
		%% The process was unknown.
		error ->
			cowboy:log(warning, "Received EXIT signal ~p for unknown process ~p.~n",
				[Msg, Pid], Opts),
			State0
	end,
	if
		State#state.http2_status =:= closing, State#state.streams =:= #{} ->
			terminate(State, {stop, normal, 'The connection is going away.'});
		true ->
			State
	end.
- `commands(State=#state{opts=Opts}, StreamID, [Log={log, _, _, _}|Tail])` - @todo Do we want to run the commands after a stop?
	%% @todo Do we even allow commands after?
	stop_stream(State, StreamID);
%% Log event.
- `update_window(State0=#state{socket=Socket, transport=Transport,
		http2_machine=HTTP2Machine0, flow=Flow, streams=Streams}, StreamID)` - Tentatively update the window after the flow was updated.
- `send_response(State0=#state{http2_machine=HTTP2Machine0}, StreamID, StatusCode, Headers, Body)` - Don't update the stream's window if it stopped.
			{<<>>, HTTP2Machine2}
	end,
	State = State0#state{http2_machine=HTTP2Machine},
	case {Data1, Data2} of
		{<<>>, <<>>} ->
			State;
		_ ->
			ok = maybe_socket_error(State, Transport:send(Socket, [Data1, Data2])),
			maybe_reset_idle_timeout(State)
	end.

%% Send the response, trailers or data.
- `send_headers(State0=#state{socket=Socket, transport=Transport,
		http2_machine=HTTP2Machine0}, StreamID, IsFin0, StatusCode, Headers)` - @todo Add a test for HEAD to make sure we don't send the body when
			%% returning {response...} from a stream handler (or {headers...} then {data...}).
			{ok, _IsFin, HeaderBlock, HTTP2Machine}
				= cow_http2_machine:prepare_headers(StreamID, HTTP2Machine0, nofin,
					#{status => cow_http:status_to_integer(StatusCode)},
					headers_to_list(Headers)),
			{_, State} = maybe_send_data(State0#state{http2_machine=HTTP2Machine},
				StreamID, fin, Body, [cow_http2:headers(StreamID, nofin, HeaderBlock)]),
			State
	end.
- `headers_to_list(Headers0=#{<<"set-cookie">> := SetCookies})` - The set-cookie header is special; we can only send one cookie per header.
- `send_data(State0=#state{socket=Socket, transport=Transport, opts=Opts}, SendData, Prefix)` - If we have prefix data (like a HEADERS frame) we need to send it
			%% even if we do not send any DATA frames.
			WasDataSent = case Prefix of
				[] ->
					no_data_sent;
				_ ->
					ok = maybe_socket_error(State1, Transport:send(Socket, Prefix)),
					data_sent
			end,
			State = maybe_send_data_alarm(State1, HTTP2Machine0, StreamID),
			{WasDataSent, State};
		{send, SendData, HTTP2Machine} ->
			State = #state{http2_status=Status, streams=Streams}
				= send_data(State0#state{http2_machine=HTTP2Machine}, SendData, Prefix),
			%% Terminate the connection if we are closing and all streams have completed.
			if
				Status =:= closing, Streams =:= #{} ->
					terminate(State, {stop, normal, 'The connection is going away.'});
				true ->
					{data_sent, maybe_send_data_alarm(State, HTTP2Machine0, StreamID)}
			end
	end.
- `send_data_terminate(State, [])` - When sendfile is disabled we explicitly use the fallback.
			{ok, _} = maybe_socket_error(State,
				case maps:get(sendfile, Opts, true) of
					true -> Transport:sendfile(Socket, Path, Offset, Bytes);
					false -> ranch_transport:sendfile(Transport, Socket, Path, Offset, Bytes, [])
				end
			),
			ok;
		_ ->
			ok = maybe_socket_error(State, Transport:send(Socket, Data))
	end || Data <- Acc],
	send_data_terminate(State, SendData).
- `prepare_data_frame(State=#state{http2_machine=HTTP2Machine0},
		StreamID, nofin, {trailers, Trailers})` - The stream is terminated in cow_http2_machine:prepare_trailers.
- `maybe_send_data_alarm(State=#state{opts=Opts, http2_machine=HTTP2Machine}, HTTP2Machine0, StreamID)` - After we have sent or queued data we may need to set or clear an alarm.
%% We do this by comparing the HTTP2Machine buffer state before/after for
%% the relevant streams.
- `connection_alarm(State0=#state{streams=Streams}, Name, Value)` - When the stream ends up closed after it finished sending data,
	%% we do not want to trigger an alarm. We act as if the buffer
	%% size did not change.
	StreamBufferSizeAfter = case cow_http2_machine:get_stream_local_buffer_size(StreamID, HTTP2Machine) of
		{ok, BSA} -> BSA;
		{error, closed} -> StreamBufferSizeBefore
	end,
	MaxConnBufferSize = maps:get(max_connection_buffer_size, Opts, 16000000),
	MaxStreamBufferSize = maps:get(max_stream_buffer_size, Opts, 8000000),
	%% I do not want to document these internal events yet. I am not yet
	%% convinced it should be {alarm, Name, on|off} and not {internal_event, E}
	%% or something else entirely. Though alarms are probably right.
	if
		ConnBufferSizeBefore >= MaxConnBufferSize, ConnBufferSizeAfter < MaxConnBufferSize ->
			connection_alarm(State, connection_buffer_full, off);
		ConnBufferSizeBefore < MaxConnBufferSize, ConnBufferSizeAfter >= MaxConnBufferSize ->
			connection_alarm(State, connection_buffer_full, on);
		StreamBufferSizeBefore >= MaxStreamBufferSize, StreamBufferSizeAfter < MaxStreamBufferSize ->
			stream_alarm(State, StreamID, stream_buffer_full, off);
		StreamBufferSizeBefore < MaxStreamBufferSize, StreamBufferSizeAfter >= MaxStreamBufferSize ->
			stream_alarm(State, StreamID, stream_buffer_full, on);
		true ->
			State
	end.
- `goaway(State0=#state{socket=Socket, transport=Transport, http2_machine=HTTP2Machine0,
		http2_status=Status, streams=Streams0}, {goaway, LastStreamID, Reason, _})
		when Status =:= connected; Status =:= closing_initiated; Status =:= closing ->
	Streams = goaway_streams(State0, maps:to_list(Streams0), LastStreamID,
		{stop, {goaway, Reason}, 'The connection is going away.'}, []),
	State1 = State0#state{streams=maps:from_list(Streams)},
	if
		Status =:= connected; Status =:= closing_initiated ->
			{OurLastStreamID, HTTP2Machine} =
				cow_http2_machine:set_last_streamid(HTTP2Machine0),
			State = State1#state{http2_status=closing, http2_machine=HTTP2Machine},
			ok = maybe_socket_error(State, Transport:send(Socket,
				cow_http2:goaway(OurLastStreamID, no_error, <<>>))),
			State;
		true ->
			State1
	end;
%% We terminate the connection immediately if it hasn't fully been initialized.
goaway(State, {goaway, _, Reason, _})` - Terminate a stream or the connection.

%% We may have to cancel streams even if we receive multiple
%% GOAWAY frames as the LastStreamID value may be lower than
%% the one previously received.
%%
%% We do not reset the idle timeout on send here. We already
%% disabled it if we initiated shutdown; and we already reset
%% it if the client sent a GOAWAY frame.
- `goaway_streams(_, [], _, _, Acc)` - Cancel client-initiated streams that are above LastStreamID.
- `initiate_closing(State, Reason)` - This happens if sys:terminate/2,3 is called twice or if the supervisor
	%% tells us to shutdown after sys:terminate/2,3 is called or vice versa.
	State;
- `closing(State=#state{http2_status=closing, opts=Opts}, Reason)` - Stop accepting new streams.
	{LastStreamID, HTTP2Machine} =
		cow_http2_machine:set_last_streamid(HTTP2Machine0),
	State = State0#state{http2_status=closing, http2_machine=HTTP2Machine},
	ok = maybe_socket_error(State, Transport:send(Socket,
		cow_http2:goaway(LastStreamID, no_error, <<>>))),
	closing(State, Reason);
- `stop_reason({stop, Reason, _})` - If client sent GOAWAY, we may already be in 'closing' but without the
	%% goaway complete timeout set.
	Timeout = maps:get(goaway_complete_timeout, Opts, 3000),
	Message = {goaway_complete_timeout, Reason},
	set_timeout(State, Timeout, Message).
- `maybe_socket_error(State, {error, closed})` - Function copied from cowboy_http.
- `terminate(_State, Reason)` - @todo We might want to optionally send the Reason value
	%% as debug data in the GOAWAY frame here. Perhaps more.
	if
		Status =:= connected; Status =:= closing_initiated ->
			%% We are terminating so it's OK if we can't send the GOAWAY anymore.
			_ = Transport:send(Socket, cow_http2:goaway(
				cow_http2_machine:get_last_streamid(HTTP2Machine),
				terminate_reason(Reason), <<>>));
		%% We already sent the GOAWAY frame.
		Status =:= closing ->
			ok
	end,
	terminate_all_streams(State, maps:to_list(Streams), Reason),
	cowboy_children:terminate(Children),
	%% @todo Don't linger on connection errors.
	terminate_linger(State),
	exit({shutdown, Reason});
%% We are not fully connected so we can just terminate the connection.
- `terminate_linger(State=#state{socket=Socket, transport=Transport, opts=Opts})` - This code is copied from cowboy_http.
- `terminate_linger_loop(State=#state{socket=Socket}, TimerRef, Messages)` - We may already be in active mode when we do this
	%% but it's OK because we are shutting down anyway.
	%%
	%% We specially handle the socket error to terminate
	%% when an error occurs.
	case setopts_active(State) of
		ok ->
			terminate_linger_loop(State, TimerRef, Messages);
		{error, _} ->
			ok
	end.
- `reset_stream(State0=#state{socket=Socket, transport=Transport,
		http2_machine=HTTP2Machine0}, StreamID, Error)` - @todo Don't send an RST_STREAM if one was already sent.
%%
%% When resetting the stream we are technically sending data
%% on the socket. However due to implementation complexities
%% we do not attempt to reset the idle timeout on send.
- `stop_stream(State=#state{http2_machine=HTTP2Machine}, StreamID)` - When the option has a period of infinity we cannot reach this clause.
					{ok, init_reset_rate_limiting(State0, CurrentTime)}
			end;
		Num ->
			{ok, State0#state{reset_rate_num=Num}}
	end.
- `stopping(State=#state{streams=Streams}, StreamID)` - When the stream terminates normally (without sending RST_STREAM)
		%% and no response was sent, we need to send a proper response back to the client.
		%% We delay the termination of the stream until the response is fully sent.
		{ok, idle, _} ->
			info(stopping(State, StreamID), StreamID, {response, 204, #{}, <<>>});
		%% When a response was sent but not terminated, we need to close the stream.
		%% We delay the termination of the stream until the response is fully sent.
		{ok, nofin, fin} ->
			stopping(State, StreamID);
		%% We only send a final DATA frame if there isn't one queued yet.
		{ok, nofin, _} ->
			info(stopping(State, StreamID), StreamID, {data, fin, <<>>});
		%% When a response was sent fully we can terminate the stream,
		%% regardless of the stream being in half-closed or closed state.
		_ ->
			terminate_stream(State, StreamID)
	end.
- `maybe_terminate_stream(State=#state{streams=Streams}, StreamID, fin)` - If we finished sending data and the stream is stopping, terminate it.
- `terminate_stream(State=#state{flow=Flow, streams=Streams0, children=Children0}, StreamID, Reason)` - We remove the stream flow from the connection flow. Any further
%% data received for this stream is therefore fully contained within
%% the extra window we allocated for this stream.
- `system_continue(_, _, {State, Buffer})` - System callbacks.

-spec system_continue(_, _, {#state{}, binary()}) -> no_return().

**Dependencies**: Transport, sys, cowboy_children, cowboy, cowboy_req, cow_http, cowboy_tracer_h, inet, cowboy_middleware, cow_http2, maps, cowboy_stream, cowboy_metrics_h, proc_lib, cow_http_hd, ranch_proxy_header, cow_http2_machine, ssl, ranch, ranch_transport

---

### cowboy_http3

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_http3.erl`

**Description**:
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

**Exported Functions**: init/4, send/2

**Functions**:

- `init(Parent, Ref, Conn, Opts)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `loop(State0=#state{opts=Opts, children=Children})` - Immediately open a control, encoder and decoder stream.
	%% @todo An endpoint MAY avoid creating an encoder stream if it will not be used (for example, if its encoder does not wish to use the dynamic table or if the maximum size of the dynamic table permitted by the peer is zero).
	%% @todo An endpoint MAY avoid creating a decoder stream if its decoder sets the maximum capacity of the dynamic table to zero.
	{ok, ControlID} = maybe_socket_error(undefined,
		cowboy_quicer:start_unidi_stream(Conn, [<<0>>, SettingsBin]),
		'A socket error occurred when opening the control stream.'),
	{ok, EncoderID} = maybe_socket_error(undefined,
		cowboy_quicer:start_unidi_stream(Conn, <<2>>),
		'A socket error occurred when opening the encoder stream.'),
	{ok, DecoderID} = maybe_socket_error(undefined,
		cowboy_quicer:start_unidi_stream(Conn, <<3>>),
		'A socket error occurred when opening the encoder stream.'),
	%% Set the control, encoder and decoder streams in the machine.
	HTTP3Machine = cow_http3_machine:init_unidi_local_streams(
		ControlID, EncoderID, DecoderID, HTTP3Machine0),
	%% Get the peername/sockname/cert.
	{ok, Peer} = maybe_socket_error(undefined, cowboy_quicer:peername(Conn),
		'A socket error occurred when retrieving the peer name.'),
	{ok, Sock} = maybe_socket_error(undefined, cowboy_quicer:sockname(Conn),
		'A socket error occurred when retrieving the sock name.'),
	CertResult = case cowboy_quicer:peercert(Conn) of
		{error, no_peercert} ->
			{ok, undefined};
		Cert0 ->
			Cert0
	end,
	{ok, Cert} = maybe_socket_error(undefined, CertResult,
		'A socket error occurred when retrieving the client TLS certificate.'),
	%% Quick! Let's go!
	loop(#state{parent=Parent, ref=Ref, conn=Conn,
		opts=Opts, peer=Peer, sock=Sock, cert=Cert,
		http3_machine=HTTP3Machine, local_control_id=ControlID,
		local_encoder_id=EncoderID, local_decoder_id=DecoderID}).
- `handle_quic_msg(State0=#state{opts=Opts}, Msg)` - Timeouts.
		{timeout, Ref, {shutdown, Pid}} ->
			cowboy_children:shutdown_timeout(Children, Ref, Pid),
			loop(State0);
		%% Messages pertaining to a stream.
		{{Pid, StreamID}, Msg} when Pid =:= self() ->
			loop(info(State0, StreamID, Msg));
		%% WebTransport commands.
		{'$webtransport_commands', SessionID, Commands} ->
			loop(webtransport_commands(State0, SessionID, Commands));
		%% Exit signal from children.
		Msg = {'EXIT', Pid, _} ->
			loop(down(State0, Pid, Msg));
		Msg ->
			cowboy:log(warning, "Received stray message ~p.", [Msg], Opts),
			loop(State0)
	end.
- `parse(State=#state{opts=Opts}, StreamID, Data, IsFin)` - @todo Different error reason if graceful?
			Reason = {socket_error, closed, 'The socket has been closed.'},
			terminate(State0, Reason);
		ok ->
			loop(State0);
		unknown ->
			cowboy:log(warning, "Received unknown QUIC message ~p.", [Msg], Opts),
			loop(State0);
		{socket_error, Reason} ->
			terminate(State0, {socket_error, Reason,
				'An error has occurred on the socket.'})
	end.
- `parse1(State=#state{opts=Opts}, Stream=#stream{id=StreamID}, Data, IsFin)` - @todo Clause that discards receiving data for stopping streams.
%%       We may receive a few more frames after we abort receiving.
- `is_fin(fin, <<>>)` - The WebTransport stream header is not a real frame.
		{webtransport_stream_header, SessionID, Rest} ->
			become_webtransport_stream(State, Stream, bidi, SessionID, Rest, IsFin);
		{more, Frame = {data, _}, Len} ->
			%% We're at the end of the data so FrameIsFin is equivalent to IsFin.
			case IsFin of
				nofin ->
					%% The stream will be stored at the end of processing commands.
					loop(frame(State, Stream#stream{status={data, Len}}, Frame, nofin));
				fin ->
					terminate(State, {connection_error, h3_frame_error,
						'Last frame on stream was truncated. (RFC9114 7.1)'})
			end;
		{more, ignore, Len} ->
			%% @todo This setting should be tested.
			%%
			%% While the default value doesn't warrant doing a streaming ignore
			%% (and could work just fine with the 'more' clause), this value
			%% is configurable and users may want to set it large.
			MaxIgnoredLen = maps:get(max_ignored_frame_size_received, Opts, 16384),
			%% We're at the end of the data so FrameIsFin is equivalent to IsFin.
			case IsFin of
				nofin when Len < MaxIgnoredLen ->
					%% We are not processing commands so we must store the stream.
					%% We also call ignored_frame here; we will not need to call
					%% it again when ignoring the rest of the data.
					Stream1 = Stream#stream{status={ignore, Len}},
					State1 = ignored_frame(State, Stream1),
					loop(stream_store(State1, Stream1));
				nofin ->
					terminate(State, {connection_error, h3_excessive_load,
						'Ignored frame larger than limit. (RFC9114 10.5)'});
				fin ->
					terminate(State, {connection_error, h3_frame_error,
						'Last frame on stream was truncated. (RFC9114 7.1)'})
			end;
		{ignore, Rest} ->
			parse(ignored_frame(State, Stream), StreamID, Rest, IsFin);
		Error = {connection_error, _, _} ->
			terminate(State, Error);
		more when Data =:= <<>> ->
			%% The buffer was already reset to <<>>.
			loop(stream_store(State, Stream));
		more ->
			%% We're at the end of the data so FrameIsFin is equivalent to IsFin.
			case IsFin of
				nofin ->
					loop(stream_store(State, Stream#stream{buffer=Data}));
				fin ->
					terminate(State, {connection_error, h3_frame_error,
						'Last frame on stream was truncated. (RFC9114 7.1)'})
			end
	end.

%% We may receive multiple frames in a single QUIC packet.
%% The FIN flag applies to the QUIC packet, not to the frame.
%% We must therefore only consider the frame to have a FIN
%% flag if there's no data remaining to be read.
- `frame(State=#state{http3_machine=HTTP3Machine0},
		Stream=#stream{id=StreamID}, Frame, IsFin)` - @todo Perhaps do this in cow_http3_machine directly.
		{ok, push, _} ->
			terminate(State0, {connection_error, h3_stream_creation_error,
				'Only servers can push. (RFC9114 6.2.2)'});
		{ok, {webtransport, SessionID}, Rest} ->
			become_webtransport_stream(State0, Stream0, unidi, SessionID, Rest, IsFin);
		%% Unknown stream types must be ignored. We choose to abort the
		%% stream instead of reading and discarding the incoming data.
		{undefined, _} ->
			loop(stream_abort_receive(State0, Stream0, h3_stream_creation_error));
		%% Very unlikely to happen but WebTransport headers may be fragmented
		%% as they are more than one byte. The fin flag in this case is an error,
		%% but because it happens in WebTransport application data (the Session ID)
		%% we only reset the impacted stream and not the entire connection.
		more when IsFin =:= fin ->
			loop(stream_abort_receive(State0, Stream0, h3_stream_creation_error));
		more ->
			loop(stream_store(State0, Stream0#stream{buffer=Data}))
	end.
- `data_frame(State=#state{opts=Opts},
		Stream=#stream{id=StreamID, state=StreamState0}, IsFin, Data)` - @todo Propagate trailers.
			send_instructions(State#state{http3_machine=HTTP3Machine}, Instrs);
		{ok, GoAway={goaway, _}, HTTP3Machine} ->
			goaway(State#state{http3_machine=HTTP3Machine}, GoAway);
		{error, Error={stream_error, _Reason, _Human}, Instrs, HTTP3Machine} ->
			State1 = send_instructions(State#state{http3_machine=HTTP3Machine}, Instrs),
			reset_stream(State1, Stream, Error);
		{error, Error={connection_error, _, _}, HTTP3Machine} ->
			terminate(State#state{http3_machine=HTTP3Machine}, Error)
	end.
- `ensure_port(<<"http">>, undefined)` - We add the protocol information for extended CONNECTs.
					Req = case PseudoHeaders of
						#{protocol := Protocol} -> Req0#{protocol => Protocol};
						_ -> Req0
					end,
					headers_frame(State, Stream, Req)
			catch _:_ ->
				reset_stream(State, Stream, {stream_error, h3_message_error,
					'The :path pseudo-header is invalid. (RFC7540 8.1.2.3)'})
			end
	catch _:_ ->
		reset_stream(State, Stream, {stream_error, h3_message_error,
			'The :authority pseudo-header is invalid. (RFC7540 8.1.2.3)'})
	end.

%% @todo Copied from cowboy_http2.
%% @todo How to handle "http"?
- `headers_to_map([], Acc)` - @todo Copied from cowboy_http2.
%% This function is necessary to properly handle duplicate headers
%% and the special-case cookie header.
- `headers_frame(State=#state{opts=Opts}, Stream=#stream{id=StreamID}, Req)` - The cookie header does not use proper HTTP header lists.
		#{Name := Value0} when Name =:= <<"cookie">> ->
			Acc0#{Name => << Value0/binary, "; ", Value/binary >>};
		#{Name := Value0} ->
			Acc0#{Name => << Value0/binary, ", ", Value/binary >>};
		_ ->
			Acc0#{Name => Value}
	end,
	headers_to_map(Tail, Acc).

%% @todo WebTransport CONNECT requests must have extra checks on settings.
%% @todo We may also need to defer them if we didn't get settings.
- `parse_datagram(State, Data0)` - We automatically terminate the stream but it is not an error
	%% per se (at least not in the first implementation).
	Reason = {stream_error, h3_no_error, HumanReadable},
	%% The partial Req is minimal for now. We only have one case
	%% where it can be called (when a method is completely disabled).
	PartialReq = #{
		ref => Ref,
		peer => Peer,
		method => Method,
		headers => headers_to_map(Headers, #{})
	},
	Resp = {response, StatusCode0, RespHeaders0=#{<<"content-length">> => <<"0">>}, <<>>},
	try cowboy_stream:early_error(StreamID, Reason, PartialReq, Resp, Opts) of
		{response, StatusCode, RespHeaders, RespBody} ->
			send_response(State0, Stream, StatusCode, RespHeaders, RespBody)
	catch Class:Exception:Stacktrace ->
		cowboy:log(cowboy_stream:make_error_log(early_error,
			[StreamID, Reason, PartialReq, Resp, Opts],
			Class, Exception, Stacktrace), Opts),
		%% We still need to send an error response, so send what we initially
		%% wanted to send. It's better than nothing.
		send_headers(State0, Stream, fin, StatusCode0, RespHeaders0)
	end.

%% Datagrams.
- `down(State0=#state{opts=Opts, children=Children0}, Pid, Msg)` - @todo Might be a future WT session or an error.
	end.

%% Erlang messages.
- `info(State=#state{opts=Opts, http3_machine=_HTTP3Machine}, StreamID, Msg)` - The stream was terminated already.
		{ok, undefined, Children} ->
			State0#state{children=Children};
		%% The stream is still running.
		{ok, StreamID, Children} ->
			info(State0#state{children=Children}, StreamID, Msg);
		%% The process was unknown.
		error ->
			cowboy:log(warning, "Received EXIT signal ~p for unknown process ~p.~n",
				[Msg, Pid], Opts),
			State0
	end,
	if
%% @todo
%		State#state.http2_status =:= closing, State#state.streams =:= #{} ->
%			terminate(State, {stop, normal, 'The connection is going away.'});
		true ->
			State
	end.
- `commands(State=#state{opts=Opts}, Stream, [Log={log, _, _, _}|Tail])` - @todo Do we want to run the commands after a stop?
	%% @todo Do we even allow commands after?
	stop_stream(State, Stream);
%% Log event.
- `maybe_send_is_fin(State=#state{http3_machine=HTTP3Machine0},
		Stream=#stream{id=StreamID}, fin)` - @todo Add a test for HEAD to make sure we don't send the body when
			%% returning {response...} from a stream handler (or {headers...} then {data...}).
			{ok, _IsFin, HeaderBlock, Instrs, HTTP3Machine}
				= cow_http3_machine:prepare_headers(StreamID, HTTP3Machine0, nofin,
					#{status => cow_http:status_to_integer(StatusCode)},
					headers_to_list(Headers)),
			State = send_instructions(State0#state{http3_machine=HTTP3Machine}, Instrs),
			%% @todo It might be better to do async sends.
			_ = case Body of
				{sendfile, Offset, Bytes, Path} ->
					ok = maybe_socket_error(State,
						cowboy_quicer:send(Conn, StreamID, cow_http3:headers(HeaderBlock))),
					%% Temporary solution to do sendfile over QUIC.
					{ok, _} = maybe_socket_error(State,
						ranch_transport:sendfile(?MODULE, {Conn, StreamID},
							Path, Offset, Bytes, [])),
					ok = maybe_socket_error(State,
						cowboy_quicer:send(Conn, StreamID, cow_http3:data(<<>>), fin));
				_ ->
					ok = maybe_socket_error(State,
						cowboy_quicer:send(Conn, StreamID, [
							cow_http3:headers(HeaderBlock),
							cow_http3:data(Body)
						], fin))
			end,
			maybe_send_is_fin(State, Stream, fin)
	end.
- `send({Conn, StreamID}, IoData)` - Temporary callback to do sendfile over QUIC.
-spec send({cowboy_quicer:quicer_connection_handle(), cow_http3:stream_id()},
	iodata()) -> ok | {error, any()}.
- `headers_to_list(Headers0=#{<<"set-cookie">> := SetCookies})` - The set-cookie header is special; we can only send one cookie per header.
- `send_instructions(State=#state{conn=Conn, local_encoder_id=EncoderID},
		{encoder_instructions, EncData})` - Encoder instructions.
- `become_webtransport_stream(State0=#state{http3_machine=HTTP3Machine0},
		Stream0=#stream{id=StreamID}, StreamType, SessionID, Rest, IsFin)` - We mark the stream as being a WebTransport stream
%% and then continue parsing the data as a WebTransport
%% stream. This function is common for incoming unidi
%% and bidi streams.
- `webtransport_event(State, SessionID, Event)` - We don't need to parse the remaining data if there isn't any.
			case {Rest, IsFin} of
				{<<>>, nofin} -> loop(stream_store(State, Stream));
				_ -> parse(stream_store(State, Stream), StreamID, Rest, IsFin)
			end
		%% @todo Error conditions.
	end.
- `wt_commands(State0=#state{conn=Conn}, Session=#stream{id=SessionID}, [Cmd|Tail])
		when Cmd =:= close; element(1, Cmd) =:= close ->
	%% We must send a WT_CLOSE_SESSION capsule on the CONNECT stream.
	{AppCode, AppMsg} = case Cmd of
		close -> {0, <<>>};
		{close, AppCode0} -> {AppCode0, <<>>};
		{close, AppCode0, AppMsg0} -> {AppCode0, AppMsg0}
	end,
	Capsule = cow_capsule:wt_close_session(AppCode, AppMsg),
	case cowboy_quicer:send(Conn, SessionID, Capsule, fin) of
		ok ->
			State = webtransport_terminate_session(State0, Session),
			%% @todo Because the handler is in a separate process
			%%       we must wait for it to stop and eventually
			%%       kill the process if it takes too long.
			%% @todo We may need to fully close the CONNECT stream (if remote doesn't reset it).
			wt_commands(State, Session, Tail)
		%% @todo Handle errors.
	end.

webtransport_terminate_session(State=#state{conn=Conn, http3_machine=HTTP3Machine0,
		streams=Streams0, lingering_streams=Lingering0}, #stream{id=SessionID})` - We must send a WT_DRAIN_SESSION capsule on the CONNECT stream.
	Capsule = cow_capsule:wt_drain_session(),
	case cowboy_quicer:send(Conn, SessionID, Capsule, nofin) of
		ok ->
			wt_commands(State, Session, Tail)
		%% @todo Handle errors.
	end;
- `stream_peer_send_shutdown(State=#state{conn=Conn}, StreamID)` - Reset/abort the WT streams.
	Streams = maps:filtermap(fun
		(_, #stream{id=StreamID, status={webtransport_session, _}})
				when StreamID =:= SessionID ->
			%% We remove the session stream but do the shutdown outside this function.
			false;
		(StreamID, #stream{status={webtransport_stream, StreamSessionID}})
				when StreamSessionID =:= SessionID ->
			cowboy_quicer:shutdown_stream(Conn, StreamID,
				both, cow_http3:error_to_code(wt_session_gone)),
			false;
		(_, _) ->
			true
	end, Streams0),
	%% Keep the streams in lingering state.
	%% We only keep up to 100 streams in this state. @todo Make it configurable?
	Terminated = maps:keys(Streams0) -- maps:keys(Streams),
	Lingering = lists:sublist(Terminated ++ Lingering0, 100),
	%% Update the HTTP3 state machine.
	HTTP3Machine = cow_http3_machine:close_webtransport_session(SessionID, HTTP3Machine0),
	State#state{
		http3_machine=HTTP3Machine,
		streams=Streams,
		lingering_streams=Lingering
	}.
- `reset_stream(State0=#state{conn=Conn, http3_machine=HTTP3Machine0},
		Stream=#stream{id=StreamID}, Error)` - Cleanly terminating the CONNECT stream is equivalent
		%% to an application error code of 0 and empty message.
		Stream = #stream{status={webtransport_session, _}} ->
			webtransport_event(State, StreamID, {closed, 0, <<>>}),
			%% Shutdown the CONNECT stream fully.
			cowboy_quicer:shutdown_stream(Conn, StreamID),
			webtransport_terminate_session(State, Stream);
		_ ->
			State
	end.
- `stop_stream(State0=#state{http3_machine=HTTP3Machine}, Stream=#stream{id=StreamID})` - @todo Do we want to close both sides?
	%% @todo Should we close the send side if the receive side was already closed?
	cowboy_quicer:shutdown_stream(Conn, StreamID,
		both, cow_http3:error_to_code(Reason)),
	State1 = case cow_http3_machine:reset_stream(StreamID, HTTP3Machine0) of
		{ok, HTTP3Machine} ->
			terminate_stream(State0#state{http3_machine=HTTP3Machine}, Stream, Error);
		{error, not_found} ->
			terminate_stream(State0, Stream, Error)
	end,
%% @todo
%	case reset_rate(State1) of
%		{ok, State} ->
%			State;
%		error ->
%			terminate(State1, {connection_error, enhance_your_calm,
%				'Stream reset rate larger than configuration allows. Flood? (CVE-2019-9514)'})
%	end.
	State1.
- `maybe_terminate_stream(State, _)` - The Stream will be stored in the State at the end of commands processing.
- `goaway(State, {goaway, _})` - @todo Graceful connection shutdown.
%% We terminate the connection immediately if it hasn't fully been initialized.
-spec goaway(#state{}, {goaway, _}) -> no_return().
- `maybe_socket_error(State, {error, closed})` - Function copied from cowboy_http.
- `terminate_reason({connection_error, Reason, _})` - @todo
%			%% We are terminating so it's OK if we can't send the GOAWAY anymore.
%			_ = cowboy_quicer:send(Conn, ControlID, cow_http3:goaway(
%				cow_http3_machine:get_last_streamid(HTTP3Machine))),
		%% We already sent the GOAWAY frame.
%		Status =:= closing ->
%			ok
%	end,
	terminate_all_streams(State, maps:to_list(Streams), Reason),
	cowboy_children:terminate(Children),
%	terminate_linger(State),
	_ = cowboy_quicer:shutdown(Conn, cow_http3:error_to_code(terminate_reason(Reason))),
	exit({shutdown, Reason}).
- `stream_closed(State=#state{local_control_id=StreamID}, StreamID, _)` - Stream closed message for a local (write-only) unidi stream.
- `stream_closed1(State=#state{http3_machine=HTTP3Machine0}, StreamID)` - In the WT session's case, streams will be
		%% removed in webtransport_terminate_session.
		{Stream=#stream{status={webtransport_session, _}}, _} ->
			webtransport_event(State, StreamID, closed_abruptly),
			webtransport_terminate_session(State, Stream);
		{#stream{state=undefined}, Streams} ->
			%% Unidi stream has no handler/children.
			stream_closed1(State#state{streams=Streams}, StreamID);
		%% We only stop bidi streams if the stream was closed with an error
		%% or the stream was already in the process of stopping.
		{#stream{status=Status, state=StreamState}, Streams}
				when Status =:= stopping; ErrorCode =/= 0 ->
			terminate_stream_handler(State, StreamID, closed, StreamState),
			Children = cowboy_children:shutdown(Children0, StreamID),
			stream_closed1(State#state{streams=Streams, children=Children}, StreamID);
		%% Don't remove a stream that terminated properly but
		%% has chosen to remain up (custom stream handlers).
		{_, _} ->
			stream_closed1(State, StreamID);
		%% Stream closed message for a stream that has been reset. Ignore.
		error ->
			case is_lingering_stream(State, StreamID) of
				true ->
					ok;
				false ->
					%% We avoid logging the data as it could be quite large.
					cowboy:log(warning, "Received stream_closed for unknown stream ~p. ~p ~p",
						[StreamID, self(), Streams0], Opts)
			end,
			State
	end.
- `is_lingering_stream(#state{lingering_streams=Lingering}, StreamID)` - We only keep up to 100 streams in this state. @todo Make it configurable?
	Lingering = [StreamID|lists:sublist(Lingering0, 100 - 1)],
	State#state{lingering_streams=Lingering}.

**Dependencies**: Transport, cowboy_children, cowboy, cow_http3, cow_http3_machine, cowboy_req, cow_http, cowboy_tracer_h, inet, cowboy_quicer, cowboy_middleware, cow_http2, maps, cowboy_stream, cow_capsule, cowboy_metrics_h, cow_http_hd, cow_http2_machine, ranch, ranch_transport

---

### cowboy_loop

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_loop.erl`

**Behaviors**: cowboy_sub_protocol

**Description**:
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

**Exported Functions**: upgrade/4, upgrade/5, loop/5, system_continue/3, system_terminate/4, system_code_change/4

**Functions**:

- `upgrade(Req, Env, Handler, HandlerState)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `loop(Req=#{pid := Parent}, Env, Handler, HandlerState, Timeout)` - @todo Handle system messages.
- `call(Req0, Env, Handler, HandlerState0, Timeout, Message)` - System messages.
		{'EXIT', Parent, Reason} ->
			terminate(Req, Env, Handler, HandlerState, Reason);
		{system, From, Request} ->
			sys:handle_system_msg(Request, From, Parent, ?MODULE, [],
				{Req, Env, Handler, HandlerState, Timeout});
		%% Calls from supervisor module.
		{'$gen_call', From, Call} ->
			cowboy_children:handle_supervisor_call(Call, From, [], ?MODULE),
			loop(Req, Env, Handler, HandlerState, Timeout);
		Message ->
			call(Req, Env, Handler, HandlerState, Timeout, Message)
	after Timeout ->
		call(Req, Env, Handler, HandlerState, Timeout, timeout)
	end.
- `system_continue(_, _, {Req, Env, Handler, HandlerState, Timeout})` - System callbacks.

-spec system_continue(_, _, {Req, Env, module(), any(), timeout()})
	-> {ok, Req, Env} | {suspend, ?MODULE, loop, [any()]}
	when Req::cowboy_req:req(), Env::cowboy_middleware:env().

**Dependencies**: sys, cowboy_children, Handler, cowboy_middleware, cowboy_handler, cowboy_req

---

### cowboy_metrics_h

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_metrics_h.erl`

**Behaviors**: cowboy_stream

**Description**:
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

**Exported Functions**: init/3, data/4, info/3, terminate/3, early_error/5

**Functions**:

- `init(StreamID, Req=#{ref := Ref}, Opts=#{metrics_callback := Fun})` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `fold([{data, nofin, Data}|Tail], State=#state{resp_body_length=RespBodyLen})` - @todo It might be worthwhile to keep the sendfile information around,
%% especially if these frames ultimately result in a sendfile syscall.
- `resp_body_length({sendfile, _, Len, _})` - As far as metrics go we are limited in what we can provide
	%% in this case.
	Metrics = #{
		ref => Ref,
		pid => self(),
		streamid => StreamID,
		reason => Reason,
		partial_req => PartialReq,
		resp_status => RespStatus,
		resp_headers => RespHeaders,
		early_error_time => Time,
		resp_body_length => resp_body_length(RespBody)
	},
	Fun(Metrics),
	Resp.

**Dependencies**: cowboy_stream, cowboy, ranch, maps, cowboy_req

---

### cowboy_middleware

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_middleware.erl`

**Description**:
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

**Dependencies**: cowboy_req

---

### cowboy_quicer

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_quicer.erl`

**Description**:
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

**Exported Functions**: peername/1, sockname/1, peercert/1, shutdown/2, start_bidi_stream/2, start_unidi_stream/2, send/3, send/4, send_datagram/2, shutdown_stream/2 ... (+2 more)

**Functions**:

- `peername(Conn)` - @todo Make quicer export these types.
-type quicer_connection_handle() :: reference().
-export_type([quicer_connection_handle/0]).

-type quicer_app_errno() :: non_neg_integer().

-include_lib("quicer/include/quicer.hrl").

%% Connection.

-spec peername(quicer_connection_handle())
	-> {ok, {inet:ip_address(), inet:port_number()}}
	| {error, any()}.
- `start_bidi_stream(Conn, InitialData)` - Streams.

-spec start_bidi_stream(quicer_connection_handle(), iodata())
	-> {ok, cow_http3:stream_id()}
	| {error, any()}.
- `shutdown_stream(_Conn, StreamID)` - @todo Fix/ignore the Dialyzer error instead of doing this.
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
- `shutdown_flag(both)` - @todo Are these flags correct for what we want?
- `handle({quic, transport_shutdown, _Conn, _Flags})` - QUIC_CONNECTION_EVENT_SHUTDOWN_INITIATED_BY_TRANSPORT

**Dependencies**: cow_http, quicer_nif, public_key, cow_http3, inet, quicer

---

### cowboy_req

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_req.erl`

**Description**:
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

**Exported Functions**: method/1, version/1, peer/1, sock/1, cert/1, scheme/1, host/1, host_info/1, port/1, path/1 ... (+54 more)

**Functions**:

- `method(#{method := Method})` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `host_info(#{host_info := HostInfo})` - @todo The host_info is undefined if cowboy_router isn't used. Do we want to crash?
-spec host_info(req()) -> cowboy_router:tokens() | undefined.
- `path_info(#{path_info := PathInfo})` - @todo The path_info is undefined if cowboy_router isn't used. Do we want to crash?
-spec path_info(req()) -> cowboy_router:tokens() | undefined.
- `parse_qs(#{qs := Qs})` - @todo Might be useful to limit the number of keys.
-spec parse_qs(req()) -> [{binary(), binary() | true}].
- `binding(Name, Req)` - Disable individual components.
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
- `cookie_name(<<$\s, Rest/binary>>)` - This is a specialized function to extract a cookie name
%% regardless of whether the name is valid or not. We skip
%% whitespace at the beginning and take whatever's left to
%% be the cookie name, up to the = sign.
- `has_body(#{has_body := HasBody})` - Request body.

-spec has_body(req()) -> boolean().
- `body_length(#{body_length := Length})` - The length may not be known if HTTP/1.1 with a transfer-encoding;
%% or HTTP/2 with no content-length header. The length is always
%% known once the body has been completely read.
-spec body_length(req()) -> undefined | non_neg_integer().
- `set_body_length(Req=#{headers := Headers}, BodyLength)` - infinity + 1000 = infinity.
		_ -> Period + 1000
	end,
	Timeout = maps:get(timeout, Opts, DefaultTimeout),
	Ref = make_ref(),
	cast({read_body, self(), Ref, Length, Period}, Req),
	receive
		{request_body, Ref, nofin, Body} ->
			{more, Body, Req};
		{request_body, Ref, fin, BodyLength, Body} ->
			{ok, Body, set_body_length(Req, BodyLength)}
	after Timeout ->
		exit(timeout)
	end.
- `read_part(Req)` - Multipart.

-spec read_part(Req)
	-> {ok, cowboy:http_headers(), Req} | {done, Req}
	when Req::req().
- `read_part_body(Req)` - Reject multipart content containing duplicate headers.
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
- `stream_multipart(Req=#{multipart := {Boundary, Buffer}}, _, _)` - We crash when the data ends unexpectedly.
		{ok, <<>>, _} ->
			exit({request_error, {multipart, Type},
				'Malformed body; multipart expected.'});
		{ok, Data, Req2} ->
			{Data, Req2}
	end;
- `set_resp_cookie(Name, Value, Req, Opts)` - The cookie name cannot contain any of the following characters:
%%   =,;\s\t\r\n\013\014
%%
%% The cookie value cannot contain any of the following characters:
%%   ,; \t\r\n\013\014
-spec set_resp_cookie(binary(), iodata(), Req, cow_cookie:cookie_opts())
	-> Req when Req::req().
- `set_resp_header(<<"set-cookie">>, _, _)` - @todo We could add has_resp_cookie and unset_resp_cookie now.

-spec set_resp_header(binary(), iodata(), Req)
	-> Req when Req::req().
- `delete_resp_header(_, Req)` - There are no resp headers so we have nothing to delete.
- `reply(Status, Headers, Body, Req)
		when Status =:= 204; Status =:= 304 ->
	do_reply_ensure_no_body(Status, Headers, Body, Req);
reply(Status = <<"204",_/bits>>, Headers, Body, Req)` - 204 responses must not include content-length. 304 responses may
%% but only when set explicitly. (RFC7230 3.3.1, RFC7230 3.3.2)
%% Neither status code must include a response body. (RFC7230 3.3)
- `do_reply(Status, Headers, _, Req=#{method := <<"HEAD">>})` - Don't send any body for HEAD responses. While the protocol code is
%% supposed to enforce this rule, we prefer to avoid copying too much
%% data around if we can avoid it.
- `stream_reply(Status, Headers=#{}, Req)
		when Status =:= 204; Status =:= 304 ->
	reply(Status, Headers, <<>>, Req);
stream_reply(Status = <<"204",_/bits>>, Headers=#{}, Req)` - 204 and 304 responses must NOT send a body. We therefore
%% transform the call to a full response and expect the user
%% to NOT call stream_body/3 afterwards. (RFC7230 3.3)
- `stream_body(Msg, Req=#{pid := Pid})` - @todo Do we need a timeout?
- `push(_, _, #{has_sent_resp := _}, _)` - @todo Optimization: don't send anything at all for HTTP/1.0 and HTTP/1.1.
%% @todo Path, Headers, Opts, everything should be in proper binary,
%% or normalized when creating the Req object.
-spec push(iodata(), cowboy:http_headers(), req(), push_opts()) -> ok.
- `cast(Msg, #{pid := Pid, streamid := StreamID})` - Stream handlers.

-spec cast(any(), req()) -> ok.
- `response_headers(Headers0, Req)` - Internal.

%% @todo What about set-cookie headers set through set_resp_header or reply?
-spec response_headers(Headers, req()) -> Headers when Headers::cowboy:http_headers().
- `kvlist_to_map(Fields, KvList)` - The set-cookie header is special; we can only send one cookie per header.
	%% We send the list of values for many cookies in one key of the map,
	%% and let the protocols deal with it directly.
	case maps:get(resp_cookies, Req, undefined) of
		undefined -> Headers;
		RespCookies -> Headers#{<<"set-cookie">> => maps:values(RespCookies)}
	end.

%% Create map, convert keys to atoms and group duplicate keys into lists.
%% Keys that are not found in the user provided list are entirely skipped.
%% @todo Can probably be done directly while parsing.
- `filter([], Map, Errors)` - Loop through fields, if value is missing and no default,
%% record the error; else if value is missing and has a
%% default, set default; otherwise apply constraints. If
%% constraint fails, record the error.
%%
%% When there is an error at the end, crash.

**Dependencies**: cowboy_stream, cow_qs, binary, file, cowboy_router, cowboy, ranch_proxy_header, cowboy_constraints, inet, cow_sse, ranch, cow_cookie, cow_multipart, maps, cowboy_clock

---

### cowboy_rest

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_rest.erl`

**Behaviors**: cowboy_sub_protocol

**Description**:
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

**Exported Functions**: upgrade/4, upgrade/5

**Functions**:

- `upgrade(Req, Env, Handler, HandlerState, _Opts)` - cowboy_rest takes no options.
- `known_methods(Req, State=#state{method=Method})` - known_methods/2 should return a list of binary methods.
- `allowed_methods(Req, State=#state{method=Method})` - allowed_methods/2 should return a list of binary methods.
- `is_authorized(Req, State)` - is_authorized/2 should return true or {false, WwwAuthenticateHeader}.
- `options(Req, State=#state{method= <<"OPTIONS">>})` - If you need to add additional headers to the response at this point,
%% you should do it directly in the options/2 call using set_resp_headers.
- `content_types_provided(Req, State)` - content_types_provided/2 should return a list of content types and their
%% associated callback function as a tuple: {{Type, SubType, Params}, Fun}.
%% Type and SubType are the media type as binary. Params is a list of
%% Key/Value tuple, with Key and Value a binary. Fun is the name of the
%% callback that will be used to return the content of the response. It is
%% given as an atom.
%%
%% An example of such return value would be:
%%    {{<<"text">>, <<"html">>, []}, to_html}
%%
%% Note that it is also possible to return a binary content type that will
%% then be parsed by Cowboy. However note that while this may make your
%% resources a little more readable, this is a lot less efficient.
%%
%% An example of such return value would be:
%%    {<<"text/html">>, to_html}
- `normalize_content_types(Normalized = {'*', _}, accept)` - Wildcard for content_types_accepted.
- `prioritize_mediatype({TypeA, SubTypeA, ParamsA}, {TypeB, SubTypeB, ParamsB})` - Same quality, check precedence in more details.
				prioritize_mediatype(MediaTypeA, MediaTypeB);
			({_MediaTypeA, QualityA, _AcceptParamsA},
			 {_MediaTypeB, QualityB, _AcceptParamsB}) ->
				%% Just compare the quality.
				QualityA > QualityB
		end, Accept).

%% Media ranges can be overridden by more specific media ranges or
%% specific media types. If more than one media range applies to a given
%% type, the most specific reference has precedence.
%%
%% We always choose B over A when we can't decide between the two.
- `choose_media_type(Req, State, [])` - Ignoring the rare AcceptParams. Not sure what should be done about them.
- `match_media_type_params(Req, State, Accept,
		[Provided = {PMT = {TP, STP, Params_P0}, Fun}|Tail],
		MediaType = {{_TA, _STA, Params_A}, _QA, _APA})` - When we match against a wildcard, the media type is text
			%% and has a charset parameter, we call charsets_provided
			%% and check that the charset is provided. If the callback
			%% is not exported, we accept inconditionally but ignore
			%% the given charset so as to not send a wrong value back.
			case call(Req, State, charsets_provided) of
				no_call ->
					languages_provided(Req#{media_type => {TP, STP, Params_A0}},
						State#state{content_type_a=Provided});
				{stop, Req2, State2} ->
					terminate(Req2, State2);
				{Switch, Req2, State2} when element(1, Switch) =:= switch_handler ->
					switch_handler(Switch, Req2, State2);
				{CP, Req2, State2} ->
					State3 = State2#state{charsets_p=CP},
					case lists:member(Charset, CP) of
						false ->
							match_media_type(Req2, State3, Accept, Tail, MediaType);
						true ->
							languages_provided(Req2#{media_type => {TP, STP, Params_A}},
								State3#state{content_type_a=Provided,
									charset_a=Charset})
					end
			end;
		_ ->
			languages_provided(Req#{media_type => {TP, STP, Params_A0}},
				State#state{content_type_a=Provided})
	end;
- `languages_provided(Req, State)` - When a charset was provided explicitly in both the charset header
			%% and the media types provided and the negotiation is successful,
			%% we keep the charset and don't call charsets_provided. This only
			%% applies to text media types, however.
			{Charset, Params_P} = case lists:keytake(<<"charset">>, 1, Params_P0) of
				false -> {undefined, Params_P0};
				{value, {_, Charset0}, Params_P1} -> {Charset0, Params_P1}
			end,
			languages_provided(Req#{media_type => {TP, STP, Params_P}},
				State#state{content_type_a={{TP, STP, Params_P}, Fun},
					charset_a=Charset});
		true ->
			languages_provided(Req#{media_type => PMT},
				State#state{content_type_a=Provided});
		false ->
			match_media_type(Req, State, Accept, Tail, MediaType)
	end.

%% languages_provided should return a list of binary values indicating
%% which languages are accepted by the resource.
%%
%% @todo I suppose we should also ask the resource if it wants to
%% set a language itself or if it wants it to be automatically chosen.
- `prioritize_languages(AcceptLanguages)` - A language-range matches a language-tag if it exactly equals the tag,
%% or if it exactly equals a prefix of the tag such that the first tag
%% character following the prefix is "-". The special range "*", if
%% present in the Accept-Language field, matches every tag not matched
%% by any other range present in the Accept-Language field.
%%
%% @todo The last sentence probably means we should always put '*'
%% at the end of the list.
- `charsets_provided(Req, State=#state{charset_a=Charset})
		when Charset =/= undefined ->
	set_content_type(Req, State);
%% If charsets_p is defined, use it instead of calling charsets_provided
%% again. We also call this clause during normal execution to avoid
%% duplicating code.
charsets_provided(Req, State=#state{charsets_p=[]})` - charsets_provided should return a list of binary values indicating
%% which charsets are accepted by the resource.
%%
%% A charset may have been selected while negotiating the accept header.
%% There's no need to select one again.
- `choose_charset(Req, State, [{_, 0}|Tail])` - A q-value of 0 means not acceptable.
- `encodings_provided(Req, State)` - @todo Match for identity as we provide nothing else for now.
%% @todo Don't forget to set the Content-Encoding header when we reply a body
%% and the found encoding is something other than identity.
- `variances(Req, State=#state{content_types_p=CTP,
		languages_p=LP, charsets_p=CP})` - variances/2 should return a list of headers that will be added
%% to the Vary response header. The Accept, Accept-Language,
%% Accept-Charset and Accept-Encoding headers do not need to be
%% specified.
%%
%% @todo Do Accept-Encoding too when we handle it.
%% @todo Does the order matter?
- `if_match_must_not_exist(Req, State)` - Strong Etag comparison: weak Etag never matches.
		{{weak, _}, Req2, State2} ->
			precondition_failed(Req2, State2);
		{Etag, Req2, State2} ->
			case lists:member(Etag, EtagsList) of
				true -> if_none_match_exists(Req2, State2);
				%% Etag may be `undefined' which cannot be a member.
				false -> precondition_failed(Req2, State2)
			end
	catch Class:Reason:Stacktrace ->
		error_terminate(Req, State, Class, Reason, Stacktrace)
	end.
- `if_unmodified_since(Req, State, IfUnmodifiedSince)` - If LastModified is the atom 'no_call', we continue.
- `is_weak_match(_, [])` - Weak Etag comparison: only check the opaque tag.
- `moved_permanently(Req, State, OnFalse)` - moved_permanently/2 should return either false or {true, Location}
%% with Location the full new URI of the resource.
- `moved_temporarily(Req, State)` - moved_temporarily/2 should return either false or {true, Location}
%% with Location the full new URI of the resource.
- `delete_resource(Req, State)` - delete_resource/2 should start deleting the resource and return.
- `delete_completed(Req, State)` - delete_completed/2 indicates whether the resource has been deleted yet.
- `accept_resource(Req, State)` - content_types_accepted should return a list of media types and their
%% associated callback functions in the same format as content_types_provided.
%%
%% The callback will then be called and is expected to process the content
%% pushed to the resource in the request body.
%%
%% content_types_accepted SHOULD return a different list
%% for each HTTP method.
- `choose_content_type(Req, State, {Type, SubType, Param},
		[{{Type, SubType, AcceptedParam}, Fun}|_Tail])
		when AcceptedParam =:= '*'; AcceptedParam =:= Param ->
	process_content_type(Req, State, Fun);
choose_content_type(Req, State, ContentType, [_Any|Tail])` - The special parameter '*' will always match any kind of content type
%% parameters.
%% Note that because it will always match, it should be the last of the
%% list for specific content type, otherwise it'll shadow the ones following.
- `maybe_created(Req, State=#state{method= <<"PUT">>})` - If PUT was used then the resource has been created at the current URL.
%% Otherwise, if a location header has been set then the resource has been
%% created at a new URL. If not, send a 200 or 204 as expected from a
%% POST or PATCH request.
- `set_resp_body_etag(Req, State)` - Set the Etag header if any for the response provided.
- `set_resp_body_last_modified(Req, State)` - Set the Last-Modified header if any for the response provided.
- `set_resp_body_expires(Req, State)` - Set the Expires header if any for the response provided.
- `if_range(Req, State)` - Strong etag comparison is an exact match with the generate_etag result.
		Etag={strong, _} ->
			range(Req, State);
		%% We cannot do a strong date comparison because we have
		%% no way of knowing whether the representation changed
		%% twice during the second covered by the presented
		%% validator. (RFC7232 2.2.2)
		_ ->
			set_resp_body(Req, State)
	catch _:_ ->
		set_resp_body(Req, State)
	end;
- `range(Req, State=#state{ranges_a=[]})` - @todo This can probably be moved to if_range directly.
- `choose_range(Req, State=#state{ranges_a=RangesAccepted}, Range={RangeUnit, _})` - @todo Maybe change parse_header to return <<"bytes">> in 3.0.
		{bytes, BytesRange} ->
			choose_range(Req, State, {<<"bytes">>, BytesRange});
		Range ->
			choose_range(Req, State, Range)
	catch _:_ ->
		%% We send a 416 response back when we can't parse the
		%% range header at all. I'm not sure this is the right
		%% way to go but at least this can help clients identify
		%% what went wrong when their range requests never work.
		range_not_satisfiable(Req, State, undefined)
	end.
- `range_satisfiable(Req, State, Callback)` - We pass the selected range onward in the Req.
			range_satisfiable(Req#{range => Range}, State, Callback);
		false ->
			set_resp_body(Req, State)
	end.
- `set_ranged_body(Req=#{range := {<<"bytes">>, _}}, State, auto)` - When the callback selected is 'auto' and the range unit
%% is bytes, we call the normal provide callback and split
%% the content automatically.
- `set_ranged_body_auto(Req=#{range := {_, Ranges}}, State, Body)` - We might also want to have some checks about range order,
%% number of ranges, and perhaps also join ranges that are
%% too close into one contiguous range. Some of these can
%% be done before calling the ProvideCallback.
- `set_ranged_body_callback(Req, State=#state{handler=Handler}, Callback)` - Sendfile with open-ended range.
		{{0, infinity}, {sendfile, 0, 12, "t"}, {{0, 11, 12}, {sendfile, 0, 12, "t"}}},
		{{6, infinity}, {sendfile, 0, 12, "t"}, {{6, 11, 12}, {sendfile, 6, 6, "t"}}},
		{{11, infinity}, {sendfile, 0, 12, "t"}, {{11, 11, 12}, {sendfile, 11, 1, "t"}}},
		%% Sendfile with open-ended range. Sendfile tuple has an offset originally.
		{{0, infinity}, {sendfile, 3, 12, "t"}, {{0, 11, 12}, {sendfile, 3, 12, "t"}}},
		{{6, infinity}, {sendfile, 3, 12, "t"}, {{6, 11, 12}, {sendfile, 9, 6, "t"}}},
		{{11, infinity}, {sendfile, 3, 12, "t"}, {{11, 11, 12}, {sendfile, 14, 1, "t"}}},
		%% Sendfile with a specific range.
		{{0, 11}, {sendfile, 0, 12, "t"}, {{0, 11, 12}, {sendfile, 0, 12, "t"}}},
		{{6, 11}, {sendfile, 0, 12, "t"}, {{6, 11, 12}, {sendfile, 6, 6, "t"}}},
		{{11, 11}, {sendfile, 0, 12, "t"}, {{11, 11, 12}, {sendfile, 11, 1, "t"}}},
		{{1, 10}, {sendfile, 0, 12, "t"}, {{1, 10, 12}, {sendfile, 1, 10, "t"}}},
		%% Sendfile with a specific range. Sendfile tuple has an offset originally.
		{{0, 11}, {sendfile, 3, 12, "t"}, {{0, 11, 12}, {sendfile, 3, 12, "t"}}},
		{{6, 11}, {sendfile, 3, 12, "t"}, {{6, 11, 12}, {sendfile, 9, 6, "t"}}},
		{{11, 11}, {sendfile, 3, 12, "t"}, {{11, 11, 12}, {sendfile, 14, 1, "t"}}},
		{{1, 10}, {sendfile, 3, 12, "t"}, {{1, 10, 12}, {sendfile, 4, 10, "t"}}},
		%% Sendfile with negative range.
		{-12, {sendfile, 0, 12, "t"}, {{0, 11, 12}, {sendfile, 0, 12, "t"}}},
		{-6, {sendfile, 0, 12, "t"}, {{6, 11, 12}, {sendfile, 6, 6, "t"}}},
		{-1, {sendfile, 0, 12, "t"}, {{11, 11, 12}, {sendfile, 11, 1, "t"}}},
		%% Sendfile with negative range. Sendfile tuple has an offset originally.
		{-12, {sendfile, 3, 12, "t"}, {{0, 11, 12}, {sendfile, 3, 12, "t"}}},
		{-6, {sendfile, 3, 12, "t"}, {{6, 11, 12}, {sendfile, 9, 6, "t"}}},
		{-1, {sendfile, 3, 12, "t"}, {{11, 11, 12}, {sendfile, 14, 1, "t"}}},
		%% Iodata with open-ended range.
		{{0, infinity}, <<"Hello world!">>, {{0, 11, 12}, <<"Hello world!">>}},
		{{6, infinity}, <<"Hello world!">>, {{6, 11, 12}, <<"world!">>}},
		{{11, infinity}, <<"Hello world!">>, {{11, 11, 12}, <<"!">>}},
		%% Iodata with a specific range. The resulting data is
		%% wrapped in a list because of how cow_iolists:split/2 works.
		{{0, 11}, <<"Hello world!">>, {{0, 11, 12}, [<<"Hello world!">>]}},
		{{6, 11}, <<"Hello world!">>, {{6, 11, 12}, [<<"world!">>]}},
		{{11, 11}, <<"Hello world!">>, {{11, 11, 12}, [<<"!">>]}},
		{{1, 10}, <<"Hello world!">>, {{1, 10, 12}, [<<"ello world">>]}},
		%% Iodata with negative range.
		{-12, <<"Hello world!">>, {{0, 11, 12}, <<"Hello world!">>}},
		{-6, <<"Hello world!">>, {{6, 11, 12}, <<"world!">>}},
		{-1, <<"Hello world!">>, {{11, 11, 12}, <<"!">>}}
	],
	[{iolist_to_binary(io_lib:format("range ~p data ~p", [VR, VD])),
		fun() -> R = ranged_partition(VR, VD) end} || {VR, VD, R} <- Tests].
-endif.
- `set_one_ranged_body(Req0, State, OneRange)` - When we receive a single range, we send it directly.
		{[OneRange], Req2, State2} ->
			set_one_ranged_body(Req2, State2, OneRange);
		%% When we receive multiple ranges we have to send them as multipart/byteranges.
		%% This also applies to non-bytes units. (RFC7233 A) If users don't want to use
		%% this for non-bytes units they can always return a single range with a binary
		%% content-range information.
		{Ranges, Req2, State2} when length(Ranges) > 1 ->
			%% We have to check whether there are sendfile tuples in the
			%% ranges to be sent. If there are we must use stream_reply.
			HasSendfile = [] =/= [true || {_, {sendfile, _, _, _}} <- Ranges],
			case HasSendfile of
				true -> send_multipart_ranged_body(Req2, State2, Ranges);
				false -> set_multipart_ranged_body(Req2, State2, Ranges)
			end
	end catch Class:{case_clause, no_call}:Stacktrace ->
		error_terminate(Req, State, Class, {error, {missing_callback, {Handler, Callback, 2}},
			'A callback specified in ranges_provided/2 is not exported.'},
			Stacktrace)
	end.
- `send_multipart_ranged_body(Req, State, [FirstRange|MoreRanges])` - Similar to set_multipart_ranged_body except we have to stream
%% the data because the parts contain sendfile tuples.
- `range_not_satisfiable(Req, State, undefined)` - We send the content-range header when we can on error.
- `set_resp_body(Req, State=#state{handler=Handler, content_type_a={_, Callback}})` - Set the response headers and call the callback found using
%% content_types_provided/2 to obtain the request body and add
%% it to the response.
- `set_resp_etag(Req, State)` - Response utility functions.
- `generate_etag(Req, State=#state{etag=Etag})` - We allow the callback to return 'undefined'
		%% to allow conditionally generating etags. We
		%% handle 'undefined' the same as if the function
		%% was not exported.
		{undefined, Req2, State2} ->
			{undefined, Req2, State2#state{etag=no_call}};
		{Etag, Req2, State2} when is_binary(Etag) ->
			Etag2 = cow_http_hd:parse_etag(Etag),
			{Etag2, Req2, State2#state{etag=Etag2}};
		{Etag, Req2, State2} ->
			{Etag, Req2, State2#state{etag=Etag}}
	end;
- `expect(Req, State, Callback, Expected, OnTrue, OnFalse)` - REST primitives.
- `switch_handler({switch_handler, Mod}, Req, #state{handler_state=HandlerState})` - We remove the content-type header when there is no body,
	%% except when the status code is 200 because it might have
	%% been intended (for example sending an empty file).
	Req = case cowboy_req:has_resp_body(Req0) of
		true when StatusCode =:= 200 -> Req0;
		true -> Req0;
		false -> cowboy_req:delete_resp_header(<<"content-type">>, Req0)
	end,
	terminate(cowboy_req:reply(StatusCode, Req), State).

**Dependencies**: Mod, cow_http_hd, io_lib, cowboy_handler, Handler, cow_multipart, cowboy_middleware, calendar, cow_iolists, cowboy_clock, cowboy_req

---

### cowboy_router

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_router.erl`

**Behaviors**: cowboy_middleware

**Description**:
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

**Exported Functions**: compile/1, execute/2

**Functions**:

- `compile(Routes)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `compile_rules(<< $], _/bits >>, _, _, _, _)` - Missing an open bracket.
- `compile_binding(<<>>, _, <<>>)` - Everything past $: until the segment separator ($. for hosts,
%% $/ for paths) or $[ or $] or end of binary is the binding name.
- `compile_brackets_split(<< C, Rest/bits >>, Acc, N) when C =:= $[ ->
	compile_brackets_split(Rest, << Acc/binary, C >>, N + 1);
compile_brackets_split(<< C, Rest/bits >>, Acc, N) when C =:= $], N > 0 ->
	compile_brackets_split(Rest, << Acc/binary, C >>, N - 1);
%% That's the right one.
compile_brackets_split(<< $], Rest/bits >>, Acc, 0)` - Make sure we don't confuse the closing bracket we're looking for.
- `match([{'_', [], PathMatchs}|_Tail], _, Path)` - If the host is '_' then there can be no constraints.
- `match_path([{'_', [], Handler, Opts}|_Tail], HostInfo, _, Bindings)` - If the path is '_' then there can be no constraints.
- `split_path(<< $/, Path/bits >>)` - Following RFC2396, this function may return path segments containing any
%% character, including <em>/</em> if, and only if, a <em>/</em> was escaped
%% and part of a path segment.
-spec split_path(binary()) -> tokens() | badrequest.
- `list_match(_List, _Match, _Binds)` - Values don't match, stop.
- `compile_test_()` - Tests.

-ifdef(TEST).
- `split_host_test_()` - Match any host and path.
		{[{'_', [{'_', h, o}]}],
			[{'_', [], [{'_', [], h, o}]}]},
		{[{"cowboy.example.org",
				[{"/", ha, oa}, {"/path/to/resource", hb, ob}]}],
			[{[<<"org">>, <<"example">>, <<"cowboy">>], [], [
				{[], [], ha, oa},
				{[<<"path">>, <<"to">>, <<"resource">>], [], hb, ob}]}]},
		{[{'_', [{"/path/to/resource/", h, o}]}],
			[{'_', [], [{[<<"path">>, <<"to">>, <<"resource">>], [], h, o}]}]},
		% Cyrillic from a latin1 encoded file.
		{[{'_', [{[47,208,191,209,131,209,130,209,140,47,208,186,47,209,128,
				208,181,209,129,209,131,209,128,209,129,209,131,47], h, o}]}],
			[{'_', [], [{[<<208,191,209,131,209,130,209,140>>, <<208,186>>,
				<<209,128,208,181,209,129,209,131,209,128,209,129,209,131>>],
				[], h, o}]}]},
		{[{"cowboy.example.org.", [{'_', h, o}]}],
			[{[<<"org">>, <<"example">>, <<"cowboy">>], [], [{'_', [], h, o}]}]},
		{[{".cowboy.example.org", [{'_', h, o}]}],
			[{[<<"org">>, <<"example">>, <<"cowboy">>], [], [{'_', [], h, o}]}]},
		% Cyrillic from a latin1 encoded file.
		{[{[208,189,208,181,208,186,208,184,208,185,46,209,129,208,176,
				208,185,209,130,46,209,128,209,132,46], [{'_', h, o}]}],
			[{[<<209,128,209,132>>, <<209,129,208,176,208,185,209,130>>,
				<<208,189,208,181,208,186,208,184,208,185>>],
				[], [{'_', [], h, o}]}]},
		{[{":subdomain.example.org", [{"/hats/:name/prices", h, o}]}],
			[{[<<"org">>, <<"example">>, subdomain], [], [
				{[<<"hats">>, name, <<"prices">>], [], h, o}]}]},
		{[{"ninenines.:_", [{"/hats/:_", h, o}]}],
			[{['_', <<"ninenines">>], [], [{[<<"hats">>, '_'], [], h, o}]}]},
		{[{"[www.]ninenines.eu",
			[{"/horses", h, o}, {"/hats/[page/:number]", h, o}]}], [
				{[<<"eu">>, <<"ninenines">>], [], [
					{[<<"horses">>], [], h, o},
					{[<<"hats">>], [], h, o},
					{[<<"hats">>, <<"page">>, number], [], h, o}]},
				{[<<"eu">>, <<"ninenines">>, <<"www">>], [], [
					{[<<"horses">>], [], h, o},
					{[<<"hats">>], [], h, o},
					{[<<"hats">>, <<"page">>, number], [], h, o}]}]},
		{[{'_', [{"/hats/:page/:number", h, o}]}], [{'_', [], [
			{[<<"hats">>, page, number], [], h, o}]}]},
		{[{'_', [{"/hats/[page/[:number]]", h, o}]}], [{'_', [], [
			{[<<"hats">>], [], h, o},
			{[<<"hats">>, <<"page">>], [], h, o},
			{[<<"hats">>, <<"page">>, number], [], h, o}]}]},
		{[{"[...]ninenines.eu", [{"/hats/[...]", h, o}]}],
			[{[<<"eu">>, <<"ninenines">>, '...'], [], [
				{[<<"hats">>, '...'], [], h, o}]}]},
		%% Path segment containing a colon.
		{[{'_', [{"/foo/bar:blah", h, o}]}], [{'_', [], [
			{[<<"foo">>, <<"bar:blah">>], [], h, o}]}]}
	],
	[{lists:flatten(io_lib:format("~p", [Rt])),
		fun() -> Rs = compile(Rt) end} || {Rt, Rs} <- Tests].

**Dependencies**: persistent_term, binary, cowboy_constraints, cowboy, io_lib, cowboy_bstr, cow_uri, cowboy_middleware, cowboy_req

---

### cowboy_static

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_static.erl`

**Description**:
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

**Exported Functions**: init/2, malformed_request/2, forbidden/2, content_types_provided/2, charsets_provided/2, ranges_provided/2, resource_exists/2, last_modified/2, generate_etag/2, get_file/2

**Functions**:

- `init(Req, {Name, Path})` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `how_to_access_app_priv1(Dir)` - If the priv directory is not a directory, it must be
	%% inside an Erlang application .ez archive. We call
	%% how_to_access_app_priv1() to find the corresponding archive.
	case filelib:is_dir(PrivDir) of
		true  -> direct;
		false -> how_to_access_app_priv1(PrivDir)
	end.
- `absname(Path) when is_list(Path)` - We go "up" by one path component at a time and look for a
	%% regular file.
	Archive = filename:dirname(Dir),
	case Archive of
		Dir ->
			%% filename:dirname() returned its argument:
			%% we reach the root directory. We found no
			%% archive so we return 'direct': the given priv
			%% directory doesn't exist.
			direct;
		_ ->
			case filelib:is_regular(Archive) of
				true  -> {archive, Archive};
				false -> how_to_access_app_priv1(Archive)
			end
	end.
- `validate_reserved([])` - When dir/priv_dir are used and there is no path_info
		%% this is a configuration error and we abort immediately.
		undefined ->
			{ok, cowboy_req:reply(500, Req), error};
		PathInfo ->
			case validate_reserved(PathInfo) of
				error ->
					{cowboy_rest, Req, error};
				ok ->
					Filepath = filename:join([Dir|PathInfo]),
					Len = byte_size(Dir),
					case fullpath(Filepath) of
						<< Dir:Len/binary, $/, _/binary >> ->
							init_info(Req, Filepath, HowToAccess, Extra);
						<< Dir:Len/binary >> ->
							init_info(Req, Filepath, HowToAccess, Extra);
						_ ->
							{cowboy_rest, Req, error}
					end
			end
	end.
- `validate_reserved1(<<>>)` - We always reject forward slash, backward slash and NUL as
%% those have special meanings across the supported platforms.
%% We could support the backward slash on some platforms but
%% for the sake of consistency and simplicity we don't.
- `fix_archived_file_info(ArchiveInfo, ContainedFileInfo)` - The Erlang application archive is fine.
			%% Now check if the requested file is in that
			%% archive. We also need the file_info to merge
			%% them with the archive's one.
			PathS = binary_to_list(Path),
			case erl_prim_loader:read_file_info(PathS) of
				{ok, ContainedFileInfo} ->
					Info = fix_archived_file_info(
						ArchiveInfo,
						ContainedFileInfo),
					{archive, Info};
				error ->
					{error, enoent}
			end;
		Error ->
			Error
	end.
- `fullpath_test_()` - We merge the archive and content #file_info because we are
	%% interested by the timestamps of the archive, but the type and
	%% size of the contained file/directory.
	%%
	%% We reset the access to 'read', because we won't rewrite the
	%% archive.
	ArchiveInfo#file_info{
		size = ContainedFileInfo#file_info.size,
		type = ContainedFileInfo#file_info.type,
		access = read
	}.

-ifdef(TEST).
- `malformed_request(Req, State)` - Reject requests that tried to access a file outside
%% the target directory, or used reserved characters.

-spec malformed_request(Req, State)
	-> {boolean(), Req, State}.
- `forbidden(Req, State={_, {_, #file_info{type=directory}}, _})` - Directories, files that can't be accessed at all and
%% files with no read flag are forbidden.

-spec forbidden(Req, State)
	-> {boolean(), Req, State}
	when State::state().
- `content_types_provided(Req, State={Path, _, Extra}) when is_list(Extra)` - Detect the mimetype of the file.

-spec content_types_provided(Req, State)
	-> {[{binary() | {binary(), binary(), '*' | [{binary(), binary()}]}, get_file}], Req, State}
	when State::state().
- `charsets_provided(Req, State={Path, _, Extra})` - Detect the charset of the file.

-spec charsets_provided(Req, State)
	-> {[binary()], Req, State} | no_call
	when State::state().
- `ranges_provided(Req, State)` - We simulate the callback not being exported.
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
- `resource_exists(Req, State={_, {_, #file_info{type=regular}}, _})` - Assume the resource doesn't exist if it's not a regular file.

-spec resource_exists(Req, State)
	-> {boolean(), Req, State}
	when State::state().
- `generate_etag(Req, State={Path, {_, #file_info{size=Size, mtime=Mtime}},
		Extra})` - Generate an etag for the file.

-spec generate_etag(Req, State)
	-> {{strong | weak, binary() | undefined}, Req, State}
	when State::state().
- `last_modified(Req, State={_, {_, #file_info{mtime=Modified}}, _})` - Return the time of last modification of the file.

-spec last_modified(Req, State)
	-> {calendar:datetime(), Req, State}
	when State::state().
- `get_file(Req, State={Path, {direct, #file_info{size=Size}}, _})` - Stream the file.

-spec get_file(Req, State)
	-> {{sendfile, 0, non_neg_integer(), binary()} | binary(), Req, State}
	when State::state().

**Dependencies**: os, file, calendar, filelib, cow_mimetypes, Module, code, erl_prim_loader, cowboy_req, filename

---

### cowboy_stream

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_stream.erl`

**Description**:
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

**Exported Functions**: init/3, data/4, info/3, terminate/3, early_error/5, make_error_log/5

**Functions**:

- `init(StreamID, Req, Opts)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `data(_, _, _, undefined)` - We call the next handler and remove it from the list of
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
- `make_error_log(init, [StreamID, Req, Opts], Class, Exception, Stacktrace)` - This is the same behavior as in init/3.
			Handler:early_error(StreamID, Reason,
				PartialReq, Resp, Opts#{stream_handlers => Tail})
	end.

-spec make_error_log(init | data | info | terminate | early_error,
	list(), error | exit | throw, any(), list())
	-> {log, error, string(), list()}.

**Dependencies**: cowboy_stream, cowboy, cow_http3, inet, Handler, logger, cow_http2, maps, cowboy_req

---

### cowboy_stream_h

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_stream_h.erl`

**Behaviors**: cowboy_stream

**Description**:
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

**Exported Functions**: init/3, data/4, info/3, terminate/3, early_error/5, request_process/3, resume/5

**Functions**:

- `init(StreamID, Req=#{ref := Ref}, Opts)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `expect(#{version := 'HTTP/1.0'})` - Ignore the expect header in HTTP/1.0.
- `data(StreamID, IsFin=nofin, Data, State=#state{
		read_body_length=ReadLen, read_body_buffer=Buffer, body_length=BodyLen})
		when byte_size(Data) + byte_size(Buffer) < ReadLen ->
	do_data(StreamID, IsFin, Data, [], State#state{
		expect=undefined,
		read_body_buffer= << Buffer/binary, Data/binary >>,
		body_length=BodyLen + byte_size(Data)
	});
%% Stream is waiting for data and we received enough to send.
data(StreamID, IsFin, Data, State=#state{read_body_pid=Pid, read_body_ref=Ref,
		read_body_timer_ref=TRef, read_body_buffer=Buffer, body_length=BodyLen0})` - @todo This is wrong, it's missing byte_size(Data).
		body_length=BodyLen
	});
%% Stream is waiting for data but we didn't receive enough to send yet.
- `info(StreamID, Info, State)` - Unknown message, either stray or meant for a handler down the line.
- `request_process(Req, Env, Middlewares)` - Request process.

%% We add the stacktrace to exit exceptions here in order
%% to simplify the debugging of errors. The proc_lib library
%% already adds the stacktrace to other types of exceptions.
-spec request_process(cowboy_req:req(), cowboy_middleware:env(), [module()]) -> ok.

**Dependencies**: cowboy_stream, cow_http, proc_lib, cowboy, ranch, cowboy_middleware, Middleware, maps, cowboy_req

---

### cowboy_sub_protocol

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_sub_protocol.erl`

**Description**:
Copyright (c) Loïc Hoguin <essen@ninenines.eu>
Copyright (c) James Fish <james@fishcakez.com>
%% Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
%% THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN

**Dependencies**: cowboy_middleware, cowboy_req

---

### cowboy_tls

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_tls.erl`

**Behaviors**: ranch_protocol

**Description**:
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

**Exported Functions**: start_link/3, start_link/4, connection_process/4

**Functions**:

- `start_link(Ref, Transport, Opts)` - Ranch 2.
-spec start_link(ranch:ref(), module(), cowboy:opts()) -> {ok, pid()}.
- `init(Parent, Ref, Socket, Transport, ProxyInfo, Opts, Protocol)` - http/1.1 or no protocol negotiated.
			Protocol = case maps:get(alpn_default_protocol, Opts, http) of
				http -> cowboy_http;
				http2 -> cowboy_http2
			end,
			init(Parent, Ref, Socket, Transport, ProxyInfo, Opts, Protocol)
	end.

**Dependencies**: Protocol, proc_lib, cowboy, ssl, ranch, maps

---

### cowboy_tracer_h

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_tracer_h.erl`

**Behaviors**: cowboy_stream

**Description**:
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

**Exported Functions**: init/3, data/4, info/3, terminate/3, early_error/5, set_trace_patterns/0, tracer_process/3, system_continue/3, system_terminate/4, system_code_change/4

**Functions**:

- `init(StreamID, Req, Opts)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `set_trace_patterns()` - API.

%% These trace patterns are most likely not suitable for production.
-spec set_trace_patterns() -> ok.
- `init_tracer(_, _, _)` - When the options tracer_match_specs or tracer_callback
%% are not provided we do not enable tracing.
- `start_tracer(StreamID, Req, Opts)` - We only start the tracer if one wasn't started before.
- `tracer_process(StreamID, Req=#{pid := Parent}, Opts=#{tracer_callback := Fun})` - The default flags are probably not suitable for production.
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
- `tracer_loop(Parent, Opts=#{tracer_callback := Fun}, State0)` - This is necessary because otherwise the tracer could stop
	%% before it has finished processing the events in its queue.
	process_flag(trap_exit, true),
	State = Fun(init, {StreamID, Req, Opts}),
	tracer_loop(Parent, Opts, State).
- `system_continue(Parent, _, {Opts, State})` - System callbacks.

-spec system_continue(pid(), _, {cowboy:opts(), any()}) -> no_return().

**Dependencies**: cowboy_stream, proc_lib, sys, cowboy, inet, maps, cowboy_req

---

### cowboy_websocket

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_websocket.erl`

**Behaviors**: cowboy_sub_protocol

**Description**:
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

**Exported Functions**: is_upgrade_request/1, upgrade/4, upgrade/5, takeover/7, loop/3, system_continue/3, system_terminate/4, system_code_change/4

**Functions**:

- `is_upgrade_request(#{version := Version, method := <<"CONNECT">>, protocol := Protocol})
		when Version =:= 'HTTP/2'; Version =:= 'HTTP/3' ->
	<<"websocket">> =:= cowboy_bstr:to_lower(Protocol);
is_upgrade_request(Req=#{version := 'HTTP/1.1', method := <<"GET">>})` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `upgrade(Req0=#{version := Version}, Env, Handler, HandlerState, Opts)` - @todo Immediately crash if a response has already been sent.
- `websocket_upgrade(State, Req=#{version := Version})` - The status code 426 is specific to HTTP/1.1 connections.
		{error, upgrade_required} when Version =:= 'HTTP/1.1' ->
			{ok, cowboy_req:reply(426, #{
				<<"connection">> => <<"upgrade">>,
				<<"upgrade">> => <<"websocket">>
			}, Req0), Env};
		%% Use 501 Not Implemented for HTTP/2 and HTTP/3 as recommended
		%% by RFC9220 3 (WebSockets Upgrade over HTTP/3).
		{error, upgrade_required} ->
			{ok, cowboy_req:reply(501, Req0), Env}
	catch _:_ ->
		%% @todo Probably log something here?
		%% @todo Test that we can have 2 /ws 400 status code in a row on the same connection.
		{ok, cowboy_req:reply(400, Req0), Env}
	end.
- `websocket_extensions(State=#state{opts=Opts, extensions=Extensions},
		Req=#{pid := Pid, version := Version},
		[{<<"permessage-deflate">>, Params}|Tail], RespHeader)` - For HTTP/2 we ARE on the controlling process and do NOT want to update the owner.
- `websocket_handshake(State, Req=#{ref := Ref, pid := Pid, streamid := StreamID},
		HandlerState, _Env)` - @todo We don't want date and server headers.
	Headers = cowboy_req:response_headers(#{
		<<"connection">> => <<"Upgrade">>,
		<<"upgrade">> => <<"websocket">>,
		<<"sec-websocket-accept">> => Challenge
	}, Req),
	Pid ! {{Pid, StreamID}, {switch_protocol, Headers, ?MODULE, {State, HandlerState}}},
	{ok, Req, Env};
%% For HTTP/2 we do not let the process die, we instead keep it
%% for the Websocket stream. This is because in HTTP/2 we only
%% have a stream, it doesn't take over the whole connection.
- `takeover(Parent, Ref, Socket, Transport, Opts, Buffer,
		{State0=#state{opts=WsOpts, handler=Handler, req=Req}, HandlerState})` - @todo We don't want date and server headers.
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
- `maybe_socket_error(_, _)` - @todo We should have an option to disable this behavior.
		_ -> ranch:remove_connection(Ref)
	end,
	Messages = case Transport of
		undefined -> undefined;
		_ -> Transport:messages()
	end,
	State = set_idle_timeout(State0#state{parent=Parent,
		ref=Ref, socket=Socket, transport=Transport,
		opts=WsOpts#{dynamic_buffer => maps:get(dynamic_buffer, Opts, false)},
		key=undefined, messages=Messages,
		%% Dynamic buffer only applies to HTTP/1.1 Websocket.
		dynamic_buffer_size=init_dynamic_buffer_size(Opts),
		dynamic_buffer_moving_average=maps:get(dynamic_buffer_initial_average, Opts, 0)}, 0),
	%% We call parse_header/3 immediately because there might be
	%% some data in the buffer that was sent along with the handshake.
	%% While it is not allowed by the protocol to send frames immediately,
	%% we still want to process that data if any.
	case erlang:function_exported(Handler, websocket_init, 1) of
		true -> handler_call(State, HandlerState, #ps_header{buffer=Buffer},
			websocket_init, undefined, fun after_init/3);
		false -> after_init(State, HandlerState, #ps_header{buffer=Buffer})
	end.

-include("cowboy_dynamic_buffer.hrl").

%% @todo Implement early socket error detection.
- `after_init(State, HandlerState, ParseState)` - Enable active,N for HTTP/1.1, and auto read_body for HTTP/2.
	%% We must do this only after calling websocket_init/1 (if any)
	%% to give the handler a chance to disable active mode immediately.
	setopts_active(State),
	maybe_read_body(State),
	parse_header(State, HandlerState, ParseState);
- `setopts_active(#state{transport=undefined})` - We have two ways of reading the body for Websocket. For HTTP/1.1
%% we have full control of the socket and can therefore use active,N.
%% For HTTP/2 we are just a stream, and are instead using read_body
%% (automatic mode). Technically HTTP/2 will only go passive after
%% receiving the next data message, while HTTP/1.1 goes passive
%% immediately but there might still be data to be processed in
%% the message queue.
- `maybe_read_body(_)` - @todo Keep Ref around.
	ReadBodyRef = make_ref(),
	Pid ! {Stream, {read_body, self(), ReadBodyRef, auto, infinity}},
	ok;
- `passive(State=#state{socket=Socket, transport=Transport, messages=Messages})` - Unfortunately we cannot currently cancel read_body.
	%% But that's OK, we will just stop reading the body
	%% after the next message.
	State#state{active=false};
- `before_loop(State=#state{hibernate=true}, HandlerState, ParseState)` - Hardcoded for compatibility with Ranch 1.x.
				Passive =:= tcp_passive; Passive =:= ssl_passive ->
			flush_passive(Socket, Messages)
	after 0 ->
		ok
	end.
- `set_idle_timeout(State=#state{opts=Opts, timeout_ref=PrevRef}, TimeoutNum)` - @todo Do we really need this for HTTP/2?
- `tick_idle_timeout(State=#state{timeout_num=?IDLE_TIMEOUT_TICKS}, HandlerState, _)` - Most of the time we don't need to cancel the timer since it
	%% will have triggered already. But this call is harmless so
	%% it is kept to simplify the code as we do need to cancel when
	%% options are changed dynamically.
	_ = case PrevRef of
		undefined -> ignore;
		PrevRef -> erlang:cancel_timer(PrevRef, [{async, true}, {info, false}])
	end,
	case maps:get(idle_timeout, Opts, 60000) of
		infinity ->
			State#state{timeout_ref=undefined, timeout_num=TimeoutNum};
		Timeout ->
			TRef = erlang:start_timer(Timeout div ?IDLE_TIMEOUT_TICKS, self(), ?MODULE),
			State#state{timeout_ref=TRef, timeout_num=TimeoutNum}
	end.

-define(reset_idle_timeout(State), State#state{timeout_num=0}).
- `parse(State, HandlerState, PS=#ps_header{buffer=Buffer}, Data)` - Socket messages. (HTTP/1.1)
		{OK, Socket, Data} when OK =:= element(1, Messages) ->
			State1 = maybe_resize_buffer(State, Data),
			parse(?reset_idle_timeout(State1), HandlerState, ParseState, Data);
		{Closed, Socket} when Closed =:= element(2, Messages) ->
			terminate(State, HandlerState, {error, closed});
		{Error, Socket, Reason} when Error =:= element(3, Messages) ->
			terminate(State, HandlerState, {error, Reason});
		{Passive, Socket} when Passive =:= element(4, Messages);
				%% Hardcoded for compatibility with Ranch 1.x.
				Passive =:= tcp_passive; Passive =:= ssl_passive ->
			setopts_active(State),
			loop(State, HandlerState, ParseState);
		%% Body reading messages. (HTTP/2)
		{request_body, _Ref, nofin, Data} ->
			maybe_read_body(State),
			parse(?reset_idle_timeout(State), HandlerState, ParseState, Data);
		%% @todo We need to handle this case as if it was an {error, closed}
		%% but not before we finish processing frames. We probably should have
		%% a check in before_loop to let us stop looping if a flag is set.
		{request_body, _Ref, fin, _, Data} ->
			maybe_read_body(State),
			parse(?reset_idle_timeout(State), HandlerState, ParseState, Data);
		%% Timeouts.
		{timeout, TRef, ?MODULE} ->
			tick_idle_timeout(State, HandlerState, ParseState);
		{timeout, OlderTRef, ?MODULE} when is_reference(OlderTRef) ->
			before_loop(State, HandlerState, ParseState);
		%% System messages.
		{'EXIT', Parent, Reason} ->
			%% @todo We should exit gracefully.
			exit(Reason);
		{system, From, Request} ->
			sys:handle_system_msg(Request, From, Parent, ?MODULE, [],
				{State, HandlerState, ParseState});
		%% Calls from supervisor module.
		{'$gen_call', From, Call} ->
			cowboy_children:handle_supervisor_call(Call, From, [], ?MODULE),
			before_loop(State, HandlerState, ParseState);
		Message ->
			handler_call(State, HandlerState, ParseState,
				websocket_info, Message, fun before_loop/3)
	end.
- `parse_payload(State=#state{opts=Opts, frag_state=FragState, utf8_state=Incomplete, extensions=Extensions},
		HandlerState, ParseState=#ps_payload{
			type=Type, len=Len, mask_key=MaskKey, rsv=Rsv,
			unmasked=Unmasked, unmasked_len=UnmaskedLen}, Data)` - All frames sent from the client to the server are masked.
		{_, _, _, _, undefined, _} ->
			websocket_close(State, HandlerState, {error, badframe});
		{_, _, _, Len, _, _} when Len > MaxFrameSize ->
			websocket_close(State, HandlerState, {error, badsize});
		{Type, FragState2, Rsv, Len, MaskKey, Rest} ->
			parse_payload(State#state{frag_state=FragState2}, HandlerState,
				#ps_payload{type=Type, len=Len, mask_key=MaskKey, rsv=Rsv}, Rest);
		more ->
			before_loop(State, HandlerState, ParseState);
		error ->
			websocket_close(State, HandlerState, {error, badframe})
	end.
- `handler_call(State=#state{handler=Handler}, HandlerState,
		ParseState, Callback, Message, NextState)` - @todo Allow receiving fragments.
		{fragment, _, _, Payload} when byte_size(Payload) + byte_size(SoFar) > MaxFrameSize ->
			websocket_close(State, HandlerState, {error, badsize});
		{fragment, nofin, _, Payload} ->
			parse_header(State#state{frag_buffer= << SoFar/binary, Payload/binary >>},
				HandlerState, #ps_header{buffer=RemainingData});
		{fragment, fin, Type, Payload} ->
			handler_call(State#state{frag_state=undefined, frag_buffer= <<>>}, HandlerState,
				#ps_header{buffer=RemainingData},
				websocket_handle, {Type, << SoFar/binary, Payload/binary >>},
				fun parse_header/3);
		close ->
			websocket_close(State, HandlerState, remote);
		{close, CloseCode, Payload} ->
			websocket_close(State, HandlerState, {remote, CloseCode, Payload});
		Frame = ping ->
			transport_send(State, nofin, frame(pong, State)),
			handler_call(State, HandlerState,
				#ps_header{buffer=RemainingData},
				websocket_handle, Frame, fun parse_header/3);
		Frame = {ping, Payload} ->
			transport_send(State, nofin, frame({pong, Payload}, State)),
			handler_call(State, HandlerState,
				#ps_header{buffer=RemainingData},
				websocket_handle, Frame, fun parse_header/3);
		Frame ->
			handler_call(State, HandlerState,
				#ps_header{buffer=RemainingData},
				websocket_handle, Frame, fun parse_header/3)
	end.
- `handler_call_result(State0, HandlerState, ParseState, NextState, Commands)` - The following call results are deprecated.
		{ok, HandlerState2} ->
			NextState(State, HandlerState2, ParseState);
		{ok, HandlerState2, hibernate} ->
			NextState(State#state{hibernate=true}, HandlerState2, ParseState);
		{reply, Payload, HandlerState2} ->
			case websocket_send(Payload, State) of
				ok ->
					NextState(State, HandlerState2, ParseState);
				stop ->
					terminate(State, HandlerState2, stop);
				Error = {error, _} ->
					terminate(State, HandlerState2, Error)
			end;
		{reply, Payload, HandlerState2, hibernate} ->
			case websocket_send(Payload, State) of
				ok ->
					NextState(State#state{hibernate=true},
						HandlerState2, ParseState);
				stop ->
					terminate(State, HandlerState2, stop);
				Error = {error, _} ->
					terminate(State, HandlerState2, Error)
			end;
		{stop, HandlerState2} ->
			websocket_close(State, HandlerState2, stop)
	catch Class:Reason:Stacktrace ->
		websocket_send_close(State, {crash, Class, Reason}),
		handler_terminate(State, HandlerState, {crash, Class, Reason}),
		erlang:raise(Class, Reason, Stacktrace)
	end.

-spec handler_call_result(#state{}, any(), parse_state(), fun(), commands()) -> no_return().
- `commands([{shutdown_reason, ShutdownReason}|Tail], State, Data)` - We reset the number of ticks when changing the idle_timeout option.
			set_idle_timeout(StateF#state{opts=Opts#{idle_timeout => IdleTimeout}}, 0);
		(max_frame_size, MaxFrameSize, StateF=#state{opts=Opts}) ->
			StateF#state{opts=Opts#{max_frame_size => MaxFrameSize}};
		(_, _, StateF) ->
			StateF
	end, State0, SetOpts),
	commands(Tail, State, Data);
- `frame(Frame, #state{deflate=false, extensions=Extensions})` - Don't compress frames while deflate is disabled.
- `system_continue(_, _, {State, HandlerState, ParseState})` - System callbacks.

-spec system_continue(_, _, {#state{}, any(), parse_state()}) -> no_return().
- `system_code_change(Misc, _, _, _)` - @todo We should exit gracefully, if possible.
	terminate(State, HandlerState, Reason).

-spec system_code_change(Misc, _, _, _)
	-> {ok, Misc} when Misc::{#state{}, any(), parse_state()}.

**Dependencies**: cowboy_stream, proc_lib, Transport, sys, cowboy_children, base64, cowboy_req, inet, Handler, cowboy_bstr, ranch, cowboy_middleware, crypto, maps, cowboy_handler, cow_ws

---

### cowboy_webtransport

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_webtransport.erl`

**Description**:
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

**Exported Functions**: upgrade/4, upgrade/5, info/3, terminate/3

**Functions**:

- `is_upgrade_request(#{version := Version, method := <<"CONNECT">>, protocol := Protocol})
		when Version =:= 'HTTP/3' ->
	%% @todo scheme MUST BE "https"
	<<"webtransport">> =:= cowboy_bstr:to_lower(Protocol);

is_upgrade_request(_)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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

%% @todo To enable WebTransport the following options need to be set:
%%
%% QUIC:
%%  - max_datagram_frame_size > 0
%%
%% HTTP/3:
%%  - SETTINGS_H3_DATAGRAM = 1
%%  - SETTINGS_ENABLE_CONNECT_PROTOCOL = 1
%%  - SETTINGS_WT_MAX_SESSIONS >= 1

%% Cowboy supports versions 07 through 13 of the WebTransport drafts.
%% Cowboy also has some compatibility with version 02.
%%
%% WebTransport CONNECT requests go through cowboy_stream as normal
%% and then an upgrade/switch_protocol is issued (just like Websocket).
%% After that point none of the events go through cowboy_stream except
%% the final terminate event. The request process becomes the process
%% handling all events in the WebTransport session.
%%
%% WebTransport sessions can be ended via a command, via a crash or
%% exit, via the closing of the connection (client or server inititated),
%% via the client ending the session (mirroring the command) or via
%% the client terminating the CONNECT stream.
-module(cowboy_webtransport).

-export([upgrade/4]).
-export([upgrade/5]).

%% cowboy_stream.
-export([info/3]).
-export([terminate/3]).

-type stream_type() :: unidi | bidi.
-type open_stream_ref() :: any().

-type event() ::
	{stream_open, cow_http3:stream_id(), stream_type()} |
	{opened_stream_id, open_stream_ref(), cow_http3:stream_id()} |
	{stream_data, cow_http3:stream_id(), cow_http:fin(), binary()} |
	{datagram, binary()} |
	close_initiated.

-type commands() :: [
	{open_stream, open_stream_ref(), stream_type(), iodata()} |
	{close_stream, cow_http3:stream_id(), cow_http3:wt_app_error_code()} |
	{send, cow_http3:stream_id() | datagram, iodata()} |
	initiate_close |
	close |
	{close, cow_http3:wt_app_error_code()} |
	{close, cow_http3:wt_app_error_code(), iodata()}
].
-export_type([commands/0]).

-type call_result(State) :: {commands(), State} | {commands(), State, hibernate}.

-callback init(Req, any())
	-> {ok | module(), Req, any()}
	| {module(), Req, any(), any()}
	when Req::cowboy_req:req().

-callback webtransport_init(State)
	-> call_result(State) when State::any().
-optional_callbacks([webtransport_init/1]).

-callback webtransport_handle(event(), State)
	-> call_result(State) when State::any().
-optional_callbacks([webtransport_handle/2]).

-callback webtransport_info(any(), State)
	-> call_result(State) when State::any().
-optional_callbacks([webtransport_info/2]).

-callback terminate(any(), cowboy_req:req(), any()) -> ok.
-optional_callbacks([terminate/3]).

-type opts() :: #{
	req_filter => fun((cowboy_req:req()) -> map())
}.
-export_type([opts/0]).

-record(state, {
	id :: cow_http3:stream_id(),
	parent :: pid(),
	opts = #{} :: opts(),
	handler :: module(),
	hibernate = false :: boolean(),
	req = #{} :: map()
}).

%% This function mirrors a similar function for Websocket.

-spec is_upgrade_request(cowboy_req:req()) -> boolean().
- `upgrade(Req=#{version := 'HTTP/3', pid := Pid, streamid := StreamID}, Env, Handler, HandlerState, Opts)` - @todo Immediately crash if a response has already been sent.
- `webtransport_init(State=#state{handler=Handler}, HandlerState)` - @todo Must ensure the relevant settings are enabled (QUIC and H3).
	%% Either we check them BEFORE, or we check them when the handler
	%% is OK to initiate a webtransport session. Probably need to
	%% check them BEFORE as we need to become (takeover) the webtransport process
	%% after we are done with the upgrade. Maybe in cow_http3_machine but
	%% it doesn't have QUIC settings currently (max_datagram_size).
	case is_upgrade_request(Req) of
		true ->
			Headers = cowboy_req:response_headers(#{}, Req),
			Pid ! {{Pid, StreamID}, {switch_protocol, Headers, ?MODULE,
				#{session_pid => self()}}},
			webtransport_init(State, HandlerState);
		%% Use 501 Not Implemented to mirror the recommendation in
		%% by RFC9220 3 (WebSockets Upgrade over HTTP/3).
		false ->
			%% @todo I don't think terminate will be called.
			{ok, cowboy_req:reply(501, Req), Env}
	end.
- `handler_call(State=#state{handler=Handler}, HandlerState, Callback, Message)` - Timeouts.
%% @todo idle_timeout
%		{timeout, TRef, ?MODULE} ->
%			tick_idle_timeout(State, HandlerState, ParseState);
%		{timeout, OlderTRef, ?MODULE} when is_reference(OlderTRef) ->
%			before_loop(State, HandlerState, ParseState);
		%% System messages.
		{'EXIT', Parent, Reason} ->
			%% @todo We should exit gracefully.
			exit(Reason);
		{system, From, Request} ->
			sys:handle_system_msg(Request, From, Parent, ?MODULE, [],
				{State, HandlerState});
		%% Calls from supervisor module.
		{'$gen_call', From, Call} ->
			cowboy_children:handle_supervisor_call(Call, From, [], ?MODULE),
			before_loop(State, HandlerState);
		Message ->
			handler_call(State, HandlerState, webtransport_info, Message)
	end.
- `handler_call_result(State0, HandlerState, Commands)` - @todo Do we need to send a close? Let cowboy_http3 detect and handle it?
		handler_terminate(State, HandlerState, {crash, Class, Reason}),
		erlang:raise(Class, Reason, Stacktrace)
	end.
- `commands([Command=close|Tail], State, _, Acc)` - close | {close, Code} | {close, Code, Msg} - CLOSE_WT_SESSION
%% @todo At this point the handler must not issue stream or send commands.
- `terminate_proc(State, HandlerState, Reason)` - @todo A set_options command could be useful to increase the number of allowed streams
%%       or other forms of flow control. Alternatively a flow command. Or both.
%% @todo A shutdown_reason command could be useful for the same reasons as Websocekt.

-spec terminate_proc(_, _, _) -> no_return().
- `handler_terminate(#state{handler=Handler, req=Req}, HandlerState, Reason)` - @todo This is what should be done if shutdown_reason gets implemented.
%	case Shutdown of
%		normal -> exit(normal);
%		_ -> exit({shutdown, Shutdown})
%	end.
	exit(normal).
- `info(StreamID, Msg, WTState=#{stream_state := StreamState0})` - cowboy_stream callbacks.
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

**Dependencies**: cowboy_stream, cow_http, proc_lib, sys, cowboy_children, cow_http3, Handler, cowboy_bstr, cowboy_middleware, cowboy_handler, maps, cowboy_req

---

## Supervisor Modules

### cowboy_sup

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_sup.erl`

**Behaviors**: supervisor

**Description**:
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

**Exported Functions**: start_link/0, init/1

**Functions**:

- `start_link()` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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

## Application Modules

### cowboy_app

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_app.erl`

**Behaviors**: application

**Description**:
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

**Exported Functions**: start/2, stop/1

**Functions**:

- `start(_, _)` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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

**Dependencies**: cowboy_sup

---

## Behavior Modules

### cowboy_clock

**File**: `/Users/ddleon/.erlviz/cache/ninenines_cowboy/src/cowboy_clock.erl`

**Behaviors**: gen_server

**Description**:
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

**Exported Functions**: start_link/0, stop/0, rfc1123/0, rfc1123/1, init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2, code_change/3

**Functions**:

- `start_link()` - Copyright (c) Loïc Hoguin <essen@ninenines.eu>
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
- `rfc1123()` - When the ets table doesn't exist, either because of a bug
%% or because Cowboy is being restarted, we perform in a
%% slightly degraded state and build a new timestamp for
%% every request.
-spec rfc1123() -> binary().
- `init([])` - gen_server.

-spec init([]) -> {ok, #state{}}.
- `handle_info(_Info, State)` - Cancel the timer in case an external process sent an update message.
	_ = erlang:cancel_timer(TRef0, [{async, true}, {info, false}]),
	T = erlang:universaltime(),
	B2 = update_rfc1123(B1, Prev, T),
	ets:insert(?MODULE, {rfc1123, B2}),
	TRef = erlang:send_after(1000, self(), update),
	{noreply, #state{universaltime=T, rfc1123=B2, tref=TRef}};
- `update_rfc1123(Bin, Now, Now)` - Internal.

-spec update_rfc1123(binary(), undefined | calendar:datetime(),
	calendar:datetime()) -> binary().
- `pad_int(X) when X < 10 ->
	<< $0, ($0 + X) >>;
pad_int(X)` - Following suggestion by MononcQc on #erlounge.
-spec pad_int(0..59) -> binary().
- `update_rfc1123_test_()` - Tests.

-ifdef(TEST).

**Dependencies**: calendar, ets

---

