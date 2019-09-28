var highlighters = {
	 smilebasic: undefined,//sbhl.html,
	 sbconsole: function(code){
		  return code
	 },
};

function escape_html(code){
	 return code.replace(/&/g,"&amp;").replace(/</g,"&lt").replace(/\n/g,"<br>");
}

function highlight(code, language){
	 return (highlighters[language] || escape_html)(code);
}

function escape_html_char(chr){
	 if(chr=='<') return "&lt;"
	 if(chr=='&') return "&amp;"
	 if(chr=='\n') return "<br>\n"
	 return chr;
}

//warning: only works in quoted attributes
function escape_html_attribute(code){
	 return code.replace(/&/g,"&amp;").replace(/"/g,"&quot;");
}

//todo: this should remove weird chars and other stuff
function anchor_name(text){
	 return text.replace(/ /g,"-");
}

function parse(code){
	 var i = -1;
	 var c;
	 var stack = [];
	 code = code.replace(/\r/g,"");

	 function test(c,str){
		  return str.indexOf(c)!=-1;
	 }

	 function has_type(stack,type){
		  for(var i=0;i<stack.length;i++)
				if(stack[i].type == type)
					 return true;
		  return false;
	 }
	 
	 function next(){
		  i++;
		  c = code[i];
	 }

	 function peek(stack){
		  return stack[stack.length-1];
	 }
	 
	 function skip_linebreak(){
		  while(c==' ' || c =='\t')
				next();
		  if(c=='\n')
				next();
		  while(c==' ' || c =='\t')
				next();
	 }

	 function is_start_of_line(){
		  return i==0 || code[i-1]=='\n';
	 }

	 function can_start_markup(type){
		 console.log(c,code[i-1]);
		  return (i-2 < 0 || test(code[i-2]," \t\n){'\"")) && 
		  (!c || !test(c," \t\n,'\"")) && 
		  !has_type(stack, type);
	 }

	 function can_end_markup(type){
		 return stack.length && peek(stack).type==type && (i-2 < 0 || !test(code[i-2]," \t\n,'\"")) && (!c || test(c," \t\n-.,:!?')}\""));
	 }

	 function do_markup(type, tag, symbol){
		 console.log("doing markup heck",stack)
		  if(can_start_markup(type)){
			  console.log("starting")
				stack.push({type:type});
				return "<"+tag+">"
		  }else if(can_end_markup(type)){
				stack.pop();
				return "</" + tag + ">";
		  }else{
				return symbol;
		  }
	 }

	 function markup_exception(message){
		  return Error(message + "\nOn line " + get_line(i));
	 }

	 function get_line(pos){
		  return -1;
	 }

	 function line_end(){
		  var output = "";
		  if(stack.length){
				var top = peek(stack);
				if(top.type == "heading"){
					 output += "</h" + stack.pop().level + ">";
					 next();
					 return output;
				}else if (top.type == "list"){
					 var old_indent = top.indent;
					 next();
					 var indent = 0;
					 while(c==' ' || c=='\t'){
						  indent += c=='\t' ? 4 : 1;
						  next();
					 }
					 if(c=='+'){
						  next();
						  if(indent>old_indent){
								stack.push({type:"list",indent:indent});
								output += "<ul><li>";
						  }else if(indent < old_indent){
								var indents = [];
								while(1){
									 
									 if(stack.length && peek(stack).type == "list"){
										  if(peek(stack).indent == indent)
												break;
										  else if(peek(stack).indent > indent){
												indents.push(stack.pop().indent);
												output += "</li></ul>";
										  }
									 }else{
										  throw Error("Bad list indentation. Got "+indent+" space while expecting: "+indents.join(", ")+", (or more)");
									 }
								}
								output += "</li><li>";
						  }else{
								output += "</li><li>";
						  }
					 }else{
						  while(stack.length && peek(stack).type=="list"){
								stack.pop();
								output += "</li></ul>";
						  }
					 }
					 return output;
				}
		  }
		  output += escape_html_char(c);
		  next();
		  return output;
	 }

	 function parse(){
		  var output = "";
		  next();
		  while(c){
				if(c=='`'){
					 next();
					 if(c=='`'){
						  next();
						  if(c=='`'){
								var language = "";
								while(1){
									 next();
									 if(c=='\n')
										  break;
									 else if(c)
										  language += c;
									 else
										  throw Error("Reached end of input while reading code block language");
								}
								language = language.trim();
								output += '<pre class="'+escape_html_attribute("highlight-"+language)+'">';
								var start = i+1;
								while(1){
									 next();
									 if(c=='`'){
										  next();
										  if(c=='`'){
												next();
												if(c=='`')
													 break;
										  }
									 }
									 if(!c)
										  throw Error("Reached end of input while reading code inside code block");
								}
								output += highlight(code.substring(start,i-2), language);
								output += "</pre>";
								next();
								skip_linebreak();
						  }else{
								output += "``";
								next();
						  }
					 }else{
						  output += "<code>"
						  while(1){
								if(c=='`'){
									 next();
									 if(c=='`'){
										  output += "`";
									 }else{
										  output += "</code>";
										  break;
									 }
								}else if(c){
									 output += escape_html_char(c);
								}else{
									 throw Error("Unclosed ` block");
								}
								next();
						  }
					 }
				}else if(c=='*'){
					 if(is_start_of_line()){
						  next();
						  var heading_level = 1;
						  while(c=="*"){
								heading_level++;
								next();
						  }
						  if(heading_level > 6){
								throw Error("Heading too deep");
						  }
						  if(c==' '){
								output += "<h" + heading_level + ">";
								next();
								stack.push({type:"heading",level:heading_level});
								continue;
						  }else if(heading_level!=1){
								throw Error("Missing space after heading");
								continue;
						  }
					 }else{
						  next();
					 }
					 output += do_markup("bold","b","*");
				}else if(c=='/'){
					 next();
					 output += do_markup("italic","i","/");
				}else if(c=='_'){
					 next();
					 output += do_markup("underline","u","_");
				}else if(c=='\n'){
					 output += line_end();
				}else if(c=='-' && is_start_of_line()){
					 next();
					 var dashes = 1;
					 while(c=='-'){
						  dashes++;
						  next();
					 }
					 if(dashes>=4){
						  skip_linebreak();
						  output += "<hr>";
					 }else{
						  output += "-"*dashes;
					 }
				}else if(c=='+' && is_start_of_line()){
					 next();
					 if(c==' '){
						  stack.push({type:"list",indent:0});
						  output += "<ul><li>";
					 }else{
						  output += "+";
					 }
				}else if(c=='\\'){
					 next();
					 if(c){
						  output += escape_html_char(c);
						  next();
					 }
				}else if(c=='['){
					 next();
					 if(c=='['){
						  next();
						  var start = i;
						  while(1){
								next();
								if(c==']'){
									 next();
									 if(c=='[' || c==']')
										  break;
								}else if(!c){
									 throw Error("Unclosed link");
								}
						  }
						  var url = code.substring(start,i-1);
						  // [[url]]
						  if(c==']'){
								// Search for last .
								for(var dot=url.length-1;dot>=0;dot--){
									 if(url[dot]=='.')
										  break;
								}
								if(dot>=0 && ["png","jpg","jpeg","bmp","gif"].indexOf(url.substr(dot+1).toLowerCase())!=-1){
									 output += '<img src="' + escape_html_attribute(url) + '">';
								}else if(dot>=0 && ["ogg","mp3","wav"].indexOf(url.substr(dot+1).toLowerCase())!=-1){
									 output += '<audio controls src="' + escape_html_attribute(url) + '"></audio>';
								}else{
									 output += '<a href="' + escape_html_attribute(url) + '">' + escape_html(url) + "</a>";
								}
								next();
						  // [[url][text]
						  }else{ //c is '['
								output += '<a href="' + escape_html_attribute(url) + '">';
								next();
								stack.push({type:"link"});
						  }
					 }else{
						  output += "[";
					 }
				}else if(c==']'){
					 next();
					 if(c==']' && stack.length && peek(stack).type == "link"){
						  next();
						  stack.pop();
						  output += "</a>";
					 }else
						  output += "]";
				}else if(c=='{'){
					 next();
					 stack.push({type:"group"});
				}else if(c=='}' && stack.length && peek(stack).type=="group"){
					 next();
					 stack.pop();
				}else if(c=='|'){
					
					 next();
					 if(stack.length && peek(stack).type=="table"){
						  skip_linebreak();
						  // next row
						  if(c=='|'){
							  console.log("new table rowww",peek(stack))
								next();
								if(peek(stack).columns == null){
									console.log("first row or something")
									 peek(stack).columns = peek(stack).cells_in_row;
								}
								if(peek(stack).cells_in_row < peek(stack).columns){
									 throw Error("not enough cells in table row");
								}else{
									 peek(stack).cells_in_row = 0;
									 if(peek(stack).header){
										  output += "</th></tr>";
										  peek(stack).header = false;
									 }else{
										  output += "</td></tr>";
									 }
									 if(c=='*'){
										  next();
										  peek(stack).header = true;
										  output += "<tr><th>"
									 }else{
										  output += "<tr><td>"
									 }
									 skip_linebreak();
								}
						  }else{
								peek(stack).cells_in_row++;
								//end of table
								if(peek(stack).columns != null && peek(stack).cells_in_row > peek(stack).columns){
									console.log("table end")
									 if(peek(stack).header){
										  output += "</th>";
									 }else{
										  output += "</td>";
									 }
									 stack.pop();
									 output += "</tr></tbody></table>";
									 skip_linebreak();
							   // next cell
								}else{
									console.log("next cell",peek(stack).columns)
									 if(peek(stack).header){
										  output += "</th><th>";
									 }else{
										  output += "</td><td>";
									 }
								}
						  }
					 // start of new table
					 }else{
						 console.log("new table")
						  stack.push({type:"table",columns:null,cells_in_row:0,header:false});
						  output += "<table><tbody><tr>";
						  if(c=="*"){
								next();
								peek(stack).header = true;
								output += "<th>"
						  }else
								output += "<td>"
					 }
				}else{
					 output += escape_html_char(c);
					 next();
				}
		  }
		  output == line_end();
		  if(stack.length){
				throw Error("Reached end of file with unclosed items: ") //need to fix ???
		  }
		  return output;
	 }
	 try{
		  return parse();
	 }catch(e){
		  alert(e);
		  return "error you heck";
	 }
}


					 
						  
						

		  
										  
						  
