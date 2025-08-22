# ErlViz Examples

This directory contains example outputs from ErlViz analyses of real Erlang projects.

## Cowboy Analysis

The `cowboy_analysis/` directory contains sample output from analyzing the [Cowboy HTTP server](https://github.com/ninenines/cowboy) project.

### Generated Files

**Graphs (`graphs/`):**
- `dependency_graph.png` - Module dependency visualization (96 DPI)
- `communication_diagram.png` - Communication pattern analysis (96 DPI)  
- `behavior_hierarchy.png` - OTP behavior hierarchy (96 DPI)

**Documentation (`docs/`):**
- `README.md` - Project overview and statistics
- `modules.md` - Detailed module documentation

### Analysis Summary

- **Project**: Cowboy HTTP Server
- **Total Modules**: 29
- **OTP Behaviors**: application, gen_server, cowboy_stream, etc.
- **Architecture**: Web Application/API Server
- **Complexity**: High

### How These Were Generated

```bash
# These examples were created using:
python main.py --cli https://github.com/ninenines/cowboy --output cowboy_analysis --dpi 96
```

### Using These Examples

These low-resolution (96 DPI) images are perfect for:
- Documentation in README files
- Web-based presentations
- Quick project overviews
- Embedding in wikis or issue trackers

For high-resolution printing or detailed analysis, generate graphs with higher DPI:

```bash
# High resolution for printing
python main.py --cli https://github.com/ninenines/cowboy --dpi 1200

# Standard resolution for documents  
python main.py --cli https://github.com/ninenines/cowboy --dpi 300
```

## Adding More Examples

To contribute additional examples:

1. Analyze an interesting Erlang project
2. Use 96 DPI for consistent web-friendly file sizes
3. Include both graphs and key documentation
4. Add a brief description of the project and findings

Popular Erlang projects for analysis:
- [RabbitMQ](https://github.com/rabbitmq/rabbitmq-server)
- [Riak](https://github.com/basho/riak)
- [MongooseIM](https://github.com/esl/MongooseIM)
- [Ejabberd](https://github.com/processone/ejabberd)
- [Wings3D](https://github.com/dgud/wings)
