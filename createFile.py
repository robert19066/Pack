import os

def create_packlet_file(execmeth, shell, isudo, contents, filename):
    folder = "packlets"
    os.makedirs(folder, exist_ok=True)  # Creates folder if missing
    execmeth = execmeth.lower()
    full_path = os.path.join(folder, filename)

    try:
        with open(full_path, 'w') as f:
            f.write(f"$type={shell}\n")
            f.write(f"$excmeth:{execmeth}\n")
            f.write(f"$isudo={'true' if isudo else 'false'}\n\n")
            for cmd in contents:
                f.write(cmd + "\n")
            f.write("---\n")

        print(f"✅ Packlet saved to: {full_path}")

    except Exception as e:
        print(f"❌ Failed to write packlet: {e}")
