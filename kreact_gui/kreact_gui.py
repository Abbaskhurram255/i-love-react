import FreeSimpleGUI as sg
import os, sys, re, shutil, time
import subprocess
from typing import Final


"""

kreact_gui_8_beta


*the export needs*:

Script:
	./_execute/kreact_gui/kreact_gui.py
	... {there's more}
.py dependencies:
	{{none}}
	...
Image dependencies:
	{as icon} ./_execute/kreact_gui/react.ico
	{as asset} ./_execute/kreact_gui/react.ico
	...
Directories:
	./_execute/kreact_gui/kreact_source
	in /kreact_source
	... {there's more}
Batch dependencies (the most crucial):
	./_execute/kreact_gui/react.bat
	./_execute/kreact_gui/node.bat
	

"""



TITLE: Final[str] = "KReact"
CWD: Final[str] = os.path.normpath(
	os.path.abspath(".")
)

sg.theme("DarkBlue7")

try:
	import ctypes
	app_id = f"com.klang.{TITLE}"
	ctypes\
		.windll\
		.shell32\
		.SetCurrentProcessExplicitAppUserModelID(
			app_id
		)
except Exception:
	...

# assets
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
	FROZEN_ROOT: str = sys._MEIPASS
else:
	FROZEN_ROOT: str = os.path.dirname(
		os.path.abspath(
			__file__
		)
	)
def to_asset(asset_path: str) -> str:
	if not isinstance(asset_path, str):
		return ""
	return os.path.normpath(
		os.path.join(
			FROZEN_ROOT,
			asset_path
		)
	)
# > icon
FAVICON: Final[str] = to_asset("react.ico")
# > batches
REACT_BATCH_FILENAME: Final[str] = to_asset("react.bat")
NODE_BATCH_FILENAME: Final[str] = to_asset("node.bat")
# > directories
SOURCE_DIR: Final[str] = to_asset("kreact_source/")


menu_items: list[list[str | list[str]]] = [
	["&File", ["E&xit"]],
	["E&dit", ["---"]],
	["&Help", ["&About"]]
]

lay: list[list] = [
	[sg.Menu(menu_items)],
	[sg.Text("Please enter the title:", p=(15, (15, 10)))],
	[sg.Push(), sg.Input(key="project-name", tooltip="The name of your project...", text_color="black", background_color="#ccc", p=(15, (10, 20)), enable_events=True), sg.Push()],
	[sg.Text(CWD, key="--destination-label--", tooltip="the path where your project will live...", s=(30, 0), p=(15, (20, 0))), sg.FolderBrowse("Choose", key="project-destination", initial_folder=CWD, tooltip="Choose the path where your project will live", button_color="black on plum")],
	[sg.Push(), sg.Button("Build", key="build-btn", tooltip="Click to build Kreact project here", button_color="white on purple", mouseover_colors="white on #404", s=(9, 2), p=(0, (50, 30)), border_width=4), sg.Push()],
	[sg.Push(), sg.Text("", key="build-status", s=(20, 0), p=(0, (25, 45)), text_color="#bbb", justification="c"), sg.Push()],
	[sg.HSep(color="#000")],
	[sg.Text("Mode:", font="Arial 12")],
	[sg.Push(), sg.Radio("React", key="react-mode", tooltip="Use React (default)?", p=((20, 10), (15, 25)), group_id="modes", default=True), sg.Radio("Typescript", key="tsx-mode", tooltip="Use Typescript?", p=((20, 10), (15, 25)), group_id="modes"), sg.Radio("Node", key="node-mode", tooltip="Use Node?", p=((20, 10), (15, 25)), group_id="modes"), sg.Push()],
	[sg.HSep(color="#000", p=(12, (20, 6)))],
	[sg.Text("Type:", font="Arial 12")],
	[sg.Push(), sg.Radio("New Project", key="type-new", tooltip="Create New\nProject (default)?", p=((20, 10), (15, 25)), group_id="project-types", default=True), sg.Radio("Raw Project", key="type-raw", tooltip="Raw Mode\n(no initialization)?", p=((20, 10), (15, 25)), group_id="project-types"), sg.Push()]
]

app: sg.Window = sg.Window(title=TITLE, icon=FAVICON, layout=lay, margins=(16, 12), element_padding=(12, 6), finalize=True)
app.bind("<Return>", "build-btn")

while True:
	event, values = app.read()
	if event in [sg.WIN_CLOSED, "Exit"]:
		break
	if values is None:
		continue
	if event == "project-name":
		project_name: str = values["project-name"].strip().strip("\\/")
		project_destination: str = values["project-destination"].strip() or CWD
		if re.search(r"(?<=[^\\/])[\\/](?=[^\\/])", project_name):
			parts: list[str] = re.split(r"(?<=[^\\/])[\\/](?=[^\\/])", project_name)
			project_name = parts.pop()
			project_destination = os.path.normpath(os.path.join(project_destination, "\\".join(parts)))
		if not (project_name and project_destination):
			continue
		new_project_path: str = os.path.normpath(os.path.join(project_destination, project_name.strip("\\/")))
		app["--destination-label--"].update(value=new_project_path)
	if event == "build-btn":
		project_name: str = values["project-name"].strip().strip("\\/")
		project_destination: str = values["project-destination"].strip() or CWD
		if re.search(r"(?<=[^\\/])[\\/](?=[^\\/])", project_name):
			parts: list[str] = re.split(r"(?<=[^\\/])[\\/](?=[^\\/])", project_name)
			project_name = parts.pop()
			project_destination = os.path.normpath(os.path.join(project_destination, "\\".join(parts)))
		if not (project_name and project_destination):
			continue
		project_path: str = os.path.normpath(os.path.join(project_destination, project_name.strip("\\/")))
		if not project_path:
			continue
		if not os.path.exists(project_path):
			try:
				os.makedirs(project_path)
			except IOError as e:
				print("Failed to create the project destination folder.")
		system_node_path = None
		pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
		for path_dir in os.environ.get("PATH", "").split(os.pathsep):
			if not path_dir:
				continue
			possible_node_exe = os.path.join(path_dir, "node.exe")
			if os.path.isfile(possible_node_exe):
				system_node_path = possible_node_exe
				break
		if not system_node_path:
			program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
			program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
			possible_paths = [
				os.path.join(program_files, "nodejs", "node.exe"),
				os.path.join(program_files_x86, "nodejs", "node.exe"),
			]
			for p in possible_paths:
				if os.path.isfile(p):
					system_node_path = p
					break
		node_does_not_exist_on_machine: bool = not system_node_path
		if node_does_not_exist_on_machine:
			app["build-status"].update(value="Installing Node...")
			app.refresh()
			node_setup_path: str = os.path.normpath(os.path.join(SOURCE_DIR, "node.msi"))
			try:
				subprocess.run(["msiexec", "/i", node_setup_path], check=True)
				default_node_dir = os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "nodejs")
				if os.path.isfile(os.path.join(default_node_dir, "node.exe")):
					os.environ["PATH"] += os.pathsep + default_node_dir
			except Exception as e:
				print(f"Installation failed or interrupted: {e}")
		new_build_status: str = f"Building project\n'{project_name}'..."
		command: str = f'"{REACT_BATCH_FILENAME}" "{project_destination}" "{project_name}"'
		tsx_mode: bool = values["tsx-mode"]
		node_mode: bool = values["node-mode"]
		raw_mode: bool = values["type-raw"]
		if raw_mode:
			new_build_status = f"Copying raw project\nfiles to existing\nReact/ TS/ Node\nproject\n'{project_name}'..."
			try:
				if not os.path.exists(SOURCE_DIR):
					sg.popup("InternalError: Failed to copy raw files\nto the destination\ndue to some internal malfunction", auto_close=True, auto_close_duration=5)
					app["build-btn"].update(disabled=False)
					app["project-destination"].update(disabled=False)
					continue
				# source
				kreact_exe_path: str = os.path.normpath(os.path.join(SOURCE_DIR, "kreact.exe"))
				scripts_path: str = os.path.normpath(os.path.join(SOURCE_DIR, "scripts"))
				# target
				dest_src_folder: str = os.path.normpath(os.path.join(project_path, "src"))
				dest_src_folder_scripts_path: str = os.path.normpath(os.path.join(dest_src_folder, "scripts"))
				dest_src_folder_node_scripts_path: str = os.path.normpath(os.path.join(dest_src_folder, "node_scripts"))
				dest_src_folder_node_msi_path: str = os.path.normpath(os.path.join(dest_src_folder, "node.msi"))
				if node_mode:
					# if node mode, in raw mode
					scripts_path = os.path.normpath(os.path.join(SOURCE_DIR, "node_scripts"))
				if os.path.exists(kreact_exe_path):
					shutil.copy(kreact_exe_path, project_path)
				if os.path.exists(scripts_path):
					shutil.copytree(scripts_path, project_path, dirs_exist_ok=True)
				shutil.copytree(SOURCE_DIR, dest_src_folder, dirs_exist_ok=True)
				# removing some redundant, leftover files, and folders
				if os.path.exists(dest_src_folder_scripts_path):
					shutil.rmtree(dest_src_folder_scripts_path)
				if os.path.exists(dest_src_folder_node_scripts_path):
					shutil.rmtree(dest_src_folder_node_scripts_path)
				if os.path.exists(dest_src_folder_node_msi_path):
					os.remove(dest_src_folder_node_msi_path)
			except OSError as e:
				sg.popup("Error: Failed to copy raw files to the destination.\nThe destination is non-existent.", title="Error", auto_close=True, auto_close_duration=5, any_key_closes=True)
				continue
		elif tsx_mode:
			command += ' "ts"'
			new_build_status = f"Building TS project\n'{project_name}'..."
		elif node_mode:
			command = f'"{NODE_BATCH_FILENAME}" "{project_destination}" "{project_name}"'
			new_build_status = f"Building Node project\n'{project_name}'..."
		app["--destination-label--"].update(value=project_path)
		app["build-status"].update(value=new_build_status)
		app["build-btn"].update(disabled=True)
		app["project-destination"].update(disabled=True)
		app.refresh()
		if not raw_mode:
			batch_dir = os.path.dirname(os.path.abspath(NODE_BATCH_FILENAME if node_mode else REACT_BATCH_FILENAME))
			subprocess.run(
				command,
				shell=True,
				cwd=batch_dir,
				creationflags=subprocess.CREATE_NEW_CONSOLE
			)
		app["build-btn"].update(disabled=False)
		app["project-destination"].update(disabled=False)
		app["build-status"].update(value="Build complete!")
	if event == "About":
		sg.popup(f"You are using {TITLE}")
app.close()