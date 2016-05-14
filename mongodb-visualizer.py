import pymongo
import numpy
#import colorlover as cl

# Offline plotting
import plotly
#plotly.offline.init_notebook_mode()
# Cloud plotting
#import plotly.plotly as py
#py.sign_in('chrbirks', 'wi7e2kfa8h')

from plotly.tools import FigureFactory as FF
import plotly.graph_objs as go

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

        values[record_index][mrm_index][0] = record[mrm_string]['A']
        #print(values[record_index][mrm_index][0])

        values[record_index][mrm_index][1] = record[mrm_string]['B']
        #print(values[record_index][mrm_index][1])

        values[record_index][mrm_index][2] = record[mrm_string]['C']
        #print(values[record_index][mrm_index][2])

        values[record_index][mrm_index][3] = record[mrm_string]['Mean']
        #print(values[record_index][mrm_index][3])

        #print("*** END OF MRM ***")

    #print("*** END OF RECORD ***")
    record_index += 1

#print(values)
#print(values[0])

#mylist = list(cursor)
#print(mylist)

#print(list(cursor))


####### Plotting using plotly
mrm_label = ['MRM 1', 'MRM 2', 'MRM 3', 'MRM 4', 'MRM 5', 'MRM 6', 'MRM 7', 'MRM 8', 'MRM 9',]
temperature_label = ['A', 'B', 'C', 'Mean']
#bupu = cl.scales['9']['seq']['BuPu']
#bupu500 = cl.interp( bupu, 500 ) # Map color scale to 500 bins
#colorscale = [[0, '#3D9970'], [150, '#001f3f']]

# Transpose x and y in array
values_trans = numpy.array(values[1]).transpose()

# Plot
fig = FF.create_annotated_heatmap(values_trans, x=mrm_label, y=temperature_label, colorscale='Jet') # 'Viridis'
fig['layout'].update({
    'title':'HFF_MRM_Temperature_Status',
    'autosize':False,
    'width':'1000',
    'height':'600',
    #'margin':go.Margin(l=50, r=50, b=100, t=100, pad=4)
    #'paper_bgcolor':'#7f7f7f',
    #'plot_bgcolor':'#c7c7c7'
})
# Cloud plotting
#py.iplot(fig, filename='mrm_temperature_status')
# Offline plotting
plotly.offline.plot(fig, filename='mrm_temperature_status.html')
