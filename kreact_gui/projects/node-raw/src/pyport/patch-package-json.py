from typing import Any
import json, os, sys

PACKAGE_JSON_PATH: str = "../package.json"
PACKAGE_JSON_BACKUP_PATH: str = f"{PACKAGE_JSON_PATH}.bak"
KREACT_BATCH_PATH: str = "kreact.bat"
PREFIX: str = f"cd src && {KREACT_BATCH_PATH} && "
SUFFIX: str = " && cd .."
try:
    if not os.path.exists(PACKAGE_JSON_PATH):
        print(f"Error: File '{PACKAGE_JSON_PATH}' not found. Exiting...")
        sys.exit(1)
    if not os.path.exists(KREACT_BATCH_PATH):
        print(f"Warning *: '{KREACT_BATCH_PATH}' is missing. The script will be added anyway.")
    data: dict[str, Any] = {}
    with open(PACKAGE_JSON_PATH, mode="r") as file:
        data = json.load(file)
    with open(PACKAGE_JSON_BACKUP_PATH, mode="w") as file:
        json.dump(data, file, indent=4)
    scripts: dict = data.get("scripts", {})
    if not isinstance(scripts, dict):
        scripts = {}
    current_prebuild: str = scripts.get("prebuild", "").strip(" &")
    if PREFIX.strip() in current_prebuild:
        print("Warning *: Prebuild script already patched. Skipping the update.")
        sys.exit(0)
    new_command: str = ""
    if current_prebuild:
        new_command = f"{PREFIX}{current_prebuild}{SUFFIX}".replace(" &&  && ", " && ")
    else:
        new_command = f"{PREFIX.strip(' &')}{SUFFIX}"
    scripts["prebuild"] = new_command.strip()
    data["scripts"] = scripts
    with open(PACKAGE_JSON_PATH, mode="w") as file:
        json.dump(data, file, indent=4)
    print("update success.")
except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
    print(e)