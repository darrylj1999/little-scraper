# Python 3
import os
import tkinter
import pandas as pd
import pandas.io.formats.excel
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tkinter import filedialog
from collections import defaultdict

def getDetails(soup):
	data = defaultdict(list)
	table = soup.find("tbody", class_="column-rows")
	for br in soup.find_all("br"):
		br.replace_with(" ")
	for row in table.find_all("tr"):
		for col in row.find_all("td"):
			heading = col.div['class'][-1].replace('-data', '')
			data[heading].append(col.text)
	return data

class System:
	def __init__(self):
		# Make sure user-defined header formats are cleared
		pandas.io.formats.excel.header_style = None
		# Initialize Memory
		self.databases = []

		# Launch Chrome 74
		self.homepageURL = "https://www.salesgenie.com/sign-in/"
		self.chromedriverPath = os.path.join(os.getcwd(), 'chromedriver')
		self.driver = webdriver.Chrome(executable_path=self.chromedriverPath)
		# Go to Website
		self.driver.get( self.homepageURL )

		# Launch GUI
		self.top = tkinter.Tk()
		self.top.title("Little Scraper")
		# Configure UI Elements
		self.statusLabelText = tkinter.StringVar()
		self.statusLabelText.set("View table in List format without extending Preview!")
		self.statusLabel = tkinter.Label(self.top, textvariable=self.statusLabelText, fg="red")
		self.snapshotButton = tkinter.Button(self.top, text="Save Snapshot to Memory", command=self.snapshot)
		self.undoButton = tkinter.Button(self.top, text="Undo Latest Snapshot", command=self.undo)
		self.saveButton = tkinter.Button(self.top, text="Save Memory to File", command=self.save)
		self.clearButton = tkinter.Button(self.top, text="Clear Memory", command=self.clear)
		self.exitButton = tkinter.Button(self.top, text="Exit", command=self.exit)
		# Set positions
		self.statusLabel.pack()
		self.snapshotButton.pack()
		self.undoButton.pack()
		self.saveButton.pack()
		self.clearButton.pack()
		self.exitButton.pack()
		# Start Read-Eval-Print loop
		self.top.mainloop()

	def snapshot(self):
		try:
			data = getDetails( BeautifulSoup(self.driver.page_source, features="html.parser") )
			frame = pd.DataFrame( data )
			self.databases.append(frame)
			self.statusLabelText.set("Snapshot! Number of Pages = {}".format( len(self.databases) ))
		except AttributeError:
			self.statusLabelText.set("Incorrect Table Format! Number of Pages = {}".format( len(self.databases) ))
		except:
			self.statusLabelText.set("Unspecified error at snapshot()")

	def undo(self):
		try:
			if len(self.databases) == 0:
				self.statusLabelText.set("Nothing to Undo!")
			else:
				self.databases.pop()
				self.statusLabelText.set("Undo! Number of Pages = {}".format( len(self.databases) ))
		except:
			self.statusLabelText.set("Unspecified error at undo()")

	def save(self):
		try:
			if len(self.databases) == 0:
				self.statusLabelText.set("Nothing to Save!")
			else:
				# Formatting parameters
				isBold = True
				fontSize = 10
				sheetName = "Sheet1"
				sortBy = "SICDescription"
				# Get filename from User
				filename = tkinter.filedialog.asksaveasfilename(initialdir=os.getcwd(), title = "Select file", filetypes = (("Excel Files","*.xlsx"),("all files","*.*")))
				writer = pd.ExcelWriter(filename, engine='xlsxwriter')
				# Set font formatting
				headerFormat = writer.book.add_format( {'bold': isBold, 'font_size': fontSize} )
				writer.book.formats[0].set_font_size( fontSize )
				# Output through writer
				memory = pd.concat(self.databases, ignore_index=True).sort_values( by=[sortBy] )
				memory.to_excel(writer, header=None, startrow=1, index=False, sheet_name=sheetName)
				# Write the column headers with the defined format.
				for col, headerName in enumerate( memory.columns.values ):
					writer.sheets[ sheetName ].write(0, col, headerName, headerFormat)
				# Save to file
				writer.save()
				self.statusLabelText.set("Saved to {}! Number of Pages = {}".format( filename, len(self.databases) ))
		except:
			self.statusLabelText.set("Unspecified error at save()")

	def clear(self):
		if len(self.databases) == 0:
			self.statusLabelText.set("Nothing to Clear!")
		else:
			self.databases = []
			self.statusLabelText.set("Cleared! Number of Pages = {}".format( len(self.databases) ))

	def exit(self):
		self.clear()
		self.driver.close()
		self.top.destroy()

me = System()
