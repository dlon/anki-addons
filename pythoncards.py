# TODO:
#	FIXMEs
#	double-check code
#	make it so that &&! and && must be (alone) on their own rows.
#	ignore closing && inside citation marks (i.e. strings)
#	convert output to HTML?
#	! improve security (allows arbitrary execution of code)
#	is it possible share the "scope"?
#		for example, variables declared in one tag are not accessible in other tags without the 'global' statement
#	limit to some templates?

import re
from cStringIO import StringIO
import sys
from aqt.utils import showInfo, showText
from anki.utils import stripHTML
from anki.hooks import addHook

# FIXME: the amperstand tags must be on their own lines
#        don't match the ending '&amp;&amp;' if it's inside a string
rex = re.compile(r'&amp;&amp;!(.*?)&amp;&amp;', re.M | re.S)

def _deHTML(content):
	# replace HTML-symbols
	# NOTE: not sure if this is correct
	lines = content.replace('&nbsp;', ' ')
	lines = re.sub('<br( /)?>|<div>|\r\n|\r', '\n', lines)
	#return anki.utils.stripHTML(lines).split('\n')[1:]
	return stripHTML(lines)[1:]

def mungeQA(html, type, fields, model, data, col):
	stdout_ = sys.stdout
	stderr_ = sys.stderr
	
	for match in rex.finditer(html):
		# remove markup
		lines = _deHTML(match.group(1))
		# exec each line; store stdout and stderr output
		out = StringIO()
		sys.stdout = out
		sys.stderr = out
		try:
			# they probably have to be in one string so that variables (etc) are accessible
			#exec '\n'.join(lines)
			exec lines
		except: # FIXME: make general exception handler
			out += 'FIX EXCEPTIONS\n'
		sys.stdout = stdout_
		sys.stderr = stderr_
		
		# replace tag with output
		html = html.replace(match.group(), out.getvalue().replace('\n', '<br>'))
		#match.span()
	return html

addHook('mungeQA', mungeQA)