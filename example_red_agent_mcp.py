from fastmcp import FastMCP

server = FastMCP()

@server.tool
def generate_hello_world():
    """
    A simple tool that returns 'Hello, World!'.
    """
    return "Hello, World!"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=12345, transport="sse")
