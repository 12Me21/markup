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

# this is very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very bad
def safe_path(path):
	return not os.path.isabs(path) and not(".." in path)

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
	def all_pages(self, list = set()):
		list.add(self.name)
		for item in self.pages:
			if isinstance(item, WikiCategory):
				item.all_pages(list)
			else:
				list.add(item)
		return list
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
	# check if `name` is the name of a category page
	# return a reference to that category, or None if the page isn't a category or doesn't exist
	def find_category(self, name):
		if self.name == name:
			return self
		for item in self.pages:
			if isinstance(item, WikiCategory):
				x = item.find_category(name)
				if x:
					return x
		return None
	#check for EVIL ABSOLUTE PATHS and duplicate names
	def check_names(self, list = set()):
		assert safe_path(self.name),"Illegal page name: "+self.name
		assert not(self.name in list),"Duplicate page name: "+self.name
		list.add(self.name)
		for item in self.pages:
			if isinstance(item, WikiCategory):
				item.check_names(list)
			else:
				assert safe_path(item),"Illegal page name: "+item
				assert not(item in list),"Duplicate page name: "+item

array_string = []

tree = WikiCategory("index",[
	WikiCategory("category/Math",["ABS","SGN","POW","SQR","LOG","EXP","MIN","MAX","CLASSIFY","Constants",
		WikiCategory("Operators",["INC","DEC","DIV","MOD"]),
		WikiCategory("Rounding",["FLOOR","ROUND","CEIL"]),
		WikiCategory("Trigonometry",["PI","RAD","DEG","SIN","COS","TAN","ASIN","ACOS","ATAN","SINH","COSH","TANH"]),
		WikiCategory("Random",["RND","RNDF","RANDOMIZE"]),
	]),
	WikiCategory("category/Audio",[
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
	WikiCategory("category/Graphics",[
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
		WikiCategory("category/Text",["ATTR","CHKCHR","CLS","COLOR","CSRX","CSRY","CSRZ","FONTDEF","LOCATE","SCROLL","WIDTH","TABSTEP","INPUT","LINPUT","PRINT"]),
		WikiCategory("category/Sprites",["CALLIDX","SPANIM","SPCHK","SPCHR","SPCLIP","SPCLR","SPCOL","SPCOLOR","SPCOLVEC","SPDEF","SPFUNC","SPHIDE","SPHITINFO","SPHITRC","SPHITSP","SPHOME","SPLINK","SPOFS","SPPAGE","SPROT","SPSCALE","SPSET","SPSHOW","SPSTART","SPSTOP","SPUNLINK","SPUSED","SPVAR"]),
		WikiCategory("category/Background",["CALLIDX","BGANIM","BGCHK","BGCLIP","BGCLR","BGCOLOR","BGCOORD","BGCOPY","BGFILL","BGFUNC","BGGET","BGHIDE","BGHOME","BGLOAD","BGOFS","BGPAGE","BGPUT","BGROT","BGSAVE","BGSCALE","BGSCREEN","BGSHOW","BGSTART","BGSTOP","BGVAR"]),
		WikiCategory("category/GRP",["GBOX","GCIRCLE","GCLIP","GCLS","GCOLOR","GCOPY","GFILL","GLINE","GLOAD","GOFS","GPAGE","GPAINT","GPRIO","GPSET","GPUTCHR","GSAVE","GSPOIT","GTRI"]),
	]),
	WikiCategory("category/Input",["BREPEAT","BUTTON","CONTROLLER","DIALOG","GYROA","GYROSYNC","GYROV","INKEY$","STICK","STICKEX","TOUCH","XOFF","XON","RESULT","ACCEL","INPUT","LINPUT"]),
	WikiCategory("category/Time",["DATE$","DTREAD","TIME$","TMREAD","MAINCNT","MILLISEC","VSYNC","WAIT"]),
	WikiCategory("category/Multiplayer",["MPCOUNT","MPEND","MPGET","MPHOST","MPLOCAL","MPNAME$","MPRECV","MPSEND","MPSET","MPSTART","MPSTAT"]),
	WikiCategory("category/Files",["DLCOPEN","FILES","PROJECT","RENAME","RESULT","SAVE","LOAD","DELETE","CHKFILE","EXEC","USE"]),
	WikiCategory("category/String",["ASC","CHR$","VAL","STR$","FORMAT$","HEX$","BIN$","INC","MID$","LEFT$","RIGHT$","SUBST$","INSTR","COPY","PUSH","POP","SHIFT","UNSHIFT","LEN"]),
	WikiCategory("category/Array",["FILL","SORT","RSORT","MIN","MAX","ARYOP","RINGCOPY","BIQUAD","BQPARAM","FFT","FFTWFN","IFFT","COPY","PUSH","POP","SHIFT","UNSHIFT","LEN"]),
	WikiCategory("category/Editor",["BACKTRACE","CLIPBOARD","ERRLINE","ERRNUM","ERRPRG","KEY","PRGDEL","PRGEDIT","PRGGET$","PRGINS","PRGNAME$","PRGSET","PRGSIZE","PRGSLOT","OPTION"]),
	WikiCategory("category/System",["EXTFEATURE","FREEMEM","HARDWARE","VERSION"]),
	WikiCategory("category/Labels",["DATA","READ","RESTORE","COPY","BGMSETD","GOTO","GOSUB","CHKLABEL","SPDEF","SPANIM","SPFUNC","BGFUNC","ON","IF"]),
	WikiCategory("category/Flow",["BREAK","CONTINUE","ELSE","ELSEIF","END","ENDIF","FOR","GOSUB","GOTO","IF","NEXT","ON","REPEAT","RETURN","STOP","THEN","UNTIL","WEND","WHILE"]),
	WikiCategory("category/Variables_and_Functions",["CALL","COMMON","DIM","VAR","OUT","SWAP","CHKCALL","CHKVAR","SPFUNC","BGFUNC","DEF"]),
])

# read line
# if indent increases
	# previous line was category page
	# read until indent level reaches original level


tree.check_names()

#no need for DLC category. just put a note on each page maybe?
#well I guess it would be nice to have a list of all DLC commands to know what you're buying
#make a "sound expansion DLC or whatever" category?

def default_title(page):
	slash = page.rfind("/")
	if slash>=0:
		return page[slash+1:]
	return page

title = {}
for page in tree.all_pages():
	title[page] = default_title(page)

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