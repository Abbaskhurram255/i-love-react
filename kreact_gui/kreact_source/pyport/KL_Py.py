from types import *
from typing import Callable, TypeVar, NewType, Any, Optional, Union, get_origin, Final, Self, Generic, Sequence, Iterable, defaultdict, Counter
from abc import abstractmethod, ABCMeta, ABC as AbstractBaseClass
import functools
from functools import reduce, lru_cache, cache, wraps, partial, partialmethod
from dataclasses import dataclass
# need both math imports for convenience
from numbers import Number
from random import randint as old_randint, uniform as old_randflt
import time as timer
from threading import Timer
from datetime import datetime
from math import *
# need both math imports for convenience
from copy import deepcopy
from pathlib import Path
import builtins, os, sys, io, traceback, time as Time, platform, json, shutil, shlex, signal, site, base64, enum, collections, collections.abc, importlib, functools, cmd, ctypes, stat, math, re, ast, webbrowser, subprocess
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from itertools import product as collective_iter, count
from re import escape
import enum # NOTE: to allow enum.auto without making it global
# both of these imports are needed ^V
from enum import Enum
from inspect import *
argv = ARGV = sys.argv[1:]
date = time = datetime
def either(*args: tuple[Any]) -> bool:
	return any(args)
def xor(*args: tuple[Any]) -> bool:
	return sum(map(bool, args)) == 1
def neither(*args: tuple[Any]) -> bool:
	return not any(args)
OR = NOR = AND = 0
# helpers
def both(*args: tuple[Any]) -> bool:
	return all(args)
def try_else(x: Any, y: Any) -> Any|None:
	try:
		if not x:
			raise Exception()
			# if x does not even exist
			# to begin with,
			# let's just skip to the except block right away
		if callable(x):
			x = x()
			# if callable,
			# replace x with its return value from the function call, if possible
		if isinstance(x, str):
			x = x.strip()
		# let's check, AND SEE if the RETURN VALUE is FALSY
		# if it is, head over to the except block, and return y
		# otherwise, return x, as-is
		if not x:
			raise ValueError()
		return x
	except:
		# upon failure,
		# try the fallback
		if y is not None and callable(y):
			y = y()
			# if callable,
			# replace y with its return value from the function call, if possible
		return y
def collective_range(*lists: list[list]) -> list[int]:
	lists = list(lists)
	# converting the tuples to actual lists
	# as Python varargs (*args)
	# return a tuple (immutable)
	# not a list
	if not lists:
		return []
	lists = [lst for lst in lists if lst is not None and isinstance(lst, list)]
	# filter
	for i, lst in enumerate(lists):
		if not isinstance(lists[i], list):
			continue
		lists[i] = range(len(lists[i]))
	return collective_iter(*lists)
# this is going to be an improved version, a replacement of (random.)randint
# to avoid stack overflow, and cyclic references,
# let's store the old_randint function
from random import randint as old_randint, uniform as old_randflt
def rand_int(x: int = 10, y: int|None = None) -> int:
	"""
	Ek random integer generate karta he range `x` (zaruri), aur `y` (kaabile ignore) ke darmyaan.
	A replacement to random.randint
	@param x				 min (switchable with @param:y)
		:type					 <int>
	@param y				 max (switchable with @param:x)
		:type					 <int, optional>
	@return					 a random int
		:type					 <int>
	"""
	if isinstance(x, float):
		x = int(x)
	if not isinstance(x, int):
		x = 0
	if y is not None:
		if isinstance(y, float):
			y = int(y)
		if not isinstance(y, int):
			y = 10
	if y is None:
		x, y = 0, x
	# with type checks out of the way
	# there shouldn't be a problem
	# if we do:
	x = int(x)
	y = int(y)
	if x == y:
		return x
	if y < x:
		x, y = y, x
	# let's make the make the function exclusive (of y itself)
	result: int = 0
	if y > x:
		result = old_randint(x, y - 1)
	else:
		result = old_randint(y, x - 1)
	return result
randint = koi_darmyan = randbetween = rand_between = randbw = rand_bw = randbelow = rand_below = rand_int
def rand_flt(x: float = 0, y: float|None = None, precision: int|None = None) -> float:
	"""
	A replacement to random.uniform
	@param x				 min (or max if y is None)
		:type					 <float>
	@param y				 max (switchable with @param:x)
		 :type		   		 <float, optional>
	@return					 a random int
	 	:type			   	 <float>
	"""
	if not isinstance(x, (int, float)):
		x = 0
	if y is not None and not isinstance(y, (int, float)):
		y = 1
	x = float(x)
	if y is not None:
		y = float(y)
	if not x and y is None:
		x, y = 0, 1
	if y is None:
		x, y = 0.0, x
	if x == y:
		return x
	if y < x:
		x, y = y, x
	# let's make the make the function exclusive (of y itself)
	if y > 0:
		y -= .1
	else:
		y += .1
	if not precision or not isinstance(precision, int) or precision <= 0:
		precision = 1
	return round(old_randflt(x, y), precision)
randfloat = rand_float = randflt = rand_flt
def choose(iterable: Iterable, n: int|None= None, koi: int|None=None) -> Any|list[Any]:
	if koi is not None and isinstance(koi, int) and not isinstance(n, int):
		n = abs(koi)
	if isinstance(iterable, int) and isinstance(n, Iterable):
		# cross compatibility: if the arguments
		# are in reverse order
		# order them
		n, iterable = iterable, n
	if not isinstance(iterable, Iterable):
		return []
	iterable = list(iterable)
	if not len(iterable):
		return [] if n != 1 else None
	if isinstance(n, int) and n < 0:
		n = abs(n)
	if not n or not isinstance(n, int):
		n = 1
	if n > len(iterable):
		n = len(iterable)
	items: list[Any] = []
	for _ in range(n):
		items.append(iterable[rand_int(len(iterable))])
	if isinstance(iterable, str):
		return "".join(items)
	if n == 1:
		return items[0]
	return items
choice = choices = choose_from = random_from = rand_from = rand_item = rand_items = rand_choice = choose_any = chuno = chuno_koi = koi = choose
def rand_range(start: int = 9, stop: int|None = None) -> list[int]:
	"""
	Generate a list of random integers.
	- If stop is provided, generate a list of length abs(stop) with elements between start and stop (exclusive of stop).
	- If stop is not provided, generate a list of length start with elements between 0 and start (exclusive of start)
	- If nothing is provided, generate a list of 10 elements between 0 and 9 (inclusive).
	@param start: The start of the range (inclusive) or length of list if stop is None.
	@param stop: The end of the range (exclusive).
	@return: A list of random integers.
	"""
	if not isinstance(start, int):
		start = 9
	if stop is None:
		if start == 0:
			return []
		length = abs(start)
		return [rand_int(0, start+1 if start > 0 else start-1) for _ in range(length)]
	else:
		if not isinstance(stop, int):
			stop = 9
		if stop < start:
			start, stop = stop, start
		length = abs(stop)
		if start == stop:
			return [start] * length  # or handle this case differently
		return [rand_int(start, stop) for _ in range(length)]
randrange = rand_range
def rand_str(length: int = 16) -> str:
	if not isinstance(length, int) or length < 8:
		length = 8
	if length > 64:
		length = 64
	chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+=_"
	return_value: str = ""
	for i in range(length):
		return_value += chars[randint(0, len(chars)-1)]
	return return_value
randstr = rand_str
def rand_hex(length: int = 16) -> str:
	if not isinstance(length, int) or length < 8:
		length = 8
	if length > 64:
		length = 64
	chars: str = "0123456789abcdef"
	return_value: str = ""
	while length := length - 1:
		return_value += chars[randint(0, len(chars)-1)]
	return return_value
randhex = rand_hex
def rand_uuid() -> str:
	from uuid import uuid4
	return str(uuid4())
randuuid = rand_uuid
haal = filhal = filhaal = bool
nahi = lambda x: not(x)
line_break = linebreak = LINE_BREAK = LINEBREAK = "\n"
tab = TAB = "\t"
one_dim = two_dim = three_dim = four_dim = five_dim = \
six_dim = seven_dim = eight_dim = nine_dim = ten_dim = list
# recognizes all, just set it to `list`
# besides, the whole point of this
# is to achieve readability;
# will fail with `list|tuple|set`,
# and trust me, it has been tried
# to allow readable list-in-list, tuple-in-tuple types like the following:
# list[two_dim], list[three_dim], tuple[two_dim], tuple[three_dim]
# test:
# x: list[two_dim[int]] = [[1, 3, 5], [2, 4, 6]]
# print(x)
def intersection_of(x: list|dict, y: list|dict) -> list|dict:
	if isinstance(x, tuple):
		x = list(x)
	if isinstance(y, tuple):
		y = list(y)
	if not isinstance(x, (list, dict)) and not isinstance(y, (list, dict)):
		return []
	if all(isinstance(each, list) for each in [x, y]):
		return_val: list[Any] = list(set(x).intersection(y))
		return_val.sort()
		# list.sort returns None
		return return_val
	if all(isinstance(each, dict) for each in [x, y]):
		return dict(x.items() & y.items())
	return []
intersection = intersection_of
class Char(str):
	def __new__(cls, value: Any):
		if value is None:
			return ""
		value = str(value).strip()
		if not len(value):
			return ""
		character: str = value[0]
		return super().__new__(cls, character)
Str = lafz = jumla = lambda x: str(x).strip() # trim the string after parsing
# no one needs additional whitespace
nr = num = Num = Nr = Number
INFINITY = Infinity = infinity = Inf = inf
INT_INFINITY = INTEGER_INFINITY = INTINFINITY = INTEGERINFINITY = IntInfinity = Int_Infinity = int_infinity = intinfinity = int_inf = IntInf = intinf = sys.maxsize
goto = open_link = link_kholo = webbrowser.open
link = webbrowser
_dir = os.getcwd()
# crucial \/
class AbstractMethodsRehteHeError(TypeError):
	def __init__(self, name: str):
		self.name = str(name)
		super().__init__(self.name)
class AbstractBaseClassMeta(ABCMeta):
	def __new__(mcs, name, bases, namespace, **kwargs):
		cls = super().__new__(mcs, name, bases, namespace, **kwargs)
		if ABCMeta in cls.__mro__ and cls.__abstractmethods__:
			return cls
		abstract_methods: set = set()
		for base in bases:
			if isinstance(base, ABCMeta):
				abstract_methods.update(base.__abstractmethods__)
		missing_methods = abstract_methods - set(cls.__dict__)
		for method_name in abstract_methods:
			if not any(method_name in base.__dict__ for base in inspect.getmro(cls)[1:]):
				missing_methods.add(method_name)
		if missing_methods:
			raise AbstractMethodsRehteHeError(
				f"Base class '{name}' ke methods {missing_methods} ko implement karna laazmi he"
			)
		for method_name in abstract_methods:
			if method_name not in cls.__dict__ :
				continue
			subclass_method = cls.__dict__[method_name]
			for base in inspect.getmro(cls)[1:]:
				if method_name not in base.__dict__:
					continue
				base_method = base.__dict__[method_name]
				base_method_type = inspect.signature(base_method)
				subclass_method_type = inspect.signature(subclass_method)
				if base_method_type == subclass_method_type:
					continue
				raise TypeError(
					f"Concrete class '{name}' ke method '{method_name}' ka kism BASE CLASS '{base.__name__}' ke sath match nahi karta"
				)
		return cls
# preserve the sequence
# it MATTERS
def extends_from(_object: Any, target: Any) -> bool:
	"""
	checks if @_object extends from (or isinstance of) @super_class
	DIFFERENT FROM regular `__builtins__.isinstance`
	in the sense that `__builtins__.isinstance` only tells you if an object x
	is strictly of type --- or an "instance" initiated directly from class --- y
	@param		_object
	::type		Any/type type (class)
	::desc		an object or a class to test if it extends from (or at least belongs to) class @target
	@param		target
	::type		Any/type type (class)
	::desc		the target class
	@return
	::type		bool
	::desc		returns True if @_object extends from @target

	Reads like: 'If X extends_from Y', or 'If X belongs_to Y'
	Handles both instances (isinstance), and classes (issubclass).
	"""
	if isinstance(target, (list, tuple, UnionType)):
		sub_targets: list[Any] = target.__args__ if isinstance(target, UnionType) else target
		return any(extends_from(_object, sub_target) for sub_target in sub_targets)
	if isinstance(_object, (list, tuple, set)) and not isinstance(_object, (str, bytes)):
		if len(_object) == 0:
			return False
		return all(extends_from(item, target) for item in _object)
	# kill int-on-bool, bool-on-int false-positive checks
	if target is int and isinstance(_object, bool):
		return False
	if target is int and _object is bool:
		return False
	if isinstance(_object, type) or hasattr(_object, "__origin__"):
		try:
			# Handle Generic Aliases like list[int] which issubclass() can reject
			_object = get_origin(_object) or _object
			target = get_origin(target) or target
			return issubclass(_object, target)
		except TypeError:
			return False
	# if _object is an object, check if it's an instance of target
	try:
		return isinstance(_object, target)
	except TypeError:
		return False
belongs_to = he_sub_class = sub_class_he = he_kism = extends_from
# ^^much needed
def kism(x: Any) -> type:
	return type(get_origin(x) or x)
is_type = istype = isinstance
# preserve the sequence
# it MATTERS
def hissa(item: Any|type, container: Any|type|Iterable, _seen: Optional[set[int]] = None) -> bool:
	try:
		if _seen is None:
			_seen = set()
		container_id = id(container)
		if container_id in _seen:
			return False  # Already checked this exact container
		_seen.add(container_id)
		if isinstance(item, str) and isinstance(container, str):
			return match_i(container, item)
			# NOTE: keep the order like this
			# has to be called in reverse
			# the parameters of this function are
			# in reverse for readability
		item_is_type_type: bool = isinstance(item, type) or hasattr(item, "__origin__")
		container_is_type_type: bool = isinstance(container, type) or hasattr(container, "__origin__")
		if item_is_type_type and container_is_type_type:
			return extends_from(container, item)
		if isinstance(container, (list, tuple, set, collections.abc.Iterable)):
			if item_is_type_type:
				return any(extends_from(parent, item) for parent in container if isinstance(parent, type) or hasattr(parent, "__origin__"))
			try:
				# direct membership check first (fast)
				if item in container:
					return True
			except TypeError:
				pass
			for element in container:
				if isinstance(element, (list, tuple, set, dict)):
					if hissa(item, element, _seen=_seen):
						return True
				elif item == element:
					return True
		return item == container
	except (TypeError, ValueError, AttributeError):
		return False
# preserve the sequence
# it MATTERS
def isinstance_each(collection: Any, target: Any) -> bool:
	"""
	WARNING:
	this is DIFFERENT from `__builtins__.isinstance`
	HERE'S HOW: it shortens multiple isinstance checks into one
	WHERE y is the type to compare each item in x with.
	So, unlike the original...
	this one won't return True for
	`isinstance([1, 2], list)`
	unlike the original!
	INSTEAD:
	this one checks if every item from the @collection on the left
	matches the type of the @target
	Here is what it WILL return True for:
		isinstance_each([1, 2], int) // output: True
		isinstance_each([1.2, 2.1], float) // output: True
		isinstance_each([1.2, 2], float) // output: False, since 2 is an int

	:: Checks if every item in @collection belongs_to @target.
	:: Returns False if the collection is empty.
	:: Also works with classes: isinstance_each([ValueError, TypeError], Exception) returns True
	"""
	if not isinstance(collection, (list, tuple, set)):
		return False
	return extends_from(collection, target)
each_isinstance = each_is_instance = is_instance_each = isinstance_each
def safe_get(
	data: Any, 
	path: str | list | tuple, 
	default: Any = None, 
	target_type: Any = object,
	ignore_case: bool = True,
	use_regex: bool = False,
	auto_flatten: bool = False,
	on_match: Optional[Callable[[Any], Any]] = None,
	deep_search: bool = True,
	max_depth: int = 20,
	_seen: Optional[set[int]] = None
) -> Any:
	if _seen is None: _seen = set()
	if max_depth < 0: return default
	if isinstance(path, (list, tuple)) and not deep_search:
		if len(path) > 0 and any(isinstance(p, (str, list, tuple)) for p in path):
			is_multi = any('.' in p if isinstance(p, str) else True for p in path)
			if is_multi:
				return [safe_get(data, p, default, target_type, ignore_case, use_regex, auto_flatten, on_match, deep_search, max_depth, _seen.copy()) for p in path]
	if isinstance(data, (list, tuple, dict, set)):
		if id(data) in _seen: return default
		_seen.add(id(data))
	def _run_finalize(val):
		if auto_flatten:
			def _gen_flatten(items):
				if isinstance(items, (list, tuple, set)):
					for item in items: yield from _gen_flatten(item)
				else: yield items
			val = list(_gen_flatten(val))
		if on_match and val is not default:
			try:
				val = [on_match(i) for i in val] if auto_flatten else on_match(val)
			except: return default
		if val is not None and target_type is not object:
			if auto_flatten:
				if not isinstance_each(val, target_type): return default
			else:
				if not extends_from(val, target_type): return default
		return val
	def _find_key(d, k):
		if use_regex:
			p = re.compile(str(k), re.IGNORECASE if ignore_case else 0)
			for existing_key in d:
				if p.search(str(existing_key)): return d[existing_key]
		elif ignore_case:
			k_map = {str(key).lower(): key for key in d.keys()}
			look = k_map.get(str(k).lower())
			if look is not None: return d[look]
		return d.get(k)
	if deep_search:
		target_key = path if isinstance(path, (list, tuple)) else str(path)
		if isinstance(data, dict):
			found = _find_key(data, target_key)
			if found is not None: return _run_finalize(found)
			for v in data.values():
				res = safe_get(v, path, default, target_type, ignore_case, use_regex, auto_flatten, on_match, True, max_depth - 1, _seen)
				if res is not default: return res
		elif isinstance(data, (list, tuple)):
			for item in data:
				res = safe_get(item, path, default, target_type, ignore_case, use_regex, auto_flatten, on_match, True, max_depth - 1, _seen)
				if res is not default: return res
		return default
	segments = path.split('.') if isinstance(path, str) else path
	current = data
	for key in segments:
		if current is None: return default
		try:
			if isinstance(current, dict):
				current = _find_key(current, key)
			elif isinstance(current, (list, tuple)):
				current = current[int(key)]
			elif hasattr(current, str(key)):
				current = getattr(current, str(key), default)
			else: return default
		except: return default
		if current is default or current is None: return default
	return _run_finalize(current)
deep_get = safe_get
autoclass = auto_class = dataclass
def auto_id(_cls=None, start: int = 1000, field: str = "__id__"):
	if not isinstance(start, int):
		start = 1000
	if not isinstance(field, str):
		field = "__id__"
	def decorator(cls):
		counters: dict[str, int] = {
			field: count(start),
			"__shanakht__": count(start)
		}
		original_init = cls.__init__
		@wraps(original_init)
		def new_init(self, *args, **kwargs):
			setattr(self, field, next(counters[field]))
			setattr(self, "__shanakht__", next(counters["__shanakht__"]))
			original_init(self, *args, **kwargs)
		cls.__init__ = new_init
		return cls
	if _cls is None:
		return decorator
	return decorator(_cls)
serialize = autoid = auto_id
______auto_variable_count_helper______: dict = {}
class AutoField:
	def __init__(self, start: int = 0, key:str|None=None, increment: bool=True):
		self.start = 0 if not isinstance(start, int) else start
		self.key = object() if key is None else key
		self.increment = increment
		______auto_variable_count_helper______[self.key] = start
	def __get__(self, instance, owner):
		if instance is None:
			return self
		key = (id(instance), self.key)
		if key not in ______auto_variable_count_helper______: ______auto_variable_count_helper______[key] = self.start
		value = ______auto_variable_count_helper______[key]
		if self.increment:
			______auto_variable_count_helper______[key] += 1
		else: ______auto_variable_count_helper______[key] -= 1
		return value
	def __call__(self):
		value = ______auto_variable_count_helper______[self.key]
		if self.increment:
			______auto_variable_count_helper______[self.key] += 1
		else: ______auto_variable_count_helper______[self.key] -= 1
		return value
def auto_inc(start: int = 0):
	if not isinstance(start, int):
		start = 0
	return AutoField(start=start)
def auto_dec(start: int = 0):
	if not isinstance(start, int):
		start = 0
	return AutoField(start, increment=False)
typename = TypeT = typeT = TypeVar("T")
def run_process(command: str|list[str], new_window: bool = False, timeout: int = int(9e9), **kwargs) -> bool:
	if not isinstance(timeout, int):
		timeout = int(9e9)
		# IntInfinity fails here, using a fallback value^^
	if not command or not isinstance(command, (str, list, tuple)):
		return False
	if isinstance(command, tuple):
		command = list(command)
	if isinstance(command, str):
		command = shlex.split(command, posix=(os.name != 'nt'))
	if (not new_window or not isinstance(new_window, bool)) and len(kwargs) > 0:
		new_window = any(kwargs.pop(k, False) for k in ["dont_block", "non_blocking"])
	kwargs["shell"] = is_shell = any(kwargs.pop(k, False) for k in ['cmd', 'internal', 'shell'])
	if is_shell and isinstance(command, list):
		command = " ".join([f'"{arg}"' if " " in arg else arg for arg in command])
	if os.name == 'nt':
		kwargs['creationflags'] = kwargs.get('creationflags', 0) | subprocess.CREATE_NEW_PROCESS_GROUP
	capture_output: bool = kwargs.pop("capture_output", False)
	print_output: bool = kwargs.pop("print_output", False)
	as_text: bool = kwargs.get("text", False)
	if print_output:
		capture_output, as_text = True, True
	kwargs["text"] = as_text
	return_code: int = 1
	empty_buf: str|bytes = "" if as_text else b""
	stdout, stderr = empty_buf, empty_buf
	try:
		if new_window:
			stdout_pipe = subprocess.PIPE if capture_output else None
			stderr_pipe = subprocess.PIPE if capture_output else None
			non_blocking_process: subprocess.Popen = subprocess.Popen(command, stdout=stdout_pipe, stderr=stderr_pipe, **kwargs)
			if not capture_output:
				return True
			try:
				stdout, stderr = non_blocking_process.communicate(timeout=timeout)
				return_code = non_blocking_process.returncode
			except subprocess.TimeoutExpired:
				if os.name == WINDOWS:
					non_blocking_process.send_signal(signal.CTRL_BREAK_EVENT)
				else:
					non_blocking_process.kill()
				stdout, stderr = non_blocking_process.communicate()
		else:
			try:
				process: subprocess.CompletedProcess = subprocess.run(command, capture_output=capture_output, timeout=timeout, **kwargs)
				return_code = process.returncode
				if not capture_output:
					return True if return_code == 0 else False
				stdout, stderr = process.stdout, process.stderr
			except subprocess.TimeoutExpired as e:
				stdout, stderr = e.stdout or empty_buf, e.stderr or empty_buf
		command_output = stdout if return_code == 0 else stderr
		if command_output:
			msg = command_output.decode(errors='replace') if isinstance(command_output, bytes) else str(command_output)
			if msg.strip():
				print(msg.strip())
		return True if return_code == 0 else False
	except Exception as e:
		print(f"Process failed to run: {e}")
		return False
run_command = execute_command = execute_process = run_process
def kill_process(process_name: str) -> bool:
	process_name: str = str(process_name).strip()
	killed: bool = False
	if not process_name:
		return False
	opsys: str = platform.system().lower()
	try:
		if opsys == "windows" or os.name == "nt":
			if not process_name.lower().endswith(".exe"):
				process_name += ".exe"
				# need this
			run_process(f"taskkill /f /im {process_name}")
		else:
			run_process(f"pkill -f {process_name}")
		killed = True
	except:
		killed = False
	return killed
kill_application = kill_app = kill_process
def Int(x: str|int|float, base: int = 10) -> int:
	try:
		if x is None or not isinstance(x, (str, int, float, bool)):
			return 0
		if isinstance(x, bool):
			return 1 if x else 0
		if not base or not isinstance(base, int) or base <= 0 or base >= Infinity:
			base = 10
		x = str(x).strip()
		x = replace(x, r"[^\-\.\d]", "")
		# NOTE: keep the dot(.), it's needed for now. keep. the. dot.
		# ^ allow the dot(.) to pass through, for now, so that 23.5 does NOT become 253
		if "." in x and len(x) >= 2:
			# and later, remove it gracefully
			x = x.split(".")[0]
		return int(x, base)
	except (ValueError, TypeError):
		return 0
def Flt(x: str|int|float) -> float:
	try:
		if x is None or not isinstance(x, (str, int, float, bool)):
			return 0.0
		if isinstance(x, bool):
			return 1.0 if x else 0.0
		if isinstance(x, str):
			x = replace(x.strip(), r"[^e\+\-\.\d]", "")
		return float(x)
	except (ValueError, TypeError):
		return 0.0
def is_pos(n: int|float) -> bool:
	"""agar number ek positive number he to kehta he `Han`,
	warna `Nahi`"""
	if not n or not isinstance(n, (int, float)):
		return False
	return n > 0
he_positive = he_pos = is_pos
def is_neg(n: int|float) -> bool:
	"""agar number ek negative number he to kehta he `Han`,
	warna `Nahi`"""
	if not n or not isinstance(n, (int, float)):
		return False
	return n < 0
he_negative = he_neg = is_neg
def is_even(n: int) -> bool:
	"""agar number ek even number he to kehta he `Han`,
	warna `Nahi`"""
	if not isinstance(n, int):
		return False
	# allow zero to pass through
	# might not seem like it,
	# but it does have the quality OF being even,
	# or odd, it even... though
	return n % 2 == 0
he_even = is_even
def is_odd(n: int) -> bool:
	"""agar number ek odd number he to kehta he `Han`,
	warna `Nahi`"""
	if not isinstance(n, int):
		return False
	# allow zero to pass through
	# might not seem like it,
	# but it does have the quality OF being even,
	# or odd, it's not odd though
	return n % 2 != 0
he_odd = is_odd
Function = Fc = Pukarne_Layak = Callable
def delay(n: int, fn: Callable) -> None:
	"""
	kism<nr> `n` seconds baad kisi operation ko perform karne ke lie
	@param
			  n							   kism<int | float>
			  the delay in seconds
	@param fn
			  fn							  kism<Pukarne_Layak / Function>
			  the function to be executed after the delay
	@return_type
			  kism<KoiNa|NoneType>
			  operation perform karke koi value return nahi karta (koi_na|None)
	"""
	if not isinstance(n, (int, float)) or n <= 0:
		n = 1
	MAX_DELAY: int = int(1e5)
	if n > MAX_DELAY:
		n = MAX_DELAY
	# good practice
	if not isinstance(fn, Callable):
		return
	timed_fn: Timer = Timer(n, fn)
	timed_fn.start()
sec, mint = 1, 60
# helpers contants
# so we can do delay(5*min, lambda: doSomeThing())
# again, helper constants
after = baad = delay
def blocking_sleep(s: Number = 5) -> None:
	if not isinstance(s, Number):
		return
	from time import sleep
	sleep(s)
wait = rukawat = rukaawat = blocking_sleep
def th(n: Number) -> str:
	if not isinstance(n, Number):
		return "0th"
	n = abs(int(n))
	if 10 <= n % 100 <= 20:
		suffix = "th"
	else:
		suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
	return str(n) + suffix
def fus(amount: Number) -> str:
	if amount is None or not isinstance(amount, Number):
		return ""
	amount = round(amount, 1)
	parts = str(amount).split('.')
	integer_part = '{:,}'.format(int(parts[0]))
	decimal_part = f".{parts[1]}" if len(parts) > 1 else ''
	return f"{integer_part}{decimal_part}"
def fpk(amount: Number) -> str:
	if amount is None or not isinstance(amount, Number):
		return ""
	amount = round(amount, 1)
	parts = str(amount).split('.')
	# Indian formatting for integer part
	integer_part = parts[0]
	if len(integer_part) > 3:
		last_three = integer_part[-3:]
		rest = integer_part[:-3]
		rest = ','.join(reversed([rest[max(0, i-2):i] for i in range(len(rest), 0, -2)]))
		integer_part = f"{rest},{last_three}" if rest else last_three
	decimal_part = f".{parts[1]}" if len(parts) > 1 else ''
	format: str = f"{integer_part}{decimal_part}"
	# fixing a bug...
	result: str = format.replace("-,", "-")
	return result
athwa: float = 0.125
chotha: float = 0.25
adha: float = 0.5
dedh: float = 1.5
dhai: float = 2.5
tin: int = 3
chaar: int = 4
ath: int = 8
aath = ath
def number_list_validator(args: tuple[Any]):
	args = list(args)
	if len(args) == 1 and isinstance(args[0], (list, tuple)):
		args = list(args[0])
	if not all(isinstance(arg, (int, float)) for arg in args):
		return []
	return args
def mean(*args: tuple[int | float]) -> float:
	args = number_list_validator(args)
	if not args:
		return 0.0
	return float(sum(args) / len(args))
avg = average = math.avg = math.average = math.mean = mean
def median(*args: tuple[int | float]) -> float:
	args = number_list_validator(args)
	if not args:
		return 0.0
	args = sorted(args)
	mid_of_length: int = len(args) // 2
	if len(args) % 2 != 0:
		return float(args[mid_of_length])
	first_middle: int | float = args[mid_of_length - 1]
	second_middle: int | float = args[mid_of_length]
	return float((first_middle + second_middle) / 2)
math.find_middle = math.middle_number = math.find_median = math.median = median
def arithmode(*args: tuple[int | float]) -> float:
	args = number_list_validator(args)
	if not args:
		return 0.0
	most_frequent_number: int | float = Counter(args).most_common(1)[0][0]
	return float(most_frequent_number)
math.frequent = math.most_frequent = math.mode = frequent = most_frequent = arith_mode = arithmode
def arithrange(*args: tuple[int | float]) -> float:
	args = number_list_validator(args)
	if not args:
		return 0.0
	return float(max(args) - min(args))
math.arith_range = math.arithrange = arith_range = arithrange
def IntInput(*args, **kwargs):
	try:
		return Int(input(*args, **kwargs))
	except Exception:
		return 0
def FltInput(*args, **kwargs):
	try:
		return Flt(input(*args, **kwargs))
	except Exception:
		return 0
intInput, fltInput = IntInput, FltInput
def flattened(lst: list[Any]) -> list[Any]:
	if lst is None or not isinstance(lst, list):
		return []
	out: list[Any] = []
	for item in lst:
		if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
			out.extend(flattened(item))
		else:
			out.append(item)
	return out
flat = flatten = flattened
def clone(item: list|tuple|dict) -> list|tuple|dict:
	if item is None:
		return None
	return deepcopy(item)
	"""
	__KL_Py.deepcopy__
	
	@param	   item
	  @@type	 (list, tuple, dict)
						:: object to clone
	@return		
	   @@type	(list, tuple, dict)
						:: a cloned object
						   depending on
						   the type passed
						   in as the argument
	"""
def lambai(x: Iterable) -> int:
	if not isinstance(x, Iterable):
		return 0
	return len(x)
def barabar(x, y) -> haal:
	if isinstance(x, str) and isinstance(y, str):
		return x.lower() == y.lower()
	return x == y
def he(x: Any, y: Any = None) -> bool:
	"""
	stricter he
	ONLY EXISTS TO BOOST READABILITY
	IN HINDGUI-ONLY (non-Klang) PROJECTS
	different from `barabar`
	which uses case-insensitivity for strings
	"""
	if x is not None and y is None:
		return bool(x)
	return x == y
mojud = bool
def yato(x, y) -> bool:
	return x or y
def collect(x, *rest) -> list[list[Any], list[Any]]:
	if not x or not rest or len(rest) == 0 or not is_iterable(x) or not all(isinstance(item, Iterable) for item in [x, *rest]):
		return [[], []]
	args: list = [x, *rest]
	return list(zip(args))
# wraps the old enumerate function
# to avoid stack overflow
# we'll need this
ikhatte = collect
old_enumerate = builtins.enumerate
def numbered(x: str|list|tuple|dict, *args, **kwargs) -> list[list[Any], list[int]]:
	if not x or not isinstance(x, (str, list, tuple, dict)):
		return []
	kwargs["start"] = kwargs.pop("shuru", kwargs.pop("start", 0))
	enumeration_object: old_enumerate = old_enumerate(x, *args, **kwargs)
	if not enumeration_object:
		return []
	lst: list = list(enumeration_object)
	if not lst:
		return []
	return [(v, i) for i, v in lst]
	# WARNING: the `old_enumerate` part
	# is supposed to be AS/IS
	# this function overrides
	# the old enumerate function
	# for Klang
	# and replaces it with numbered
	# also, the swapping is a mandatory step
	# allowing the following syntax:
	#	for item, i in numbered(arr):
	#		print("{i}. {item}")
enumer = numbered
__old_list__ = builtins.list
class Arr(__old_list__):
	current_type = Any
	length_is_final: bool = False
	def __init__(self, *objs, fixed: bool = False):
		objs = flattened(__old_list__(objs))
		if len(objs) > 0 and objs[0] is not None and objs[0] is not Iterable:
			self.current_type = type(objs[0])
		super().__init__()
		self.push(objs)
		filtered_lst: list = []
		if self.current_type is not Any:
			for item in self:
				if isinstance(item, Number) and not isinstance(item, bool) and self.current_type == str:
					item = Str(item)
				if re.search(r"\d|\b(?:True|False)\b", str(item)) and isinstance(item, (str, int, float, bool)) and self.current_type in [int, float]:
					if self.current_type == int:
						item = Int(item)
					else:
						item = Flt(item)
					# ^ WARNING (change not needed): refers to `Int` instead of
					# builtin `int`
					# FOR A REASON:
					# forced int-ification (if possible)
					# applying the type filter on items
				if type(item) != self.current_type:
					continue
				filtered_lst.append(item)
		self.clear()
		self[:] = filtered_lst
		if fixed:
			self.length_is_final = True
	def filter_out(self, fn):
		if not callable(fn):
			return self
		self[:] = [x for x in self if not fn(x)]
		return self
	def keep_if(self, fn):
		if not callable(fn):
			return self
		self[:] = [x for x in self if fn(x)]
		return self
	def map(self, fn):
		if not callable(fn):
			return self
		self[:] = [fn(x) for x in self]
		return self
	def unique(self):
		self[:] = __old_list__(dict.fromkeys(self))
		return self
	def has(self, x):
		return x in self
	def includes(self, x):
		return self.has(x)
	def i(self, i, default=None):
		if not isinstance(i, int):
			return self
		if i < 0:
			i = len(self) + i
		if 0 <= i < len(self):
			return self[i]
		return default
	def last(self):
		if self:
			return self[-1]
		return self
	def last_i(self, n: int = 1):
		if not isinstance(n, int):
			return self
		if n > 0 and n <= len(self):
			return self[-n]
		return self
	def nth(self, n):
		return self.i(n)
	def nth_last(self, n):
		return self.last_i(n)
	def first(self):
		if self:
			return self[0]
		return None
	def second(self):
		return self.i(1)
	def sec_last(self):
		return self.last_i(2)
	def update(self, i, x):
		if not isinstance(i, int):
			return self
		if i < 0:
			i = len(self) + i
		if 0 <= i < len(self):
			self[i] = x
		return self
	def replace(self, i, x):
		return self.update(i, x)
	def shuffle(self):
		import random
		if len(self) > 1:
			random.shuffle(self)
		return self
	def sort(self, key=None, reverse=False):
		if len(self) > 1:
			super().sort(key=key, reverse=reverse)
		return self
	def reverse(self):
		if len(self) > 1:
			super().reverse()
		return self
	def key_array(self):
		return __old_list__(range(len(self)))
	def keys(self):
		return self.key_array()
	def values(self):
		return __old_list__(self)
	def entries(self):
		return [self.keys(), self.values()]
	def slice(self, start: int = None, end: int = None):
		if not isinstance(start, int) or not isinstance(end, int) or start >= len(self) or end > len(self) or start == end:
			return self[:]
		return Arr(self[start:end])
	def slice_keep(self, x):
		if not isinstance(x, int) or x <= len(self) or x > len(self):
			return self.copy()
		return self.slice(0, x)
	def slice_right(self, x):
		if not isinstance(x, int):
			return self.copy()
		return self.slice(len(self) - x)
	def slice_end(self, x):
		if not isinstance(x, int):
			return self.copy()
		return self.slice(0, len(self) - x)
	def random(self):
		import random
		if self:
			return random.choice(self)
		return None
	def empty(self) -> Self:
		self.clear()
		return self
	def eq(self, other):
		if not isinstance(other, __old_list__):
			return False
		return self == other
	def compare(self, other):
		if not isinstance(other, __old_list__):
			return False
		intersection = Arr(set(self) & set(other))
		return len(intersection) > len(self) / 2
	def union(self, *arrays):
		return self.combine(*arrays)
	def cat(self, *arrays):
		return self.combine(*arrays)
	def concat(self, *arrays):
		return self.combine(*arrays)
	def join(self, *arrays):
		return self.combine(*arrays)
	def join_str(self, s: str = ""):
		return str(s).join(map(str, self))
	def intersection(self, *arrays):
		for arr in arrays:
			if isinstance(arr, __old_list__):
				self[:] = [x for x in self if x in arr]
			elif isinstance(arr, Arr):
				self[:] = [x for x in self if x in arr]
		return self
	def negative_intersection(self, *arrays):
		for arr in arrays:
			if isinstance(arr, __old_list__):
				self[:] = [x for x in self if x not in arr]
			elif isinstance(arr, Arr):
				self[:] = [x for x in self if x not in arr]
		return self
	def map_val(self, old_val, new_val) -> Self:
		for i, x in enumerate(self):
			if x == old_val:
				self[i] = new_val
		return self
	def sum(self) -> Number:
		if not len(self):
			return 0.0
		nums: __old_list__[Number] = [num for num in self if num is not None and isinstance(num, Number)]
		# this is a necessary check
		if not len(nums):
			return 0.0
		return sum(nums)
	def difference(self) -> Number:
		if not len(self):
			return 0.0
		nums: __old_list__[Number] = [num for num in self if num is not None and isinstance(num, Number)]
		# this is a necessary check
		if not len(nums):
			return 0.0
		diff: Number = nums[0]
		for i, item in old_enumerate(nums):
			if i == 0:
				continue
			# since we've already taken care of the first item
			# we don't that
			if item > 1e9:
				item = 1e9
			if item < 1e-9:
				item = 1e-9
			diff -= item
		return diff
	diff = difference
	def product(self) -> Number:
		if not len(self):
			return 0.0
		nums: __old_list__[Number] = [num for num in self if num is not None and isinstance(num, Number)]
		# this is a necessary check
		if not len(nums):
			return 0.0
		prd: Number = nums[0]
		for i, item in old_enumerate(nums):
			if i == 0:
				continue
			# since we've already taken care of the first item
			# we don't that
			if item > 1e9:
				item = 1e9
			if item < 1e-9:
				item = 1e-9
			prd *= item
		return prd
	prd = product
	def quotient(self) -> Number:
		if not len(self):
			return 0.0
		nums: __old_list__[Number] = [num for num in self if num is not None and isinstance(num, Number)]
		# this is a necessary check
		if not len(nums):
			return 0.0
		quo: Number = nums[0]
		for i, item in old_enumerate(nums):
			if i == 0:
				continue
			# since we've already taken care of the first item
			# we don't that
			if item == 0:
				item = 1
			if item > 1e9:
				item = 1e9
			if item < 1e-9:
				item = 1e-9
			quo /= item
		return quo
	quo = quotient
	def max(self) -> Number:
		if not len(self):
			return 0.0
		nums: __old_list__[Number] = [num for num in self if num is not None and isinstance(num, Number)]
		# this is a necessary check
		if not len(nums):
			return 0.0
		return max(nums)
	def min(self) -> Number:
		if not len(self):
			return 0.0
		nums: __old_list__[Number] = [num for num in self if num is not None and isinstance(num, Number)]
		# this is a necessary check
		if not len(nums):
			return 0.0
		return min(nums)
	def combine(self, *args) -> Self:
		if self.length_is_final:
			return self
		if not args:
			return self
		for arg in args:
			if isinstance(arg, tuple):
				arg = __old_list__(arg)
				# a tuple?
				# no thanks,
				# we need a list
			if isinstance(arg, __old_list__):
				arg = flatten(arg)
				self.extend(arg)
				return self
			else:
				if self.current_type is not Any:
					if isinstance(arg, Number) and not isinstance(arg, bool) and self.current_type == str:
						item = Str(arg)
					if re.search(r"\d|\b(?:True|False)\b", str(arg)) and isinstance(arg, (str, int, float, bool)) and self.current_type in [int, float]:
						if self.current_type == int:
							arg = Int(arg)
						else:
							arg = Flt(arg)
						# ^ WARNING (change not needed): refers to `Int` instead of
						# builtin `int`
						# FOR A REASON:
						# forced int-ification (if possible)
					if type(arg) != self.current_type:
						continue
				self.append(arg)
		return self
	add = push = me_dalo = combine
	def push_at(self, i: int, *items) -> Self:
		if self.length_is_final:
			return self
		if not len(items):
			return self
		if not isinstance(i, int):
			i = len(self)
		if i < 0:
			i = 0
		elif i > len(self):
			i = len(self)
		#items = flatten(__old_list__(items))
		items = list(items)
		if self.current_type is not Any:
			for i, item in enumerate(items):
				if isinstance(items[i], Number) and not isinstance(items[i], bool) and self.current_type == str:
					items[i] = Str(item)
				if re.search(r"\d|\b(?:True|False)\b", str(items[i])) and isinstance(items[i], (str, int, float, bool)) and self.current_type in [int, float]:
					if self.current_type == int:
						items[i] = Int(item)
					else:
						items[i] = Flt(item)
					# ^ WARNING (change not needed): refers to `Int` instead of
					# builtin `int`
					# FOR A REASON:
					# forced int-ification (if possible)
					# applying the type filter on items
				if type(items[i]) != self.current_type:
					items.pop(i)
		x = self[:i] + items + self[i+len(items)-1:]
		updated_list: __old_list__ = __old_list__(x)
		self.clear()
		self.extend(updated_list)
		return self
	def push_start(self, *items) -> Self:
		self.push_at(0, *items)
		return self
	pehla_dalo = ke_pehle_dalo = unshift = push_start
	def shift(self) -> Any|None:
		if self.length_is_final:
			return None
		if len(self) == 0:
			return None
		return self.pop(0)
		# pop the first item, "shift"ing all to the left by one bit
	pehla_nikalo = shift
	# OVERRIDE self.remove
	old_remove = __old_list__.remove
	def remove(self, *items) -> Any|None:
		if self.length_is_final:
			return None
		if not len(self):
			return None
		if not len(items):
			return super().pop()
		items = flatten(__old_list__(items))
		last_removed: Any = items[-1]
		for item in items:
			if not self.contains(item):
				continue
			self.old_remove(item)
		return last_removed
	rmv = se_nikalo = mese_nikalo = remove
	# OVERRIDE self.pop
	old_pop = __old_list__.pop
	def pop(self, *items) -> Any|None:
		if self.length_is_final:
			return None
		if not len(self):
			return None
		if not len(items):
			return super().pop()
		items = flatten(__old_list__(items))
		last_popped: Any = self.old_pop(items[-1])
		for index in items:
			if index >= len(self):
				continue
			if index < 0:
				index = len(self) - abs(index)
				if index < 0 or index >= len(self):
					continue
			self.old_pop(index)
		return last_popped
	def contains(self, item) -> bool:
		return self.count(item) > 0
	has = includes = me_shamil = me_mojud = contains
	def index_of(self, x: Any) -> int:
		if not self.contains(x):
			return -1
		return self.index(x)
	find = find_index = index_of
	no_of = counts_of = __old_list__.count
	def print_map(self):
		print(self)
	def length(self):
		return len(self)
class numlist(list[Number]):
	def __init__(self, *items: Number|list[Number]):
		super().__init__()
		self.push(*items)
	def __add__(self, other: Number|list[Number]) -> Self:
		if isinstance(other, list):
			lst: numlist = numlist()
			for a, b in zip(self, other):
				lst.append(a+b)
			return lst
		if isinstance(other, Number):
			self.append(other)
		return self
	def __radd__(self, other: Number|list[Number]) -> Self:
		if isinstance(other, list):
			lst: numlist = numlist()
			for a, b in zip(self, other):
				lst.append(b+a)
			return lst
		if isinstance(other, Number):
			self.insert(0, other)
		return self
	def __sub__(self, other: list[Number]) -> Self:
		lst: numlist = numlist()
		for a, b in zip(self, other):
			lst.append(a-b)
		return lst
	def __rsub__(self, other: list[Number]) -> Self:
		lst: numlist = numlist()
		for a, b in zip(self, other):
			lst.append(b-a)
		return lst
	def __mul__(self, other: list[Number]) -> Self:
		lst: numlist = numlist()
		for a, b in zip(self, other):
			lst.append(a*b)
		return lst
	def __truediv__(self, other: list[Number]) -> Self:
		lst: numlist = numlist()
		for a, b in zip(self, other):
			if b == 0:
				b = 1
			lst.append(a/b)
		return lst
	def __pos__(self) -> Self:
		return numlist(+x for x in self)
	def __neg__(self) -> Self:
		return numlist(-x for x in self)
	def __abs__(self) -> Self:
		return numlist(abs(x) for x in self)
	def __pow__(self, other: list[Number]) -> Self:
		lst: numlist = numlist()
		for a, b in zip(self, other):
			if b == 0:
				b = 1
			lst.append(a ** b)
		return lst
	def __gt__(self, other: list[Number]) -> bool:
		return all(a > b for a, b in zip(self, other))
	def __lt__(self, other: list[Number]) -> bool:
		return all(a < b for a, b in zip(self, other))
	def __ge__(self, other: list[Number]) -> bool:
		return all(a >= b for a, b in zip(self, other))
	def __le__(self, other: list[Number]) -> bool:
		return all(a <= b for a, b in zip(self, other))
	def __eq__(self, other: list[Number]) -> bool:
		return all(a == b for a, b in zip(self, other))
	def __ne__(self, other: list[Number]) -> bool:
		return not all(a == b for a, b in zip(self, other))
	def __str__(self) -> str:
		return f"numlist([{', '.join(map(str, self))}])"
	def __repr__(self) -> str:
		return f"numlist([{', '.join(map(repr, self))}])"
	def sum(self) -> Number:
		if not len(self):
			return 0
		return sum(self)
	def difference(self) -> Number:
		if not len(self):
			return 0
		diff: Number = self[0]
		for i, item in old_enumerate(self):
			if i == 0:
				continue
			# since we've already taken care of the first item
			# we don't that
			if item > 1e9:
				item = 1e9
			if item < 1e-9:
				item = 1e-9
			diff -= item
		return diff
	diff = difference
	def product(self) -> Number:
		if not len(self):
			return 0
		prd: Number = self[0]
		for i, item in old_enumerate(self):
			if i == 0:
				continue
			# since we've already taken care of the first item
			# we don't that
			if item > 1e9:
				item = 1e9
			if item < 1e-9:
				item = 1e-9
			prd *= item
		return prd
	prd = product
	def quotient(self) -> Number:
		if not len(self):
			return 0
		quo: Number = self[0]
		for i, item in old_enumerate(self):
			if i == 0:
				continue
			# since we've already taken care of the first item
			# we don't that
			if item == 0:
				item = 1
			if item > 1e9:
				item = 1e9
			if item < 1e-9:
				item = 1e-9
			quo /= item
		return quo
	quo = quotient
	def max(self) -> Number:
		if not len(self):
			return 0
		return max(self)
	def min(self) -> Number:
		if not len(self):
			return 0
		return min(self)
	def combine(self, *args: list[Number]) -> Self:
		if not args:
			return self
		for arg in args:
			if not isinstance(arg, (Number, list)):
				continue
			if (isinstance(arg, list) and not all(isinstance(item, Number) for item in arg)):
				# if it's neither of the supported types
				# don't push anything
				continue
			if isinstance(arg, tuple):
				arg = list(arg)
				# a tuple?
				# no thanks,
				# we need a list
			if isinstance(arg, list):
				self.extend(arg)
			else:
				self.append(arg)
		return self
	add = push = me_dalo = combine
	def push_at(self, i: int, *items) -> Self:
		if not len(items) or not all(isinstance(item, Number) for item in items):
			return self
		if not isinstance(i, int):
			i = len(self)
		if i < 0:
			i = 0
		elif i > len(self):
			i = len(self)
		items = flatten(list(items))
		x = self[:i] + list(items) + self[i+len(items)-1:]
		updated_list: numlist = numlist(x)
		self.clear()
		self.extend(updated_list)
		return self
	def push_start(self, *items) -> Self:
		self.push_at(0, *items)
		return self
	unshift = push_start
	def shift(self) -> Number:
		if len(self) == 0:
			return 0
		return self.pop(0)
	# OVERRIDE self.remove
	old_remove = list[Number].remove
	def remove(self, *items: list[Number]) -> Number:
		if not len(self) or not all(isinstance(item, (Number, list)) for item in items if item is not None):
			return 0
		if not len(items):
			return super().pop()
		items = flatten(list(items))
		last_removed: Number = items[-1]
		for item in items:
			if not self.contains(item):
				continue
			self.old_remove(item)
		return last_removed
	rmv = se_nikalo = remove
	# OVERRIDE self.pop
	old_pop = list[Number].pop
	def pop(self, *items: list[Number]) -> Number:
		if not len(self) or not all(isinstance(item, (Number, list)) for item in items if item is not None):
			return 0
		if not len(items):
			return super().pop()
		items = flatten(list(items))
		last_popped: Number = self.old_pop(items[-1])
		for index in items:
			if index >= len(self):
				continue
			if index < 0:
				index = len(self) - abs(index)
				if index < 0 or index >= len(self):
					continue
			self.old_pop(index)
		return last_popped
	#def pop_at
	def contains(self, item) -> bool:
		return self.count(item) > 0
	has = includes = me_mojud = contains
	def index_of(self, x: Number) -> int:
		if not isinstance(x, Number) or not self.contains(x):
			return -1
		return self.index(x)
	find = find_index = index_of
	no_of = counts_of = list[Number].count
"""
nlist: numlist = numlist([2, 0, 5])
print(nlist.pop(0, -2))
print(nlist.quo())
print(nlist.find(1))
print(nlist)
"""
num_list = numlist
class intlist(list[int]):
	def __init__(self, *items: int):
		super().__init__(items)
	def __add__(self, other: list[int]) -> Self:
		lst: intlist = intlist()
		for a, b in zip(self, other):
			lst.append(Int(a)+Int(b))
		return lst
	def __radd__(self, other: list[int]) -> Self:
		lst: intlist = intlist()
		for a, b in zip(self, other):
			lst.append(Int(b)+Int(a))
		return lst
	def __sub__(self, other: list[int]) -> Self:
		lst: intlist = intlist()
		for a, b in zip(self, other):
			lst.append(Int(a)-Int(b))
		return lst
	def __rsub__(self, other: list[int]) -> Self:
		lst: intlist = intlist()
		for a, b in zip(self, other):
			lst.append(Int(b)-Int(a))
		return lst
	def __mul__(self, other: list[int]) -> Self:
		lst: intlist = intlist()
		for a, b in zip(self, other):
			lst.append(Int(a)*Int(b))
		return lst
	def __truediv__(self, other: list[int]) -> Self:
		lst: intlist = intlist()
		for a, b in zip(self, other):
			if b == 0:
				b = 1
			lst.append(Int(a)/Int(b))
		return lst
	def __pos__(self) -> Self:
		return intlist(Int(+x) for x in self)
	def __neg__(self) -> Self:
		return intlist(Int(-x) for x in self)
	def __abs__(self) -> Self:
		return intlist(Int(abs(x)) for x in self)
	def __pow__(self, other: list[int]) -> Self:
		lst: intlist = intlist()
		for a, b in zip(self, other):
			if b == 0:
				b = 1
			lst.append(Int(a) ** Int(b))
		return lst
	def __gt__(self, other: list[int]) -> bool:
		return all(Int(a) > Int(b) for a, b in zip(self, other))
	def __lt__(self, other: list[int]) -> bool:
		return all(Int(a) < Int(b) for a, b in zip(self, other))
	def __ge__(self, other: list[int]) -> bool:
		return all(Int(a) >= Int(b) for a, b in zip(self, other))
	def __le__(self, other: list[int]) -> bool:
		return all(Int(a) <= Int(b) for a, b in zip(self, other))
	def __eq__(self, other: list[int]) -> bool:
		return all(Int(a) == Int(b) for a, b in zip(self, other))
	def __ne__(self, other: list[int]) -> bool:
		return not all(Int(a) == Int(b) for a, b in zip(self, other))
	def __str__(self) -> str:
		return f"intlist([{', '.join(map(str, self))}])"
	def __repr__(self) -> str:
		return f"intlist([{', '.join(map(repr, self))}])"
int_list = intlist
class fltlist(list[float]):
	def __init__(self, *items: int):
		super().__init__(items)
	def __add__(self, other: list[float]) -> Self:
		lst: fltlist = fltlist()
		for a, b in zip(self, other):
			lst.append(Flt(a)+Flt(b))
		return lst
	def __radd__(self, other: list[float]) -> Self:
		lst: fltlist = fltlist()
		for a, b in zip(self, other):
			lst.append(Flt(b)+Flt(a))
		return lst
	def __sub__(self, other: list[float]) -> Self:
		lst: fltlist = fltlist()
		for a, b in zip(self, other):
			lst.append(Flt(a)-Flt(b))
		return lst
	def __rsub__(self, other: list[float]) -> Self:
		lst: fltlist = fltlist()
		for a, b in zip(self, other):
			lst.append(Flt(b)-Flt(a))
		return lst
	def __mul__(self, other: list[float]) -> Self:
		lst: fltlist = fltlist()
		for a, b in zip(self, other):
			lst.append(Flt(a)*Flt(b))
		return lst
	def __truediv__(self, other: list[float]) -> Self:
		lst: fltlist = fltlist()
		for a, b in zip(self, other):
			if b == 0:
				b = 1
			lst.append(Flt(a)/Flt(b))
		return lst
	def __pos__(self) -> Self:
		return fltlist(Flt(+x) for x in self)
	def __neg__(self) -> Self:
		return fltlist(Flt(-x) for x in self)
	def __abs__(self) -> Self:
		return fltlist(Flt(abs(x)) for x in self)
	def __pow__(self, other: list[float]) -> Self:
		lst: fltlist = fltlist()
		for a, b in zip(self, other):
			if b == 0:
				b = 1
			lst.append(Flt(a) ** Flt(b))
		return lst
	def __gt__(self, other: list[float]) -> bool:
		return all(Flt(a) > Flt(b) for a, b in zip(self, other))
	def __lt__(self, other: list[float]) -> bool:
		return all(Flt(a) < Flt(b) for a, b in zip(self, other))
	def __ge__(self, other: list[float]) -> bool:
		return all(Flt(a) >= Flt(b) for a, b in zip(self, other))
	def __le__(self, other: list[float]) -> bool:
		return all(Flt(a) <= Flt(b) for a, b in zip(self, other))
	def __eq__(self, other: list[float]) -> bool:
		return all(Flt(a) == Flt(b) for a, b in zip(self, other))
	def __ne__(self, other: list[float]) -> bool:
		return not all(Flt(a) == Flt(b) for a, b in zip(self, other))
	def __str__(self) -> str:
		return f"fltlist([{', '.join(map(str, self))}])"
	def __repr__(self) -> str:
		return f"fltlist([{', '.join(map(repr, self))}])"
flt_list = fltlist
# preserve the sequence
T: TypeVar = TypeVar('T')
class Stack[T]:
	def __init__(self, *items: T):
		self.array: list[T] = []
		self.length: int = -1
		if len(items) != 0:
			for item in items:
				self.push(item)
	def push(self, item: T) -> Self:
		self.array.append(item)
		self.length += 1
		return self
	def pop(self) -> Optional[T]:
		if self.length == -1:
			return None
		popped: T = self.array[self.length]
		self.length -= 1
		return popped
	def top(self) -> Optional[T]:
		if self.length == -1:
			return None
		return self.array[self.length]
	def len(self) -> int:
		return self.length + 1
	def size(self) -> int:
		return self.len()
	def __len__(self) -> int:
		return self.len()
	def __str__(self) -> str:
		return str(self.array)
class obj(dict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._convert_nested_dicts(self)
	def _convert_nested_dicts(self, object):
		if isinstance(object, dict):
			for k, v in object.items():
				if isinstance(v, dict):
					object[k] = obj(v)
				elif isinstance(v, (list, tuple)):
					object[k] = self._convert_nested_collections(v)
		elif isinstance(object, (list, tuple)):
			return self._convert_nested_collections(object)
		return object
	def _convert_nested_collections(self, collection):
		converted_collection = []
		for item in collection:
			if isinstance(item, dict):
				converted_collection.append(obj(item))
			elif isinstance(item, (list, tuple)):
				converted_collection.append(self._convert_nested_collections(item))
			else:
				converted_collection.append(item)
		return type(collection)(converted_collection)
	def __getattr__(self, key) -> Any|None:
		try:
			return self[key]
		except KeyError as e:
			 raise AttributeError(f"the object 'obj' has no key '{key}'") from None
	def __setattr__(self, key, value):
		if isinstance(value, dict):
			self[key] = obj(value)
		elif isinstance(value, (list, tuple)):
			self[key] = self._convert_nested_collections(value)
		else:
			self[key] = value
	def __setitem__(self, key, value):
		if isinstance(value, dict):
			super().__setitem__(key, obj(value))
		elif isinstance(value, (list, tuple)):
			super().__setitem__(key, self._convert_nested_collections(value))
		else:
			super().__setitem__(key, value)
	def keys(self):
		return list(super().keys())
	def values(self):
		return list(super().values())
	def entries(self):
		return list(super().items())
# allows obj($x=$valueForX, $y=$valueForY)
o = obj
# for older dictionaries
def keys(dictionary: dict) -> list:
	if not isinstance(dictionary, dict):
		return []
	return list(dictionary.keys())
def values(dictionary: dict) -> list:
	if not isinstance(dictionary, dict):
		return []
	return list(dictionary.values())
def entries(dictionary: dict) -> list:
	if not isinstance(dictionary, dict):
		return []
	return list(dictionary.items())
get_keys = keys_of = keys
get_values = values_of = values
get_entries = entries_of = entries
def remove_duplicates(lst: list) -> list:
	if not lst or not isinstance(lst, list):
		return []
	return list(dict.fromkeys(lst).keys())
def swap_keys(_obj: dict[Any, Any]) -> dict[Any, Any]:
	if not isinstance(_obj, Iterable):
		return {}
	return {v: k for k, v in _obj.items()}
def Count(itrbl: Iterable) -> dict[int, Any]:
	if not isinstance(itrbl, Iterable):
		return {}
	counted: dict[int, Any] = {}
	for key in itrbl:
		counted[key] = counted.get(key, 0) + 1
	counted = swap_keys(counted)
	return counted
count_occur = Count
# ^DIFFERENT FROM collections.count
def get_local_declarations() -> obj:
	"""
	@return
		<dict>
		::a dictionary holding all the local variables, (sub)classes (of classes), and the functions of the local scope of a class/function
	"""
	[variables, classes, functions] = [{}, {}, {}]
	frame = currentframe().f_back
	for name, _obj in frame.f_locals.items():
		# Exclude built-in names and imported modules
		if not name.startswith('__'):
			if isfunction(_obj):
				functions[name] = _obj
			elif isclass(_obj):
				classes[name] = _obj
			# For variables, we can assume anything else that's not a function or class
			# and is user-defined in this module is a variable.
			# This is a simplification; more robust checks might be needed for complex cases.
			elif not ismodule(_obj):						   # Exclude imported modules
				variables[name] = _obj
	return o(variables=variables, classes=classes, functions=functions)
def get_global_declarations() -> obj:
	"""
	@return
		<dict>
		::a dictionary holding all the local variables, (sub)classes (of classes), and the functions of the local scope of a class/function
	"""
	[variables, classes, functions] = [{}, {}, {}]
	for name, _obj in globals().items():
		# Exclude built-in names and imported modules
		if not name.startswith('__') and getmodule(_obj) is sys.modules[__name__]:
			if isfunction(_obj):
				functions[name] = _obj
			elif isclass(_obj):
				classes[name] = _obj
			# For variables, we can assume anything else that's not a function or class
			# and is user-defined in this module is a variable.
			# This is a simplification; more robust checks might be needed for complex cases.
			elif not ismodule(_obj):						  # Exclude imported modules
				variables[name] = _obj
	return o(variables=variables, classes=classes, functions=functions)
Yes = Ha = Han =  true = True
No = Na = Nahi = false = False
none: NoneType = None
null = none
sort = sorted
sortMutate = lambda x: x.sort()
reverseSort = lambda arr: sorted(arr, reverse=True)
reverseSortMutate = lambda arr: arr.sort(reverse=True)
def reverse(x: str | list[any]):
	if not isinstance(x, str) and not isinstance(x, list): return None
	if isinstance(x, list):
		x.reverse()
		return x
	return x[::-1]
filter = lambda arr, condition: filter(condition, arr)
# test this	
def rng(x: str|list|tuple|Number, y: str|list|tuple|Number|None = None, step: Number = 1, **kwArgs) -> list[int] | list[float]:
	if x is None or not isinstance(x, (str, list, tuple, Number)) or not isinstance(y, (str, list, tuple, Number, NoneType)) or step is None or not isinstance(step, Number):
		return []
	x_is_a_parsable_char: bool = False
	y_is_a_parsable_char: bool = False
	if isinstance(x, str) and len(str(x).strip()) != 0 and 0 <= ord(x) <= 127:
		if not y:
			y = ord(x[0])
			x = 97 if x[0].lower() == x[0] else 65
		else:
			x = ord(x[0])
		x_is_a_parsable_char = True
	if isinstance(y, str) and len(str(y).strip()) != 0 and 0 <= ord(y) <= 127:
		y = ord(y[0])
		y_is_a_parsable_char = True
	if len(kwArgs.keys()) > 0:
		if "s" in kwArgs:
			step = kwArgs.get("s", 1)
		elif "step" in kwArgs:
			step = kwArgs.get("step", 1)
	if step <= 0:
		step = 1
	if (isinstance(y, Number) and step >= y):
		step = 1
	if isinstance(x, (str, list, tuple)) and step >= len(x):
		step = 1
	if isinstance(y, (str, list, tuple)) and step >= len(y):
		step = 1
	return_list: list[int] | list[float] = []
	if y is None:
		if not isinstance(x, Number) and isinstance(step, int):
			i: int = 0
			while i < len(x):
				return_list.append(i)
				i += step
			return return_list
		x = abs(x)
		if isinstance(x, int) and isinstance(step, int):
			i: int = 0
			while i < x:
				return_list.append(i)
				i += step
		if isinstance(x, float):
			i: float = 0
			while i < x:
				return_list.append(i)
				i += step
		return return_list
	if (isinstance(x, int) and isinstance(step, int)) and not isinstance(y, Number):
		y_length: int = len(y)
		if x < 0 or x >= y_length:
			return []
		while x < y_length:
			return_list.append(x)
			x += step
		return return_list
	if isinstance(x, int) and isinstance(y, int) and isinstance(step, int):
		if x == y:
			return []
		if x > y:
			while x >= y:
				return_list.append(x)
				x -= step
		else:
			while x <= y:
										return_list.append(x)
										x += step
	if isinstance(x, float) or isinstance(y, float):
		if x == y:
			return []
		if x > y:
			while x >= y:
				return_list.append(x)
				x -= step
		else:
			while x <= y:
				return_list.append(x)
				x += step
	if x_is_a_parsable_char or y_is_a_parsable_char:
		return_list = [chr(n) for n in return_list]
	return return_list
def f(*args) -> str:
	formatted: str = ""
	curframe: Optional[FrameType] = currentframe()
	frames: list[Optional[FrameType]] = []
	caller_locals: dict[str, Any] = {}
	while curframe is not None:
		frames.append(curframe)
		curframe = curframe.f_back
		# keep retrieving until you hit the oldest ancestor
	frames = reversed(frames)
	# reverse the frames to prioritize the closest local scope first
	for scope in frames:
		caller_locals.update(scope.f_globals | scope.f_locals)
	blacklisted_keywords: list[str] = ['import', '__', 'open', 'exec', 'eval', 'del', 'lambda']
	blacklisted_functions: list[str] = ['system', 'popen', 'subprocess']
	blacklisted_items: list[str] = [*blacklisted_keywords, *blacklisted_functions]
	for arg in args:
		if isinstance(arg, bool):
			arg = "Yes" if arg == True else "No"
		try:
			ast.parse(f"f'{arg}'")
			arg_lower: str = arg.lower()
			for item in blacklisted_items:
				if item in arg_lower:
					print(f"Forbidden keyword/function in input: '{item}'")
					continue
			# Evaluate the expression
			arg = re.sub(r"(?<!\\)[\$\{]+([^\s\{\}\(\)\$]+(?:\(([\w\.\-]+(,\s*)?)*\))?)(\}(?!#{4}))?", r"{\1}", arg)
			# (?<!\\) means recognize escapes, and only match if the dollar '$', and opening_brace '{'' are not precededed by a forward slash '\' (which is the standard pattern for regex escapes)
			evaluation: str = eval(f"f'{arg}'", {"__builtins__": {}}, caller_locals)
			WHITESPACE_CHAR = " "
			# for readability, there should be a whitespace character after each argument, except the last one (though, for the last one, it does not really matter, as it usually goes unnoticed)
			formatted += evaluation + WHITESPACE_CHAR
		except Exception as e:
			...
	formatted = formatted.rstrip()
	return formatted
def printf(*args, **kwargs) -> None:
	print(f(*args), **kwargs)
kaho = printf
def khali(x: Iterable) -> bool:
	if x is None:
		return True
	if not isinstance(x, Iterable):
		return not x
	if isinstance(x, str):
		return not x.strip()
	return len(x) == 0
is_empty = isempty = khali_he = khali
# type checks
is_none = isnone = is_null = isnull = lambda x: x is None
isnt_none = isntnone = non_none = nonnone = lambda x: not is_none(x)
is_string = isstring = is_str = isstr = lambda x: isinstance(x, str)
isnt_string = isntstring = isnt_str = isntstr = non_string = nonstring = non_str = nonstr = lambda x: not is_string(x)
is_integer = isinteger = is_int = isint = lambda x: isinstance(x, int) and not isinstance(x, bool)
isnt_integer = isntinteger = isnt_int = isntint = non_integer = noninteger = non_int = nonint = lambda x: not is_integer(x)
def is_int_like(x: str) -> bool:
	x = str(x)
	parsed: int = 0
	try:
		parsed = int(x)
		return True
	except ValueError:
		...
	return False
is_float = isfloat = is_flt = isflt = lambda x: isinstance(x, float) and not isinstance(x, bool)
isnt_float = isntfloat = isnt_float = isntfloat = non_float = nonfloat = non_flt = nonflt = lambda x: not is_float(x)
def is_float_like(x: str) -> bool:
	x = str(x)
	parsed: float = 0.0
	try:
		parsed = float(x)
		return True
	except ValueError:
		...
	return False
is_flt_like = is_float_like
is_boolean = isboolean = is_bool = isbool = lambda x: isinstance(x, bool)
isnt_boolean = isntboolean = isnt_bool = isntbool = non_boolean = nonboolean = non_bool = nonbool = lambda x: not is_boolean(x)
def is_bool_like(x: str) -> bool:
	x = str(x)
	parsed: bool = False
	if x == "True":
		parsed = True
	elif x == "False":
		parsed = False
	return parsed
is_array = isarray = is_arr = isarr = lambda x: isinstance(x, (list, tuple))
isnt_array = isntarray = isnt_arr = isntarr = non_array = nonarray = non_arr = nonarr = lambda x: not is_array(x)
is_stringarray = is_stringarr = is_strarray = is_strarr = isstringarray = isstringarr = isstrarray = isstrarr = lambda x: isinstance(x, (list[str], tuple[str, ...]))
isnt_stringarray = isnt_stringarr = isnt_strarray = isnt_strarr = isntstringarray = isntstringarr = isntstrarray = isntstrarr = non_stringarray = non_stringarr = non_strarray = non_strarr = nonstringarray = nonstringarr = nonstrarray = nonstrarr = lambda x: not is_stringarray(x)
is_integerarray = is_integerarr = is_intarray = is_intarr = isintegerarray = isintegerarr = isintarray = isintarr = lambda x: isinstance(x, (list[int], tuple[int, ...]))
isnt_integerarray = isnt_integerarr = isnt_intarray = isnt_intarr = isntintegerarray = isntintegerarr = isntintarray = isntintarr = non_integerarray = non_integerarr = non_intarray = non_intarr = nonintegerarray = nonintegerarr = nonintarray = nonintarr = lambda x: not is_integerarray(x)
is_floatarray = is_floatarr = is_fltarray = is_fltarr = isfloatarray = isfloatarr = isfltarray = isfltarr = lambda x: isinstance(x, (list[float], tuple[float, ...]))
isnt_floatarray = isnt_floatarr = isnt_fltarray = isnt_fltarr = isntfloatarray = isntfloatarr = isntfltarray = isntfltarr = non_floatarray = non_floatarr = non_fltarray = non_fltarr = nonfloatarray = nonfloatarr = nonfltarray = nonfltarr = lambda x: not is_floatarray(x)
is_booleanarray = is_booleanarr = is_boolarray = is_boolarr = isbooleanarray = isbooleanarr = isboolarray = isboolarr = lambda x: isinstance(x, (list[bool], tuple[bool, ...]))
isnt_booleanarray = isnt_booleanarr = isnt_boolarray = isnt_boolarr = isntbooleanarray = isntbooleanarr = isntboolarray = isntboolarr = non_booleanarray = non_booleanarr = non_boolarray = non_boolarr = nonbooleanarray = nonbooleanarr = nonboolarray = nonboolarr = lambda x: not is_booleanarray(x)
is_iterable = isiterable = lambda x: isinstance(x, Iterable)
isnt_iterable = isntiterable = non_iterable = noniterable = lambda x: not is_iterable(x)
is_callable = iscallable = is_function = isfunction = is_func = isfunc = lambda x: callable(x)
isnt_callable = isntcallable = non_callable = noncallable = lambda x: not is_callable(x)
def split(src: str, regex: str|NoneType = None, maxsplits: int = IntInfinity, flags: int = 0) -> list[str]:
	if not src or not isinstance(src, str) or not isinstance(regex, (str, NoneType)):
		# allow regex to be empty, as it sometimes can be
		return []
	if regex is None:
		# if the regex is None, split into words (hyphen, and quote preserved, for max reliability)
		regex = r"([^\-\w\"\']|(?<!\w)[\-\"\'](?!\w))"
	regex = str(regex)
	if not isinstance(maxsplits, int):
		maxsplits = IntInfinity
	if maxsplits <= 0:
		return [src]
	if not isinstance(flags, int):
		flags = 0
	try:
		regex = re.sub(r"(\?)(<\w+>)", r"\1P\2", regex)
		raw_list: list[str] = re.split(regex, src, maxsplit=maxsplits, flags=flags)
		result: list[str] = []
		for x in raw_list:
			if not x:
				continue
			result.append(x)
		return result
	except re.error as e:
		# fallback to original splitting
		# if regex splitting fails
		print(f"re.warning:\n  * Bad regex split pattern. Falling back to the original `'string'.split`. *Reason*: {str(e).capitalize()}.")
		return [x for x in src.split(regex) if x]
def joined_words(*args: tuple[Any]) -> str:
	"""
	@param			args
		:type			tuple[Any]
		:description		arguments to join in "x, y, aur z" format
	@return			
		:type										  str <blankable, if len(args) == 0>
		:description		the joined arguments (initially of type, Any)
	"""
	result: list[str] = []
	for arg in args:
		if arg is None:
			continue
		if isinstance(arg, (list, tuple)):
			arg = joined_words(*arg)
			arg = re.sub(r"(?<=, )aur (?=.+$)", "", str(arg))
		if isinstance(arg, float):
			arg = round(arg, 1)
		if isinstance(arg, bool):
			arg = "Han" if arg else "Nahi"
		arg = str(arg)
		if ", " in arg:
			sub_args: list[str] = arg.split(", ")
			for sub_arg in sub_args:
				result.append(sub_arg)
			continue
		result.append(arg)
	if len(result) < 2:
		return ", ".join(result)
	last: str = str(result.pop())
	return ", ".join(result) + ", aur " + last
jurewe = joined_words
def replace(src: str, to_replace: str|dict|None = None, replacement: str|Callable = "", ignore_case: bool = False, case_insensitive: bool = False, count: int = IntInfinity) -> str:
	if not src or not isinstance(src, str) or not ((isinstance(to_replace, str)) or (isinstance(to_replace, dict) and not replacement) or isinstance(replacement, (str, Callable))):
		# allow empty replacement for removals
		return ""
	ignore_case = ignore_case or case_insensitive
	if not ignore_case or not isinstance(ignore_case, bool):
		ignore_case = False
	if not isinstance(count, int) or count < 0:
		count = IntInfinity
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
		src_trunc: str = f"{src[:30]}... ..." if len(src) > 30 else src
		print(f"re.warning:\n  * Bad regex, or replacement pattern '{to_replace}'. Returning the original source string '{src_trunc}' as-is. *Reason*: {str(e).capitalize()}.")
		result = src
	return result
replacei = ireplace = replace_i = i_replace = functools.partial(replace, ignore_case=True)
replaceone = replace_one = functools.partial(replace, count=1)
replace_i_one = replace_one_i = replace_ione = replace_onei = replace_ins_first = replace_first_ins = replace_insfirst = functools.partial(replace, ignore_case=True, count=1)
def find_matches(src: str, to_find: str) -> list[str]:
	if not src or not isinstance(src, str) or not to_find or not isinstance(to_find, str):
		return []
	to_find = re.sub(r"(\?)(<\w+>)", r"\1P\2", to_find)
	matches: list[str] = re.findall(to_find, src)
	return matches
def find_matches_i(src: str, to_find: str) -> list[str]:
	if not src or not isinstance(src, str) or not to_find or not isinstance(to_find, str):
		return []
	to_find = re.sub(r"(\?)(<\w+>)", r"\1P\2", to_find)
	matches: list[str] = re.findall(to_find, src, re.IGNORECASE)
	return matches
def find_matches_as_obj(src: str, to_find: str) -> obj[str, str]:
	if not src or not isinstance(src, str) or not to_find or not isinstance(to_find, str):
		return obj()
	to_find = re.sub(r"(\?)(<\w+>)", r"\1P\2", to_find)
	matches: obj[str, str] = obj()
	if matches_found := re.search(to_find, src):
		matches = matches_found.groupdict()
	return matches
def find_matches_as_obj_i(src: str, to_find: str) -> obj[str, str]:
	if not src or not isinstance(src, str) or not to_find or not isinstance(to_find, str):
		return obj()
	to_find = re.sub(r"(\?)(<\w+>)", r"\1P\2", to_find)
	matches: obj[str, str] = obj()
	if matches_found := re.search(to_find, src, flags=re.IGNORECASE):
		matches = matches_found.groupdict()
	return matches
def find_match(src: str, to_find: str) -> str:
	if not src or not isinstance(src, str) or not to_find or not isinstance(to_find, str):
		return ""
	to_find = re.sub(r"(\?)(<\w+>)", r"\1P\2", to_find)
	matches: list[str] = find_matches(src, to_find)
	if len(matches) == 0:
		return ""
	return matches[0]
def find_match_i(src: str, to_find: str) -> str:
	if not src or not isinstance(src, str) or not to_find or not isinstance(to_find, str):
		return ""
	to_find = re.sub(r"(\?)(<\w+>)", r"\1P\2", to_find)
	matches: list[str] = find_matches_i(src, to_find)
	if len(matches) == 0 or not matches[0]:
		return ""
	return matches[0]
def match(src: str, to_find: str) -> bool:
	if not src or not isinstance(src, str) or not to_find or not isinstance(to_find, str):
		return False
	to_find = re.sub(r"(\?)(<\w+>)", r"\1P\2", to_find)
	matches: list[str] = find_matches(src, to_find)
	if len(matches) == 0:
		return False
	return True
def match_i(src: str, to_find: str) -> bool:
	if not src or not isinstance(src, str) or not to_find or not isinstance(to_find, str):
		return False
	to_find = re.sub(r"(\?)(<\w+>)", r"\1P\2", to_find)
	matches: list[str] = find_matches_i(src, to_find)
	if len(matches) == 0:
		return False
	return True
def find_words(src: Any) -> list[str]:
	"""
	@param			src
		:type			Any
		:description		the source to find the words from
	@return			
		:type										  list <blankable, if no words are found>
		:description		a word list containing all the words from the object
	"""
	if not src:
		return ""
	src = str(src).strip()
	word_list: list[str] = find_matches(src, r"(?:[A-Za-z]+\-)*[A-Za-z]+")
	return word_list
dhundo_alfaaz = dhundo_alfaz = words_of = to_words = find_words
def startswith(x: str|list, y: str|list) -> bool:
	if not isinstance(x, (str, list, tuple)):
		return False
	if isinstance_each([x, y], str):
		try:
			return re.search(f"^{y}", x)
		except re.error as e:
			print(f"re.warning:\n  * Bad regex. Switching to default `str.startswith` mode, now that the regex mode failed. *Reason*: {str(e).capitalize()}.")
			return x.startswith(y)
	elif isinstance(x, (list, tuple)):
		if isinstance(x, tuple):
			x = list(x)
		if not isinstance(y, (list, tuple)):
			y = [y]
		if isinstance(y, tuple):
			y = list(y)
		if len(x) < len(y):
			return False
		return x[:len(y)] == y
	return False
starts_with = startswith
def endswith(x: str|list, y: str|list) -> bool:
	if not isinstance(x, (str, list, tuple)):
		return False
	if isinstance_each([x, y], str):
		try:
			return re.search(f"{y}$", x)
		except re.error as e:
			print(f"re.warning:\n  * Bad regex. Switching to default `str.endswith` mode, now that the regex mode failed. *Reason*: {str(e).capitalize()}.")
			return x.endswith(y)
	elif isinstance(x, (list, tuple)):
		if isinstance(x, tuple):
			x = list(x)
		if not isinstance(y, (list, tuple)):
			y = [y]
		if isinstance(y, tuple):
			y = list(y)
		if len(x) < len(y):
			return False
		return x[-len(y):] == y
	return False
ends_with = endswith
def upper(src: str) -> str:
	if not isinstance(src, str):
		return ""
	result: str = src.upper()
	return result
def isupper(src: str) -> bool:
	if not isinstance(src, str):
		return False
	return src.isupper()
is_upper = isupper
def lower(src: str) -> str:
	if not isinstance(src, str):
		return ""
	result: str = src.lower()
	return result
def islower(src: str) -> bool:
	if not isinstance(src, str):
		return False
	return src.islower()
is_lower = islower
def snake_case(src: str) -> str:
	if not isinstance(src, str):
		return ""
	all_were_upper: bool = False
	if src.upper() == src:
		all_were_upper = True
	result: str = src.casefold()
	result = re.sub(r"[^\-\.\w\n]+", "_", result).strip("_")
	if all_were_upper:
		result = result.upper()
	return result
snakecase = snake_case
def is_snake_case(src: str) -> bool:
	if not isinstance(src, str):
		return False
	return src == snake_case(src)
issnakecase = is_snakecase = is_snake_case
def title_case(src: str) -> str:
	if not isinstance(src, str):
		return ""
	result: str = src.title()
	return result
def is_title_case(src: str) -> bool:
	if not isinstance(src, str):
		return False
	return src.istitle()
istitle = is_title = istitlecase = is_titlecase = is_title_case
def sentence_case(src: str) -> str:
	if not isinstance(src, str):
		return ""
	result: str = src.capitalize()
	return result
sentcase = sent_case = sentence_case
def is_sentence_case(src: str) -> bool:
	if not isinstance(src, str):
		return False
	return src == sentence_case(src)
issentcase = is_sentcase = is_sent_case = issentencecase = is_sentencecase = is_sentence_case
class Money:
	def __init__(self, amount=0, currency="Rs. "):
		self.amount = amount if amount >= 0 else 0
		self.currency = currency if currency and len(currency) <= 4 else "Rs. "
	def set_currency(self, currency):
		if currency and len(currency) <= 4:
			self.currency = currency
		return self
	def set_amount(self, new_amount):
		if new_amount >= 0:
			self.amount = new_amount
		return self
	def add(self, *nums):
		self.amount += sum(nums)
		return self
	def subtract(self, *nums):
		self.amount -= sum(nums)
		return self
	def multiply(self, *nums):
		for n in nums:
			self.amount *= n
		return self
	def divide(self, *nums):
		for n in nums:
			if n == 0:
				n = 1
			self.amount /= n
		return self
	def __str__(self):
		return f"{self.currency}{self.amount:.2f}"
	def balance(self):
		return str(self)
class Pesa(Money):
	def __init__(self, amount, currency):
		super().__init__(amount, currency)
pesa = Pesa
def open_file_case_ins(filename: str, mode: str = 'r', **kwargs):
	filename = str(filename)
	if not mode or not isinstance(mode, str):
		mode = "r"
	if not filename or not os.path.isfile(filename):
		raise FileNotFoundError(f"File '{filename}' doesn't exist")
	directory, name = os.path.split(filename)
	directory = directory or '.'  # Default to current directory if none specified
	name_lower = name.lower()
	for actual_file_name in os.listdir(directory):
		if actual_file_name.lower() == name_lower:
			actual_path = os.path.join(directory, actual_file_name)
			if os.path.isfile(actual_path):
				return open(actual_path, mode, **kwargs)
open_case_ins = open_file_case_ins
class File:
	def __init__(self, path: Union[str, Path]):
		self.pathname = Path(path)
	def __str__(self) -> str:
		return str(self.pathname)
	def path(self) -> Path:
		return self.pathname
	def absolute_path(self) -> str:
		return str(self.pathname.absolute())
	def abs_path(self) -> str:
		return self.absolute_path()
	def is_file(self) -> bool:
		return self.pathname.is_file()
	def is_folder(self) -> bool:
		return self.pathname.is_dir()
	def exists(self) -> bool:
		return self.pathname.exists()
	def exists_file(self) -> bool:
		return self.is_file() and self.exists()
	def exists_folder(self) -> bool:
		return self.is_folder() and self.exists()
	mojud_file = mojud_he_file = he_mojud_file = found_file = exists_file
	exists_directory = exists_dir = found_dir = mojud_folder = mojud_he_folder = he_mojud_folder = mojud_directory = mojud_he_directory = he_mojud_directory = exists_folder
	mojud = mojud_he = he_mojud = found = exists_path = exists
	@staticmethod
	def create(fname: str, content: str = "") -> bool:
		try:
			if not fname or not content:
				raise ValueError("File name, and content are required")
			if re.search(r"(?<=\\w)\\s*[\\|\\+\\&\\,\\;]\\s*(?=\\w)", fname):
				for subFileName in re.split(r"\\s*[\\|\\+\\&\\,\\;]\\s*", fname):
					File.create(subFileName, content)
				return True
			with open(fname, 'w') as f:
				f.write(content)
			print(f"[KL.file.JobSuccess]:\nFile {fname} created successfully.")
			return True
		except ValueError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except PermissionError:
			print(f"[KL.file.JobFailed]: Permission denied to create file {fname}")
		except OSError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except Exception as e:
			print(f"[KL.file.JobFailed]: {e}")
		return False
	@staticmethod
	def createBlankFile(fname: str) -> bool:
		try:
			if not fname:
				raise ValueError("File name is required")
			Path(fname).touch()
			print(f"[KL.file.JobSuccess]:\nBlank file {fname} created successfully.")
			return True
		except ValueError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except PermissionError:
			print(f"[KL.file.JobFailed]: Permission denied to create file {fname}")
		except OSError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except Exception as e:
			print(f"[KL.file.JobFailed]: {e}")
		return False
	@staticmethod
	def createFolder(folderName: str) -> bool:
		try:
			if not folderName:
				raise ValueError("Folder name is required")
			if re.search(r"(?<=\\w)\\s*[\\|\\+\\&\\,\\;]\\s*(?=\\w)", folderName):
				for folder in re.split(r"\\s*[\\|\\+\\&\\,\\;]\\s*", folderName):
					File.createFolder(folder)
				return True
			os.makedirs(folderName, exist_ok=True)
			return True
		except ValueError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except PermissionError:
			print(f"[KL.file.JobFailed]: Permission denied to create folder {folderName}")
		except OSError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except Exception as e:
			print(f"[KL.file.JobFailed]: {e}")
		return False
	@staticmethod
	def read(fname: str) -> str:
		try:
			if not fname:
				raise ValueError("File name is required")
			with open_case_ins(fname, 'r') as f:
				contents: str = f.read()
				return contents
		except ValueError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except FileNotFoundError:
			print(f"[KL.file.JobFailed]: File {fname} does not exist")
		except PermissionError:
			print(f"[KL.file.JobFailed]: Permission denied to read file {fname}")
		except OSError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except Exception as e:
			print(f"[KL.file.JobFailed]: {e}")
		return ""
	@staticmethod
	def get_lines(fname: str) -> list[str]:
		contents: str = File.read(fname)
		lines: list[str] = []
		if not contents.strip():
			return False
		if re.search(r"\n", contents):
			split_content: list[str] = split(contents, r"\n")
			for line in split_content:
				lines.append(line)
		else:
			lines.append(contents)
			# no lines found other than the first, append the contents as-is
		return lines
	readlines = read_lines = getlines = get_lines
	@staticmethod
	def readJson(fname: str) -> Optional[dict]:
		try:
			return json.loads(File.read(fname))
		except json.JSONDecodeError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except Exception as e:
			print(f"[KL.file.JobFailed]: {e}")
		return None
	@staticmethod
	def write(fname: str, content: str) -> bool:
		try:
			if not fname or not content:
				raise ValueError("File name and content are required")
			with open(fname, 'w') as f:
				f.write(content)
			print(f"[KL.file.JobSuccess]:\nFile {fname} written successfully.")
			return True
		except ValueError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except PermissionError:
			print(f"[KL.file.JobFailed]: Permission denied to write to file {fname}")
		except OSError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except Exception as e:
			print(f"[KL.file.JobFailed]: {e}")
		return False
	@staticmethod
	def append(fname: str, content: str) -> bool:
		try:
			if not fname or not content:
				raise ValueError("File name and content are required")
			if re.search(r"(?<=\\w)\\s*[\\|\\+\\&\\,\\;]\\s*(?=\\w)", fname):
				for subFileName in re.split(r"\\s*[\\|\\+\\&\\,\\;]\\s*", fname):
					File.append(subFileName, content)
				return True
			with open(fname, 'a') as f:
				f.write(content)
			print(f"[KL.file.JobSuccess]:\nAppending to file {fname} was successful.")
			return True
		except ValueError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except PermissionError:
			print(f"[KL.file.JobFailed]: Permission denied to append to file {fname}")
		except OSError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except Exception as e:
			print(f"[KL.file.JobFailed]: {e}")
		return False
	@staticmethod
	def delete(fname: str) -> bool:
		try:
			if not fname:
				return
			if re.search(r"(?<=\\w)\\s*[\\|\\+\\&\\,\\;]\\s*(?=\\w)", fname):
				for subFileName in re.split(r"\\s*[\\|\\+\\&\\,\\;]\\s*", fname):
					File.delete(subFileName)
				return True
			if os.path.isdir(fname):
				shutil.rmtree(fname)
			else:
				os.remove(fname)
			print(f"[KL.file.JobSuccess]:\nFile {fname} deleted successfully.")
			return True
		except FileNotFoundError:
			print(f"[KL.file.JobFailed]: File {fname} does not exist")
		except PermissionError:
			print(f"[KL.file.JobFailed]: Permission denied to delete file {fname}")
		except OSError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except Exception as e:
			print(f"[KL.file.JobFailed]: {e}")
		return False
	@staticmethod
	def rename(fname: str, destinationString: str) -> bool:
		try:
			if not fname or not destinationString:
				raise ValueError("File name and destination are required")
			if re.search(r"(?<=\\w)\\s*[\\|\\+\\&\\,\\;]\\s*(?=\\w)", fname) and re.search(r"[\\\\\\/]", destinationString):
				for subFileName in re.split(r"\\s*[\\|\\+\\&\\,\\;]\\s*", fname):
					File.rename(subFileName, destinationString)
				return True
			os.rename(fname, destinationString)
			print(f"[KL.file.JobSuccess]:\nFile {fname} was successfully moved/renamed to {destinationString}")
			return True
		except ValueError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except FileNotFoundError:
			print(f"[KL.file.JobFailed]: File {fname} does not exist")
		except PermissionError:
			print(f"[KL.file.JobFailed]: Permission denied to rename file {fname}")
		except OSError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except Exception as e:
			print(f"[KL.file.JobFailed]: {e}")
		return False
	@staticmethod
	def copy(from_path: str, to_path: str, overwrite: bool = True) -> bool:
		try:
			if not from_path or not to_path:
				raise ValueError("Source and destination paths are required")
			if re.search(r"(?<=\\w)\\s*[\\|\\+\\&\\,\\;]\\s*(?=\\w)", from_path):
				for subFileName in re.split(r"\\s*[\\|\\+\\&\\,\\;]\\s*", from_path):
					File.copy(subFileName, to_path, overwrite)
				return True
			if overwrite:
				shutil.copy(from_path, to_path)
			else:
				shutil.copy2(from_path, to_path)
			return True
		except ValueError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except FileNotFoundError:
			print(f"[KL.file.JobFailed]: File {from_path} does not exist")
		except PermissionError:
			print(f"[KL.file.JobFailed]: Permission denied to copy file {from_path}")
		except OSError as e:
			print(f"[KL.file.JobFailed]: {e}")
		except Exception as e:
			print(f"[KL.file.JobFailed]: {e}")
		return False
file: File = File
def encode(data: any) -> str:
	try:
			return base64.b64encode(str(data).encode()).decode()
	except TypeError as e:
			return ""
def decode(data: str) -> str:
	import binascii
	try:
			return base64.b64decode(data).decode()
	except (TypeError, binascii.Error) as e:
			return ""

import time
def time_it(fn):
	if not callable(fn):
		return 
	def wrapper(*args, **kwargs):
		start: float = timer.time()
		return_value = fn(*args, **kwargs)
		# if possible, get the return value
		end: int = timer.time()
		duration: int = end - start
		print(f"@timeit:\n\tFunction `{fn.__name__}` took {duration:.3f} second(s) to fulfil its job")
		return return_value
	return wrapper
def time_lia(fn):
	if not callable(fn):
		return 
	def wrapper(*args, **kwargs):
		start: float = timer.time()
		return_value = fn(*args, **kwargs)
		# if possible, get the return value
		end: int = timer.time()
		duration: int = end - start
		print(f"@timelia:\n\tFunction `{fn.__name__}` ne apna kaam {duration:.1f} second(s) me kia")
		return return_value
	return wrapper
timeme = time_me = timeit = time_it
timelia = time_lia
def internet_access() -> bool:
	try:
		requests.get("https://www.google.com", timeout=5)
		return True
	except requests.ConnectionError:
		return False
def fetch(url: str = "") -> dict|list:
	if not url or not "requests" in globals():
		return {}
	try:
		response = requests.get(url, timeout=60)
		response.raise_for_status()
		if not (response.status_code >= 200 and response.status_code <= 299):
			return {}
		return response.json()
	except Exception as e:
		print(f"Error fetching data: {e}")
		return {}
def filepath(to_filename: str) -> str:
	if not isinstance(to_filename, str): 
		return ""
	if hasattr(sys, '_MEIPASS'):
		base = Path(sys._MEIPASS)
	elif getattr(sys, 'frozen', False):
		base = Path(sys.executable).parent
	else:
		base = Path(__file__).resolve().parent
	target = to_filename.strip().replace("\\", "/")
	if target.startswith(".."):
		if not (hasattr(sys, '_MEIPASS') or getattr(sys, 'frozen', False)):
			base = base.parent
		target = target[2:].lstrip("/")
	else:
		target = target.lstrip("/")
	full_path: str = os.path.normpath(os.path.join(str(base), target))
	# normalize the path, and make it cross-platform
	return full_path
file_path = get_path = to_path = path_to = ki_path = ki_location = ki_directory = filepath
def asset(to_filename: str) -> str:
	path: str = ""
	try:
		if either(hasattr(sys, '_MEIPASS'), getattr(sys, 'frozen', False)) and both("_filepaths" in globals(), "PROGRAMS_DIR" in dir(globals().get("_filepaths", {}))):
			from _filepaths import PROGRAMS_DIR
			path = os.path.join(PROGRAMS_DIR, to_filename)
		else:
			path = to_path(f"../{to_filename}")
		# SEQUENCE IS MANDATORY
		fallback_dirs: list[str] = [
			f"../asset/{to_filename}",
			f"../assets/{to_filename}",
			f"../files/{to_filename}",
			f"../data/{to_filename}",
			f"../res/{to_filename}",
			f"../resource/{to_filename}",
			f"../resources/{to_filename}",
			f"../____programs____/{to_filename}",
			f"../____programs____/asset/{to_filename}",
			f"../____programs____/assets/{to_filename}",
			f"../____programs____/files/{to_filename}",
			f"../____programs____/data/{to_filename}",
			f"../____programs____/res/{to_filename}",
			f"../____programs____/resource/{to_filename}",
			f"../____programs____/resources/{to_filename}",
			f"../_execute/{to_filename}",
			f"../_execute/asset/{to_filename}",
			f"../_execute/assets/{to_filename}",
			f"../_execute/files/{to_filename}",
			f"../_execute/data/{to_filename}",
			f"../_execute/res/{to_filename}",
			f"../_execute/resource/{to_filename}",
			f"../_execute/resources/{to_filename}",
			f"./{to_filename}",
			f"./asset/{to_filename}",
			f"./assets/{to_filename}",
			f"./files/{to_filename}",
			f"./data/{to_filename}",
			f"./res/{to_filename}",
			f"./resource/{to_filename}",
			f"./resources/{to_filename}",
			f"./____programs____/{to_filename}",
			f"./____programs____/asset/{to_filename}",
			f"./____programs____/assets/{to_filename}",
			f"./____programs____/files/{to_filename}",
			f"./____programs____/data/{to_filename}",
			f"./____programs____/res/{to_filename}",
			f"./____programs____/resource/{to_filename}",
			f"./____programs____/resources/{to_filename}",
			f"./_execute/{to_filename}",
			f"./_execute/asset/{to_filename}",
			f"./_execute/assets/{to_filename}",
			f"./_execute/files/{to_filename}",
			f"./_execute/data/{to_filename}",
			f"./_execute/res/{to_filename}",
			f"./_execute/resource/{to_filename}",
			f"./_execute/resources/{to_filename}"
		]
		if not os.path.exists(path):
			for fallback_dir in fallback_dirs:
				fallback_dir = to_path(fallback_dir)
				if os.path.exists(fallback_dir):
					path = fallback_dir
					break
		return os.path.normpath(path)
	except Exception as e:
		return ""
define_asset = to_asset = get_asset = new_asset = load_asset = naya_asset = asset
## belongs at the bottom of KL_Py.py
## a helper function for def= operator
def get_initial_of(x: Any) -> Any:
	if not x:
		return None
	out: Any
	match x:
		case "str":
			out = ""
		case "int":
			out = 0 
		case "flt" | "float" | "dbl" | "double" | "Number" | "nr":
													  # a number is both a float, and int
													  # lets just assume its a float
			out = 0.0
		case "bool" | "haal":
			out = False
		case "list":
			out = []
		case "tuple":
			out = ()
		case "set":
			out = {}
		case "Arr":
			out = Arr()
		case "numlist":
			out = numlist()
		case "intlist":
			out = intlist()
		case "fltlist":
			out = fltlist()
		case "dict" | "obj":
			out = obj()
		case _:
			out = None
	return out
# a helper constant for platform checks
WINDOWS: Final[str] = "nt"


def main() -> none:
	print(Int("100", 2))
	print(Flt("2.22"))
	print(Int(2.22))
	print(Flt(2.22))
	print(Int(2))
	print(Flt(2))
	dictionary: obj = obj(key="value")
	cloned = clone(dictionary)
	cloned.key = 4
	print(dictionary.entries())
	print(cloned.entries())
	name: lafz = "Misty"
	print(name)
	x: num = 4
	print(x)
	printf("$name dont! You are, but a $10+5-8 -year-old kid. $x")
	print(isstr(""))
	print(isint(3))
	print(isflt(""))
	print(isstr(None))
	print(isstr(None))
	print(isstr(None))
	print(isstr(None))
	print(isstr(None))
	print(isstr(None))
	print(isfunc(internet_access))
	print(flatten([1, [2, [3, 4, [5, 6]]]]))
	print(remove_duplicates([1, 3, 1, 5, 6, 3, 7, 8, 9]))
	print(kism(7.5))
	print(he_kism(7.5, float))
	printf("hi, $75000.77778:,")
	x = 12345.6789
	print(f("$x", "$x:.2f", f"{x:,}", f"{x:,.2f}"))
	array = intlist(1.4, 2.9, 3.5)
	array2 = fltlist(2, 4, 6)
	result = array * array2
	print(result)
	nlist: numlist = numlist(1, 3, 5, 7)
	print(nlist.push([9, 11]))
	array = Arr([1.2, 3, 5, 6, None, ""], fixed=False)
	array.me_dalo("x")
	array.me_dalo("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx0			xxx")
	print(f"{array=}")
	#pprint({"name": "Mike", "age": 17, "hobbies": ["horse riding", "country music", "farming"]})
	print(Msg, Message, Error, Err)
	@auto_id
	@auto_class
	class Book:
		name: str
		author: str
		release: int
	book1: Book = Book("To Kill A MockingBird", "Anonymous", 2003)
	book2: Book = Book("The Subtle Art of Not Caring", "Mark Manson", 2007)
	print(book1.name, book1.author, book1.release, book1.__id__, book1.__shanakht__)
	print(book1.name, book1.author, book1.release, book1.__id__, book1.__shanakht__)
	print(book2.name, book2.author, book2.release, book2.__id__, book2.__shanakht__)
	print(book2.name, book2.author, book2.release, book2.__id__, book2.__shanakht__)
	print(belongs_to(book1, Book))
	print(isinstance_each([IOError, OSError], (Exception | BaseException)))
	print(hissa(None, ["hello world", None]))
	print(belongs_to(IOError | OSError, Exception))
	print(chuno(rng(1, 10), koi=2))
	my_dict: dict[str, dict[str, str] | int] = {"name": {"first": "Mike", "last": "Dawson"}, "age": 22}
	print(deep_get(my_dict, "first"))
	
if __name__ == "__main__":
	main()

del globals()["main"]
# ^ NECESSARY EVIL
# removing this will have
# negative side effects on Klang