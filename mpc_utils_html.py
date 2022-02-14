def html_begin():
	return '<html><head/><body style=" font-family:''MS Shell Dlg 2''; font-size:8pt; font-weight:400; font-style:normal;">'
	
def html_end():
	return '</body></html>'
	
def html_par(x):
	return '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">{}</p>'.format(x)
	
def html_empty():
	return '<p>\n</p>'
	
def html_boldtext(x):
	return '<span style=" font-size:10pt; font-weight:600;">{}</span>'.format(x)
	
def html_vtop(x):
	return '<span style=" vertical-align:super;">{}</span>'.format(x)
	
def html_href(link,name):
	return '<a href="{}"><span style=" text-decoration: underline; color:#0000ff;">{}</span></a>'.format(link,name)
	
def html_col(color,x):
	return '<span style=" color:{};">{}</span>'.format(color,x)