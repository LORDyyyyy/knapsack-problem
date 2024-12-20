import sys


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise AttributeError("Environment type is not specified.")
    env = sys.argv[1]

    if env not in ["api", "cli"]:
        raise AttributeError("Invalid Environment value. Only api, cli are accepted.")

    if env == "api":
        import web

        web.start()
    else:
        import cli

        cli.start()
