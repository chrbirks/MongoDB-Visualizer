import pymongo
import plotly.plotly as pl
from plotly.tools import FigureFactory as FF

client = pymongo.MongoClient("localhost", 27017)

db = client.test # Use DB name 'test'
collection = db.HFF_MRM_Temperature_Status
cursor = collection.find()
#cursor = collection.find({'Temperature_Vec_1.Mean':30}, {'Temperature_Vec_1.Mean': 1})
#cursor = collection.find({'Temperature_Vec_1.Mean':30}, {'Temperature_Vec_1.$.Mean':30})
#cursor = collection.find({}, {'Temperature_Vec_1.Mean':'true', '_id':'false'})
#cursor = collection.find({}, {'Temperature_Vec_1':'true'})

# Find number of records
z = 0
for record in collection.find():
    z += 1

# Matrix with all temperature values. x=temperatures, y=mrms, z=records
# Index using [z][y][x]. First index is 0
values = [[[0 for x in range(4)] for y in range(9)] for z in range(z)]
#print(values)

# For all MRM temperature records
record_index = 0
for record in collection.find():
    #print(record)

    # For all 9 temperature arrays
    for mrm_index in range(0, 9):

        mrm_string = 'Temperature_Vec_' + str(mrm_index+1)
        #print(mrm_string)

        #a = record[mrm_string]['A']
        values[record_index][mrm_index][0] = record[mrm_string]['A']
        #print(values[record_index][mrm_index][0])

        #b = record[mrm_string]['B']
        values[record_index][mrm_index][1] = record[mrm_string]['B']
        #print(values[record_index][mrm_index][1])

        #c = record[mrm_string]['C']
        values[record_index][mrm_index][2] = record[mrm_string]['C']
        #print(values[record_index][mrm_index][2])

        #mean = record[mrm_string]['Mean']
        values[record_index][mrm_index][3] = record[mrm_string]['Mean']
        #print(values[record_index][mrm_index][3])

        #print("*** END OF MRM ***")

    #print("*** END OF RECORD ***")
    record_index += record_index

print(values[0])

#mylist = list(cursor)
#print(mylist)

#print(list(cursor))


####### Plotting using plotly
fig = FF.create_annotated_heatmap(values[0])
pl.iplot(fig, filename='mrm_temperature_status')
