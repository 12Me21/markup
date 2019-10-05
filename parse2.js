function escape_html(text){
	return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/\n/g, "<br>").replace(/"/g, "&quot;").replace(/'/g, "&apos;");
}

function tags(name) {
	return {start: "<"+name+">", end: "</"+name+">"};
}

options = {
	escape_text: escape_html,
	
	heading: {
		start: ["<h1>","<h2>","<h3>","<h4>","<h5>","<h6>"],
		end: ["</h1>","</h2>","</h3>","</h4>","</h5>","</h6>"],
	},
	horizontal_line: "<hr>",
	//code
	inline_code: tags("code"),
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
	//lists
	list: tags("ul"),
	list_item: tags("li"),
	//table stuff
	table: {start: "<table><tbody>", end: "</tbody></table>"},
	row: tags("tr"),
	cell: tags("td"),
	header_cell: tags("th"),
	//text styles
	bold: tags("b"),
	italic: tags("i"),
	underline: tags("u"),
	strikethrough: tags("s"),
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
		//===============
		// { group start
		} else if (c == '{') {
			scan();
			stack.push(["group"]);
		//=============
		// } group end
		} else if (c == '}') {
			scan();
			close_all(false);
		//========
		// * bold
		} else if (c == '*') {
			scan();
			do_markup("bold", options.bold, '*');
		//========
		// / italic
		} else if (c == '/') {
			scan();
			do_markup("italic", options.italic, '/');
		//========
		// _ underline
		} else if (c == '_') {
			scan();
			do_markup("underline", options.underline, '_');
		//=================
		// ~ strikethrough
		// perhaps it should be +text+ or =text= or ...
		} else if (c == '~') {
			scan();
			do_markup("strikethrough", options.strikethrough, '~');
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
		//=================
		// |... table
		} else if (c == '|') {
			// I think somewhere here I use skip_linebreak when I shouldnt ...
			scan();
			var top = stack_top();
			// continuation
			if (top[0] == "table") {
				skip_linebreak();
				//--------------
				// | | next row
				if (c == '|') {
					scan();
					if(top.columns == null) //end of first row
						top.columns = top.row_cells;
					/*if (top.row_cells < top.columns) { //not enough cells in row
						
					} else {*/
						top.row_cells = 0;
						if (top.header)
							output += options.header_cell.end;
						else
							output += options.cell.end;
						output += options.row.end + options.row.start;
						
						if (c == '*') {
							scan()
							top.header = true;
							output += options.header_cell.start;
						} else {
							top.header = false;
							output += options.cell.start;
						}
						skip_linebreak();
				//--------------------------
				// | next cell or table end
				} else {
					top.row_cells++;
					// end of table
					// table ends when number of cells in current row = number of cells in first row
					// single-row tables are not easily possible ..
					if (top.columns != null && top.row_cells > top.columns) {
						if (top.header)
							output += options.header_cell.end;
						else
							output += options.cell.end;
						stack.pop();
						output += options.row.end;
						output += options.table.end;
						skip_linebreak();
					// next cell
					} else {
						if (top.header)
							output += options.header_cell.end + options.header_cell.start;
						else
							output += options.cell.end + options.cell.start;
					}
				}
			// start of new table
			} else {
				stack.push({"0": "table", header:false, columns: null, row_cells: 0});
				output += options.table.start + options.row.start;
				if (c == '*') {
					scan();
					stack_top().header = true;
					output += options.header_cell.start;
				} else
					output += options.cell.start;
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

	close_all(true);
	
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
	
	function close_all(force) {
		while (stack.length) {
			var top = stack.pop();
			if (top[0] == "heading") {
				output += options.heading.end[top[1]];
				skip_linebreak();
			} else if (top[0] == "list") {
				output += options.list_item.end;
				output += options.list.end;
				skip_linebreak();
			} else if (top[0] == "table") {
				if (top.header)
					output += options.header_cell.end;
				else
					output += options.cell.end;
				output += options.row.end + options.table.end;
				skip_linebreak();
			} else if (char_in(top[0], ["bold", "italic", "underline", "strikethrough"])) {
				output += options[top[0]].end;
			} else if (top[0] == "group") {
				if (!force)
					return;
			} else {
				console.log("unknown unclosed object", top);
			}
		}
	}
	
	function do_markup(type, tags, symbol) {
		if (can_start_markup(type)) {
			stack.push([type]);
			output += tags.start;
		} else if (can_end_markup(type)) {
			stack.pop();
			output += tags.end;
		} else
			output += symbol;
	}
	
	function can_start_markup(type) {
		return (
			(!code[i-2] || char_in(code[i-2], " \t\n({'\"")) && //prev char is one of these (or start of text)
			!char_in(c, " \t\n,'\"") && //next char is not one of these
			!stack_has(type) //not already inside this type of block
		);
	}
	
	function can_end_markup(type) {
		return (
			stack_top()[0] == type && //there is an item to close
			!char_in(code[i-2], " \t\n,'\"") && //prev char is not one of these
			(!c || char_in(c, " \t\n-.,:!?')}\"")) //next char is one of these (or end of text)
		);
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
	
	function stack_has(type) {
		for (var i = 0; i < stack.length; i++)
			if (stack[i][0] == type)
				return true;
		return false;
	}
	
	function char_in(chr, list) {
		return chr && list.indexOf(chr) != -1;
	}
}
