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

databases = [] 
url = "https://www.salesgenie.com/sign-in/"

# Launch Chrome 74
driver = webdriver.Chrome(executable_path='/Users/darryl/Documents/RESEARCH/SALESGENIE/chromedriver')

# Go to Website
driver.get(url)

def snapshot():
	global databases, driver
	data = getDetails( BeautifulSoup(driver.page_source, features="html.parser") )
	frame = pd.DataFrame.from_records( data )
	databases.append(frame)

def undo():
	global databases
	try:
		databases.pop()
	except IndexError:
		tkinter.messagebox.showinfo("Error", "Nothing Left to Undo!")
	except:
		tkinter.messagebox.showinfo("Error", "Unspecified error at undo()")

def save():
	global databases
	try:
		database = pd.concat( databases, ignore_index=True )
		filename = tkinter.filedialog.asksaveasfilename(initialdir = "./",title = "Select file",filetypes = (("Excel Files","*.xlsx"),("all files","*.*")))
		database.to_excel(filename, index=False, header=None)
	except:
		tkinter.messagebox.showinfo("Error", "Unspecified error at save()")

def clear():
	global databases
	databases = []
	

userame = "al@allschoolfundraising.com"
password = "little1"

top = tkinter.Tk()
snapshotButton = tkinter.Button(top, text="Save Snapshot to Memory", command=snapshot)
undoButton = tkinter.Button(top, text="Undo Latest Snapshot", command=undo)
saveButton = tkinter.Button(top, text="Save Memory to File", command=save)
clearButton = tkinter.Button(top, text="Clear Memory", command=clear)
snapshotButton.pack()
undoButton.pack()
saveButton.pack()
clearButton.pack()
top.mainloop()
