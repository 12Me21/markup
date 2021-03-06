import sys
import os
import category as Category
import shutil

sbhl = __import__("sbhighlight")

label_suffix = 0

def sbsyntax(code):
	global label_suffix
	list = sbhl.make_list(code)
	if len(list)>1:
		label_suffix += 1
		return sbhl.html(code)+'''<input type="checkbox" id="syntax%d"><label for="syntax%d">show all forms</label>
<div class="syntax-full">''' %((label_suffix,)*2) + sbhl.html("\n".join(list))+'''</div>'''
	else:
		return sbhl.html(code)

exists = {}

def page_link(page):
	if Category.tree.find_category(page):
		return '<a href="%s.html" class="category">' % escape_html_attribute(page)
	else:
		if page in exists and exists[page]:
			return '<a href="%s.html">' % escape_html_attribute(page)
		else:
			
			return '<a href="%s.html" class="missing">' % escape_html_attribute(page)

def sbconsole(code):
	return code

highlighters = {
	"smilebasic": sbhl.html,
	"sbsyntax": sbsyntax,
	"sbconsole": sbconsole
}

def escape_html(code):
	return code.replace("&","&amp;").replace("<","&lt;").replace("\n","<br>")

def highlight(code, language):
	if language in highlighters:
		return highlighters[language](code)
	return escape_html(code)

def escape_html_char(char):
	if char=="<":
		return "&lt;"
	if char=="&":
		return "&amp;"
	if char=="\n":
		return "<br>\n"
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
		lines.append('<ul class="navigation"><li class="up">%s%s</a></li><li class="previous">%s%s</a></li><li class="next">%s%s</a></li></ul>' % (
			page_link(category.name),
			escape_html(Category.title[category.name]),
			page_link(neighbors[0]),
			escape_html(Category.title[neighbors[0]]),
			page_link(neighbors[1]),
			escape_html(Category.title[neighbors[1]])
		))
	return "".join(lines)

#todo: this should remove weird chars and other stuff
def anchor_name(text):
	return text.replace(" ","-")

def parse(code, filename):
	global label_suffix
	label_suffix=0
	i = -1
	c = None
	stack = []
	code = code.replace("\r","")
	
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
		if c == "\n":
			next()
		while c in (" ","\t"):
			next()
	
	def is_start_of_line():
		nonlocal i
		return i==0 or code[i-1]=="\n"
	
	def can_start_markup(type):
		nonlocal i,c,code,stack
		return (i-2 < 0 or code[i-2] in " \t\n({'\"") and (not(c) or not(c in " \t\n,'\"")) and not(type in stack)
	
	class Item():
		type=""
		def __eq__(self,type):
			return self.type==type
		def __str__(self):
			return self.type
		def __init__(self,type):
			self.type=type
	
	class Table(Item):
		type="table"
		columns=None
		cells_in_row=0
		header=False
		def __init__(self):
			pass
	
	class Heading(Item):
		type="heading"
		level=None
		def __init__(self,level):
			self.level=level
	
	class List(Item):
		type="list"
		indent=0
		def __init__(self,indent):
			self.indent=indent
		
	def can_end_markup(type):
		nonlocal i,c,code,stack
		return stack and stack[-1]==type and (i-2 < 0 or not(code[i-2] in " \t\n,'\"")) and (not(c) or c in " \t\n-.,:!?')}\"")
	
	def do_markup(type, tag, symbol):
		if can_start_markup(type):
			stack.append(Item(type))
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
	
	def line_end():
		nonlocal stack,c,i
		output = ""
		if stack:
			if stack[-1]=="heading":
				output += "</h%d>" % stack.pop().level
				next()
				return output
			elif stack[-1]=="list":
				old_indent = stack[-1].indent
				next()
				indent = 0
				while c==" " or c=="\t":
					indent += 4 if c=="\t" else 1
					next()
				if c=="+":
					#next()
					#if c==" ":
						next()
						#increasing list depth (assumed to increase by 1 level)
						if indent > old_indent:
							stack.append(List(indent))
							output += "<ul><li>"
						#decreasing list depth
						elif indent < old_indent:
							indents = []
							while 1:
								if stack and stack[-1]=="list":
									if stack[-1].indent == indent:
										break
									elif stack[-1].indent > indent:
										indents.append(stack[-1].indent)
										stack.pop()
										output += "</li></ul>"
									else:
										raise ParseError("Bad list indentation. Got "+str(indent)+" space while expecting: "+", ".join(str(x) for x in indents)+", (or more)")
								else:
									raise ParseError("Bad list indentation. Item was indented less than start of list (probably)")
							output += "</li><li>"
						else: # same depth
							output += "</li><li>"
					#else:
					#	output += "<br>+"
				else:
					while stack and stack[-1]=="list":
						stack.pop()
						output += "</li></ul>"
				return output
		output += escape_html_char(c)
		next()
		return output
	
	def parse():
		nonlocal i,c,code,filename
		output=""
		next()
		while c:
			# todo: make ``whatever` -> <code>`whatever</code>
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
							next()
							if c=="`":
								output += "`"
							else:
								output += "</code>"
								break
						elif c:
							output += escape_html_char(c)
						else:
							raise ParseError("Unclosed ` block")
						next()
			## heading and bold
			elif c=="*":
				# todo: add anchors to headings
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
						stack.append(Heading(heading_level))
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
			# elif c=="^":
				# next()
				# output += do_markup("superscript","sup","^")
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
					skip_linebreak()
					output += "<hr>"
				else:
					output += "-"*dashes
			## list
			elif c=="+" and is_start_of_line():
				next()
				if c==" ":
					stack.append(List(0))
					output += "<ul><li>"
				else:
					output += "+"
			## comment
			elif c=="#" and is_start_of_line():
				next()
				if c=="+":
					next()
					start=i
					command = ""
					while c and c!=" " and c!="\n":
						command += c
						next()
					
					args = ""
					if c==" ":
						next()
						start = i
						while c and c!="\n":
							args += c
							next()
					
					if command == "NAVIGATION":
						output += generate_navigation(filename)
					elif command == "TITLE":
						output += "<h1>"+escape_html(Category.title[filename])+"</h1>"
					elif command == "PAGES":
						category = Category.tree.find_category(filename)
						if not category:
							raise ParseError("tried to insert page list on page that isn't a category")
						output += "<ul>"
						for page in category.pages:
							name = str(page)
							output += "<li>"+page_link(name)+Category.title[name]+"</a></li>"
						output += "</ul>"
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
					url = code[start:i-1]
					# [[url]]
					if c=="]":
						# check if url is a page filename
						if url in Category.title:
							output += page_link(url) + escape_html(Category.title[url]) + "</a>"
						elif url.isdigit():
							output += '<sup><a href="%s" name="%s">%s</a></sup>' % (escape_html_attribute(filename+".html#"+url), escape_html_attribute(url), escape_html(url))
						elif url.startswith("#"):
							output += '<sup><a href="%s">%s</a></sup>' % (escape_html_attribute(filename+".html"+url), escape_html(url[1:]))
						else:
							dot = url.rfind(".")
							if dot>=0 and url[dot+1:].upper() in {"PNG","JPG","JPEG","BMP","GIF"}:
								output += '<img src="%s">' % escape_html_attribute(url)
							else:
								output += '<a href="%s">%s</a>' % (escape_html_attribute(url), escape_html(url))
						next()
					# [[url][text]]
					else: #c=="["
						if url in Category.title:
							output += page_link(url)
						elif url.startswith("#"):
							output += '<a href="' + escape_html_attribute(filename+".html#"+url)+ '">'
						else:
							output += '<a href="' + escape_html_attribute(url) + '">'
						next()
						stack.append(Item("link"))
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
				next()
				stack.append(Item("group"))
			elif c=="}" and stack and stack[-1]=="group":
				next()
				stack.pop()
			elif c=="|":
				next()
				if stack and stack[-1] == "table":
					skip_linebreak()
					# next row
					if c=="|":
						next()
						if stack[-1].columns == None: #end of the very first row in the table
							stack[-1].columns = stack[-1].cells_in_row
						
						if stack[-1].cells_in_row < stack[-1].columns:
							raise ParseError("not enough cells in table row")
							#actually start of new table ooo
							#stack.append(Table())
							#output += "<table><tbody><tr><td>"
						else:
							stack[-1].cells_in_row = 0
							if stack[-1].header:
								output += "</th></tr>"
								stack[-1].header=False
							else:
								output += "</td></tr>"
							
							if c=="*":
								next()
								stack[-1].header=True
								output += "<tr><th>"
							else:
								output += "<tr><td>"
							skip_linebreak()
					# next cell or end of table
					else:
						stack[-1].cells_in_row += 1
						# end of table
						if stack[-1].columns != None and stack[-1].cells_in_row > stack[-1].columns:
							if stack[-1].header:
								output += "</th>"
							else:
								output += "</td>"
							stack.pop()
							output += "</tr></tbody></table>"
							skip_linebreak()
						# next cell
						else:
							if stack[-1].header:
								output += "</th><th>"
							else:
								output += "</td><td>"
				#start of new table
				else:
					stack.append(Table())
					output += "<table><tbody><tr>"
					if c=="*":
						next()
						stack[-1].header=True
						output += "<th>"
					else:
						output += "<td>"
			else:
				output += escape_html_char(c)
				next()
		output += line_end()
		if stack:
			raise ParseError("Reached end of file with unclosed items: " + ",".join(str(item) for item in stack)) #need to fix
		return output
	
	try:
		return parse()
	except ParseError as e:
		print(e)
		return '<div class="error-message">'+escape_html(str(e))+"</div>"+escape_html(code)

def parse_file(input_dir, output_dir, name, stdio = False):
	output_filename = os.path.join(output_dir, name+".html")
	if stdio:
		output_file = sys.stdout
		text = sys.stdin.read()
	else:
		filename = os.path.join(input_dir, name+".m")
		if not os.path.isdir(os.path.dirname(output_filename)):
			os.makedirs(os.path.dirname(output_filename), exist_ok=True)
		output_file = open(output_filename, mode="w+", encoding="utf-8")
		
		file = None
		if os.path.isfile(filename):
			print("%-10s: converting page" % name)
			file = open(filename, mode="r", encoding="utf-8")
			text = file.read()
			file.close()
		else:
			if Category.tree.find_category(name):
				print("%-10s: generating placeholder category page" % name)
				text = "#+NAVIGATION\n#+TITLE\n#+PAGES"
			else:
				text = "#+NAVIGATION\n#+TITLE\nPage missing"
				print("%-10s: missing!" % name)
				#return
	
	output_file.write(
		'<!DOCTYPE html><html><head><meta charset="UTF-8"><base href="{base}"><link rel="stylesheet" href="style.css"><title>{title}</title></head>\n<body>{contents}</body></html>'.format(
			base = os.path.relpath(output_dir, os.path.dirname(output_filename)),
			#base = output_dir,
			#navigation = generate_navigation(name), {navigation}\n
			contents = parse(text, name),
			title = escape_html(Category.title[name]),
		)
	)
	
	if not stdio:
		output_file.close()

args = sys.argv
if len(args)==1:
	args.append(os.path.join(os.path.dirname(__file__), "input"))
	args.append(os.path.join(os.path.dirname(__file__), "output"))
	#args.append("")
	#args.append("temp")
	#args.append("Temporary Page")

# input output - parse all pages
# input output page1 page2 ... - parse list of pages
# input output "" name title - preview thing using stdin/stdout

if len(args)>=3:
	assert os.path.isdir(args[1]), "missing input dir"
	assert os.path.isdir(args[2]), "missing output dir"
	Category.load_titles(os.path.join(args[1], "titles.txt"))
	# convert all pages
	if len(args)==3:
		# check which pages exist
		for page in Category.title:
			exists[page] = os.path.isfile(os.path.join(args[1], page+".m")) #(use for red links)
		print(exists)
		
		# copy css file
		css = os.path.join(args[1],"style.css")
		if os.path.isfile(css):
			try:
				shutil.copyfile(css, os.path.join(args[2],"style.css"))
			except PermissionError:
				print("darn.")
		else:
			print("Warning: Missing CSS file in input")
		
		for page in Category.title:
			parse_file(args[1], args[2], page)
	
	else:
		if args[3]=="" and len(args)==6:
			# preview
			Category.title[args[4]] = args[5]
			parse_file(args[1], args[2], args[4], stdio=True)
		else:
			# convert list of pages
			for page in args[3:]:
				assert page in Category.title, "invalid page: "+page
				parse_file(args[1], args[2], page)
else:
	raise Exception("Wrong number of arguments")