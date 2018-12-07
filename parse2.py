import sys
import os
import category as Category

def fp(path):
	return os.path.join(os.path.dirname(__file__), path)

filename = fp(sys.argv[1] if 1 in sys.argv else "in.m")

def rel(path):
	global filename
	return os.path.join(os.path.dirname(filename), path)

sbhl = __import__("sbhighlight")

def sbsyntax(code):
	list = sbhl.make_list(code)
	return sbhl.html(code)+'''<input hidden type="checkbox" id="syntax" name="syntax"><label for="syntax">show all forms</label>
<div class="syntax-full">'''+sbhl.html("\n".join(list))+'''</div>'''

highlighters = {
	"smilebasic": sbhl.html,
	"sbsyntax": sbsyntax
}

def highlight(code, language):
	if language in highlighters:
		return highlighters[language](code)
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
	return char
#maybe remove \n if last element was a block or something...

#warning: only works in quoted attributes
def escape_html_attribute(code):
	return code.replace("&","&amp;").replace('"',"&quot;")

def generate_navigation(page):
	categories = Category.tree.categories(page)
	lines = []
	for category in categories:
		neighbors = category.neighbors(page)
		lines.append("[[{category}.html][Up ({category})]] | [[{previous}.html][< Previous ({previous})]] | [[{next}.html][Next ({next}) >]]".format(
			category=category, previous=neighbors[0], next=neighbors[1]
		))
	return "\n".join(lines)

def parse(code):
	i = -1
	c = None
	stack = []
	
	def next():
		nonlocal i,c
		i += 1
		if i < len(code):
			c = code[i]
			if c=="\r":
				next()
		else:
			c = ""
	
	def skip_linebreak():
		nonlocal i,c
		while c in (" ","\t"):
			next()
		if c == "\n":
			next()
	
	def skip_whitespace(): #really this should just skip spaces, then 1 line break, then more spaces
		nonlocal c
		while c in c in (" ","\t","\n"):
			next()
	
	def is_start_of_line():
		nonlocal i
		return i==0 or code[i-1]=="\n"
	
	def can_start_markup(type):
		nonlocal i,c,code,stack
		return (i-2 < 0 or code[i-2] in " \t\n({'\"") and (not(c) or not(c in " \t\n,'\"")) and not(type in stack)
	
	def can_end_markup(type):
		nonlocal i,c,code,stack
		return stack and stack[-1]==type and (i-2 < 0 or not(code[i-2] in " \t\n,'\"")) and (not(c) or c in " \t\n-.,:!?')}\"")
	
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
	
	def markup_exception(message):
		nonlocal i
		return Exception("%s\nOn line %d" % (message, get_line(i)))
	
	def get_line(pos):
		nonlocal code
		return code[0:pos].count("\n")+1
	
	def sub_parse(new_code):
		nonlocal code,i,c
		old_code = code
		old_i = i
		code = new_code
		i = -1
		output = parse()
		code = old_code
		i = old_i-1
		next()
		return output
	
	class ParseError(Exception):
		nonlocal i
		def __init__(self, message):
			self.args = [message, i]
		def __str__(self):
			return "%s\nOn line %d" % (self.args[0], get_line(self.args[1]))
	
	filestack=[]
	
	def line_end():
		nonlocal stack,c,i
		output = ""
		if stack:
			if stack[-1][0:7]=="heading":
				output += "</h%d>" % int(stack[-1][-1])
				stack.pop()
				next()
				return output
			elif stack[-1][0:4]=="list":
				depth = int(stack[-1][4:])
				next()
				spaces = 0
				while c==" " or c=="\t":
					spaces += 1
					next()
				if c=="+":
					next()
					if c==" ":
						next()
						if spaces>depth: #increasing list depth
							for j in range(depth+1, spaces+1):
								stack.append("list%d" % j)
							output += "<ul><li>"*(spaces-depth)
						elif spaces<depth: #decreasing list depth
							for j in range(spaces, depth):
								if stack[-1][0:4]=="list":
									stack.pop()
								else:
									raise ParseError("item must be closed before list changes")
							output += "</li></ul>"*(depth-spaces)+"</li><li>"
						else:
							output += "</li><li>"
					else:
						output += "<br>+"
				else:
					print("ending list",depth)
					for j in range(depth+1):
						if stack[-1][0:4]=="list":
							stack.pop()
						else:
							raise ParseError("item must be closed before list changes")
					output += "</li></ul>"*(depth+1)
				return output
		output += escape_html_char(c)
		next()
		return output
	
	def parse():
		nonlocal i,c,filestack,code
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
						language = ""
						while 1:
							next()
							if c=="\n":
								break
							elif c:
								language += c
							else:
								raise ParseError("Reached end of input while reading code block language")
						language = language.strip()
						output += '<pre class="'+escape_html_attribute("highlight-"+language)+'">'
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
								raise ParseError("Reached end of input while reading code inside code block")
						output += highlight(code[start:i-2], language)
						output += "</pre>"
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
							raise ParseError("Unclosed ` block")
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
						raise ParseError("Heading too deep")
					if c==" ":
						output += "<h%d>" % heading_level
						next()
						stack.append("heading%d" % heading_level)
						continue
					elif heading_level!=1:
						raise ParseError("Missing space after heading")
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
			## superscript
			elif c=="^":
				next()
				output += do_markup("superscript","sup","^")
			## line break
			elif c=="\n":
				output += line_end()
			## horizontal rule
			elif c=="-" and is_start_of_line():
				next()
				dashes = 1
				while c=="-":
					dashes += 1
					next()
				if dashes >= 4:
					output += "<hr>"
				else:
					output += "-"*dashes
			## list
			elif c=="+" and is_start_of_line():
				next()
				if c==" ":
					stack.append("list0")
					output += "<ul><li>"
				else:
					output += "+"
			## comment
			elif c=="#" and is_start_of_line():
				next()
				if c=="+":
					next()
					start=i
					while c and c!=" " and c!="\n":
						next()
					command = code[start:i]
					args = ""
					if c==" ":
						next()
						start = i
						while c and c!="\n":
							next()
						args=code[start:i]
					if command == "INCLUDE":
						output += sub_parse(open(rel(args)).read())
					elif command == "NAVIGATION":
						output += sub_parse(generate_navigation("MIN"))
					elif command == "TITLE":
						output += sub_parse("* MIN")
						output += "<title>MIN</title>"
					else:
						raise ParseError("Unrecognized command: "+command)
					next()
				else:
					while c and c!="\n":
						next()
			## escape
			elif c=="\\":
				next()
				if c:
					output += escape_html_char(c)
					next()
			## link
			elif c=="[":
				next()
				if c=="[":
					next()
					start = i
					while 1:
						next()
						if c=="]":
							next()
							if c=="[" or c=="]":
								break
						elif not c:
							raise ParseError("Unclosed link")
					output += '<a href="' + escape_html_attribute(code[start:i-1]) + '">'
					if c=="]":
						output += escape_html(code[start:i-1]) + "</a>"
						next()
					else:
						next()
						stack.append("link")
				else:
					output+="["
			#link end
			elif c=="]":
				next()
				if c=="]" and stack and stack[-1] == "link":
					next()
					stack.pop()
					output += "</a>"
				else:
					output+="]"
			elif c=="{":
				print("A")
				next()
				stack.append("group")
			elif c=="}" and stack and stack[-1]=="group":
				next()
				stack.pop()
			## tables
			elif c=="|":
				next()
				# |= table start
				if c=="=":
					next()
					while c=="=": next()
					if c=="|": next()
					else: raise ParseError("Missing | in table start")
					skip_whitespace()
					if c=="|": next()
					else: raise ParseError("Missing | in table start")
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
								else: raise ParseError("Missing | in table end")
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
						output += "|"
			else:
				output += escape_html_char(c)
				next()
		output += line_end()
		if stack:
			raise ParseError("Reached end of file with unclosed items: " + ",".join(stack))
		return output
	
	try:
		return parse()
	except ParseError as e:
		print(e)
		return '<div class="error-message">'+escape_html(str(e))+"</div>"+escape_html(code)

file = open(filename)
output_file = open(fp(sys.argv[2] if 2 in sys.argv else "out.html"),"w")
output_file.write('<link rel="stylesheet" href="test.css"></link>\n\n'+parse(file.read())) #parse should just take the stream as input
file.close()
output_file.close()