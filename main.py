import sys
import json
import dijkstra

#We need to mention __name__ as main as we are importing methods from other classes
if __name__ == '__main__':

 
    #json.load(data_file) #Loading the file containing our vehicles-requets-edges distances

    datastore = json.load(open('data.json','r'))

    #Parsing the input JSON data file into 3 variables with key word in '.....'
    distances = datastore['distances']
    requests = datastore['requests']
    vehicles = datastore['vehicles']

    #Iterating over all the items in vehicles and initializing the availability for each one to TRUE
    for vehicle in vehicles:
        vehicle['available'] = True

    #Creating an object of Dijkstra's class to use the methods inside
    g = dijkstra.Graph()

    #Iterating over all the elements in distances variable and adding vertices/nodes/points it to graph
    for distance in distances:
        #We are adding the zipcode1 and zipcode2(nodes) only after checking whether they already exist in the object 'g'(graph) or not
        #If the zipcode is present, we skip it and if not, we add it to our graph as a new vertex/node point
        if not distance['zipcode1'] in g.get_vertices():
            g.add_vertex(distance['zipcode1'])

        if not distance['zipcode2'] in g.get_vertices():
            g.add_vertex(distance['zipcode2'])

        #Adding the edges to the graph from start
        #passing vertices as arguments, we are drawing an edge between the two nodes and assigning thier weightage.
        g.add_edge(distance['zipcode1'], distance['zipcode2'], distance['distance'])

    """
    print('Graph data:')
    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))
    """

	#Here the input is zipcode and vehicle which requests for particular vehicle at that area
    #This method returns list of all available vehicles along with distances
    def get_vehicle(vehicle_type, zipcode):

        #Here we find the list of all available specified vehicles  
        available_vehicles = [v for v in vehicles if v['type'] == vehicle_type and v['available']]

        #If there are available vehicles
        if len(available_vehicles) > 0:
            g.reset_vertices() #resets our graph
            place = g.get_vertex(zipcode) #Returns Our Starting vertex
            dijkstra.dijkstra(g, place) # setting distance of each node with respect to our starting vertex

            #Stores the distance of available vehicle from origin of request
            for av in available_vehicles:
                av['distance'] = g.get_vertex(av['zipcode']).get_distance()

            #Sorting the list of all the available vehicles, based on key with inline function Lambda(sorts based on Distances)
            #The below contains list of KEY, VALUE pairs
            available_vehicles = sorted(available_vehicles, key=lambda k: k['distance'])
        
        return available_vehicles #Sorted list of available vehicles



#Each request contains the vehicle Type and the Node at which it is requested
    for request in requests:
        #Each request served on FIFO. Providing us with available vehicles sorted on distance 
        ev = get_vehicle(request['vehicle_type'], request['zipcode']) 

        if len(ev) > 0: #If their are  vehicles available 
        	#if required vehicle and request is from same place skip it
        	if request['zipcode'] == vehicles[vehicles.index(ev[0])]['zipcode']:
        		print("No need to process request here:\n","**"*7,"\n")
        		pass
        	else:
	            vehicles[vehicles.index(ev[0])]['available'] = False # Availability to FALSE of nearest vehicle
	            request['vehicle_id'] = ev[0]['id'] 
	            request['distance'] = ev[0]['distance'] 
	            #Here we print we the request processed
	            print("Vehicle Number {} is available at a distance {} from zipcode {} for service" .format(request['vehicle_id'],request['distance'],ev[0]['zipcode'] ))
	            print("Request_NO   vehicle_type   requested_at_zipcode   avialable_vehicle_id	 at_distance of")
	           # [print(k,' ',request[k],end='     ') for k in request] #Printing key value pairs in each of the requests
	            print('',request['id'],"         ",request['vehicle_type'],"    	     ",request['zipcode'],"       	   ",request['vehicle_id'],"      	        ",request['distance'])
	            print('-------------------------------------------------------------------------')

    with open('vehicles_updated.json','w') as f:
        json.dump(requests,f, ensure_ascii=False)
