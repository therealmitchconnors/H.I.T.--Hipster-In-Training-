#!/usr/bin/python
# convert_putty_settings.py
# Ver. 2.0. Reldate 02Mar2012
import fileinput
import re
import string

rgxSession = re.compile(r"(?<=Sessions\\)\S+(?=]$)")
rgxDword = re.compile(r"dword:([0-9a-fA-F]{8})$")
lineNum = 0
fileNum = 0
f = None 
for line in fileinput.input():
	#print line
	lineNum++
	if (not line):
		#empty line, move along
		continue
	if line[:1]=='[':
		#control or session line
		m = rgxSession.search(line)
		if m:
			#session line
			if isinstance(f, file):
				f.close()
			f = open(m.group(0), 'w')
			fileNum++
			#print m.group(0)
		continue
	line = line.replace("\"", "")
	m = rgxDword.search(line)
	if m:
		#line is dword, convert to decimal before writing
		i = int(m.group(1), 16)
		if i >= int('0x80000000', 16):
			i = (-int('0xffffffff', 16)+i-1)
		line = line.replace(m.group(0), str(i))
	if isinstance(f, file):
		f.write(line)
	#print line	
print "Successfully converted $lineNum lines into $fileNum session files!"

# To convert your PuTTy settings from Windows to Linux, open regedit, 
# and navigate to HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions.
# Right click sessions, and export to a .reg file that is accessible to your new
# Linux box.  From Linux, run "/downloadpath/convert_putty_settings.py < /path/to/reg/file.reg"
# from ~/.putty/sessions/.  Then, in that same folder, run 
# "sed -i 's/Font=Courier New/FontName=server:fixed/g' ./*" to ensure that you are 
# using Linux fonts (this line may need to be adapted based on what fonts you were
# using in Wondows).  If after following these steps, PuTTy will still not load
# your sessions, attempt to launch the session from the command line (putty -load "Session Name")
# to get a specific error message.  Happy Tunneling.
