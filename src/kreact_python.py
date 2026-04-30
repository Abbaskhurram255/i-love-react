import os, sys, re
from typing import Callable, Any
from _translate import translate_for_react, translate_for_css

import subprocess
try:
	subprocess.run([r"pyport\python.exe", r"patch-package-json.py"])
except Exception:
	...

def replace(src: str, to_replace: str|dict|None = None, replacement: str|Callable = "", ignore_case: bool = False, case_insensitive: bool = False, count: int = sys.maxsize) -> str:
	if not src or not isinstance(src, str) or not ((isinstance(to_replace, str)) or (isinstance(to_replace, dict) and not replacement) or isinstance(replacement, (str, Callable))):
		# allow empty replacement for removals
		return ""
	ignore_case = ignore_case or case_insensitive
	if not ignore_case or not isinstance(ignore_case, bool):
		ignore_case = False
	if not isinstance(count, int) or count < 0:
		count = sys.maxsize
	if isinstance(to_replace, str):
		if not len(to_replace):
			return src
		if not re.search(r"[\(\)]", to_replace):
			to_replace = f"({to_replace})"
		to_replace = re.sub(r"(\?)(<\w+>)", r"\1P\2", to_replace)
	if isinstance(replacement, str):
		# if it's a string, rather than a callable---usually in the form of a lambda function
		if re.search(r"[\$\\][&0]", replacement):
			return src
		replacement = re.sub(r"\$\{?(\d+)(\}(?!#{4}))?", r"\\\1", replacement) # the function sees and uses 4 hashes (####) as an escape sequence for a replacement regex group's closing brace
		# achieve JavaScript-like numbered-group convention ^
		replacement = re.sub(r"\$\{?([A-Za-z]\w*)(\}(?!#{4}))?", r"\\g<\1>", replacement) # the function sees and uses 4 hashes (####) as an escape sequence for a replacement regex group's closing brace
		# achieve JavaScript-like named-group convention ^
	flags: int = re.MULTILINE
	if ignore_case:
		flags |= re.IGNORECASE
	result: str = ""
	if not replacement and isinstance(to_replace, dict):
		result = src
		# for now
		for key, value in to_replace.items():
			if not key.strip():
				continue
			result = replace(result, key, value)
		return result
	if not isinstance(to_replace, str):
		to_replace = ""
	try:
		result = re.sub(to_replace, replacement, src, flags=flags, count=count)
	except re.error as e:
		print(f"re.warning:\n  * Bad regex, or replacement pattern. Returning the original source string as-is. *Reason*: {str(e).capitalize()}.")
		result = src
	return result

if __name__ == "__main__":
	for root, dirs, files in os.walk("."):
		for filename in files:
			if not re.search(r"\.jsx?$", filename) and not re.search(r"\.css$", filename):
				continue
			print(filename)
			with open(filename) as f:
				content: str = f.read()
			if re.search(r"\.jsx$", filename):
				updated_content = translate_for_react(content)
			else:
				print("processing the css...")
				updated_content = translate_for_css(content)
			with open(filename, mode="w") as f:
				f.write(updated_content)