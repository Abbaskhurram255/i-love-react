import os, sys, re
from typing import Callable, Any
from KL_Py import replace
from _translate import translate_for_react, translate_for_css

import subprocess
try:
	subprocess.run([r"pyport\python.exe", r"patch-package-json.py"])
except Exception:
	...

if __name__ == "__main__":
	for root, dirs, files in os.walk("."):
		for filename in files:
			if "pyport" in root:
				continue
			filename = os.path.normpath(
				os.path.join(
					root,
					filename
				)
			)
			if not re.search(r"\.[jt]sx?$", filename) and not re.search(r"\.css$", filename):
				continue
			print(filename)
			with open(filename) as f:
				content: str = f.read()
			if re.search(r"\.[jt]sx$", filename):
				updated_content = translate_for_react(content)
			else:
				print("processing the css...")
				updated_content = translate_for_css(content)
			with open(filename, mode="w") as f:
				f.write(updated_content)