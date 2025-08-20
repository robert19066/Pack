from helper_functions import HelperFunctions

import subprocess

class Main:
    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.lines = f.readlines()
        
        self.helper = HelperFunctions(self.filepath)
        self.exported = []

    def select_to_examine(self, path):
        if path.endswith(".paklt") or path.endswith(".pakl") or path.endswith(".fopak"):
            self.exported.clear()

            # add the things to output
            self.exported.append(self.helper.parse_type())
            self.exported.append(self.helper.parse_execution_method())
            self.exported.append(self.helper.parse_issudo())
            self.exported.append(self.helper.parse_cmds())

            return self.exported
        else:
            self.exported.clear()
            return "err"
        
    def executeShell(self, shell, isudo, contents, isbulldozer):
        failed_cmds = []

        for cmd in contents:
            full_cmd = f"{shell} -c '{cmd}'"
            if isudo:
                full_cmd = f"sudo {full_cmd}"

            try:
                subprocess.run(full_cmd, shell=True, check=not isbulldozer)
            except subprocess.CalledProcessError as e:
                if isbulldozer:
                    print(f"⚠️ Bulldozer mode: Ignored error in → {cmd}")
                    failed_cmds.append(cmd)
                else:
                    print(f"❌ Error in → {cmd}\n{e}")
                    return "err"

        if isbulldozer and failed_cmds:
            print(f"\n🔍 Bulldozer Summary: {len(failed_cmds)} command(s) failed but were skipped.")
            for i, fc in enumerate(failed_cmds, 1):
                print(f"  {i}. {fc}")

        return "ok"
    def run(self, packlet_paths):
        results = []

        for path in packlet_paths:
            selected = self.select_to_examine(path)
            if selected == "err":
                results.append((path, "invalid packlet"))
                continue

            shell = selected[0]
            isudo = selected[2] if len(selected) > 2 else False
            cmds = selected[-1]
            exec_method = selected[1] if len(selected) > 1 else "default"
            isbuldozer = exec_method == "bulldozer"

            result = self.executeShell(shell, isudo, cmds, isbuldozer)
            results.append((path, "success" if result != "err" else "failed"))

        return results
    


