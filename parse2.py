def highlight(code, language):
	return code

def escape_html(code):
	return code.replace("&","&amp;").replace("<","&lt;").replace("\n","<br>")

def escape_html_char(char):
	if char=="<":
		return "&lt;"
	if char=="&":
		return "&amp;"
	if char=="\n":
		return "<br>"
	if char=="\r":
		return ""
	return char
#maybe remove \n if last element was a block or something...

def parse(code):
	i = -1
	c = None
	stack = []
	
	def next():
		nonlocal i,c
		i += 1
		if i < len(code):
			c = code[i]
		else:
			c = ""
	
	def skip_linebreak():
		nonlocal i,c
		while c in (" ","\t"):
			next()
		if c in ("\n","\r"):
			next()
	
	def skip_whitespace(): #really this should just skip spaces, then 1 line break, then more spaces
		nonlocal c
		while c in c in (" ","\t","\n","\r"):
			next()
	
	def is_start_of_line():
		nonlocal i
		return i==0 or code[i-1]=="\n"
	
	def can_start_markup(type):
		nonlocal i,c,code,stack
		return (i-2 < 0 or code[i-2] in " \t\n\r({'\"") and (not(c) or not(c in " \t\n\r,'\"")) and not(type in stack)
	
	def can_end_markup(type):
		nonlocal i,c,code,stack
		return stack and stack[-1]==type and (i-2 < 0 or not(code[i-2] in " \t\n\r,'\"")) and (not(c) or c in " \t\n\r-.,:!?')}\"")
	
	def do_markup(type, tag, symbol):
		if can_start_markup(type):
			stack.append(type)
			return "<"+tag+">"
			#no next()
		elif can_end_markup(type):
			stack.pop()
			return "</"+tag+">"
		else:
			return symbol
	
	def parse():
		nonlocal i,c
		output=""
		next()
		while c:
			## code block
			if c=="`":
				next()
				if c=="`":
					next()
					# multiline code block
					if c=="`":
						output += "<code>"
						language = ""
						while 1:
							next()
							if c=="\n":
								break
							elif c:
								language += c
							else:
								raise Exception("Reached end of input while reading ``` start")
						start = i+1
						while 1:
							next()
							if c=="`":
								next()
								if c=="`":
									next()
									if c=="`":
										break;
							if not c:
								raise Exception("Reached end of input while reading code inside ```")
						output += highlight(code[start:i-2], language.strip())
						output += "</code>"
						next()
						skip_linebreak()
					# bad
					else:
						output += "``"
						next()
				# inline code block
				else:
					output += "<code>"
					while 1:
						if c=="`":
							output += "</code>"
							break
						elif c:
							output += escape_html_char(c)
						else:
							raise Exception("Unclosed ` block")
						next()
					next()
			## heading and bold
			elif c=="*":
				if is_start_of_line():
					next()
					heading_level = 1
					while c=="*":
						heading_level += 1
						next()
					if heading_level > 6:
						raise Exception("Heading too deep")
					if c==" ":
						output += "<h%d>" % heading_level
						next()
						stack.append("heading%d" % heading_level)
						continue
					elif heading_level!=1:
						raise Exception("Missing space after heading")
						continue
				else:
					next()
				output += do_markup("bold","b","*")
			## italics
			elif c=="/":
				next()
				output += do_markup("italic","i","/")
			## underline
			elif c=="_":
				next()
				output += do_markup("underline","u","_")
			## line break
			elif c=="\n":
				if stack:
					if stack[-1][0:-1]=="heading":
						output += "</h%d>" % int(stack[-1][-1])
						stack.pop()
						next()
						continue
				output += escape_html_char(c)
				next()
			## comment
			elif c=="#" and is_start_of_line():
				next()
				while c and c!="\n":
					next()
			## escape
			elif c=="\\":
				next()
				if c:
					output += escape_html_char(c)
					next()
			## tables
			elif c=="|":
				next()
				# |= table start
				if c=="=":
					next()
					while c=="=": next()
					if c=="|": next()
					else: raise Exception("missing | in table start")
					skip_whitespace()
					if c=="|": next()
					else: raise Exception("missing | in table start")
					stack.append("table")
					output += "<table><tbody><tr><td>"
					skip_linebreak()
				# other
				else:
					if stack and stack[-1] == "table":
						skip_whitespace() # this is used for the linebreak after | as well as the linebreak between ||
						# table end or next row
						if c=="|":
							next()
							# ||= table end
							if c=="=":
								next()
								while c=="=": next()
								if c=="|": next()
								else: raise Exception("missing | in table end at %d" % i)
								stack.pop()
								output += "</td></tr></tbody></table>"
								skip_linebreak()
							# || next row
							else:
								output += "</td></tr><tr><td>"
								skip_linebreak()
						# | next cell
						else:
							output += "</td><td>"
					else:
						output += escape_html_char(c)
						next()
			## return
			#elif c=="}":
			#	next()
			#	return output
			## other symbol
			else:
				output += escape_html_char(c)
				next()
		if stack:
			if stack[-1][0:-1]=="heading":
				output += "</h%d>" % int(stack[-1][-1])
				stack.pop()
				next()
		if stack:
			raise Exception("unclosed items: ",stack)
		return output
	
	return parse()