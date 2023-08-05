# Work In Progress!

# Air Adverse Effect Index (AAEI)

## Introduction
In this repository, the python code to calculate an Air Adverse Effect Index is presented. The Comptox **Generalized Read-Across Database** [GenRA](https://comptox.epa.gov/genra/) applies Read-Across methodology on a large database of toxicological values for many chemicals. Gaps can be filled, and a report on confidence of the results is given, plus a likeliness that this effect is positive (present). This tool can provide up to 15 *analog* chemicals, which properties will be extrapolated to the chemical of interest. This extrapolation can be exported, this is the input-format for the **AAEI** tool.

Additionally, files for four OpenFOAM simulations are made available. It is explained how these files can be run and how the post-processing steps can be applied to calculate the AAEI.



## Software
A brief list of software used in this project

### OpenFoam
[OpenFoam](https://openfoam.org/) .org version 9 has been used to run the simulation in this repository.
I would recommend installing OpenFOAM V9 through docker, following the guide at https://openfoam.org/download/9-linux/. For linux this leads to a straight-forward setup, which is easily accessible.
There are no instructions on Windows, but this is fairly easy.:
 1. Download and install Docker: https://docs.docker.com/desktop/windows/install/. You might need to setup WSL.
 2. Once setup, go to https://hub.docker.com/r/openfoam/openfoam9-paraview56 and use the docker pull command to start installing the docker.
 3. Run the docker and access it through a terminal, set up some-sort of shared folder in order to work efficiently.

After an installation like this, you access the docker image first and then execute OpenFOAM specific commands. All commands use a certain naming convention, so they are easy to find with autocompletion. To give you a head-start, see the cheat-sheet below.

<img src=https://s3.studylib.net/store/data/025453706_1-bd2eaeb6355a6e966ae4632a763f7e10-768x994.png width="600" height="800">

[Solver capability matrix](https://www.openfoam.com/documentation/guides/latest/doc/openfoam-guide-applications-solvers.html) *(Note: for openfoam.com version, mostly the same but might differ!)*

### PyFoam
[PyFoam](https://pypi.org/project/PyFoam/) Very convenient library which adds functionality and tools for [OpenFoam](#OpenFoam)
 * Used to monitor every simulation with: *pyFoamPlotWatcher --with-all log*
 * Opens number of real-time plots to monitor residuals, specific values
 * *customRegExp* found under some simulation is also shown every timestep, in this case it calculates the total *average gas concentration [ppm]* using functionObjects

### ParaView
[Paraview](https://www.paraview.org/) has been used for analysis of simulation results. A post-processing script is provided to automatically apply the results of the **AAEI**
 * Installation instructions can be found on the website
 * Make sure that you install a version of paraview **with python!** Otherwise the macro-script will not work.

### Jupyter notebook
[Jupyter](https://jupyter.org/) notebooks have been used to do all major data-processing, visualization and analysis. It is also used as an IDE, the **GenRA AEI** scripts have been developed in Jupyter.
 * Installation instructions can be found on website

### Scripts

#### Case-copy script
To ease the copying and management of OpenFOAM cases, a simple script has been written and provided, to copy and clean cases on a per-case basis, it will put the cleaned cases in /CleanCases relative from where you are.
 * Simply make sure it is executable, and run CopyCase \<CaseName\>.

#### AAEI calculation script
The most extensive script here.
it provides standard methods to calculate an output file GenRA_
It provides the following methods:
 * Filter out Metadata from the GenRA files, calculate statistical values and export as **genra_\<formula\>_\<chemical_name\>_metadata.csv**
     * List of all found **Target** afflictions + statistics is exported as **Batch_Report_Target.csv"
     * list of all found **Test** groups + statistics is exported as **Batch_Report_Meta.csv
 * Batch process a group of chemicals in one go
     * Visualizations can be exported with a flag
     * Total summary from this step, **AEI_Norm.csv** needs to be opened in [ParaView](#ParaView), if the automatic application wants to be followed
     * The resulting normalized AEI can be applied to any dataset
         * To averages over time, to determine the **relative** effect on different effect-groups
         * To spatial data, this can locate the more healthier or less healthy locations.
         * To see the contribution to AEI by different **gases**, **test-types** or **effect-types**

#### ParaView AAEI applications script/Macro

First this script needs to be imported into ParaView, name it for example AAEI
Once the AAEI script is imported:
 * Select the source-simulation (*.foam* file in the source-tree)
 * Make sure that there is a **AEI_Norm.csv** available in the ParaView source-tree, values are directly read and applied from there.
 * Run the script [AEI.py](/AEI.py), A pop-up will open
     * give the text-box a comma-separated list of chemicals, such as: **"C10H16","CO2","O3"**
     * press ok/apply/enter, almost instantly many calculators will be added to the source-tree. The final result is put into the **AEI** calculator, all the other ones are appropriately named.


## Adverse effect index

The table below shows the presence of a certain *health/target effect* per row, related to the *test group* it is categorized under in [GenRA](https://comptox.epa.gov/genra/). This categorization is initially used as an intermediate step before calculating the total sum or average.

<img src=gfx/Toxicity_Effects.png width="600" height="700">

<img src=gfx/Weights.png width="450" height="150" align = "right">

The sum or average is normalized, and a matrix can be created with chemical species against test-types or effect-types.
See the image to the right for an example (colored with LibreOffice)


### Method

<img src=gfx/Paraview_AEI.png width="100" height="300" align="right">

 1. go to [GenRA](https://comptox.epa.gov/genra/)
 2. go through the 5 steps:
     * Select target chemical
     * select analogs
     * generate read-across prediction
     * export read-across prediction
     * rename export to **genra_\<formula\>.csv**, in the case of CO2: **genra_CO2.csv**
 3. do this for every chemical you are interested in, or in your simulation (Names need to match!)
 4. By running the script in the following way:
 ```python
fileNames = ["genra_O3","genra_C10H16","genra_CO2","genra_CH2O"]
compoundNames = ["Ozone","D-Limonene","Carbon dioxide","Formaldehyde"]
FileName = "Batch_Report"
BatchReport(fileNames,compoundNames,FileName,Viz=True,fcn="sum")
```
     * GenRA files O3, C10H16, CO2 and CH2O will be processed
     * their compound names are given and matched in the array below, these need to match the names found on GenRA
     * FileName will persist into the export
     * Viz=True will generate a 3D-bubble plot, with X = Effectgroup, Y = species, Z = Testgroup. And bubble-size = positive effect magnitude
     * DEBUG = false will turn off excessive printing of values.
 5. **AEI_Norm.csv** Follows from this step and can be applied however desired.
 6. Follow the steps under [ParaView AAEI applications script/Macro](#ParaView-AAEI-applications-script/Macro) to apply the results to a run simulatin
 7.The resulting normalized AEI can be applied to any dataset
     * To averages over time, to determine the **relative** effect on different effect-groups
     * To spatial data, this can locate the more healthier or less healthy locations.
     * To see the contribution to AEI by different **gases**, **test-types** or **effect-types**
     * To the right the ParaView source-tree is shown, the different effect categories are visible.


### Steps

### 1. Input

### 2. Output

#### .csv

#### graphs and plots

### 3. Apply.

#### Result

## Simulations

### File structure
<img src=gfx/Openfoam_files.png width="150" height="280">
### General case setup

### case 1

### case 2

### case 3

### case 4
<img src=gfx/Sim_Overview_Kazuhide.png width="150" height="280">
<img src=gfx/AEI_opaq.png width="150" height="280">
<img src=gfx/Plane_Definitions_STL.png width="150" height="280">
<img src=gfx/X3_Overview_Geom.png width="150" height="280">
:tada: :fireworks::tada:
Note To Self:
```bash
python setup.py sdist
pip install .  # dry-run from folder
pip uninstall aaei # uninstall
pip install -e # install with symlink
twine upload dist/* #because pip doesn't work anymore for some magical reason.
```
:fireworks::tada: :fireworks:
