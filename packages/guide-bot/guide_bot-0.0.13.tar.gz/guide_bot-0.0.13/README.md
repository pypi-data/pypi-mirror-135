# Early version of guide_bot in python

This project is a rewrite of the guide_bot software that was originally coded in MATLAB, https://github.com/mads-bertelsen/guide_bot.

The purpose of guide_bot is to automate optimization of neutron guide systems given a simple job description and a description of the desired guide geometry. The guide geometry can be provided with as much or as little detail as desired, and everything not specified will be optimized. This has been used for many ESS instruments in early phases, as this allows investigating a broad range of different guide systems without much effort. guide_bot was also used at PSI for their guide upgrades for existing instruments. The guide simulations are performed by McStas and optimization was performed with iFit, usually on a cluster running SLURM.

The rewrite in python is underway and is thus far from fully functional. The rewrite will provide several important benefits:

* Open source software, no MATLAB license required
* Can depend on McStasScript which will handle McStas jobs, simplifying the guide_bot code
* The original guide_bot could only scan two dimensions, and only certain were allowed, this limitation was removed
* Much easier for the user to add a new figure of merit or source
* Avoided complex parameter space transformations by using constraints during optimization instead
* Can have python code executed before each optimization step, moves complexity away from instrument file
* User defined parameters are possible, which can depend on one another using arbitrary functions
* User defiend constraints can be added to the user defined parameters
* Computing tasks written as pickled python code, easy to perform the task on other hardware
* Now have unit tests (in progress)

This is the earliest public version of the software, and is not yet ready for production. There are many systems which are yet to be added, such as allowing guides that break line of sight, specification of the guide coating, only the bare minimum of plots are shown.

Currently these guide elements are implemented:

* Straight guide (or tapered, start and end dimensions can differ, but the mirrors are straight)
* Elliptic guide
* Curved guide
* Gap
* Slit

The software can be installed through pip with the following line:
```
pip install guide_bot --upgrade
```
As part of the dependencies [McStasScript](https://github.com/PaNOSC-ViNYL/McStasScript) will be installed, this software needs to be configured, follow the instructions on its github page to do so.

To install from git, it is recommended to install the software in a virtual python environment, follow the steps below. This is necessary if a specific branch is to be used, as only the master branch is available through pip.

1) clone the repository
2) navigate to the folder in a terminal
3) create the virtual environement with: python -m venv venv
4) activate the virtual environemnt: source ./venv/bin/activate
5) install required packages with pip: pip install -r requirements.txt
6) install guide_bot with: pip install -e .

Before using guide_bot, that virtual environment need to be activated by repeating step 4.

For any suggestions on development or questions, please write Mads.Bertelsen@ess.eu
The project is funded by the EU project HighNESS and is done under work package 7.

# Breif user manual
The software is still in a very early stage, but can be used by someone curious.

## Setting up a guide_bot project
The main module is called guide_bot and in examples is loaded as gb.
```
import guide_bot as gb
```

### Setting up figure of merit
The figure of merit in guide_bot is reffered to as the sample. Create a sample object to describe the figure of merit, which is a description of the desired beam after the guide. In the example below a list is given for height, that ensures a scan is performed, meaning guide_bot will perform an optimization for both a 1 cm and 3 cm tall sample.
```
sample = gb.Sample(width=0.02, height=[0.01, 0.03],
                   div_horizontal=0.75, div_vertical=1.0,
                   min_wavelength=1.5, max_wavelength=3.0,
                   instrument_length=60, sample_guide_distance=0.5)
```
### Setting up sources
One can set up a source for several reasons, the primary one is the source for the optimization, but its also possible to add sources for analysis. Here we add two sources, one with a scan of moderator heights and one for analysis which can not have scans.

```
moderator = gb.Moderator(name="fom_moderator", width=0.1,
                         height=[0.02, 0.04, 0.06, 0.08, 0.1], guide_start=2.0)

large_moderator = gb.Moderator(name="large_moderator", width=0.2, height=0.2, guide_start=2.0)
```

### Creating the project
Now a project can be created, this uses the sample and source objects defined above. It also includes settings, this can adjust the optimizer and ncount used for optimization and analysis. The analysis moderator is used for analysis in addition to the figure of merit moderator.
```
settings = {"maxiter": 400, "swarmsize": 25, "minstep": 5E-4,
            "ncount": 5E6, "ncount_analysis": 1E8, "logfile": True}

first_project = gb.Project(name="first_project", sample=sample, moderator=moderator,
                           settings=settings, analysis_moderators=large_moderator)
```

### Adding a guide
With a guide_bot run defined, one can add guide geometries to be optimized. Below is an example with a feeder and elliptic guide. The '+=' operator is used to add an additional guide modeule to an existing guide object.
```
guide = first_project.new_guide(name="Elliptic_with_feeder")
guide += gb.Elliptic(name="Feeder", m=4)
guide += gb.Gap(name="Chopper_gap", start_point=6.5, length=0.1, start_width=0.03, start_height=0.04)
guide += gb.Elliptic(name="Main_guide", m=3)
```
Currently these elements are available:
- Gap: Gap in the guide
- Slit: Slit (As gap, but with limited entrance)
- Straight: Guide with straight mirrors
- Elliptic: Elliptic guide
- Curved: Curved guide

All guide elements have the following common keyword arguments:
- start_point: Starting point measured in [m] from the source
- length: Length of the element
- start_width: Width at the start of the element in [m]
- start_height: Height at the start of the element in [m]
- end_width: Width at the end of the element in [m]
- end_height: Height at the end of the element in [m]

These can be used in several ways.
- If not set, it will be a free parameter.
- If set as a float value, that parameter will be locked.
- If set as a list with length two, that will be min, max for that free parameter.

When setting a range with a list, None is allowed for min or max to avoid setting that end of the range, these will be overwritten with default values.

This input scheme should be used for as many of the keyword arguments as possible to streamline the input method. The vast majority of cases can be be handled with only the above input method, but more complex tools are available.

In addition to the above ways, some keyword arguments can be controlled with user defined parameters. The main advantage with these is that one user defined parameter can be set to controll multiple parameters, locking them together.

The user defined parameters are of these three types:
- FixedInstrumentParameter(name, value)
- RelativeFreeInstrumentParameter(name, min_value, max_value)
- DependentInstrumentParameter(name, dependent_list, dependent_function)

The locked parameter sets a specific value for the parameter, similar to setting a float. The free parameter sets a range, similar to setting the min/max values. The dependent parameter depends on one or more other user defined parameters, and have a general function that will be evaluated. An arbitrary number of inputs can be used, but they must match the number of function inputs, a few examples are shown below.

```
guide_width = gb.RelativeFreeInstrumentParameter("guide_width", 0.01, 0.08)
double_guide_width = gb.DependentInstrumentParameter("double_guide_width", [guide_width], lambda x: 2*x)

guide_height = gb.RelativeFreeInstrumentParameter("guide_height", 0.01, 0.1)
guide_area = gb.DependentInstrumentParameter("guide_area", [guide_width, guide_height], lambda x, y: x*y)
```

It is also possible to add user defined constraints to the user defined parameters. This is represented much like a dependent parameter, but where the constraint is considered fulfilled if the returned value of the function is above 0. Such a constraint need to be added to the guide object, as it can not be added to any one guide element.

```
constraint_area = Constraint([guide_area], lambda x: 0.01 - x)
guide.add_constraint(constraint_area)
```

With these parameters defined we can define a completely straight guide with a gap, and a constraint on the guide area.
```
guide = first_project.new_guide(name="straight_with_gaps")
guide += gb.Straight(name="first_section", m=2,
                     start_width=guide_width, end_width=guide_width,
                     start_height=guide_height, end_height=guide_height)
guide += gb.Gap(name="chopper_gap", start_point=6.5)
guide += gb.Straight(name="second_section", m=2,
                     start_width=guide_width, end_width=guide_width,
                      start_height=guide_height, end_height=guide_height)
guide.add_constraint(constraint_area)
```

### Special options for each module

The elliptic guide module have the following special options:
- minor_axis_x: The minor axis of the elliptic guide in the horizontal direction [m]
- minor_axis_y: The minor axis of the elliptic guide in the vertical direction [m]
- max_width: Maximum width of the guide [m]
- max_height: Maximum height of the guide [m]

The curved guide module have the following special options:
- angle: The angle the curved guide rotates, together with its length this defines the curvature, given in radians
- bend: String to give direction of curve, can be "left", "right", "up" or "down"

Notice that due to limitations in the used McStas component, the gravity is disabled in the curved segments, and the width / height is constant, so end_width and end_height will be set to the start values.


### Writing the project to disk
Before writing the job to disk, its good practice to print the job to ensure it has the expected guides and scan. 

```
print(first_project)
```
```
guide_bot Project named 'first_project'
Included guides: 
  Elliptic_with_feeder
  straight_with_gaps
Moderator scan configurations: 5
Sample scan configurations: 2
Total optimizations to be performed: 20
```
Then the run can be performed, which will write the project folder to disk.
```
first_project.write()
```
If the project is to be executed on a cluster, a cluster configuration need to be added. The package has a default folder for cluster config files called cluster_config, another path can be given with the keyword argument config_path.
```
from guide_bot.cluster import SLURM
DMSC = SLURM.ClusterSLURM(cluster_name="DMSC")
first_project.write(cluster=DMSC)
```
If the project is being executed on a local computer, one has to run each task written to disk with the runner. Navigate to the correct folder in python with for example os.chdir and execute the RunFromFile method with the path to the task file.
```
gb.RunFromFile("Ballistic_with_feeder_sam_height_0_mod_height_4.plk")
```

## Launching a run on a cluster
In order to launch a project on a cluster, one have to specify the desired cluster when writing the project to disk as detailed above. Then the entire generated project folder is uploaded to the cluster, for example:
```
scp -r first_project mbertelsen@login.esss.dk:/users/mbertelsen/py_guide_bot/tests/.
```
Then login to the cluster and navigate to the project folder. In the project folder there will be a number of launch_all scripts corresponding to each queue configured for the cluster. For the DMSC cluster, only quark is configured correctly.
```
./launch_all_quark.sh
```
This will launch all the guide optimizations simultaniously, and after optimization analysis will be performed along with plots describing the simulated beam. When all the jobs have concluded, download the project folder.

## Analyzing the data
The amount of data produced by a guide_bot run can be quite overwhelming, but there are tools included to get an overview and dive into the data. This is done through widgets in jupyter notebooks.

From a terminal, navigate to the project folder on your computer and open a jupyter notebook.
```
jupyter notebook
```

Load the guide_bot packages for analysis.
```
import matplotlib
%matplotlib widget

from guide_bot.scan_visualization.interfaces import Results
```

To create a Result object, provide the path to a project folder produced by guide_bot where at least some of the optimizations have been started
```
results = Results("cluster_data/scan_demo_slit")
```
The results object can show which optimizations succeeded with the *show_status* method.
```
results.show_status()
```
It is possible to browse the contained data using widgets in a jupyter notebook, these are accessed by different methods.

- *plot_guide*: Plots the optimized guide
- *plot_any_monitor*: Plots any single monitor
- *compare_monitors*: Compare 1D monitors for any number of guides
- *compare_monitors_scan*: Compare 1D monitors over a scan
- *plot_sum*: Shows sum of any monitor as function of scan

Showing an interface is done by calling the corresponding method.
```
results.plot_any_guide()
```

Its possible to access the data directly through the overview attribute, which is an object of type ScanOverview, that contains the data. This object can contain a lot of data in a complex structure, so here an example is shown on how to retrieve a single dataset, along with how to find the legal indices.
```
data = results.overview.data["Elliptic_with_feeder"][1,3]["fom_moderator"].runs["fom_wavelength_band"].get_data("Lambda")
```
The data object is first indexed with the guide name, an overview is available from the results object:
```
results.get_guide_names()
```
The next field is the scan indices, and an overview of the indicies can be retrieved with *show_scan*.
```
results.show_scan()
```
The last field in the data dictionary is the used moderator, these can be found from *get_moderators*
```
results.get_moderators()
```
The resulting data object contains a runs attribute with the data, and the available runs can be displayed with *show_runs*. This will include some wavelength snapshots where a single wavelength is used, and some wavelength ranges, one of which is the fom_wavelength_band which was the one used for the optimization.
```
results.overview.data["Elliptic_with_feeder"][1,3]["fom_moderator"].show_runs()
```
A single run correspond to one McStas simulation, and there are multiple monitors available. These can be shown with *get_monitor_list*.
```
results.overview.data["Elliptic_with_feeder"][1,3]["fom_moderator"].runs["fom_wavelength_band"].get_monitor_list()
```
And finally the desired dataset can be retrieved.
```
data = results.overview.data["Elliptic_with_feeder"][1,3]["fom_moderator"].runs["fom_wavelength_band"].get_data("Lambda")
```

