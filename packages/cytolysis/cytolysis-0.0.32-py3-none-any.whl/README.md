# Cytolysis
A python module to facilitate the automatic analysis cytosim simulations.
By itself, it does not include many analysis functions but mostly an API.

## Installation
```bash
pip3 install cytolysis
```

## Requirements
Requires Python3 and modules numpy, pandas.  
To visualize the simulation in iPython (Jupyter Notebook), 
you should install [ipyvolume](https://ipyvolume.readthedocs.io/en/latest/install.html) :
```bash
conda install -c conda-forge ipyvolume
```

## Practical examples
We provide several examples where we analyze the result of a simulation for an example [config file](example_data/example.cym). 
This simulation has two asters of microtubules brought to the center by the rigidity of the microtubules and by the activity of dyneins.  
![](examples/example.jpg) 

An example counting the number of fiber points for each filament, and at each time:
```bash
python3 examples/example_fibers.py
```
An example where we compute the fiber bending energy as a function of time
```bash
python3 examples/example_fiber_curvature.py
```
We can also analyze any cytosim class that can be reported, by creating custom objects. 
For example, this is done here for solids and spaces :
```bash
python3 examples/example_solid.py
```
Several ipython notebooks are also available in the notebook folder. 

## Interface (examples)
Import the module : 
```python
from cytolysis import cytosim_analysis as ana
```

The main class is *Simulation*, a list of time frames. Create an instance of a simulation analysis via :
```python
microtubule_reports={'points' : 'fiber_points.txt' }
simul = ana.Simulation(reports={'microtubule': microtubule_reports},
                        config='config.cym') 
```

You can specify analysis functions for the different simulation objects, specifying by object name :
```python
def count_points(fiber):
    return fiber.shape[0]

def count_fibers(frame):
    return len(frame.fibers)

analyzer={}
analyzer['microtubule'] = {'pts_number': count_points}
analyzer['frame'] = {'fib_number': count_fibers}
```

You can then run the analysis :
```python
simul.make_analysis(analyzer=analyzer)
```

The analysis of objects is stored as pandas dataframes in the frames. For exemple, the analysis of microtubules for frame *5* is stored in :
```python
simul[5].analysis['microtubule']
```
Similarly, the analysis for couples 'arp_2_3' at frame 10 is stored in :
```python
simul[10].analysis['arp_2_3']
```
Simul is a set of frames, and the results of the analysis of all frames can be accessed in :
```python
simul.frames_analysis
```
While a global analysis of the simulation is available in : 
```python
simul.analysis
```

The module contains a function to export analysis dataframes into csv files :
```python
ana.export_analysis(simul.frames_analysis, 'frames.csv')
```

There is also experimental support for showing the system in 3D in notebooks :
```python
simul.show(frame_number)
```


## Components

### Simulation
The class *Simulation* is a set of *frames*, instances of the class [Frame](#frame). Input arguments : 
- reports : a dictionary of dictionaries of pathes to report files.
- options : a dictionary of dictionaries of options.
- config : path to the config file
- dim : dimensionality of the simulation (by default, 3)

Simulation has a method *make_analysis* to perform the analysis. 
This takes as option *analyzer*, a dictionary of dictionaries of analysis functions.  

*simulation.make_analysis* performs the analysis specified in *analyzer["simulation"]*, 
and the result is stored in *simulation.analysis*.  

As a set of frames , simulation implements *simulation.analyze(frame, analyzer=..., ... )* (see [Object_set](#object_set)).
This performs the analysis specified in *analyzer['frame']*. The results are stored in *simulation.frames_analysis*
 
### Frame
Each frame contains several types of dictionaries of object_sets.
Each dictionary is of the type : { name : [object_set](#object_set) }.
For instance, if fibers have been loaded, they are available in *frame.objects["fibers"]*.

Once the analysis has been performed, the analysis results are stored in :
- *frame.analysis[object_type]*, e.g. *frame.analysis["fibers"]*.

Frame implements the analysis method *frame.make_analysis(...)* that calls the *object_set.analyze(object, ...)* method of all object sets. 
 
### Object_set
Object set is a class derived from list. *Fibers_set* and *Couples_set* are derived from *Object_set*. Input arguments :
- *name* : name of the object (e.g. "microtubule")
- *type* : type of the object (e.g. "fiber")  
Optional input arguments :
- *config* : the pile read from the configuration file
- *build* : a function to build the object set from the reports  
 
Beyond the initialization (*__init__*) method, object set need to implement the methods :
- *object_set.analyze(object, ... )* : a function that analyzes *object*, a given item from the object set
- *object_set.type* : object type 
- *object_set.name* : object name 
- *object_set.id* : object id (a number) 
- *object_set.properties* : a dictionary of properties read from the config file
- *object_set.show* : a way to plot the object set in 3D using iPyVolume

### Analysis
All the analysis results (*simulation.analysis*, *frame.analysis["fibers"]*, etc.) are stored as Pandas dataframes 
and, by default, exported as csv files. Examples:   
- *frame.analysis["fiber"][fiber_name]* is a dataframe with as many rows as there are fibers.
- *simulation.frame_analysis* is a dataframe with as many rows as there are frames.
- *simulation.analysis* is a dataframe with a single row.

Therefore, if one wants to look at the distribution of some property among objects for a given frame, 
one would export *frame.analysis[object_type][object_name]*.  
If one wants to analyze something over time, one would export *simulation.frame_analysis*.  
If one wants a single line to sumarize the simulation, for instance in order to compare different simulations, one would
export *simulation.analysis*.

### Plotting
When used in iPython, cytolysis can represent the system in 3D, 
and allows to plot objects differently according to their properties, 
see this [example](notebooks/display_examples.ipynb).
