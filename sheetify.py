import pandas

prefix = "page_"
postfix = ".csv"
start = 1
end = 7
sheet = "Page 1"
massive_df = pandas.DataFrame()

with pandas.ExcelWriter('Surprise AZ.xlsx') as writer:
	for i in range(start, end+1):
		filename = prefix + str(i) + postfix
		df = pandas.read_csv(filename, header=None)
		# Add as separate sheet
		#df.to_excel( writer, sheet_name="Page "+str(i), index=False )
		# Add on same sheet
		massive_df = pandas.concat( [massive_df, df], ignore_index=True )
	massive_df.sort_values(by=[0]).to_excel( writer, sheet_name=sheet, index=False, header=False )
