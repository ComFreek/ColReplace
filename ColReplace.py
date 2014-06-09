#!/usr/bin/env python
"""Plugin for Notepad++ which provides a row and column constrained search/replace feature
See the GitHub project page for more information: https://github.com/ComFreek/ColReplace
"""

import re

__author__ = "ComFreek"
__copyright__ = "Copyright 2014, ComFreek"
__credits__ = []
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "ComFreek"


def getIntRangeInput(desc, title, defText):
	rangeStr = notepad.prompt(desc, title, defText)
	if (rangeStr == None):
		return None
	
	numbers = rangeStr.split(',')
	if not (len(numbers) == 2):
		return None

	try:
		return [int(numbers[0]), int(numbers[1])]
	except ValueError:
		return None

def getUserInputs():
	rows = getIntRangeInput("Please enter the range of rows being taken into account.\n" + "Format:x,y where x and y >= 1", "ColReplace - Enter rows", "")
	if (rows == None):
		return None
	
	cols = getIntRangeInput("Please enter the range of columns being taken into account.\n" + "Format:x,y where x and y >= 1", "ColReplace - Enter columns", "")
	if (cols == None):
		return None

	# Normalize user input because row and col access
	# are zero based
	rows[0] -= 1
	rows[1] -= 1

	cols[0] -= 1
	cols[1] -= 1

	needle = notepad.prompt("Enter needle", "Enter needle")
	if (needle == None):
		return None

	replacement = notepad.prompt("Enter replacement", "Enter replacement")
	if (replacement == None):
		return None
	
	return {'rows': rows, 'cols': cols, 'needle': needle, 'replacement': replacement}

def replaceLine(contents, lineNumber, totalLines, userInputs):
	# expose dictionary entries to local variables for easier access
	rows = userInputs['rows']
	cols = userInputs['cols']
	needle = userInputs['needle']
	replacement = userInputs['replacement']
	
	if not (rows[0] <= lineNumber <= rows[1]):
		return 1
		
	contents = contents.strip()

	before = contents[0:cols[0]]
	after = contents[cols[1]:]
	middle = contents[cols[0]:cols[1]]
		
	newMiddle = middle.replace(needle, replacement)
		
	editor.replaceLine(lineNumber, before + newMiddle + after)

userInputs = getUserInputs()

def replaceLineWrapper(contents, lineNumber, totalLines):
	replaceLine(contents, lineNumber, totalLines, userInputs)

if not (userInputs == None):
	editor.forEachLine(replaceLineWrapper)