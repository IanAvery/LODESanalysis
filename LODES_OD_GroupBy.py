import pandas as pd
import os
import time

"""
~~~~~~~~~~~~~~~~~~~~~~~
LODES Data Aggregation
~~~~~~~~~~~~~~~~~~~~~~~

Steps:
1. Add raw LODES Origin-Destination data to inputCSV path
2. Choose 'Tracts' or 'Blockgroups' for aggregationLevel variable
3. Enter your list of Tracts of Blockgroups of interest in the GEOIDs list
4. Run LODES_OD_GroupBy.py in terminal, outputs will be saved to same directory as input data

"""

def aggregateBlocks(df, homeOrWork, aggregationLevel):
	if aggregationLevel == 'Tract':
		aggDF = df
		aggDF = aggDF[aggDF[homeOrWork+'GEOID'].isin(GEOIDs)]
		aggDF = aggDF.groupby(['workGEOID', 'homeGEOID']).sum()[fields]

	if aggregationLevel == 'Blockgroup':
		aggDF = df
		aggDF = aggDF[aggDF[homeOrWork+'GEOID'].isin(GEOIDs)]
		aggDF = aggDF.groupby(['workGEOID', 'homeGEOID']).sum()[fields]

	aggDF = aggDF.reset_index()

	return aggDF

def groupAggregations(df, GEOIDs, fields, homeOrWork):
	groupDF = df.groupby([homeOrWork+'GEOID'])[fields].sum().reset_index()
	return groupDF

if __name__ == '__main__':

	#	Time it
	start = time.time()

	## File Paths
	inputCSV = '/Users/ianbick/Desktop/LODES_Testing/ca_od_main_JT05_2015.csv'
	basename = os.path.splitext(os.path.basename(inputCSV))[0]
	pathname = os.path.dirname(inputCSV)

	outputWorkCSV = pathname + '/' + basename + '_Work.csv'
	outputHomeCSV = pathname + '/' + basename + '_Home.csv'

	outputWorkGroupCSV = pathname + '/' + basename + '_WorkGrouped.csv'
	outputHomeGroupCSV = pathname + '/' + basename + '_HomeGrouped.csv'

	## Data Processing Options
	# Can aggregate LODES data to 'Tract' or 'Blockgroup', or not at all and maintain Block aggegation
	aggregationLevel = 'Blockgroup'

	if aggregationLevel == 'Blockgroup':
		# Which census blockgroup(s) are you interested in?
		GEOIDs = ['060014028001','060014029001']

	if aggregationLevel == 'Tract':
		# Which census tract(s) are you interested in?
		GEOIDs = ['06081610500','06081610601','06081610602']
	
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

	# Remove duplicate rows
	df = df.drop_duplicates(subset=['w_geocode', 'h_geocode'], keep='first')

	# Add GEOIDs for tracts and blockgroups
	if aggregationLevel == 'Blockgroup':
		df['workGEOID'] = df['w_geocode'].str.slice(0, 12)
		df['homeGEOID'] = df['h_geocode'].str.slice(0, 12)

	if aggregationLevel == 'Tract':
		df['workGEOID'] = df['w_geocode'].str.slice(0, 11)
		df['homeGEOID'] = df['h_geocode'].str.slice(0, 11)

	# Run block aggregation functions
	workAggregation = aggregateBlocks(df, 'work' ,aggregationLevel)
	homeAggregation = aggregateBlocks(df, 'home' ,aggregationLevel)

	workAggregation.to_csv(outputWorkCSV)
	homeAggregation.to_csv(outputHomeCSV)

	# Run grouping functions
	workGEOIDGroup = groupAggregations(workAggregation, GEOIDs, fields, 'work')
	homeGEOIDGroup = groupAggregations(homeAggregation, GEOIDs, fields, 'home')

	workGEOIDGroup.to_csv(outputWorkGroupCSV)
	homeGEOIDGroup.to_csv(outputHomeGroupCSV)

	end = time.time()
	print("{} seconds".format((end - start)))

