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

def parse(code):
	i = -1
	c = None
	
	def next():
		nonlocal i
		nonlocal c
		i += 1
		if i < len(code):
			c = code[i]
		else:
			c = ""
	
	def skip_linebreak():
		nonlocal i
		nonlocal c
		if c=="\n" or c=="\r":
			next()
	
	def skip_whitespace():
		nonlocal c
		while c in " \t\n\r":
			next()
	
	def is_start_of_line():
		return i==0 or code[i-1]=="\n"
	
	def parse():
		nonlocal i
		nonlocal c
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
			## heading
			elif c=="*" and is_start_of_line(): #this needs to be changed
				next()
				if c==" ":
					next()
					heading_level = 1
					while c=="*":
						heading_level += 1
						next()
					if heading_level > 6:
						raise Exception("Heading too deep")
					output += "<h%d>" % heading_level
					while 1:
						if not c or c=="\n":
							break
						output += escape_html_char(c)
						next()
					output += "</h%d>" % heading_level
					next()
				else:
					raise Exception("aaaa")
			elif c=="#" and is_start_of_line():
				next()
				while c and c!="\n":
					next()
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
					while c=="=":
						next()
					if c=="|":
						next()
					else:
						raise Exception("missing | in table start")
					skip_whitespace()
					if c=="|":
						next()
					else:
						raise Exception("missing | in table start")
					output += "<table><tbody><tr><td>"
					skip_linebreak()
				elif c=="-":
					next()
					while c=="-":
						next()
					if c=="|":
						next()
					else:
						raise Exception("missing | in table header end")
					skip_whitespace()
					if c=="|":
						next()
					else:
						raise Exception("missing | in table header end")
					#todo: set header
				# other
				else:
					skip_whitespace() # this is used for the linebreak after | as well as the linebreak between ||
					# table end or next row
					if c=="|":
						next()
						# ||= table end
						if c=="=":
							next()
							while c=="=":
								next()
							if c=="|":
								next()
							else:
								raise Exception("missing | in table end at %d" % i)
							output += "</td></tr></tbody></table>"
							skip_linebreak()
						# || next row
						else:
							output += "</td></tr><tr><td>"
							skip_linebreak()
					# | next cell
					else:
						output += "</td><td>"
			## return
			#elif c=="}":
			#	next()
			#	return output
			## other symbol
			else:
				output += escape_html_char(c)
				next()
		return output
	
	return parse()