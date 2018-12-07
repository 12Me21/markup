import collections

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
			if isinstance(item, WikiCategory):
				output.update(item.categories(page))
			elif item==page:
				output.add(self)
		return output
	# get a full list of all pages (files)
	def all_pages(self):
		output = set()
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

array_string = ["COPY","PUSH","POP","SHIFT","UNSHIFT"]

tree = WikiCategory("Root",[
	WikiCategory("Math",["ABS","SGN","POW","SQR","LOG","EXP","MIN","MAX","CLASSIFY",
		WikiCategory("Operators",["INC","DEC","DIV","MOD"]),
		WikiCategory("Rounding",["FLOOR","ROUND","CEIL"]),
		WikiCategory("Trigonometry",["PI","RAD","DEG","SIN","COS","TAN","ASIN","ACOS","ATAN","SINH","COSH","TANH"]),
		WikiCategory("RNG",["RND","RNDF","RANDOMIZE"])
	]),
	WikiCategory("String",["ASC","CHR$","VAL","STR$","FORMAT$","HEX$","BIN$","LEN","INC","MID$","LEFT$","RIGHT$","SUBST$","INSTR"]+array_string),
	WikiCategory("Array",["FILL","SORT","RSORT","MIN","MAX","ARYOP"]+array_string)
])