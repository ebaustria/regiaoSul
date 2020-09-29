# regiaoSul
A set of files for visualizing long-distance simulations from The-ONE

## Requirements
* Python 3.4+

## Getting Started
Clone the necessary repositories:

```
git clone https://github.com/ebaustria/regiaoSul.git
git clone https://github.com/ebaustria/deck.gl.git
git clone https://github.com/ebaustria/the-one.git
```

In order to visualize public transit in deck.gl, it is necessary to create a file that maps local coordinates (used in the-ONE) to GPS coordinates. There are two ways to do this depending on whether you are visualizing regiaoSul or a short-distance scenario.

### regiaoSul

Navigate to ```regiaoSul``` and run ```readMap.py```:

```
cd regiaoSul
python3 -m readMap
```

On line 136, ```readMap.py``` writes a file called ```gps_coordinates_brazil.csv```. This file is a mapping of the local coordinates of each node (used in the ONE and taken from ```local_coordinates_brazil.txt```) to that node's corresponding GPS coordinates. Running ```readMap.py``` also writes a WKT linestring file for each route that consists of GPS coordinates. These files are written on line 132. The WKT linestring file names have the format ```route_name + _gps_nodes.wkt```. Move each of the WKT linestring files to ```regiaoSul/routes```.

### Short-Distance Scenarios

Navigate to ```the-one``` and compile the program:

```
./compile.sh
cd the-one
```

**Note**: If you are using Java 11, you will need to compile the program with ```./compileJava11.sh```. ```the-one/README.txt``` or ```the-one/README.md``` can be consulted for more information on compiling and running the-ONE, if necessary.

Navigate to ```the-one/toolkit/gtfs``` and prepare a map for one of the scenarios in ```the-one/toolkit/gtfs/map_definitions```:

<pre>
cd toolkit/gtfs
./prepare_map.sh <i>your_map_definition</i>.sh
</pre>

Next, navigate to the map you just created, create the GTFS files for the map, navigate to the output directory, and compress the files into a zip drive:

<pre>
cd maps/<i>your_map</i>
pfaedle -D -m tram -x ./<i>your_map</i>.osm .
cd gtfs-out
zip <i>your_map</i>.zip *
</pre>

Navigate back to ```the-one/toolkit/gtfs``` and run ```scenario.py``` using the zip drive you just made as an argument:

<pre>
cd ..
cd ..
cd ..
python3 scenario.py -t 0 maps/freiburg1/gtfs-out/<i>your_map</i>.zip
</pre>

Running ```scenario.py``` creates the files that are needed to run the simulation with your map, and it will also create a file called ```gps_coordinates.csv```. This file contains the mapping of local coordinates to GPS coordinates. Move this file to the ```regiaoSul``` repository.

### Running the-ONE

After creating the mapping of local coordinates to GPS coordinates, navigate to the-one, compile the code if you haven't already, and run the simulation:

<pre>
cd
cd <i>your_path_to</i>/the-one
./compile.sh
./one.sh <i>your_map</i>_settings.txt
</pre>

# CONTINUE WORKING HERE
**Note**: It may be necessary to remove the flight recorder in order to run the simulation. If this is the case, open ```the-one/one.sh``` and remove ```-XX:+FlightRecorder  -XX:StartFlightRecording=duration=60s,filename=myrecording.jfr ``` from the file. Afterwards, it should work. When the simulation is finished, it will write two reports. One of the reports has the following form: DTNHost name, local coordinates, timestamp. The DTNHost name is the name of the DTNHost in question, the local coordinates are a pair of local coordinates used in the ONE, and the timestamp is the simulation time at which the DTNHost is located at the local coordinates in question. The other report has the following form: local coordinates, timestamp, action. The action is a short string that describes the messaging activity of the DTNHost at that timestamp.

Open ```the-one/reports```. Find the aforementioned reports. They should be the most recent reports. Their names should end with ```LocalCoordinatesReport.txt``` and ```MessageCoordinatesReport.txt```. If it is your first time running the simulation, they will be the only files in ```the-one/reports```. Rename the report that ends with ```LocalCoordinatesReport.txt``` as ```local_coordinates_brazil.txt```, and rename the report that ends with ```MessageCoordinatesReport.txt``` as ```messages.txt```. Move both of these files to the ```regiaoSul``` repository.

Next, open ```the-one/data/regiaoSul```. Find ```stations.wkt``` and ```cities.wkt``` and copy them to the ```regiaoSul``` repository. Do not change the name of either file.

Navigate to ```regiaoSul```, create a virtual environment, and install the required dependencies:

```
cd ..
cd regiaoSul
python3 -m venv --without-pip .venv
curl -sS https://bootstrap.pypa.io/get-pip.py | .venv/bin/python
source .venv/bin/activate
pip install -r requirements.txt
```

## Creating JSON Files:

Run ```json_generator.py```:

```
python3 -m json_generator
```

The first function call in ```json_generator.py``` reads ```local_coordinates_brazil.txt``` and ```gps_coordinates_brazil.csv```, parses the data in each file, and uses it to build a list of dictionaries that each contain a list of GPS coordinates and a list of corresponding timestamps for a vehicle. This list of dictionaries is then written to a JSON file called ```trips.json``` that can be used to visualize vehicle movement in deck.gl. The second function call in ```json_generator.py``` reads in each of the WKT linestring files, parses the data in them, and creates a list of dictionaries that each contain a route name, a color, and a list of the route's GPS coordinates in linestring form. This list is then written to a JSON file called ```routes_brazil.json``` that can be used to visualize the public transit lines in deck.gl. The third function call in ```json_generator.py``` reads ```stations.wkt``` and ```cities.wkt```, parses the data in each file, and builds a list of dictionaries that each contain a single pair of GPS coordinates. This list is then written to a JSON file called ```stops.json``` that can be used to visualize public transit stops in deck.gl. The third function call reads ```arrivals.txt``` (includes timestamps for when vehicles arrive at stops in the ONE) and ```gps_coordinates_brazil.csv```, parses the data in each file, and builds a list of dictionaries. Each dictionary contains a vehicle name, a set of coordinates, a single timestamp, and a color (RGB format). The list is written to a file called ```arrivals.json```, which is used to visualize the arrivals of vehicles at public transit stops in deck.gl. The final function call reads ```messages.txt``` and ```gps_coordinatesbrazil.csv``` and creates a file called ```messages.json``` which is used to visualize messaging activity in the-ONE. This part of the visualization is still a work in progress.

## Visualizing the Data
Create a remote repository and add it if you haven't already. Stage the five JSON files from the previous section to be committed, commit them, and push them to your remote:

<pre>
git remote add <i>remote_name</i> https://github.com/<i>user</i>/<i>repo</i>.git
git add trips.json
git add routes_brazil.json
git add stops.json
git add arrivals.json
git add messages.json
git commit -m "<i>message</i>"
git push <i>remote_name</i> master
</pre>

deck.gl uses special classes called layers to visualize datasets. Each layer class produces a different effect. In this visualization, we use five different layers: TripsLayer, PathLayer, IconLayer, ScatterplotLayer, and TextLayer. Each of the JSON files we've created needs to be passed to one of these layers so they can be visualized.

Open ```deck.gl/examples/website/trips/app.js```. We need to modify ```app.js``` to get it to visualize our data.

**Note**: A functioning version of ```app.js``` is located in the ```regiaoSul``` repository and can be consulted for an example. If you would like to skip the rest of this section, you should be able to navigate to ```deck.gl/examples/website/trips``` and replace the version of ```app.js``` that is located there with the version of ```app.js``` that is located in ```regiaoSul```. Once you have replaced ```app.js``` you can continue with these steps starting at "Running the Visualization".

First, make sure the necessary layer classes are imported at the top of the file:

```
import {TripsLayer} from '@deck.gl/geo-layers';
import {PathLayer} from '@deck.gl/layers';
import {IconLayer} from '@deck.gl/layers';
import {TextLayer} from '@deck.gl/layers';
import {ScatterplotLayer} from '@deck.gl/layers';
```

You will need a mapbox token to see the base map. Create a mapbox token at https://www.mapbox.com/ if you don't already have one and set the token in ```app.js``` directly beneath the imports:

<pre>
const MAPBOX_TOKEN = "<i>your_mapbox_token</i>";
</pre>

**Note**: Be sure to enclose the mapbox token in quotes.

Next, we need to provide the raw data URLs of our JSON arrays to ```app.js```. We will define constant references to the raw data URLs within the ```DATA_URL``` constant. Open the raw data for each JSON file in the remote GitHub repository you have set up and assign each raw data URL as a string to a constant in ```DATA_URL```. For example, you might define the constant reference to ```trips.json``` as:

```
TRIPS: 'https://raw.githubusercontent.com/ebaustria/regiaoSul/master/trips.json'
```

In general, ```DATA_URL``` and the constants defined within it should have the following structure:

<pre>
const DATA_URL = {
  <i>CONST_NAME</i>: 'https://raw.githubusercontent.com/<i>your_github_profile</i>/<i>your_remote_repository</i>/<i>branch</i>/<i>your_data.json</i>',
  ...
};
</pre>

**Note**: Do not forget to add commas in between constant references.

Scroll down to ```export default function App```. At the beginning of the function, use the previously defined constant references to define variables to pass to each layer instance:

<pre>
export default function App({
  <i>data_variable</i> = DATA_URL.<i>CONST_NAME</i>,
  ...
</pre>

The final step is to initialize each layer instance in the ```layer``` constant and provide its respective properties. The correspondence between the datasets and the layers is as follows:

* trips.json --> TripsLayer
* routes_brazil.json --> PathLayer
* stops.json --> IconLayer
* arrivals.json --> ScatterplotLayer
* messages.json --> TextLayer

The following sections provide examples of how to initialize the necessary layers within ```layer```, as well as some additional information.

### TripsLayer
```app.js``` already includes an instance of TripsLayer that can be used in the visualization with minimal changes:

```
    new TripsLayer({
      id: 'trips',
      data: trips,
      getPath: d => d.path,              //do not edit
      getTimestamps: d => d.timestamps,  //do not edit
      getColor: [253, 128, 93],
      opacity: 1,
      widthMinPixels: 3,
      rounded: true,
      trailLength,                       //do not edit
      currentTime: time,                 //do not edit
      getWidth: 3,
      shadowEnabled: false
    }),
```

**Note**: ```data:``` is the property that determines which dataset the layer uses. Every layer needs to be provided with a data property.

The name that is assigned to ```data:``` should correspond to one of the URL variables you defined in the ```App``` function. ```trips``` is passed to the data property of TripsLayer by default. If you gave the constant reference that corresponds to ```trips.json``` a different name in ```App```, make sure you pass that name to the data property instead of ```trips```.

### PathLayer
The general template for the PathLayer's properties is:

<pre>
    new PathLayer({
      id: '<i>layer_id</i>',
      data: <i>your_variable_name</i>,
      widthMinPixels: 3,    //deck.gl will not render a path thinner than 3 pixels no matter how far the user zooms out
      rounded: true,
      getPath: e => e.path,   //do not edit
      getColor: e => e.color,  //do not edit
      getWidth: 3           //the width of each path in meters
    }),
</pre>

**Note**: The ordering of the layer initializations within ```layer``` seems to affect the visibility of some layers. For this reason, it is best to initialize the PathLayer **before** you initialize the TripsLayer in your code.

### IconLayer
The general template for the IconLayer's properties is:

<pre>
    new IconLayer({
      id: '<i>layer_id</i>',
      data: <i>your_variable_name</i>,
      iconAtlas: 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png',   //do not edit
      iconMapping: ICON_MAPPING,  //do not edit
      getIcon: g => 'marker',     //do not edit
      sizeScale: 10,
      getPosition: g => g.coordinates,  //do not edit
      getSize: g => 3,
      getColor: g => g.color,           //do not edit
      getPixelOffset: [0, -10]          //offsets the icon 10 pixels upward
    }),
</pre>

Also make sure to add the following lines below ```DATA_URL```:

```
const ICON_MAPPING = {
  marker: {x: 0, y: 0, width: 128, height: 128, mask: true}
};
```

### ScatterplotLayer
The general template for the ScatterplotLayer's properties is:

<pre>
    new ScatterplotLayer({
      id: '<i>layer_id</i>',
      data: <i>your_variable_name</i>,
      radiusScale: 6,
      radiusMinPixels: 0,     //the minimum circle radius in pixels that deck.gl will display
      radiusMaxPixels: 100,   //the maximum circle radius in pixels that deck.gl will display
      getPosition: d => d.coordinates,                         //do not edit
      getRadius: d => isVisible(d.timestamp, time, 70, 600),   //only edit last two parameters in function call
      getFillColor: d => [253, 128, 93],
      updateTriggers: {
        getRadius: [d => isVisible(d.timestamp, time, 70, 600)]   //only edit last two parameters in function call
      },
      transitions: {
        getRadius: {
          type: 'spring',     //do not edit
          stiffness: 0.01,
          damping: 0.15,
          duration: 100,
          enter: d => [0]     //do not edit
        }
      }
    }),
</pre>

### TextLayer
The general template for the TextLayer's properties is:

<pre>
    new TextLayer({
      id: '<i>layer_id</i>',
      data: <i>your_variable_name</i>,
      getPosition: d => d.coordinates,    //do not edit
      getText: d => d.notification,       //do not edit
      getSize: 16,
      getColor: d => [0, 0, 0, isVisible(d.timestamp, time, 30, 255)],     //only edit last two parameters in function call
      backgroundColor: [255, 255, 255],
      getTextAnchor: 'middle',            //determines where the text is displayed relative to the object's position ('start', 'middle', or 'end')
      getAlignmentBaseline: 'top',     //determines where the text is displayed relative to the object's position ('top', 'center', or 'bottom')
      getPixelOffset: [0, 3],
      updateTriggers: {
        getColor: [d => [0, 0, 0, isVisible(d.timestamp, time, 30, 255)]]  //only edit last two parameters in function call
      }
    }),
</pre>

**Note**: Layer IDs must be unique.

**Note**: Each of the layers presented here has additional properties that have not been included in any of the above code samples. The information provided here is only intended to help users create a working visualization. https://deck.gl/docs/api-reference/layers can be consulted for more information on deck.gl's layers, their properties, and how to modify them.

## Running the Visualization
Navigate to ```deck.gl/examples/website/trips```, install the dependencies, and run the visualization:

```
cd ..
cd deck.gl/examples/website/trips
npm install
npm start
```

https://deck.gl/docs can be consulted for more information, if necessary.

## License
This code is licensed under the MIT license.
