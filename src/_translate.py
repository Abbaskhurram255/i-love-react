import KL_Py
# ^ the import above is a MANDATORY import, and so is the following:
from KL_Py import *

__all__: list[str] = ["translate_for_react", "translate_for_css"]

def translate_for_css(code: str) -> str:
	if not isinstance(code, str):
		return ""
	keys: dict[str, str] = {
		# properties
		"fg|clr": "color",
		"mt": "margin-top",
		"mr": "margin-right",
		"mb": "margin-bottom",
		"ml": "margin-left",
		"m(?:ar)?gi?n?": "margin",
		"pt": "padding-top",
		"pr": "padding-right",
		"pb": "padding-bottom",
		"pl": "padding-left",
		"pa?d": "padding",
		"bsh(?:a?d(?:ow)?)?": "box-shadow",
		"tsh(?:a?d(?:ow)?)?": "text-shadow",
		"brad(?:ius)?": "border-radius",
		"brtl": "border-radius-top-left",
		"brtr": "border-radius-top-right",
		"brbr": "border-radius-bottom-right",
		"brbl": "border-radius-bottom-left",
		"bdt": "border-top",
		"bdr": "border-right",
		"bdb": "border-bottom",
		"bdl": "border-left",
		"bd": "border",
		"bsi?zi?n?g?": "box-sizing",
		"bbox": "border-box",
		"cbox": "content-box",
		# gradients
		"lg": "linear-gradient",
		"rg": "radial-gradient",
		r"s(?:i|ee)dhe[_ \-]ha{1,2}th": "to right",
		r"ulte[_ \-]ha{1,2}th": "to left",
		r"n(?:i|ee)ch(?:l|e[_ \-](?:k|wal))i[_\- ]tara?f": "to bottom",
		r"upar[_\- ](?:k|wal)i[_ \-]tara?f": "to top",
		# functions
		r"ki[\-\_]jaga": "url",
		# selectors
		"sab(?:[\-\_ ]?ka)?": "*",
	}
	code = replace(code, r"[\"']{3}([\s\S]*?)[\"']{3}", r"/*$1*/")
	strings: list[str] = find_matches(code, r"(?<![\"\\])(?:\"{3}|\"{1})[^\"]*(?:\"{1}|\"{3})(?!\")") + find_matches(code, r"(?<![\'\\])(?:\'{1}|\'{3})[^\'\"]*(?:\'{1}|\'{3})(?!\')") + find_matches(code, r"/\*[\s\S]*?\*/")
	for i, string in enumerate(strings):
		code = code.replace(string, f"__STRING_{i}__", 1)
	code = replace(code, r"[#:](?:def(?:ine)?|farz|var)\b", ":root")
	# keep the sequence AS-IS
	code = replace(code, r"@? *mangao *[\"\']?([\w\-\.\\\/]+)[\"\']?", "@import '$1'")
	# sequence matters
	for key, value in keys.items():
		code = replace(code, fr"(?<!\.)\b({key})\b", value)
	code = replace(code, "\t", " " * 4)
	code = replace(code, r" *\: *$(?!\\)(?=\n(?: {4,}|\t))", " {")
	# the fucking sequence matters
	code = replace(code, r" *\\$", "")
	code = replace(code, r"(?<!\S)\:?\/$", "}")
	code = replace(code, " *= *", ": ")
	code = replace(code, r"(?<![{}:,;\/\s()])(?<!^)(?<!\d__\b) *$", ";")
	code = replace(code, r"\bbg", "background") #intentionally, shouldn't be a word boundary at the end
	# units
	code = replace(code, r"(?<=\d)rm\b", "rem")
	code = replace(code, r"(?<=\d)dg\b", "deg")
	code = replace(code, r"^(?<some_whites_at_start>[ \t]+)?\$ *(?<varname>[A-Za-z_][\w\-]*)", "$some_whites_at_start--$varname")
	code = replace(code, r"\$ *(?<varname>[A-Za-z_][\w\-]*)", "var(--$varname)")
	while re.search(r"\b([A-Za-z]\w*) *_ *(?!STRING)([A-Za-z]\w*)\b", code):
		code = replace(code, r"\b(?<current>[A-Za-z]\w*) *_ *(?!STRING)(?<next>[A-Za-z]\w*)\b", "$current-$next")
	for j, string in old_enumerate(strings):
		code = code.replace(f"__STRING_{j}__", string)
	return code

def translate_for_react(code: str) -> str:
	if not isinstance(code, str):
		return ""
	keys: dict[str, str] = {
		# functions, and classes
		"dcm": "document",
		"qs": "document.querySelector",
		"qs[Aa](?:ll)?": "document.querySelectorAll",
		r"cls(?= *\=)": "className",
		r"cl(?:ic)?k(?= *\=)": "onClick",
		r"loc(?= *\=)": "src",
		r"alt[_\-]?[Tt]ext": "alt",
		"f[cn]": "function",
		r"n(?:a(?:ya|i))": "new",
		r"hamesha|musalsal": "const",
		r"koshish(?: karo)?": "try",
		r"naka{1,2}mi": "} catch",
		"__(?:str|print)__": "toString",
		"__(f(?:mt)?|k)__": "__format__",
		"c(?:ons)?tr": "constructor",
		"it": "this",
		"its": "this",
		"me": "this",
		"mera": "this",
		"apna": "this",
		"meri": "this",
		"mujhe": "this",
		# diff: capital first, not-capital first
		r"khud(?:[_ ]?k[aeio])?": "this",
		"my": "this",
		"mom": "super",
		r"ret|out|lota{1,2}o": "return",
		# math
		r"(?<=\S )div(?= \S)": "/",
		r"(?<=\S )times(?= \S)": "*",
		r"(?<=\S )tms(?= \S)": "*",
		r"(?<=\S )mul(?= \S)": "*",
		r"(?<=\S )guna(?= \S)": "*",
		r"(?<=\S )plus(?= \S)": "+",
		r"(?<=\S )pls(?= \S)": "+",
		r"(?<=\S )minus(?= \S)": "-",
		r"(?<=\S )mns(?= \S)": "-",
		# printing
		r"(?:kaho|print)(?= *\()": "console.log",
		# match-case
		r"aga?r[_ ]match(?= [^\n\t\:]+\:)": "switch",
		r"(?<=(?<!\w) {2})sath(?! (?:open|khola) ?\()": "case",
		# same keyword, different operations
		# if-else
		# sequence
		# no-colon else
		# comes first
		# ^ a shorter way to say `else: ret|return|out X|Y` would be `else ret|return|out X|Y` without a colon
		"othe?r?ws[_ ]?if|warna?[_ ]?agar": "else if",
		r"othe?r?ws(?![_ ]?if)|warna(?![_ ]?a?gar)": "else",
		"(?<!(?:but|par|(?<=wa)rna|(?<=e)l(?:se|if))[_ ])(?:agar|tab[_ ]jab)(?![_ ]match)": "if",
		# regular else
		# leave it as-is
		# sequence
		r"(?<=\S )\bchot[aei][_ ]ya[_ ]ba?ra?ba?r(?:[ _]hen?)?\b(?= \S)": "<=",
		r"(?<=\S )\bbar[aei][_ ]ya[_ ]ba?ra?ba?r(?:[ _]hen?)?(?= \S)": ">=",
		r"(?<=\S )\b(chot[aei](?:[_ ]hen?)?|is[_ ](?:less(?:er)?|s(?:mall|hort)er)[_ ]than)\b(?= \S)": "<",
		r"(?<=\S )\b(bar[aei](?![ _]ya)(?:[ _]hen?)?|is[_ ](?:large|bigg|great)er[_ ]than)\b(?= \S)": ">",
		# sequence!
		r"(?<=(?<!i|(?<=\bag)a|\bh|(?<=\bwar)n|(?<=\bel)[si]|(?<=\bna)h)[^ \=] )(?:nahi[ _]?(?:hen? )?(?:hen?|ba?ra?ba?r(?: hen?)?)?|(?:is|ai)n'?t)(?= +\S(?!(?:ndar|(?:ith)?n|nder|armya{1,2}n|eech|issa)\b))": "!=",
		# if it works, don't touch it
		# sequence
		# equality_keyword=he|brbr|barabar
		r"(?<=(?<!\bi|(?<=\bag)a|(?<=\bwar)n|(?<=\bel)[si]|(?<=\bna)h|(?<=\bpak)k|(?<=(?<=[wa])ak)a)\S )(?:(?:hen? )?(?:ba?ra?ba?r|hen?)(?: hen?)?)(?= +\S)": "==",
		# assignment_keyword=is (as long as it's not followed by ` *(not None|type|kism| *a| *an))`
		r"(?<=\S )\b(?:is|are|be|rakh[aeio]|ab)\b(?!(?: (?:not None|type|kism)| *an?))": "=",
		# strict equality operator: pakka he, wakai he
		r"(?<=\S )\b(?:pakka|wa{1,2}kai) (?:(?:hen? )?(?:ba?ra?ba?r|hen?)(?: hen?)?)\b(?= +\S)": "===",
		# sequence
		r"a(?:ur|nd)(?= +\S)": "&&",
		r"(?:ya|or)(?= +\S)": "||",
		r"(?:nahi|na[_ ]mojud|kha{1,2}li|(?:is|ai)n'?t)(?= \S)": "!",
		r"kuch(?= ?\()": "any",
		r"sa{1,2}re(?= ?\()": "all",
		"ja?bta?k": "while",
		r"har(?= *[A-Za-z_]\w*)": "for",
		"every": "for",
		r"(?<=\S )(?:andar|(?:with)?in|under|da?rmya{0,2}n|beech|hissa)(?= \S)": " in ",
		# tests needed, but keep the " in " as-is
		r"until(?= ?\()": "in range",
		r"(?:limit|da?rmya{0,2}n|b(?:et)?w(?:een)?)(?= *\()": "range",
		r"next(?= [^ \(])": "yield",
		r"(?<=(?<!\w) {2})ruko": "break",
		r"(?<=(?<!\w) {2})ignore(?= ?[^\(])": "continue",
		# ignore only translates to continue as long as it's indented
		# and ISN'T followed by a (
		# no messing around^
		r"(?<n>\d+) +dafa(?= *\:)": "for (let i=0; i<$n; i++)",
		r"baad(?= ?\()": "setTimeout",
		r"(with_i(?:ndex)?|numbered)(?= ?\()": "numbered",
		r"kism(?= *\()": "typeof",
		r"Shayad(?= ?\[[A-Za-z_])": "Union",
		r"(?:is|he)_?func(?= ?\()": "callable",
		r"[Cc]har(?= ?\()": "String",
		# * both sides are needed
		# ^^ much needed
		# char is the keyword user
		# will look for
		# when they would
		# actually mean Char
		# with a capital C
		# (i.e. the class 'Char' from KL_Py)
		"lafz|jumla": "String",
		# "jumle": "list[str]",
		"flt|d(?:ou)?ble?": "float",
		# "flts": "list[float]",
		# "floats": "list[float]",
		"Nr": "Number",
		# "Nrs": "list[Number]",
		"haal|filha{1,2}l": "bool",
		r"(?:[Yy]es|[Ss]ach|[Hh]an?(?! par))(?! *\()": "true",
		r"(?:[Nn]o|[Jj]hoot|[Nn]ahi)(?! *\()": "false",
		r"k(?:lang)?__(?:name|version)": "\"Klang v0.8\"",
		r"k(?:lang)?__about": r"''",
		# € implement help later
		r"uthao(?= [A-Za-z_])": "throw",
		r"akhir(?= ?\:)": "finally",
		r"(?<=(?<=\bn)akami|\bcatch) *tor (?<err_name>[A-Za-z_]\w*)": " ($err_name)",
		#"tor(?= [A-Za-z_])": "as",
	}
	# Remove comments
	# --- since they're only meant for the developer ---
	# to help us save memory,
	# and this removal of
	# multi-line comments
	# occurs before the 
	# replacement of strings
	# with placeholders
	# remove multi-line comments
	# single-line comments will be gotten rid of later
	# FOR A BIG REASON (being settings can contains hashes --- # --- too)
	multi_line_comments: list[str] = re.findall(r"(?:\= *[kflerb]*)?[\"\']{3}[\s\S]*?[\"\']{3}", code)
	# *? is used for LAZY matching (matching only one match at a time)
	# it's better if you DO NOT TOUCH THE REGEX
	for multi_line_comment in multi_line_comments:
		if multi_line_comment.startswith("="):
			# if it startswith an equals sign,
			# it must be a variable assignment
			# to a multi-line STRING, rather than
			# a comment
			continue
		unprocessed_multi_line_comment: str = multi_line_comment
		# storing the original comment for later
		processed_multi_line_comment: str = multi_line_comment[3:-3]
		processed_multi_line_comment = re.sub("[^\n]*\n[^\n]*", "\n", processed_multi_line_comment)
		code = code.replace(unprocessed_multi_line_comment, processed_multi_line_comment)
	# Remove strings (actual strings, now that multi-line comments are GONE)
	strings: list[str] = find_matches(code, r"(?<![\"\\])(?:\"{3}|\"{1})[^\"]*(?:\"{1}|\"{3})(?!\")") + find_matches(code, r"(?<![\'\\])(?:\'{1}|\'{3})[^\'\"]*(?:\'{1}|\'{3})(?!\')") + find_matches(code, r"(?<![\`\\])(?:\`{1}|\`{3})[^\`]*(?:\`{1}|\`{3})(?!\`)")
	# added partial support for apostrophe strings (strings initiated with an apostrophe, rather than quotes)
	for i, string in old_enumerate(strings):
		# for it to work,
		# this boolean check down here
		# has to stay in the loop's scope
		# and has to keep resetting on
		# every single iteration
		# and keep catching literal strings
		was_multi_line_string_initially: bool = False
		was_t_string_initially: bool = False
		if re.search(r"^[\"\']{3}(?=[\s\S]+)", strings[i]):
			strings[i] = strings[i][2:-2].replace("\n", "\\n")
			was_multi_line_string_initially = True
		if strings[i].startswith("`"):
			was_t_string_initially = True
		strings[i] = strings[i][1:-1]
		if len(strings[i]) == 1:
			# safety: let single characters pass through
			# to allow working with
			# single characters, and character ranges
			continue
		#if not was_t_string_initially:
		#	strings[i] = replace(strings[i], r"\$(\{\})", r"$1")
		# handle blank templates without throwing an error
		# WARNING: this changes core Python f-string functionality for {}
		# actually, for the sake of commas, and spaces (as the $-based syntax can mess them up), let's allow both
		# so the use has a choice to either:
		# print "Name is $name, Age is $age"
		# which is messed up, as the dollar recognizes the comma as part of the template --- resulting  in a tuple of `({{name}},)`
		# or they could do {{{varname}}} for the problematic template, or a template with spaces:
		# print "Name is {name}, Age is $age"
		# which WORKS
		# and results in "Name is {{name}}, Age is {{age}}"
		print(f"PRE, {strings[i]=}")
		strings[i] = "`" + replace(replace(strings[i], r"(?<!\\)\$\{?([^ \n\t]+)\}?", r"\${$1}####"), r"(?<=\})#{4}", "").replace("}}", "}") + "`"
		print(f"here, {strings[i]=}")
		# if the template strings is
		# escaped, leave it be,
		# so that
		# \$30
		# translates to
		# regular $30
		# and not 30
		# (parsed from the
		# evaluation of the
		# template string)
		strings[i] = strings[i].replace(r"\$", "$")
		# find the template strings, and if found, for each, post-process
		if re.search(r"\$\{?[^\}]+\}?", strings[i]):
				print("here")
				templates_found_in_string: list[str] = find_matches(strings[i], r"(?<!\\)\$\{?[^\},]+\}?")
				print(f"{templates_found_in_string=}")
				for templt in templates_found_in_string:
					# {sum (is|he)} should translate to
					# sum (is|he): {sum}
					print(f"here {templt=}")
					if re.search(r"[^\w:=]$", templt.strip("${}")):
						templt = "${" + re.sub(r"[^\w:=]+$", "", templt.strip("${}")) + "}"
					print(f"now {templt=}")
					processed_templt: str = replace(replace(templt, r"\$\{(?<placeholder_slash_varname>[^\{\} ]+)(?<! )(?: +(?<separator>is|hen?)|[\:\=]) *:? *\}", "$placeholder_slash_varname $separator: ${$placeholder_slash_varname}####"), "(?<!#)####(?!#)", "").replace("=:", ":").replace("::", ":").replace(" : ", ": ")
					# Warning: the 4-hashes part might seem ridiculous, BUT IS A BUG FIX, and better stay untouched
					for key, value in keys.items():
						processed_templt = replace(processed_templt, fr"(?<!\.)\b(({key})(?! ?\: ?\w+))\b", value)
					processed_templt = replace(processed_templt, r"(?<=\w )=(?=:)", "is")
					# ^ a bug fix
					strings[i] = replace(strings[i], re.escape(templt), processed_templt.replace("${", r"####{####")).replace("####{####", "${") # escaping here is mandatory
					# NOTE: the RE.ESCAPE part here, is NECESSARY
					# and allows template strings like "${2+3 he}", "${a+b he}"
					strings[i] = replace(strings[i], r"(?<=\S\.)\b_cl(?:as)?s_?name\b", "__class__.__name__")
					strings[i] = replace(strings[i], r"(?<=\S\.)\b_cl(?:as)?s\b", "__class__")
					# readable index access
					# sequence MATTERS
					# sequence is the only thing holding it together
					strings[i] = replace(strings[i], r"\[\.?(?:ba{1,2}d *\:?|har) *(?<n>\-?\d+)(?: ?(?:ke[_ ])?ba{1,2}d)?[ _\/\-]\d+\]", "[::$n]")
					strings[i] = replace(strings[i], r"\[\.?ba{1,2}d *\:? *(?<n>\-?\d+)\]", "[$n:]")
					# reversing
					strings[i] = replace(strings[i], r"\[\.?(?:k[aeio]\:?[_ ])?(?:ula?t[ai]?|rev(?:erse)?d?)\]", "[::-1]")
					# number-based mid slicing (rather than index-based)
					# comes before
					strings[i] = replace(strings[i], r"\[\.?(?:da?rmya{0,2}n|beech) *\: *(?<start>\-?\d+)(?:st|nd|rd|h?l[ae]|th|th?[ae]|s?r[ae]|w[ae])?(?:[,:~\-]| *(?:se|aur)) *(?<stop>\-?\d+)?(?:st|nd|rd|h?la|th|th?a|s?ra|wa)?(?:[, ]*(?:chor[_ ]?k?e|ba?ge?r))\]", "[$start-1 if $start > 0 else $start:$stop-1 if $stop > 0 else $stop]")
					# comes after {similar, but different:}
					strings[i] = replace(strings[i], r"\[\.?(?:da?rmya{0,2}n|beech) *\: *(?<start>\-?\d+)(?:st|nd|rd|h?l[ae]|th|th?[ae]|s?r[ae]|w[ae])?(?:[,:~\-]| *(?:se|aur)) *(?<stop>\-?\d+)?(?:st|nd|rd|h?la|th|th?a|s?ra|wa)?(?:[, ]*(?:rakhe|sha{1,2}mil))?\]", "[$start-1 if $start > 0 else $start:$stop]")
					strings[i] = replace(strings[i], r"\[\.?(?:(?:se|f(?:ir)?st|pehl(?:e|a))(?:[_ ]ke)?|shuru?(?:[_ ][smk]e|wa{1,2}ti)) *[\: ] *(?<n>\-?\d+)(?: tak)?\]", "[0:$n]")
					strings[i] = replace(strings[i], r"\[\.?(?:la?st|akhri|akhir)(?:[_ ]?[smk]e)? *[\: ] *(?<n>\d+)\b\]", "[-$n:]")
					strings[i] = replace(strings[i], r"\[(?:\.(?:f(?:ir)?st|pehla)|\.?1(?:st|h?la))\]", "[0]")
					strings[i] = replace(strings[i], r"\[(?:\.(?:sec(?:o|d|o?nd?)?|d(?:u|oo)sra)|\.?2(?:nd|s?ra))\]", "[1]")
					strings[i] = replace(strings[i], r"\[(?:\.(?:th(?:i|d|i?rd?)|t(?:i|ee)sra)|\.?3(?:rd|s?ra))\]", "[2]")
					strings[i] = replace(strings[i], r"\[\.?(?:(?:f(?:ir)?st|shuru?(?:wat)?(?:[_ ]?(?:i|(?:k|wal)a|me))?|n)\:)?(?<n>\d+)(?:st|nd|rd|h?la|th|th?a|s?ra|wa)\]", "[$n-1]")
					strings[i] = replace(strings[i], r"\[\.?(?:(?:la?st|a{1,2}kh(?:ir|ri)(?:[_ ]?(?:(?:k|wal)a|[sm]e))?|\-n)\:)(?<n>\d+)(?:st|nd|rd|h?la|th|th?a|s?ra|wa)\]", "[-$n]")
					# ^ catches arr[akhri:4tha]
					strings[i] = replace(strings[i], r"\[\.?(?<n>\d+)(?:st|nd|rd|h?la|th|th?a|s?ra|wa) (?:la?st|a{1,2}kh(?:ir|ri)(?:[_ ]?(?:(?:k|wal)a|[sm]e))?)\]", "[-$n]")
					# ^ catches arr[4tha akhri], same functionality, too different allowed orders for convenience
					strings[i] = replace(strings[i], r"\[(?:(?:(?:\.th(?:i|d|i?rd?))[_ ]?la?st)|\.?[t3](?:i|ee)?(?:s?ra|rd)[_ ]?(?:a{1,2}khri|la?st))\]", "[-3]")
					strings[i] = replace(strings[i], r"\[(?:(?:(?:\.sec(?:o|d|o?nd?)?|2nd)[_ ]?la?st)|\.?[d2](?:u|oo)?(?:s?ra|nd)[_ ]?(?:a{1,2}khri|la?st))\]", "[-2]")
					strings[i] = replace(strings[i], r"\[\.?(?:(?:f(?:ir)?st|pehla)|1(?:st|h?la))?[_ ]?(?:\.?(?:la?st|a{1,2}khri))\]", "[-1]")
					
					strings[i] = replace(strings[i], r"(?<=^\<)class(?= [\"\'][A-Za-z_][\w\.]*[\"\']\>$)", "kism:")
					# ^ meaning <class 'int'>  SHOULD BE  <kism 'int'>
					# dont mess around
					strings[i] = replace(strings[i], r"^(?<pre>\<(?:kism|class)\:? [\"\'])NoneType(?<post>[\"\']\>)$", "${pre}KoiNa${post}")
					strings[i] = replace(strings[i], r"^(?<pre>\<(?:kism|class)\:? [\"\'])float(?<post>[\"\']\>)$", "${pre}flt${post}")
					strings[i] = replace(strings[i], r"^(?<pre>\<(?:kism|class)\:? [\"\'])Number(?<post>[\"\']\>)$", "${pre}nr${post}")
					strings[i] = replace(strings[i], r"^(?<pre>\<(?:kism|class)\:? [\"\'])bool(?<post>[\"\']\>)$", "${pre}haal${post}")
					strings[i] = replace(strings[i], r"^\bNone\b$", "koi_na")
					strings[i] = replace(strings[i], r"^\bTrue\b$", "Han")
					strings[i] = replace(strings[i], r"^\bFalse\b$", "Nahi")
		# the #### part helps get rid of a bug
		# this replaces previously removed {formatted_var} functionality with new $-based functionality
		# WARNING: r"{$1}####" should be as is
		# the additional whitespace keeps the whole together
		# ^ needed as-is
		old_string = string
		# ^^this is a mandatory step
		if not was_t_string_initially and not "$" in old_string:
			# recognize literal strings
			# and return a non-processed
			# version of the string
			# if the `l"{{content}}"` handle is used
			strings[i] = old_string
			# ^^mandatory step
			strings[i] = replace(strings[i], "(?:(?<=^[A-Za-z])[ler]+|^[ler]+)(?=[A-Za-z]*[\"\'])", "")
			# now that the string is back to being its original version
			# ^ this replacement has to
			# take place again
		# auto-escape bad escapes (EXCEPT SPECIAL CHARACTERS LIKE newline \n, tabbreak \t, return carriage \r, backspace \b, vertical space \v, ASCII bell \a, form feed \f, escaped backslash \\, escaped quote \", escaped apostrophe \', among others.)
		# kill the need for r-strings
		# completely
		strings[i] = replace(strings[i], "(?:(?<=^[A-Za-z])[ler]+|^[ler]+)(?=[A-Za-z]*[\"\'])", "")
		strings[i] = replace(strings[i], r"(\\[^abfnrtv\\\'\"\nxuUN])", r"\\$1")
		code = code.replace(old_string, f"__STRING_{i}__", 1) # editor, here's a NOTE: if it works, DON'T touch it! should be `code.replace(old_string, ...`, i.e. just AS-IS, and NOT replace(strings[i], ...
		# ^ needed as-is
	#print(f"{code=}")
	# Replace context-based keywords
	# handling import cases
	# sequence matters!
	FOUR_WHITES: str = " " * 4
	# NOTE: now that strings have been gotten rid of entirely
	# --- i.e. multi-line comments ("""{content}""") have been replaced with "" {that is, removed}, and base strings ("") have been replaced with
	# their placeholders
	# so that we only translate keywords outside of a string, or a multi-line comment
	# we might as well get rid of single-line comments
	# which, we DIDN'T BEFORE...
	# AS STRINGS CAN CONTAIN
	# hashes (#'s') TOO
	code = replace(code, r"#[^\n]*", "")
	code = replace(code, "\t", FOUR_WHITES)
	code = replace(code, r"(?<= {4})(\.+|ba{1,2}d_?me|later|pass)(?![^\n])", "throw new Error('Function not implemented.')")
	code = replace(code, r"\:(?= *\n)", " {")
	code = replace(code, r"(?<!\S)\:?\/$", "}")
	code = replace(code, r"<\.(?! *\d)", "<div") #start of div
	code = replace(code, r"\.(?= *>(?! *\d))", "div") #end of div, functional
	code = replace(code, r"< *btn\b", "<button") #start of button
	code = replace(code, r"btn(?= *>(?! *\d))", "button") #end of button, functional
	while re.search(r"([A-Za-z]+)_([A-Za-z])(\w*)", code):
		code = re.sub(r"([A-Za-z]+)_([A-Za-z])(\w*)", lambda m: f"{m.group(1)}{m.group(2).upper()}{m.group(3).lower()}", code)
	# ^ was too needy for this
	# snake case to camelCase
	code = replace(code, r"(?<=(?<= {3}) |\t)\.{4,}(?![^\n])", "throw new Error('Function not implemented.')")
	# unlike Python, every ...{4,} should translate to ... as well, to allow forgiveness
	# so long as it's preceded by either a tab, or 4 spaces, AND ALSO followed by a
	# NON line-break character, to allow ranges to pass through, the following are the exceptions:
	# ....5, .1....5, 1..5, ..5, 2..10, 2..10 baad 2-2, 5..50::5

	__pretty_function_imports_regex__: str = r"^(?<intentionally_allow_some_space> *)\b(?<![^  \n  ])(?:tor|surat) (?<aliases>[A-Za-z_][\w, ]*) mangao (?<functions>[A-Za-z_\*][\w, \*]*)\b [\"'`]?(?<module>[A-Za-z\.][\w\.\\\/-]*)[\"'`]? (?:k[aei]|(?:me[_ ]?)?se)\b"
	def __pretty_function_imports_replacer__(match: re.Match) -> str:
		pre_whitespace_for_indented_imports: str = match.group("intentionally_allow_some_space")
		module: str|list[str] = match.group("module").rstrip(r".\\\/-")
		functions: str|list[str] = match.group("functions")
		aliases: str|list[str] = match.group("aliases")
		functions = [f.strip() for f in re.split(r", ?(?:(?:aur|(?:ke[_ ])?sath) )?", functions)]
		aliases = [a.strip() for a in re.split(r", ?(?:(?:aur|(?:ke[_ ])?sath) )?", aliases)]
		length: int = min(len(functions), len(aliases))
		functions_with_aliases: list[str] = [f"{functions[i]} as {aliases[i]}" for i in range(length)]
		result: str = pre_whitespace_for_indented_imports + ("import {" + ', '.join(functions_with_aliases) + "} from '" + module + "'")
		return result
	code = replace(code, __pretty_function_imports_regex__, __pretty_function_imports_replacer__)
	# ^ example of usage:
	# | tor DF mangao DataFrame pandas mese
	code = replace(code, r"^(?<intentionally_allow_some_space> *)(?<![^  \n  ])(?<module>[A-Za-z\.][\w\.\-\/]*)\b (?:me)?[_ ]?se mangao (?<functions>sab[_ ]kuch|[A-Za-z_\{\*][\w, \{\}\*]*)", "${intentionally_allow_some_space}import $functions from '$module'")
	# this one KNOWINGLY doesn't use work boundary at the start
	# to allow `.sublib mese mangao functions` to pass through
	# pretty useful if you are working with a __init__ file
	# ^ example of usage:
	# | pandas mese mangao DataFrame, read_csv
	code = replace(code, r"^(?<intentionally_allow_some_space> *)\b(?<![^  \n  ])mangao (?<functions>sab[_ ]kuch|[A-Za-z_\{\*][\w, \{\}\*]*) (?<module>[A-Za-z\.][\w\.\-\/]*)\b (?:me)?[_ ]?se\b", "${intentionally_allow_some_space}import $functions from '$module'")
	# ^ example of usage:
	# | mangao DataFrame, read_csv pandas mese
	# look similar, but are different
	__pretty_function_imports_regex_2__: str = r"^(?<intentionally_allow_some_space> *)\b(?<![^  \n  ])(?:tor|surat) (?<aliases>[A-Za-z_][\w, ]*) mangao (?<module>[A-Za-z\.][\w\.\\\/-]*)\b(?: (?:k[aei]|(?:me[_ ]?)?se))? ?(?:[\[\:]|->)? ?(?<functions>(?<!\.)[A-Za-z_\*\{][\w, \*\{\}]*)(?!\w)\]?"
	def __pretty_function_imports_replacer_2__(match: re.Match) -> str:
		pre_whitespace_for_indented_imports: str = match.group("intentionally_allow_some_space")
		module: str|list[str] = match.group("module").rstrip(".")
		functions: str|list[str] = match.group("functions")
		aliases: str|list[str] = match.group("aliases")
		functions = [f.strip() for f in re.split(r", ?(?:(?:aur|(?:ke[_ ])?sath) )?", functions)]
		aliases = [a.strip() for a in re.split(r", ?(?:(?:aur|(?:ke[_ ])?sath) )?", aliases)]
		length: int = min(len(functions), len(aliases))
		functions_with_aliases: list[str] = [f"{functions[i]} as {aliases[i]}" for i in range(length)]
		result: str = pre_whitespace_for_indented_imports + (f"import {', '.join(functions_with_aliases)} from '{module}'")
		return result
	code = replace(code, __pretty_function_imports_regex_2__, __pretty_function_imports_replacer_2__)
	# ^ example of usage:
	# | tor DF, rcsv mangao pandas[DataFrame, read_csv]
	code = replace(code, r"^(?<intentionally_allow_some_space> *)\b(?<![^  \n  ])mangao (?<module>[A-Za-z\.][\w\.\\\/-]*)\b(?: (?:k[aei]|(?:me[_ ]?)?se)) ?(?:[\[\:]|->)? ?(?<functions>sab[_ ]kuch|[A-Za-z_\*\{][\w, \*\{\}]*(?!\w))\]?", "${intentionally_allow_some_space}import $functions from '$module'")
	# ^ example of usage:
	# | mangao pandas[DataFrame]
	__pretty_module_imports_regex__: str = r"^(?<intentionally_allow_some_space> *)\b(?<![^  \n  ])(?:tor|surat) (?<aliases>[A-Za-z_][\w, ]*) mangao (?<modules>[A-Za-z_\.][\w\., ]*)\b"
	def __pretty_module_imports_replacer__(match: re.Match) -> str:
		pre_whitespace_for_indented_imports: str = match.group("intentionally_allow_some_space")
		modules: str|list[str] = match.group("modules")
		aliases: str|list[str] = match.group("aliases")
		modules = [m.strip() for m in re.split(r"\.*,+ *(?:(?:aur|(?:ke[_ ])?sath) )?", modules)]
		aliases = [a.strip() for a in re.split(r", ?(?:(?:aur|(?:ke[_ ])?sath) )?", aliases)]
		length: int = min(len(modules), len(aliases))
		result: str = pre_whitespace_for_indented_imports + ("; ".join(f"import {modules[i]} as {aliases[i]}" for i in range(length)))
		return result
	code = replace(code, __pretty_module_imports_regex__, __pretty_module_imports_replacer__)
	# ^ example of usage:
	# | tor pd, np mangao pandas, numpy
	# comes after\/
	__default_imports_regex__: str = r"^(?<intentionally_allow_some_space> *)\b(?<![^  \n  ])mangao (?<modules>[A-Za-z\_\.\"\'\/][\w\., \"\'\/]*)(?!\w)"
	def __default_imports_replacer__(match: re.Match) -> None:
		module_string: str = match.group("modules")
		modules: list[str] = [m.strip(" \'\"") for m in re.split(r", *(?:(?:aur|(?:ke[_ ])?sath) )?", module_string)]
		result: str = ""
		for m in modules:
			if "." not in m:
				result += f"import {m} from '{m.lower()}'; "
				continue
			result += f"import '{m}'; "
		return result
	code = replace(code, __default_imports_regex__, __default_imports_replacer__)
	# ^ example of usage:
	#| mangao pandas
	# sequence matters!
	# post processing module syntax
	# which NOW HAS KEYWORD IMPORT instead of mangao
	code = replace(code, r"\b(?<=import )sabKuch\b", "*")
	code = replace(code, r"(?<=,) \b(?:a(?:nd|ur)|ya|(?:ke[_ ]?)?sath)\b", "")
	# sequence matters!
	code = replace(code, r"(?<![\t\t])\b(?:f[cn]|act|def) (?:main|start)(?:\([^\)\n\t]*\))?(?=(?: *-> *[\w\?]+)?\:)", "function main()")
	# operators
	# try..else
	code = replace(code, r"\b(?:try|koshish)(?: karo)? (?<x>[^\n]+) (?:else|warna|naka{1,2}mi(?: p(e|ar))?) (?<y>[^\n]+)\b", "try_else(() -> $x, $y)")
	# the if[cn]ONDITION(is true, then)=
	code = replace(code, r"(?<A>[_A-Za-z]\w*) (?:if|agar) ?(?<condition>[^\=\n\t]+)\= ?(?<B>[^\n\t]+)", "$A = $B if not('$A' in globals() or '$A' in locals()) or $A == $condition else $A")
	# the min= operator
	code = replace(code, r"(?<A>[_A-Za-z]\w*) min *\={1}(?!\=) *(?<B>[^\n\t]+)", "$A = $B if '$A' in globals()|locals() and ((isinstance($A, (int, float)) and $A < $B) or (not isinstance($A, (int, float)))) else $A if '$A' in globals()|locals() and isinstance($A, (int, float)) else $B")
	# the max= operator
	code = replace(code, r"(?<A>[_A-Za-z]\w*) max *\={1}(?!\=) *(?<B>[^\n\t]+)", "$A = $B if '$A' in globals()|locals() and isinstance($A, (int, float)) and $A > $B else $A if '$A' in globals()|locals() and isinstance($A, (int, float)) else 0")
	# the (def|fb)= operator
	code = replace(code, r"(?<A>[_A-Za-z]\w*) (?:def|fb|othe?r?ws) *\={1}(?!\=) *(?<B>[^\n\t]+)", "$A = $B if not('$A' in globals() or '$A' in locals()) or not $A or type($A) != type($B) else $A")
	# the ^t `^{initial_type}=` operator
	# /made for strs \ | /
	# comes before
	# WARNING: since 'is' is a reserved keyword
	# 'is None' no longer works
	# had to use ' ... he None' here
	# which works fine \ | /
	# changing the 'he' back to 'is' ONLY BREAKS the code
	code = replace(code, r"(?<varname>[A-Za-z]\w*) (?:[\^\&][tk]|[\^\&]?(?:za?ba?r(?:da?sti)?|force)) ?\= ?str\b", "$varname = '' if not('$varname' in globals() or '$varname' in locals()) or $varname he None else Str($varname)")
	# /made for ints \ | /
	# comes after
	code = replace(code, r"(?<varname>[A-Za-z]\w*) (?:[\^\&][tk]|[\^\&]?(?:za?ba?r(?:da?sti)?|force)) ?\= ?int\b", "$varname = 0 if not('$varname' in globals() or '$varname' in locals()) or not $varname or not isinstance($varname, (str, int, float)) else Int($varname)")
	# /made for floats \ | /
	# comes after
	code = replace(code, r"(?<varname>[A-Za-z]\w*) (?:[\^\&][tk]|[\^\&]?(?:za?ba?r(?:da?sti)?|force)) ?\= ?(?:fl(?:oa)?t|d(?:ou)?ble?|Number|nr)\b", "$varname = 0.0 if not('$varname' in globals() or '$varname' in locals()) or not $varname or not isinstance($varname, (str, int, float)) else Flt($varname)")
	# /made for other types \ | /
	# comes at last
	code = replace(code, r"\b(?<varname>[_A-Za-z]\w*) (?:[\^\&][tk]|[\^\&]?(?:za?ba?r(?:da?sti)?|force)) ?\= ?(?<type>[A-Za-z_]\w*)\b", "$varname = get_initial_of('$type') if not('$varname' in globals() or '$varname' in locals()) or not $varname or not isinstance($varname, $type) else $varname")
	# glitchy self-assignment operator
	def __self_assignment_operations_replacer__(match: re.Match) -> str:
		varname: str|list[str] = match.group("varname")
		re_value_group: str = match.group("values")
		result: str = ""
		if not "," in re_value_group:
			value: str = re_value_group[1:-1]
			result += f"{varname}={value}; "
			return result.strip()
		values = re.split(r", *(?=[\-\.\w])", re_value_group)
		for value in values:
			if not value:
				continue
			if value.startswith("("):
				value = value[1:]
			if re.search(r"(?<=[\-\.\w\)])\)$", value):
				value = value[:-1]
			result += f"{varname}={value}; "
		result = result.strip()
		return result
	# self-assignment parser
	code = replace(code, r"(?<varname>[_A-Za-z]\w*) ?:: ?(?<values>\([^\n\t]+\))", __self_assignment_operations_replacer__)
	# handle increment
	# comes before
	code = replace(code, r"\b(?<varname>[A-Za-z]\w*) (?:me (?<val>[\w\-\.]+\b)(?: k[ao])? (?:(?:barht?a?|da{1,2}l)(?:o|t?[aei] (?:rah|ja|chal)[eo])|izafa)(?: (?:hot[ai]?|karte)(?: (?:rah|ja|chal)[eo]))?)\b", "$varname+=$val")
	# after
	code = replace(code, r"\b(?<varname>[A-Za-z]\w*)(?:\+{2}|(?: (?:me|k[ao]))? (?:(?:barht?a?|da{1,2}l)(?:o|t?[aei] (?:rah|ja|chal)[eo])|izafa)(?: (?:hot[ai]?|karte)(?: (?:rah|ja|chal)[eo]))?\b)", "$varname+=1")
	# handle decrement
	# comes before
	code = replace(code, r"\b(?<varname>[A-Za-z]\w*) (?:me(?:[_ ]?se)? (?<val>[\w\-\.]+\b)(?: k[aoi])? (?:(?:ghat{1,2}a?|kam ho|nika{1,2}l)(?:o|t?[aei] (?:rah|ja|chal)[eo])|ghata|kami?)(?: (?:hot[ai]?|karte)(?: (?:rah|ja|chal)[eo]))?)\b", "$varname-=$val")
	# after
	code = replace(code, r"\b(?<varname>[A-Za-z]\w*)(?:\-{2}|(?: (?:k[aoi]|me[_ ]?(?:se)?))? (?:(?:ghat{1,2}a?|kam ho|nika{1,2}l)(?:o|t?[aei] (?:rah|ja|chal)[eo])|ghata|kami?)(?: (?:hot[ai]?|karte)(?: (?:rah|ja|chal)[eo]))?\b)", "$varname-=1")
	# SEQUENCE MATTERS
	# IT DOES!
	# section for membership checks
	# handling `A me B`, and `B A me` cases
	# First, let's handle A-me-B checks
	# non-negated versions come before
	# \/ A-me-nahi-B (negation v1)
	code = replace(code, r"(?<A>(?:[\w\-\.]+|[\[\"\'](?:[\"\'\w\-\., ][\]]*)+[\]\"\'])) (?:me|ke_(?:beech|da?rmya{0,2}n))(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)? nahi(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)? (?<B>(?:[\[\"\'](?:[\"\'\w\-\.,][\]]*)+[\]\"\']|[\w\-\.]+))(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)?\b", "!($B in $A)")
	# bonus negation (negation v2 \|/ )
	# \/ A-me-B-nahi
	code = replace(code, r"(?<A>(?:[\w\-\.]+|[\[\"\'](?:[\"\'\w\-\., ][\]]*)+[\]\"\'])) (?:me|ke_(?:beech|da?rmya{0,2}n))(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)? (?<B>(?:[\[\"\'](?:[\"\'\w\-\.,][\]]*)+[\]\"\']|[\w\-\.]+))(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)? nahi\b", "!($B in $A)")
	# and then the regular
	# A-me-B \/
	code = replace(code, r"(?<A>(?:[\w\-\.]+|[\[\"\'](?:[\"\'\w\-\., ][\]]*)+[\]\"\'])) (?:me|ke_(?:beech|da?rmya{0,2}n))(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)? (?<B>(?:[\[\"\'](?:[\"\'\w\-\.,][\]]*)+[\]\"\']|[\w\-\.]+))(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)?\b", "$B in $A")
	# and now let's handle A-me-B checks
	# negated versions come before
	code = replace(code, r"(?<B>(?:[\[\"\'](?:[\"\'\w\-\.,][\]]*)+[\]\"\']|[\w\-\.]+))(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)? nahi(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)? (?<A>(?:[\w\-\.]+|[\[\"\'](?:[\"\'\w\-\., ][\]]*)+[\]\"\'])) (?:me|ke_(?:beech|da?rmya{0,2}n))(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)?\b", "!($B in $A)")
	# \^^^/ bonus negation (negation v1): B-nahi-A-me
	# as compared to
	# \V/ B-A-me-nahi (negative v2 down below \|/ )
	code = replace(code, r"(?<B>(?:[\[\"\'](?:[\"\'\w\-\.,][\]]*)+[\]\"\']|[\w\-\.]+))(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)? (?<A>(?:[\w\-\.]+|[\[\"\'](?:[\"\'\w\-\., ][\]]*)+[\]\"\'])) (?:me|ke_(?:beech|da?rmya{0,2}n))(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)? nahi(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)?\b", "!($B in $A)")
	# and then the regular
	code = replace(code, r"(?<B>(?:[\[\"\'](?:[\"\'\w\-\.,][\]]*)+[\]\"\']|[\w\-\.]+))(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)? (?<A>(?:[\w\-\.]+|[\[\"\'](?:[\"\'\w\-\., ][\]]*)+[\]\"\'])) (?:me|ke_(?:beech|da?rmya{0,2}n))(?:(?: hen?)?(?: (?:mojud|shamil)(?: hen?)?|hen?)?)?\b", "$B in $A")
	# section for ranges
	code = replace(code, r"(?<=[A-Za-z_]) ?(\.\.(?!\.)) ?(?=[^\:]+\:)", " in ")
	# the numA .. num
	# numeric ranges
	# comes before\/
	code = replace(code, r"(?<!(?<!\.)\.)(?<n1>\-?\d*\.?\d+) ?(?:\.\.|se) ?(?<n2>\-?\d*\.?\d+)(?: ?(?:\:\:|step|kadam|gap|ba{1,2}d|har(?= ?\d+ ?ke_ba{1,2}d)) ?(?<step_optional>\d+)(?: ?ke[_ ]ba{1,2}d)?[ _\/\-]?\d*)?(?: ke[_ ]lie)?", "range($n1, $n2, $step_optional)")
	# comes after\/
	code = replace(code, r"(?<!\d|(?<!\.)\.)(?:\.\. ?(?<n>\-?\d*\.?\d+))", "range($n)")
	# character ranges
	# comes before\/
	code = replace(code, r"(?<charA>[\"\']\w[\"\']) ?(?:\.\.|se) ?(?<charB>[\"\']\w[\"\'])(?: ?(?:\:\:|step|kadam|gap|ba{1,2}d|har(?= ?\d+ ?ke_ba{1,2}d)) ?(?<step_optional>\d+)(?: ?ke[_ ]ba{1,2}d)?[ _\/\-]?\d*)?(?: ke[_ ]lie)?", "range($charA, $charB, $step_optional)")
	# comes after\/
	code = replace(code, r"(?<![\w\"\']|(?<!\.)\.)(?:\.\. ?(?<char>[\"\']\w[\"\']))", "range($char)")
	# ..{list} -> *{list}
	# sequence
	code = replace(code, r"(?<![\.\d]|(?<!,) )\.{2,} ?(?<object>[\"']?[_A-Za-z]\w*[\"']?)", "...$object")
	# handling mathematical operations
	# SEQUENCE MATTERS
	code = replace(code, r"(?<A>\-?\d*\.?\d+) *\^{3}", "$A^3")
	code = replace(code, r"(?<A>\-?\d*\.?\d+) *\^{2}", "$A^2")
	code = replace(code, r"(?<A>\-?\d*\.?\d+) \%(?! *[\-\.\d])", "$A/100")
	code = replace(code, r"√ ?(?<A>\-?\d*\.?\d+)", "parseInt($A^(1/2))")
	#Number system
	code = replace(code, r"(?<=\d) ?z(?<exponent>[\+\-]?\d+)\b", "e$exponent")
	code = replace(code, r"(?<=\d) ?(?:[\*_]|times|guna|mul)? ?so\b", f"*1{'0'*2}")
	code = replace(code, r"(?<=\d) ?(?:[\*_]|times|guna|mul)? ?hazar\b", f"*1{'0'*3}")
	code = replace(code, r"(?<=\d) ?(?:[\*_]|times|guna|mul)? ?la{1,2}(?:c|kh)\b", f"*1{'0'*5}")
	code = replace(code, r"(?<=\d) ?(?:[\*_]|times|guna|mul)? ?million\b", f"*1{'0'*6}")
	code = replace(code, r"(?<=\d) ?(?:[\*_]|times|guna|mul)? ?crore?\b", f"*1{'0'*7}")
	code = replace(code, r"(?<=\d) ?(?:[\*_]|times|guna|mul)? ?hund(?:o|red) ?(?:[\*_]|times|guna|mul)? ?million\b", f"*1{'0'*8}")
	code = replace(code, r"(?<=\d) ?(?:[\*_]|times|guna|mul)? ?(?:ara?b|billion)\b", f"*1{'0'*9}")
	code = replace(code, r"(?<=\d) ?(?:[\*_]|times|guna|mul)? ?(?:kharab|hund(?:o|red) ?(?:[\*_]|times|guna|mul)? ?billion)\b", f"*1{'0'*11}")
	code = replace(code, r"(?<=\d) ?(?:[\*_]|times|guna|mul)? ?trillion\b", f"*1{'0'*12}")
	# come before
	# KEEP the sequence
	# comes after
	# to avoid conflict
	code = replace(code, r"(?<!\w)(?<nA>\-?\d*\.?\w+) in (?<nB>\-?\d*\.?\d+)\b", "($nA/$nB)")
	code = replace(code, r"(?<!\w)(?<n>\-?\d*\.?\w+) (?:ka a{1,2}thwa|eighth|into eight)\b", "(.125*$n)")
	code = replace(code, r"(?<!\w)(?<n>\-?\d*\.?\w+) (?:ka chotha|(?:in )(quarter|four)|quartered|fou?rth)\b", "(.25*$n)")
	code = replace(code, r"\b(?:adh[aei]|hal(?:ved|f[ _](?:of|as))) (?<n>\-?\d*\.?\w+)\b", "(.5*$n)")
	code = replace(code, r"(?<!\w)(?<n>\-?\d*\.?\w+) (?:ka adha|halved|in (?:two|half))\b", "(.5*$n)")
	code = replace(code, r"\bpon[ae] (?<n>\w+)\b", "(-.25+$n)")
	code = replace(code, r"\bsawa (?<n>\w+)\b", "(.25+$n)")
	code = replace(code, r"\bsa{1,2}dhe (?<n>\w+)\b", "(.5+$n)")
	code = replace(code, r"\b(?:twice(?:[_ ]as)?|d[uo] ?gu?n[aei]) (?<n>\-?\d*\.?\w+)\b", "(2*$n)")
	code = replace(code, r"(?<!\w)(?<n>\-?\d*\.?\w+)( ka)? (?:twice|d[uo] ?gu?n[aei])\b", "(2*$n)")
	code = replace(code, r"\b(?:thrice(?:[_ ]as)?|teen gun[aei]) (?<n>\-?\d*\.?\w+)\b", "(3*$n)")
	code = replace(code, r"(?<!\w)(?<n>\-?\d*\.?\w+)( ka)? (?:thrice|teen gun[aei])\b", "(3*$n)")
	code = replace(code, r"(?<!\w)(?<n>\-?\d*\.?\w+) (?:cha{1,2}r|4) gu?n[aei]\b", "(4*$n)")
	code = replace(code, r"(?<!\w)(?<n>\-?\d*\.?\w+) (?:a{1,2}th|8) gu?n[aei]\b", "(8*$n)")
	#code = replace(code, r"(?<!\w)\(?(?<params>(?:[A-Za-z_\.][\w\.]*(?:, *)?)*)\)? ?\->(?= ?\S)", "($params) =>")
	code = replace(code, r"->", "=>")
	# the actual support for `x ->` 
	#code = replace(code, r"\b(?:f[cn]|act) (?<param>[A-Za-z_]\w*)(?=\: ?[^\n]{2,})", "$param")
	# helps drop the parentheses if the function doesn't allow parameters
	# f[cn] log: -> f[cn] log():
	code = replace(code, r"\b(?:f[cn]|act) (?<funcname_followed_not_by_parens>[A-Za-z_]\w*)(?=(?<could_have_a_return_type>[^\(\)\{]+)?\{)", "function $funcname_followed_not_by_parens()")
	code = replace(code, r"\b(?:f[cn]|act) (?<funcname_regular>[A-Za-z_]\w*)\((?<params>[^\)]+)?\)(?=(?<could_have_a_return_type>[^\:]+)?\:)", "function $funcname_regular($params)")
	# "metaclass" is a keyword argument for the base class
	# to avoid conflict
	# comes before ^
	# comes after \/
	# replace "cls" with "class"
	# to make the future replacements
	# easier
	# also, replace "cls" with "class"
	# ONLY IF the user is not working
	# on a @classmethod
	# to avoid conflict
	code = replace(code, r"(?<=\S\.)\b_cl(?:as)?s_?name\b", "__class__.__name__")
	code = replace(code, r"(?<=\S\.)\b_cl(?:as)?s\b", "__class__")
	code = replace(code, r"@calls?[_ ]?me\b", "@classmethod")
	code = replace(code, r"@(?:abstr(?:act)?|follow|emp?ty?_?body)\b", "@abstractmethod")
	code = replace(code, r"@auto(c(?:l(?:as)?s|(?:ons)?tr)|make)\b", "@dataclass")
	# the key-value pair does not remove anything preceded by a ., so...
	code = replace(code, r"(?<=[\w\)]\.)call\b(?=\()", "__init__")
	# sequence matters
	# \/ handle (?<=(?:cls|class) )`B (of|from|>|ext(ends)?|is_?an?) A` cases
	code = replace(code, r"(?<=\bclass )(?<B>\w+)(?: (?:of|from|ext(?:ends)?|impl(?:em(?:ents)?)?|follows|is[ _]?an?) | ?[>\/] ?)(?<A>(?:\w+(?:, *)?)+)\b", "$B($A)")
	# \/ handle (?<=(?:cls|class) )`A [\.>] B` cases
	code = replace(code, r"(?<=\bclass )(?<A>(?:\w+(?:, *)?)+) (?:produces?|peda karen?|jana?m den?) (?<B>\w+)(?: ko)?\b", "$B($A)")
	code = replace(code, r"\benum (?<enumclassname>\w+)", "class $enumclassname(Enum)")
	code = replace(code, r"(?<varname>[\[\{\"\']{1,2}(?:[\-\.\w\"\' ](?:, *)?)+[\]\}\"\']{1,2}|[A-Za-z_][\w\.]*(?:\(\))?)\.\b(?<replacement_method>replace(?:_first)?)\(", "$replacement_method($varname, ")
	# >> custom starts_with, and ends_with, that work with arrays as well
	code = replace(code, r"(?<varname>[\[\{\"\']{1,2}(?:[\-\.\w\"\' ](?:, *)?)+[\]\}\"\']{1,2}|[A-Za-z_][\w\.]*(?:\(\))?)\.\b(?:starts_?with)\(", "startswith($varname, ") #custom, comes from KL_Py
	code = replace(code, r"(?<varname>[\[\{\"\']{1,2}(?:[\-\.\w\"\' ](?:, *)?)+[\]\}\"\']{1,2}|[A-Za-z_][\w\.]*(?:\(\))?)\.\b(?:ends_?with)\(", "endswith($varname, ") #custom, comes from KL_Py
	code = replace(code, r"(?<varname>[\[\{\"\']{1,2}(?:[\-\.\w\"\' ](?:, *)?)+[\]\}\"\']{1,2}|[A-Za-z_][\w\.]*(?:\(\))?)\.\b(?:is_?(?:sent(?:ence)?_?case|sentn?[cs]s?))\(\)", "is_sentence_case($varname)")
	code = replace(code, r"(?<varname>[\[\{\"\']{1,2}(?:[\-\.\w\"\' ](?:, *)?)+[\]\}\"\']{1,2}|[A-Za-z_][\w\.]*(?:\(\))?)\.\b(?:sent(?:ence)?_?case|sentn?[cs]s?)\(\)", "sentence_case($varname)")
	code = replace(code, r"(?<varname>[\[\{\"\']{1,2}(?:[\-\.\w\"\' ](?:, *)?)+[\]\}\"\']{1,2}|[A-Za-z_][\w\.]*(?:\(\))?)\.\b(?:is_?(?:snake_?case))\(\)", "is_snake_case($varname)")
	code = replace(code, r"(?<varname>[\[\{\"\']{1,2}(?:[\-\.\w\"\' ](?:, *)?)+[\]\}\"\']{1,2}|[A-Za-z_][\w\.]*(?:\(\))?)\.\b(?:snake_?case)\(\)", "snake_case($varname)")
	code = replace(code, r"\blambai (?<iterable>[\[\{\"\']{1,2}(?:[\-\.\w\"\' ](?:, *)?)+[\]\}\"\']{1,2}|[A-Za-z_][\w\.]*(?:\(\))?)", "lambai($iterable)" if "lambai" in {**globals(), **locals()} and isinstance(lambai, Callable) else "${iterable}.length")
	# don't touch it
	# doesn't need a work boundary ^
	code = replace(code, r"(?<varname>[\[\{\"\']{1,2}(?:[\-\.\w\"\' ](?:, *)?)+[\]\}\"\']{1,2}|[A-Za-z_][\w\.]*(?:\(\))?)\.\b(?:ki_?)?(?:len(?:gth)?|lambai|size)\b(?! *\()", "lambai($varname)" if "lambai" in {**globals(), **locals()} and isinstance(lambai, Callable) else "${varname}.length")
	# don't change this\/
	# the ^\n part stays as-is
	# the negated version comes before,
	# to avoid conflict
	code = replace(code, r"(?<A>[\-\.\w,\"'\[\]]+) (?:not|nahi) (?:instance[ _]?of|(?:is[ _]?)an?|he[_ ]ek|(?:is|he|ki|has|of)?[ _]?(?:type|kism)(?:of)?) (?<B>[\"'][A-Za-z_][\w\.\|]*[\"'])", "typeof($A) != $B")
	code = replace(code, r"(?<A>[\-\.\w,\"'\[\]]+) (?:instance[ _]?of|(?:is[ _]?)an?|he[_ ]ek|(?:is|he|ki|has|of)?[ _]?(?:type|kism)(?:of)?) (?<B>[\"'][A-Za-z_][\w\.\|]*[\"'])", "typeof($A) == $B")
	code = replace(code, r"\b(?:print|kaho) (?<args>[^\(\)\{\}\t\n]+)?", "console.log('' + $args)")
	code = replace(code, r",? <?(?:(?:might|shayad) (?:throw|raise|de|uthae)|(?:throw|raise)s|uthae) [^\:\n\t]+>?(?=\:)", "")
	# ^ supposedly after a function f[cn] x({...}?) might throw SomeError, and before a colon
	code = replace(code, r"\bfarz\b", "let")
	code = replace(code, r"\b(?:farz|lo|either|yato|kisi) ", "")
	code = replace(code, r"(?<=\w )\b(?:present|mojud) (?=\S)", "")
	code = replace(code, r" (?:(?<=[\w\"\'] )se(?=(?: tabtak)? ?\:)|to|tak|tabtak(?= ?\:)|hua|k[aeio](?:[_ ]?lie)?)\b", "")
	code = replace(code, r"\b(?:collect(?:ed)?|together|ikhat{1,2}e)\((?<params>(?<firstparam>[^\(\)]+), *(?<restofparams>[^\(\)]+))\)", "collect($params)" if "collect" in {**globals(), **locals()} and callable({**globals(), **locals()}["collect"]) else "list(zip($params))")
	# sequence matters
	# core
	code = replace(code, r"\bf(?=__STRING_\d+__)", "")
	# sequence matters
	code = replace(code, r",(?= ?\b(?:tor|as)\b)", "")
	# adds a sprinkle of English-like flavor: with open(x, "r") as file [bad] -> with open(x, "r"), as file [better, or at least a little more readable]
	code = replace(code, r"\{(?:\.{3}|\*{1,2})\} *= *(?<obj>[A-Za-z]\w*)", "globals().update(**$obj)")
	def __destructure_objects__(match):
		keys = [k.strip() for k in match.group(1).split(',') if k]
		keys_with_aliases: list[str] = keys.copy()
		for i, _ in old_enumerate(keys):
			keys[i] = replace(keys[i], r"tor ([A-Za-z_]\w*) ([A-Za-z_]\w*)", r"$2 as $1")
			if re.search(r"(?<=\w)(?: (?:as|tor) | ?\: ?)(?=[A-Za-z_])", keys[i]):
				parts = split(keys[i], r"(?: (?:as|tor) | ?\: ?)")
				keys[i] = parts[0]
				keys_with_aliases[i] = parts[1]
			if keys_with_aliases[i].startswith("...") and len(keys_with_aliases[i]) > 3:
				keys_with_aliases[i] = f"**{keys[i][3:]}"
			if keys_with_aliases[i].startswith("**"):
				keys[i] = keys[i].lstrip("**")
				keys_with_aliases[i] = keys_with_aliases[i].lstrip("**")
		obj: str = match.group(2)
		lhs: str = ", ".join(keys_with_aliases)
		rhs: str = ", ".join(f"{obj}?.{k}" if k not in ("keys", "values", "items") else (f"{obj}.{k}() if '{obj}' in " + "{**globals(), **locals()}" + f" and isinstance({obj}, dict) else " + "{}") for k in keys)
		rhs = replace(rhs, r"([A-Za-z_]\w*\.items\(\))", "[list(tuple) for tuple in list($1)]")
		new_pair: str = lhs + " = " + rhs
		return new_pair
	code = replace(code, r"\{([A-Za-z\*][, \w\*\:]*)\} *= *([A-Za-z]\w*)", __destructure_objects__)
	# sequence should be watched
	# this comes after the destruction, to see if the destructured value even exists or not:
	code = replace(code, r"(?<object>[_A-Za-z]\w*)\?\.(?<field>[_A-Za-z]\w*)", "$object.$field if ('$object' in globals() or '$object' in locals()) and hasattr($object, '$field') and $object.$field is not None else {}")
	code = replace(code, r"\b(?:neither|nato) (?<A>[^\n\t]+) (?:or )?(?:n?or|na(?:[ _]?hi)?) (?<B>[^\n\t]+)", "!($A or $B)")
	code = replace(code, r"(?<=(?<![^ \t])[ \t])(?:is|he|kism) (?<type>(?:[A-Za-z]\w*\.?)+)\b(?=(?: (?:as|tor) [A-Za-z_]\w*)?\:)", "case $type()")
	# KEY-VALUE replacement
	for key, value in keys.items():
		code = replace(code, r"(?<!\.)\b(" + key + r"(?! ?\: ?\w+))\b", value)
	code = replace(code, r"(?<type>[A-Za-z]*\w*\.?[A-Za-z]\w*)(?:\[\]|<list>)", "list[$type]")
	# int[] -> list[int]
	# int<list> -> list[int]
	# comes before
	code = replace(code, r"(?<!\w )(?:type|kism) ?\< ?(?<type>[A-Za-z\?][\w\[\]\|\?\. ]*) ?\>", "$type")
	# SEQUENCE
	# this comes after
	# similar, but different
	code = replace(code, r"(?<=\w) (?:type|kism) ?\< ?(?<type>[A-Za-z\?][\w\[\]\|\?\. ]*) ?\>", ": $type")
	# watch the sequence
	code = replace(code, r"(?<=\=) *(?:not|nahi)(?=\n)", "false")
	# relies ultimately on the positive lookahead (?= ?\=)
	# `type x=` = `x: type=`
	# needed
	#code = replace(code, r"(?<type>[_A-Za-z\?][\w\[\]\.\|\?]*) (?<varname>[_A-Za-z]\w*) ?\={1}(?!\=)", "$varname: $type =")
	code = replace(code, r"\b(?<varname>[_A-Za-z]\w*) (expects|ume{0,2}d|chah(?:e|ta)|wants|mange|needs) (?<type>[_A-Za-z\?][\w\[\]\.\|\?]*)", "$varname: $type")
	# handling Optionality: default, and null cases
	# <type>? means the type is optional
	code = replace(code, r"(?<=\S )\bkwarg\b(?= *[,\)])", "= null")
	# DON'T edit
	code = replace(code, r"(?<type>[A-Za-z][\w\[\],\.]*)(?:\?| \boptional\b)(?!\.)", "$type|null")
	code = replace(code, r"(?<=(?<!\w) {2})(?:sath|case) (?:[\.\?]{3}|ba{1,2}ki|anja{1,2}n)(?=(?: (?:if|agar) [^\:]+)? ?\:)", "case default")
	# since the key-value replacement has already occured
	# (scroll up a few lines)
	# we need to catch bot sath|case
	# as sath will not be replaced
	# with case anymore
	code = replace(code, r"\b(?:none|koi_na)\b", "null")
	# REMINDER:
	# there's a difference between None, and NoneType
	code = replace(code, r"\b(?:KoiNa)\b", "typeof null")
	code = replace(code, r"(?<!\w)\?(?![\w\.])", "null")
	# readable index access
	# sequence MATTERS
	# sequence is the only thing holding it together
	code = replace(code, r"\[\.?(?:ba{1,2}d *\:?|har) *(?<n>\-?\d+)(?: ?(?:ke[_ ])?ba{1,2}d)?[ _\/\-]\d+\]", "[::$n]")
	code = replace(code, r"\[\.?ba{1,2}d *\:? *(?<n>\-?\d+)\]", "[$n:]")
	# reversing
	code = replace(code, r"\[\.?(?:k[aeio]\:?[_ ])?(?:ula?t[ai]?|rev(?:erse)?d?)\]", "[::-1]")
	# number-based mid slicing (rather than index-based)
	# comes before
	code = replace(code, r"\[\.?(?:da?rmya{0,2}n|beech) *\: *(?<start>\-?\d+)(?:st|nd|rd|h?l[ae]|th|th?[ae]|s?r[ae]|w[ae])?(?:[,:~\-]| *(?:se|aur)) *(?<stop>\-?\d+)?(?:st|nd|rd|h?la|th|th?a|s?ra|wa)?(?:[, ]*(?:chor[_ ]?k?e|ba?ge?r))\]", "[$start-1 if $start > 0 else $start:$stop-1 if $stop > 0 else $stop]")
	# comes after {similar, but different:}
	code = replace(code, r"\[\.?(?:da?rmya{0,2}n|beech) *\: *(?<start>\-?\d+)(?:st|nd|rd|h?l[ae]|th|th?[ae]|s?r[ae]|w[ae])?(?:[,:~\-]| *(?:se|aur)) *(?<stop>\-?\d+)?(?:st|nd|rd|h?la|th|th?a|s?ra|wa)?(?:[, ]*(?:rakhe|sha{1,2}mil))?\]", "[$start-1 if $start > 0 else $start:$stop]")
	code = replace(code, r"\[\.?(?:(?:se|f(?:ir)?st|pehl(?:e|a))(?:[_ ]ke)?|shuru?(?:[_ ][smk]e|wa{1,2}ti)) *[\: ] *(?<n>\-?\d+)(?: tak)?\]", "[0:$n]")
	# ^ e.g. "hello world"[.first4] -> "hell"
	code = replace(code, r"\[\.?(?:la?st|akhri|akhir)(?:[_ ]?[smk]e)? *[\: ] *(?<n>\d+)\]", "[-$n:]")
	# ^ e.g. "hello world"[.last:?4] -> "orld"
	code = replace(code, r"\[(?:\.(?:f(?:ir)?st|pehla)|\.?1(?:st|h?la))\]", "[0]")
	# ^ e.g. "hello world"[.1st] -> "h"
	code = replace(code, r"\[(?:\.(?:sec(?:o|d|o?nd?)?|d(?:u|oo)sra)|\.?2(?:nd|s?ra))\]", "[1]")
	# ^ e.g. "hello world"[.second] -> "e"
	code = replace(code, r"\[(?:\.(?:th(?:i|d|i?rd?)|t(?:i|ee)sra)|\.?3(?:rd|s?ra))\]", "[2]")
	# ^ e.g. "hello world"[.third] -> "l"
	code = replace(code, r"\[\.?(?:(?:f(?:ir)?st|shuru?(?:wat)?(?:[_ ]?(?:i|(?:k|wal)a|me))?|n)\:)?(?<n>\d+)(?:st|nd|rd|h?la|th|th?a|s?ra|wa)\]", "[$n-1]")
	code = replace(code, r"\[\.?(?:(?:la?st|a{1,2}kh(?:ir|ri)(?:[_ ]?(?:(?:k|wal)a|[sm]e))?|\-n)\:)(?<n>\d+)(?:st|nd|rd|h?la|th|th?a|s?ra|wa)\]", "[-$n]")
	# ^ catches arr[akhri:4tha]
	code = replace(code, r"\[\.?(?<n>\d+)(?:st|nd|rd|h?la|th|th?a|s?ra|wa) (?:la?st|a{1,2}kh(?:ir|ri)(?:[_ ]?(?:(?:k|wal)a|[sm]e))?)\]", "[-$n]")
	# ^ catches arr[4tha akhri], same functionality, too different allowed orders for convenience
	code = replace(code, r"\[(?:(?:(?:\.th(?:i|d|i?rd?))[_ ]?la?st)|\.?[t3](?:i|ee)?(?:s?ra|rd)[_ ]?(?:a{1,2}khri|la?st))\]", "[-3]")
	# ^ e.g. "hello world"[.third] -> "l"
	code = replace(code, r"\[(?:(?:(?:\.sec(?:o|d|o?nd?)?|2nd)[_ ]?la?st)|\.?[d2](?:u|oo)?(?:s?ra|nd)[_ ]?(?:a{1,2}khri|la?st))\]", "[-2]")
	# ^ e.g. "hello world"[.secondlast] -> "s"
	code = replace(code, r"\[\.?(?:(?:f(?:ir)?st|pehla)|1(?:st|h?la))?[_ ]?(?:\.?(?:la?st|a{1,2}khri))\]", "[-1]")
	# e.g. ^ "hello world"[.last] -> "d"
	# custom data types
	# much needed
	# Restore strings
	__python_a_b_eq_x_y_regex__: str = r"(?<keys>(?:[A-Za-z_]\w*(?:, *(?:aur )?))+) *= *(?<values>[^\n]+)"
	def __python_a_b_eq_x_y_replacer_fn__(m: re.Match|None) -> str:
		key_group: str = m.group("keys")
		value_group: str = m.group("values")
		keys: list[str] = [k.strip() for k in re.split(", *(?:aur )?", key_group) if "," in key_group]
		values: list[str] = [v.strip(" []") for v in re.split(", *(?:aur )?", value_group) if "," in value_group]
		result: str = ""
		for k, v in zip(keys, values):
			if not k or not v:
				continue
			result += f"let {k} = {v};\n"
		return result
	code = replace(code, __python_a_b_eq_x_y_regex__, __python_a_b_eq_x_y_replacer_fn__)
	code = replace(code, r"\blet let\b", "let")
	for j, string in old_enumerate(strings):
		code = code.replace(f"__STRING_{j}__", string, 1)
	# should come after
	code = replace(code, r"(?<=(?:\bfrom|(?<=\bim)port) )`(?<module>[A-Za-z\.][\w\.\\\/-]*)`(?!\w)", "\'$module\'")
	if not re.search(r"(?<=(?:\bfrom|(?<=\bim)port) )[\"\'\`]react[\"\'\`](?!\w)", code) and not code.strip().startswith("import * as React"):
		code = f"import * as React from 'react';\nObject.assign(window, React);\n\n{code}"
	return code

def main() -> None:
	print(translate_for_react("kaho 'hi ${2+5 is:}'"))
	print(translate_for_react("""
farz x, y, = 1, aur 
hamesha PI = 3.1415
print "$x $y"
print("$x= $y")
print("${x=} ${y=}")
print("${x:} ${y:}")
koshish:
	
nakami tor e:
	
:/
fn App:
	lotao (
		<.>
			<. cls="App">
				<button clk={() -> print("you clicked this button.")}>Click</button>
			</.>
		</.>
	)
:/
fn x(p1, p2):
	...
:/
fc add(x, y):
	ret x + y;
:/

fc new_func(..items):
	...
:/
farz [score, aur set_score] = use_state(0)
hamesha const_func = x, y -> x+y
farz score, set_score = use_state(none)
farz [score, setScore] = use_state_x(0)
farz [score, set_score] = use_state(0)
set_score(score -> score + 1)
fc test_fn() {
	...
}
hamesha my_func = (x, y, .....rest_of_args) -> {
	...
}
arr = [1, 6, 11, 16, 21, 26, 31]
arr[6ta]
tor use_st mangao useState react mese
tor create_rt mangao createRoot react-dom/client mese

create_rt(
	qs("#root")
).render(
	<App />
)
farz x = 4
print '$x, $y'
return 4

farz w, x, = "hello world $", "test $2+3"
farz y = `test $2+3`
farz z = 'test \\$$2+3'
farz string = "world"
print "hello $string"
#print(x)
print("C:\Progra~1\")

mangao sab_kuch react mese
mangao ReactDOM react-dom/client mese
mangao App.css, globals.css, React
mangao React
mangao ./App
mangao App ./App mese

class Book:
    constr(name, author, release):
        apna.name = name
        apna.author = author
        apna.release = release
    /
    __print__():
        lotao `Book(name=$apna.name , author=$apna.author , release= $apna.release )`
    /
/
        
        
fc App:
    ...
/

farz book1 = nai Book("The Subtle Art", "Mark Manson", 2016)
kaho book1

koshish:
    kaho 0/0
nakami:
    kaho("Javascript does not allow division by zero")
/
"""))
	print(translate_for_css("""
body:
    bg: purple
    jumle-ka-font: "Roboto", ms-serif
    jumle-ka-motapa: bold
    jumle-ka-style: italic
    jumle-ki-size: 12px
/
"""))

if __name__ == "__main__":
	main()