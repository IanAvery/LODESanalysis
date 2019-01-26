import pandas as pd
import time

def aggregateWork(df, aggregationLevel, outputPath):
	if aggregationLevel == 'Tract':
		aggDF = df
		aggDF = aggDF[aggDF['workTractGEOID'].isin(tracts)]
		print(aggDF.head())
		aggDF = aggDF.groupby(['workTractGEOID', 'homeTractGEOID']).sum()[fields]
		print(aggDF.head())
		aggDF.to_csv(outputPath)
	if aggregationLevel == 'Blockgroup':
		aggDF = df
		aggDF = aggDF[aggDF['workBkgpGEOID'].isin(blockgroups)]
		print(aggDF.head())
		aggDF = aggDF.groupby(['workBkgpGEOID', 'homeBkgpGEOID']).sum()[fields]
		print(aggDF.head())
		aggDF.to_csv(outputPath)

def aggregateHome(df, aggregationLevel, outputPath):
	if aggregationLevel == 'Tract':
		aggDF = df
		aggDF = aggDF[aggDF['homeTractGEOID'].isin(tracts)]
		aggDF = aggDF.groupby(['homeTractGEOID', 'workTractGEOID']).sum()[fields]
		aggDF.to_csv(outputPath)
	if aggregationLevel == 'Blockgroup':
		aggDF = df
		aggDF = aggDF[aggDF['homeBkgpGEOID'].isin(blockgroups)]
		aggDF = aggDF.groupby(['homeBkgpGEOID', 'workBkgpGEOID']).sum()[fields]
		aggDF.to_csv(outputPath)

if __name__ == '__main__':

	#	Time it
	start = time.time()

	## File Paths
	inputCSV = '/Volumes/sdc-sus$/CEE224Y/Resilience/Data_Library/LODES 2015/Origin_Destination/ca_od_2015_combined.csv'
	outputWorkCSV = '/Volumes/sdc-sus$/CEE224Y/Resilience/LODES_analysis/NorthFairOaks_Work_Blockgroup.csv'
	outputHomeCSV = '/Volumes/sdc-sus$/CEE224Y/Resilience/LODES_analysis/NorthFairOaks_Home_Blockgroup.csv'

	## Data Processing Options
	# Can aggregate LODES data to 'Tract' or 'Blockgroup', or not at all and maintain Block aggegation
	aggregationLevel = 'Blockgroup'

	## Which census tract(s) are you interested in? 
	tracts = ['06081610500','06081610601','06081610602'] # Use for North Fair Oaks
	#tracts = ['06001402800']

	## Which census blockgroup(s) are you interested in?
	blockgroups = ['060816105001','060816105004','060816106021','060816105002', '060816105003', '060816106024','060816106023','060816106022', '060816106011', '060816106013', '060816106012'] # Use for North Fair Oaks
	#blockgroups = ['060014028001']
	

	# Fields to aggregate data to tracts
	fields = ['S000', 'SA01', 'SA02', 'SA03', 'SE01', 'SE02', 'SE03', 'SI01', 'SI02', 'SI03']

	## Read input OD CSV
	print('Reading input CSV')
	df = pd.read_csv(inputCSV)
	df = df.drop(columns=['createdate'])
	df[['w_geocode','h_geocode']] = df[['w_geocode','h_geocode']].astype(str)

	# Ensure there is a leading zero in the block GEOID
	df['w_geocode'] = df['w_geocode'].str.zfill(15)
	df['h_geocode'] = df['h_geocode'].str.zfill(15)

	# Add GEOIDs for tracts and blockgroups
	df['workTractGEOID'] = df['w_geocode'].str.slice(0, 11)
	df['homeTractGEOID'] = df['h_geocode'].str.slice(0, 11)

	df['workBkgpGEOID'] = df['w_geocode'].str.slice(0, 12)
	df['homeBkgpGEOID'] = df['h_geocode'].str.slice(0, 12)

	# Remove duplicate rows
	df = df.drop_duplicates(subset=['w_geocode', 'h_geocode'], keep='first')

	# Run aggregation functions
	aggregateWork(df, aggregationLevel, outputWorkCSV)
	aggregateHome(df, aggregationLevel, outputHomeCSV)

	end = time.time()
	print("{} seconds".format((end - start)))

