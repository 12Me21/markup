function escape_html(text){
	return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/\n/g, "<br>").replace(/"/g, "&quot;").replace(/'/g, "&apos;");
}

options = {
	heading: {
		start: ["<h1>","<h2>","<h3>","<h4>","<h5>","<h6>"],
		end: ["</h1>","</h2>","</h3>","</h4>","</h5>","</h6>"],
	},
	inline_code: {start: "<code>", end: "</code>"},
	escape_text: escape_html,
	horizontal_line: "<hr>",
	list: {start: "<ul>", end: "</ul>"},
	list_item: {start: "<li>", end: "</li>"},
	code_block: function(text, language) {
		var output = '<pre class="highlight-sb">';
		var prevType = false;
		var opt = undefined;
		if (language == "sb4")
			opt = true;
		else if (language == "sb3")
			opt = false;
		
		highlight_smilebasic(text, function(word, type) {
			if (word) {
				//only make a new span if the CSS class has changed
				if (type != prevType) {
					if (prevType)
						output += "</span>";
					if (type)
						output += "<span class=\""+type+"\">";
				}
				output += escape_html(word);
				prevType = type;
			}
		}, opt);
		output += "</pre>";
		return output;
	},
};

function parse(code, options) { //with (options){
	var i = -1, start;
	var c;
	scan();
	
	var output = "";
	var stack = [];
	var start_of_line = true;
	
	while (c) {
		start_of_line = i <= 0 || code[i - 1] == '\n';
		
		//============
		// Line break
		if (c == '\n') {
			scan();
			line_end();
		//==========
		// \ escape
		} else if (c == '\\') {
			scan();
			output += options.escape_text(c);
			scan();
		//==============
		// #... Heading
		} else if (c == '#' && start_of_line) { //todo: prevent nested headings somehow
			var heading_level = 0;
			while (c == '#') {
				heading_level++;
				scan();
			}
			if (heading_level >= options.heading.start.length) //heading too big
				output += options.escape_text('#'.repeat(heading_level));
			else {
				output += options.heading.start[heading_level];
				stack.push(["heading", heading_level]);
			}
		//==============
		// -... list/hr
		} else if (c == '-' && start_of_line) {
			start = i;
			scan();
			//-----------------------
			// --... horizontal rule
			if (c == '-') {
				scan();
				while (c == '-')
					scan();
				if (c == '\n' || c == '') { //linebreak or end of file
					skip_linebreak();
					output += options.horizontal_line;
				} else {
					output += options.escape_text('-'.repeat(i - start)); //this is wrong?
				}
			//------------
			// - ... list
			} else if (c == ' ') {
				scan();
				stack.push(["list", 0]);
				output += options.list.start + options.list_item.start;
				
			//------------
			// -? nothing
			} else { //no scan here!
				output += options.escape_text('-');
			}
		//==================
		// backtick... code
		} else if (c == '\x60') {
			scan();
			//----------------------
			// backtick inline code
			if (c != '\x60') {
				start = i;
				while (c && c != '\x60') {
					scan();
				}
				output += options.inline_code.start;
				output += options.escape_text(code.substring(start, i));
				output += options.inline_code.end;
				scan();
			//---------------
			// backtick*2...
			} else {
				scan();
				//-----------------------
				// backtick*3 code block
				if (c == '\x60') {
					scan();
					// read language name
					start = i;
					while (c && c != '\n' && c != '\x60')
						scan();
					var language = code.substring(start, i).trim().toLowerCase();
					if (c == '\n')
						scan();
					// TODO: what if users type ```code``` by accident?
					
					// Find end of codeblock
					start = i;
					i = code.indexOf("\x60\x60\x60", i);
					output += options.code_block(code.substring(start, i != -1 ? i : code.length), language);
					if (i != -1) {
						i += 2;
						scan();
					} else {
						i = code.length;
					}
					skip_linebreak();
				//--------------------
				// backtick*2 invalid
				} else {
					scan();
					output += options.escape_text("\x60\x60");
				}
			}
		//================
		// any other char
		} else {
			// TODO: since most of the text will be handled here, it would be better to escape it all at once rather than 1 char at a time...
			output += options.escape_text(c);
			scan();
		}
		//==============
		// end c switch
	}

	close_all();
	
	console.log(output);
	return output;
	
	//things to do at the end of a line
	//note that this is not called when a newline is escaped
	function line_end() {
		while (1) {
			var top = stack_top();
			if (top[0] == "heading") {
				output += options.heading.end[stack.pop()[1]];
			} else if (top[0] == "list") {
				var old_indent = top[1];
				var indent = 0;
				while (c == ' ') {
					scan();
					indent++;
				}
				if (c == '-' && code[i + 1] == ' ') {
					scan();
					scan();
					if (indent > old_indent) {
						stack.push(["list",indent]);
						output += options.list.start + options.list_item.start;
					} else if (indent < old_indent) {
						var indents = [];
						while (1) {
							top = stack_top();
							if (top[0] == "list") {
								if (top[1] == indent)
									break;
								else if (top[1] > indent) {
									indents.push(stack.pop()[1]);
									output += options.list_item.end + options.list.end;
								} else {
									throw Error("Bad list indentation. Got "+indent+" space while expecting: "+indents.join(", ")+", (or more)");
								}
							} else {
								throw Error("Bad list indentation. Item was indented less than start of list (probably)");
							}
						}
						output += options.list_item.end + options.list_item.start;
					} else {
						output += options.list_item.end + options.list_item.start;
					}
				} else {
					while (stack_top()[0] == "list") {
						stack.pop();
						output += options.list_item.end + options.list.end;
					}
				}
				break; // is this right?
			// ...
			} else {
				output += options.escape_text('\n'); //TODO!!!
				break;
			}
		}
	}
	
	function scan() {
		i++;
		c = code.charAt(i);
	}
	
	function close_all() {
		while (stack.length) {
			var top = stack.pop();
			if (top[0] == "heading") {
				output += options.heading.end[top[1]];
			} else if (top[0] == "list") {
				output += options.list_item.end;
				output += options.list.end;
			}
		}
	}
	
	function skip_linebreak() {
		while (c == ' ' || c == '\t')
			scan();
		if (c == '\n')
			scan();
		while (c == ' ' || c == '\t')
			scan();
	}
	
	function stack_top() { return stack[stack.length-1] || [null]; }
}
