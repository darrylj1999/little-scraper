# Python 3
import tkinter
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tkinter import filedialog
from tkinter import messagebox

def getDetails(soup):
	data = []
	table = soup.find("tbody", class_="column-rows")
	for br in soup.find_all("br"):
		br.replace_with(" ")
	for row in table.find_all("tr"):
		data.append([])
		for col in row.find_all("td"):
			data[-1].append( col.text )
	return data

class System:
	def __init__(self):
		# Initialize Memory
		self.databases = []

		# Launch Chrome 74
		self.homepageURL = "https://www.salesgenie.com/sign-in/"
		self.driver = webdriver.Chrome(executable_path='/Users/darryl/Documents/RESEARCH/SALESGENIE/chromedriver')
		# Go to Website
		self.driver.get( self.homepageURL )

		# Launch GUI
		self.top = tkinter.Tk()
		# Configure UI Elements
		snapshotButton = tkinter.Button(self.top, text="Save Snapshot to Memory", command=self.snapshot)
		undoButton = tkinter.Button(self.top, text="Undo Latest Snapshot", command=self.undo)
		saveButton = tkinter.Button(self.top, text="Save Memory to File", command=self.save)
		clearButton = tkinter.Button(self.top, text="Clear Memory", command=self.clear)
		exitButton = tkinter.Button(self.top, text="Exit", command=self.exit)
		# Set positions
		snapshotButton.pack()
		undoButton.pack()
		saveButton.pack()
		clearButton.pack()
		exitButton.pack()
		# Start Read-Eval-Print loop
		self.top.mainloop()

	def snapshot(self):
		data = getDetails( BeautifulSoup(self.driver.page_source, features="html.parser") )
		frame = pd.DataFrame.from_records( data )
		self.databases.append(frame)

	def undo(self):
		try:
			self.databases.pop()
		except IndexError:
			tkinter.messagebox.showinfo("Error", "Nothing Left to Undo!")
		except:
			tkinter.messagebox.showinfo("Error", "Unspecified error at undo()")

	def save(self):
		try:
			filename = tkinter.filedialog.asksaveasfilename(initialdir = "./", title = "Select file", filetypes = (("Excel Files","*.xlsx"),("all files","*.*")))
			pd.concat( self.databases, ignore_index=True ).sort_values(by=[0]).to_excel(filename, index=False, header=None)
		except:
			tkinter.messagebox.showinfo("Error", "Unspecified error at save()")

	def clear(self):
		self.databases = []

	def exit(self):
		self.clear()
		self.driver.close()
		self.top.destroy()

me = System()
