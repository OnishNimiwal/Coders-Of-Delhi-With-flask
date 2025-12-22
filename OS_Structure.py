import os

IGNORE = {"venv", ".git", "__pycache__", ".idea", ".vscode"}

print("project-root/")

for item in sorted(os.listdir(".")):
    if item in IGNORE:
        continue

    if os.path.isdir(item):
        print(f"├── {item}/")
        for sub in sorted(os.listdir(item)):
            if sub in IGNORE:
                continue
            print(f"│   └── {sub}")
    else:
        print(f"├── {item}")
