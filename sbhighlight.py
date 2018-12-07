keywords={"BREAK","CALL","COMMON","CONTINUE","DATA","DEC","DIM","ELSE","ELSEIF","END","ENDIF","EXEC","FOR","GOSUB","GOTO","IF","INC","INPUT","LINPUT","NEXT","ON","OUT","PRINT","READ","REM","REPEAT","RESTORE","RETURN","STOP","SWAP","THEN","UNTIL","USE","VAR","WEND","WHILE"}
functions={"ABS","ACCEL","ACLS","ACOS","ARYOP","ASC","ASIN","ATAN","ATTR","BACKCOLOR","BACKTRACE","BEEP","BGANIM","BGCHK","BGCLIP","BGCLR","BGCOLOR","BGCOORD","BGCOPY","BGFILL","BGFUNC","BGGET","BGHIDE","BGHOME","BGLOAD","BGMCHK","BGMCLEAR","BGMCONT","BGMPAUSE","BGMPLAY","BGMPRG","BGMPRGA","BGMSET","BGMSETD","BGMSTOP","BGMVAR","BGMVOL","BGOFS","BGPAGE","BGPUT","BGROT","BGSAVE","BGSCALE","BGSCREEN","BGSHOW","BGSTART","BGSTOP","BGVAR","BIN$","BIQUAD","BQPARAM","BREPEAT","BUTTON","CALLIDX","CEIL","CHKCALL","CHKCHR","CHKFILE","CHKLABEL","CHKMML","CHKVAR","CHR$","CLASSIFY","CLIPBOARD","CLS","COLOR","CONTROLLER","COPY","COS","COSH","CSRX","CSRY","CSRZ","DATE$","DEG","DELETE","DIALOG","DISPLAY","DLCOPEN","DTREAD","EFCOFF","EFCON","EFCSET","EFCWET","ERRLINE","ERRNUM","ERRPRG","EXP","EXTFEATURE","FADE","FADECHK","FFT","FFTWFN","FILES","FILL","FLOOR","FONTDEF","FORMAT$","FREEMEM","GBOX","GCIRCLE","GCLIP","GCLS","GCOLOR","GCOPY","GFILL","GLINE","GLOAD","GOFS","GPAGE","GPAINT","GPRIO","GPSET","GPUTCHR","GSAVE","GSPOIT","GTRI","GYROA","GYROSYNC","GYROV","HARDWARE","HEX$","IFFT","INKEY$","INSTR","KEY","LEFT$","LEN","LOAD","LOCATE","LOG","MAINCNT","MAX","MICDATA","MICPOS","MICSAVE","MICSIZE","MICSTART","MICSTOP","MID$","MILLISEC","MIN","MPCOUNT","MPEND","MPGET","MPHOST","MPLOCAL","MPNAME$","MPRECV","MPSEND","MPSET","MPSTART","MPSTAT","OPTION","PCMCONT","PCMPOS","PCMSTOP","PCMSTREAM","PCMVOL","POP","POW","PRGDEL","PRGEDIT","PRGGET$","PRGINS","PRGNAME$","PRGSET","PRGSIZE","PRGSLOT","PROJECT","PUSH","RAD","RANDOMIZE","RENAME","RESULT","RGB","RGBREAD","RIGHT$","RINGCOPY","RND","RNDF","ROUND","RSORT","SAVE","SCROLL","SGN","SHIFT","SIN","SINH","SNDSTOP","SORT","SPANIM","SPCHK","SPCHR","SPCLIP","SPCLR","SPCOL","SPCOLOR","SPCOLVEC","SPDEF","SPFUNC","SPHIDE","SPHITINFO","SPHITRC","SPHITSP","SPHOME","SPLINK","SPOFS","SPPAGE","SPROT","SPSCALE","SPSET","SPSHOW","SPSTART","SPSTOP","SPUNLINK","SPUSED","SPVAR","SQR","STICK","STICKEX","STR$","SUBST$","SYSBEEP","TABSTEP","TALK","TALKCHK","TALKSTOP","TAN","TANH","TIME$","TMREAD","TOUCH","UNSHIFT","VAL","VERSION","VISIBLE","VSYNC","WAIT","WAVSET","WAVSETA","WIDTH","XOFF","XON","XSCREEN"}

def highlight_sb(code,callback):
	i=-1
	c=""
	
	def next():
		nonlocal i,c,code
		i += 1
		c = code[i] if i<len(code) else ""
	
	def jump(pos):
		nonlocal i
		i=pos-1
		next()
	
	prev=0
	def push(type=None):
		nonlocal i,prev,callback
		global keywords,functions
		word=code[prev:i]
		prev=i
		if type=="word":
			upper=word.upper()
			
			if upper in {"TO", "STEP"}:
				type="to-step keyword"
			elif upper in {"TRUE", "FALSE"}:
				type="true-false keyword"
			elif upper in {"DIV", "MOD", "AND", "OR", "XOR", "NOT"}:
				type="word-operator keyword"
			elif upper == "DEF":
				type="def keyword"
			elif upper in keywords:
				type="keyword"
			elif upper in functions:
				type="function"
			else:
				type="variable"
		callback(word,type)
	
	next()
		
	#loop until the end of the string
	while c:
		#
		# keywords, functions, variables
		#
		if c.isalpha() or c=="_":
			next()
			# read name
			while c.isalpha() or c.isdigit() or c=="_":
				next()
			# read type suffix
			if c in {'#','%','$'}:
				next()
			# push word type
			push("word")
		# 
		# numbers
		# 
		elif c.isdigit() or c=='.':
			# if digit was found, read all of them
			while c.isdigit():
				next()
			# if there's a decimal point
			if c=='.':
				next()
				# read digits after
				if c.isdigit():
					next()
					while c.isDigit():
						next()
				else:
					# if GOTO is available: GOTO @skip_e
					if c=='#':
						next()
					push("number")
					continue
			# E notation
			if c in {'E','e'}:
				ePos=i
				next()
				# check for + or -
				if c in {'+','-'}:
					next()
				# read digits
				if c.isdigit():
					next()
					while c.isdigit():
						next()
				# no digits (invalid)
				else:
					jump(ePos)
					push()
					continue
			# (if GOTO is available: @skip_e)
			# read float suffix
			if c=='#':
				next()
			push("number")
		# 
		# strings
		# 
		elif c=='"':
			next()
			# read characters until another quote, line ending, or end of input
			while c and not c in {'"','\n','r'}:
				next()
			# read closing quote
			if c=='"':
				next()
			push("string")
		# 
		# comments
		# 
		elif c=='\'':
			next()
			# read characters until line ending or end of input
			while c and not c in {'\n','\r'}:
				next()
			push("comment")
		# 
		# logical AND, hexadecimal, binary
		# 
		elif c=='&':
			next()
			# logical and
			if c=='&':
				next();
				push("operator");
			# hexadecimal
			elif c in {'H','h'}:
				hPos=i
				next()
				# read hexadecimal digits
				if c.isdigit() or 'A'<=c<='F' or 'a'<=c<='f':
					next()
					while c.isdigit() or 'A'<=c<='F' or 'a'<=c<='f':
						next()
					push("number")
				else:
					jump(hPos)
					push()
			# binary
			elif c in {'B','b'}:
				bPos=i
				next()
				# read hexadecimal digits
				if c in {'0','1'}:
					next()
					while c in {'0','1'}:
						next()
					push("number")
				else:
					jump(bPos)
					push()
			# invalid &
			else:
				push()
		# 
		# labels
		# 
		elif c=='@':
			next()
			# read name
			while c.isalnum() or c=='_':
				next()
			# ok
			push("label")
		# 
		# constants
		# 
		elif c=='#':
			next()
			# read name
			if c.isalnum() or c=='_':
				next()
				while c.isalnum() or c=='_':
					next()
				push("number")
			else:
				push()
		# 
		# logical or
		# 
		elif c=='|':
			next()
			# logical or
			if c=='|':
				next()
				push("operator")
			# invalid
			else:
				push()
		# 
		# less than, less than or equal, left shift
		# 
		elif c=='<':
			next()
			# <= <<
			if c in {'=','<'}:
				next()
			push("operator")
		# 
		# greater than, greater than or equal, right shift
		# 
		elif c=='>':
			next()
			# >= >>
			if c in {'=','>'}:
				next()
			push("operator")
		# 
		# equal, equal more
		# 
		elif c=='=':
			next()
			# ==
			if c=='=':
				next()
				push("operator")
			else:
				push("equals")
		# 
		# logical not, not equal
		# 
		elif c=='!':
			next()
			# !=
			if c=='=':
				next()
			push("operator")
		# 
		# add, subtract, multiply, divide
		# 
		elif c in {'+','-','*','/'}:
			next()
			push("operator")
		# 
		# other
		#
		else:
			next()
			push()

# escape < and &
def escape_html(text):
	return text.replace("&","&amp;").replace("<","&lt;");

def html(code):
	html = ""
	prev_type = None
	prev_link = False
	# this is called for each highlightable token
	def callback(word, type=None):
		nonlocal html, prev_type, prev_link
		# only make a new span if the CSS class has changed
		if type != prev_type:
			# close previous span
			if prev_type:
				if prev_link:
					html += "</a>"
				else:
					html += "</span>"
			# open new span
			if type:
				if "keyword" in type or type in {"function", "operator"}:
					html += '<a href="'+word+'.html" class="'+type+'">'
					prev_link = True
				else:
					html += '<span class="'+type+'">'
					prev_link = False
		html += escape_html(word)
		prev_type = type
	
	highlight_sb(code, callback)
	# close last span
	if prev_type:
		if prev_link:
			html += "</a>"
		else:
			html += "</span>"
	return html

def make_list(code):
	list = []
	
	def parse_args(code, string, i):
		c=""
		list = []
		def next():
			nonlocal i,c,code
			i += 1
			c = code[i] if i<len(code) else ""
		
		i -= 1
		next()
		
		while 1:
			if c == '[':
				next()
				if c == ']':
					string += '['
					string += c
					next()
					continue
				list = parse_args(code, string, i) + list
				level = 1
				while 1:
					if c=='[':
						level += 1
					elif c==']':
						level -= 1
						if level == 0:
							break
					elif c=='' or c=='O' or c=='\n':
						string += "(Error, missing ']')"
						break
					next()
			if c=='' or c=='\n':
				break
			elif c != ']':
				string += c
			next()
		list = [string.replace("  "," ").replace("  "," ").replace(" , ",", ")] + list
		return list
	
	for line in code.split("\n"):
		list = list + parse_args(line,"",0)
	
	return list