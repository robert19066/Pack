from pyparsing import line


class HelperFunctions:
    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.lines = f.readlines()

    def parse_type(self):
        line = self.lines[0].strip()
        if line.startswith("$type="):
            return line.split("=")[1].strip()
        return "bash"

    def parse_execution_method(self):
        line = self.lines[1].strip()
        if line.startswith("$excmeth:"):
            method = line.split(":", 1)[1].strip().lower()
            return "bulldozer" if method == "bulldozer" else "default"

        return "default"

    def parse_issudo(self):
        line = self.lines[2].strip()
        if line.startswith("$isudo="):
            value = line.split("=")[1].strip().lower()
            return value == "true"
        return False

    def parse_cmds(self):
        return [line.strip() for line in self.lines[3:-1] if line.strip()]
