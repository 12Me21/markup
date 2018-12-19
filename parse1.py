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
	output = ""
	
	def next():
		nonlocal i
		nonlocal c
		i += 1
		if i < len(code):
			c = code[i]
		else:
			c = ""
	
	def nextb():
		next()
		while c=="{":
			parse()
	
	def skip_linebreak():
		nonlocal i
		nonlocal c
		if c=="\n" or c=="\r":
			next()
	
	def is_start_of_line():
		return i==0 or code[i-1]=="\n"
	
	def parse():
		nonlocal i
		nonlocal c
		nonlocal output
		nextb()
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
							nextb()
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
						nextb()
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
					nextb()
			## heading
			elif c=="*" and is_start_of_line():
				heading_level = 1
				nextb()
				while c=="*":
					heading_level += 1
					nextb()
				if heading_level > 6:
					raise Exception("Heading too deep")
				output += "<h%d>" % heading_level
				while 1:
					if not c or c=="\n":
						break
					output += escape_html_char(c)
					nextb()
				output += "</h%d>" % heading_level
				nextb()
			## escaped char
			elif c=="\\":
				nextb()
				if c:
					output += escape_html_char(c)
					nextb()
			## tables
			elif c=="|":
				nextb()
				# table start
				if c=="=":
					nextb()
					while c=="=":
						nextb()
					if c=="|":
						nextb()
					else:
						raise Exception("missing | in table start")
					while c=="\n" or c=="\r":
						nextb()
					if c=="|":
						nextb()
					else:
						raise Exception("missing | in table start")
					output += "<table><tbody><tr><td>"
					skip_linebreak()
				# table start (with header)
				elif c=="*":
					nextb()
					if c=="*":
						nextb()
					if c=="|":
						nextb()
					else:
						raise Exception("missing | in table start")
					if c=="\n" or c=="\r":
						nextb()
					if c=="|":
						nextb()
					else:
						raise Exception("missing | in table start")
					output += "<table class='header_table'><tbody><tr><td>"
					skip_linebreak()
				# other
				else:
					skip_linebreak() # this is used for the linebreak after | as well as the linebreak between ||
					# table end or next row
					if c=="|":
						nextb()
						#table end
						if c=="=":
							nextb()
							if c=="=":
								nextb()
							if c=="|":
								nextb()
							else:
								raise Exception("missing | in table end")
							output += "</td></tr></tbody></table>"
							skip_linebreak()
						#next row
						else:
							output += "</td></tr><tr><td>"
							skip_linebreak()
					# next cell
					else:
						output += "</td><td>"
			## return
			elif c=="}":
				nextb()
				return
			## other symbol
			else:
				output += escape_html_char(c)
				nextb()
	
	parse()
	return output