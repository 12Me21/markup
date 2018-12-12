import collections
import os

class OrderedSet(collections.OrderedDict, collections.MutableSet):
	
	def update(self, *args, **kwargs):
		if kwargs:
			raise TypeError("update() takes no keyword arguments")
	
		for s in args:
			for e in s:
				 self.add(e)
	
	def add(self, elem):
		self[elem] = None
	
	def discard(self, elem):
		self.pop(elem, None)
	
	def __le__(self, other):
		return all(e in other for e in self)
	
	def __lt__(self, other):
		return self <= other and self != other
	
	def __ge__(self, other):
		return all(e in self for e in other)
	
	def __gt__(self, other):
		return self >= other and self != other
	
	def __repr__(self):
		return 'OrderedSet([%s])' % (', '.join(map(repr, self.keys())))
	
	def __str__(self):
		return '{%s}' % (', '.join(map(repr, self.keys())))
	
	difference = property(lambda self: self.__sub__)
	difference_update = property(lambda self: self.__isub__)
	intersection = property(lambda self: self.__and__)
	intersection_update = property(lambda self: self.__iand__)
	issubset = property(lambda self: self.__le__)
	issuperset = property(lambda self: self.__ge__)
	symmetric_difference = property(lambda self: self.__xor__)
	symmetric_difference_update = property(lambda self: self.__ixor__)
	union = property(lambda self: self.__or__)

class WikiCategory():
	name = ""
	pages = []
	def __init__(self, name, pages):
		self.name = name
		self.pages = pages
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name + ": " + ",".join(str(x) for x in self.pages)
	# category, page name -> all subcategories that directly contain that page
	def categories(self, page):
		output = OrderedSet() #this should be an ordered set
		for item in self.pages:
			if str(item)==page:
				output.add(self)
			if isinstance(item, WikiCategory):
				output.update(item.categories(page))
		return output
	# get a full list of all pages (files)
	def all_pages(self):
		output = set()
		output.add(self.name)
		for item in self.pages:
			if isinstance(item, WikiCategory):
				output.add(item.name)
				output.update(item.all_pages())
			else:
				output.add(item)
		return output
	# category, page name -> previous and next pages
	def neighbors(self, page):
		index = None
		for i, item in enumerate(self.pages):
			if isinstance(item, WikiCategory):
				name=item.name
			else:
				name=item
			if page==name:
				index = i
				break
		if index != None:
			return (str(self.pages[(index-1) % len(self.pages)]), str(self.pages[(index+1) % len(self.pages)]))
	def find_category(self, name):
		if self.name == name:
			return self
		for item in self.pages:
			if isinstance(item, WikiCategory):
				if item.name == name:
					return item
				x = item.find_category(name)
				if x:
					return x
		return None
	def sanitize(self): #check for EVIL ABSOLUTE PATHS
		assert not os.path.isabs(self.name),"Illegal page name"
		for item in self.pages:
			if isinstance(item, WikiCategory):
				item.sanitize()
			else:
				assert not os.path.isabs(item),"Illegal page name"

array_string = ["COPY","PUSH","POP","SHIFT","UNSHIFT","LEN"]

tree = WikiCategory("index",[
	WikiCategory("Math",["ABS","SGN","POW","SQR","LOG","EXP","MIN","MAX","CLASSIFY","Constants",
		WikiCategory("Operators",["INC","DEC","DIV","MOD"]),
		WikiCategory("Rounding",["FLOOR","ROUND","CEIL"]),
		WikiCategory("Trigonometry",["PI","RAD","DEG","SIN","COS","TAN","ASIN","ACOS","ATAN","SINH","COSH","TANH"]),
		WikiCategory("Random",["RND","RNDF","RANDOMIZE"]),
	]),
	WikiCategory("Audio",[
		WikiCategory("Music",["BGMSET","BGMSETD","BGMPLAY","BGMSTOP","BGMPAUSE","BGMCONT","BGMVOL","BGMCHK","BGMVAR","BGMCLEAR","CHKMML"]),
		WikiCategory("Microphone",["MICDATA","MICPOS","MICSAVE","MICSIZE","MICSTART","MICSTOP"]),
		WikiCategory("Speech",["TALK","TALKCHK","TALKSTOP"]),
		WikiCategory("PCM",["PCMCONT","PCMPOS","PCMSTOP","PCMSTREAM","PCMVOL"]),
		WikiCategory("Instruments",["WAVSET","WAVSETA"]),
		WikiCategory("Effector",["EFCON","EFCOFF","EFCSET","EFCWET"]),
		"BEEP",
		"SNDSTOP",
		"SYSBEEP",
	]),
	WikiCategory("Graphics",[
		"ACLS",
		"BACKCOLOR",
		"DIALOG",
		"DISPLAY",
		"FADE",
		"FADECHK",
		"RGB",
		"RGBREAD",
		"VISIBLE",
		"XSCREEN",
		WikiCategory("Text",["ATTR","CHKCHR","CLS","COLOR","CSRX","CSRY","CSRZ","FONTDEF","LOCATE","SCROLL","WIDTH","TABSTEP","INPUT","LINPUT","PRINT"]),
		WikiCategory("Sprites",["CALLIDX","SPANIM","SPCHK","SPCHR","SPCLIP","SPCLR","SPCOL","SPCOLOR","SPCOLVEC","SPDEF","SPFUNC","SPHIDE","SPHITINFO","SPHITRC","SPHITSP","SPHOME","SPLINK","SPOFS","SPPAGE","SPROT","SPSCALE","SPSET","SPSHOW","SPSTART","SPSTOP","SPUNLINK","SPUSED","SPVAR"]),
		WikiCategory("Background",["CALLIDX","BGANIM","BGCHK","BGCLIP","BGCLR","BGCOLOR","BGCOORD","BGCOPY","BGFILL","BGFUNC","BGGET","BGHIDE","BGHOME","BGLOAD","BGOFS","BGPAGE","BGPUT","BGROT","BGSAVE","BGSCALE","BGSCREEN","BGSHOW","BGSTART","BGSTOP","BGVAR"]),
		WikiCategory("GRP",["GBOX","GCIRCLE","GCLIP","GCLS","GCOLOR","GCOPY","GFILL","GLINE","GLOAD","GOFS","GPAGE","GPAINT","GPRIO","GPSET","GPUTCHR","GSAVE","GSPOIT","GTRI"]),
	]),
	WikiCategory("cat/Input",[
		"BREPEAT",
		"BUTTON",
		"CONTROLLER",
		"DIALOG",
		"GYROA",
		"GYROSYNC",
		"GYROV",
		"INKEY$",
		"STICK",
		"STICKEX",
		"TOUCH",
		"XOFF",
		"XON",
		"RESULT",
		"ACCEL",
		"INPUT",
		"LINPUT",
	]),
	WikiCategory("Time",[
		"DATE$",
		"DTREAD",
		"TIME$",
		"TMREAD",
		"MAINCNT",
		"MILLISEC",
		"VSYNC",
		"WAIT",
	]),
	WikiCategory("Multiplayer",["MPCOUNT","MPEND","MPGET","MPHOST","MPLOCAL","MPNAME$","MPRECV","MPSEND","MPSET","MPSTART","MPSTAT"]),
	WikiCategory("cat/Files",["DLCOPEN","FILES","PROJECT","RENAME","RESULT","SAVE","LOAD","DELETE","CHKFILE","EXEC","USE"]),
	WikiCategory("String",["ASC","CHR$","VAL","STR$","FORMAT$","HEX$","BIN$","INC","MID$","LEFT$","RIGHT$","SUBST$","INSTR"]+array_string),
	WikiCategory("Array",["FILL","SORT","RSORT","MIN","MAX","ARYOP","RINGCOPY","BIQUAD","BQPARAM","FFT","FFTWFN","IFFT"]+array_string),
	WikiCategory("Editor",["BACKTRACE","CLIPBOARD","ERRLINE","ERRNUM","ERRPRG","KEY","PRGDEL","PRGEDIT","PRGGET$","PRGINS","PRGNAME$","PRGSET","PRGSIZE","PRGSLOT","OPTION"]),
	WikiCategory("System",["EXTFEATURE","FREEMEM","HARDWARE","VERSION"]),
	WikiCategory("Labels",["DATA","READ","RESTORE","COPY","BGMSETD","GOTO","GOSUB","CHKLABEL","SPDEF","SPANIM","SPFUNC","BGFUNC","ON","IF"]),
	WikiCategory("Flow",["BREAK","CONTINUE","ELSE","ELSEIF","END","ENDIF","FOR","GOSUB","GOTO","IF","NEXT","ON","REPEAT","RETURN","STOP","THEN","UNTIL","WEND","WHILE"]),
	WikiCategory("Variables and Functions",["CALL","COMMON","DIM","VAR","OUT","SWAP","CHKCALL","CHKVAR","SPFUNC","BGFUNC","DEF"]),
])

tree.sanitize()

#keywords={,,,,,,,,,,,,,,"REM",,,,,,,,}

#no need for DLC category. just put a note on each page maybe?
#well I guess it would be nice to have a list of all DLC commands to know what you're buying
#make a "sound expansion DLC or whatever" category?

#,,,
# ,,,,,,,,,,,
# ,,
# ,,,,,,,,,,,

title = {page:page for page in tree.all_pages()}

def load_titles(filename):
	if(os.path.isfile(filename)):
		print("Reading titles")
		for line in open(filename).read().split("\n"):
			colon = line.find(":")
			if colon>=0:
				title[line[0:colon]]=line[colon+1:]
	else:
		print("Warning: titles file missing")

# for any pages where the title is different from the filename, this is used:
# titles do not NEED to be unique, but it's best if they are, to avoid confusion