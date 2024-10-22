# Project klima-kollektiv

* Communication via slack channel [project-klima-kollektiv-2024-07](https://correlaid.slack.com/archives/C07DAG9RR52).
* Big files (and all raw data) and useful presentations are stored in our [Google Drive](https://drive.google.com/drive/u/0/folders/1NIZPTE6bbTeMzjccTsxFNPS_JI491H-i).
* [Wiki](https://github.com/CorrelAid/klima-kollektiv/wiki) for tutorials and other help.
* Minutes from our weekly meetings are stored [here](https://drive.google.com/drive/u/0/folders/1GW-cFpNl4-H6kCT7CsSK6VPhYxSsGWI1).


## For Project Set Up:
* Clone repo to local folder (local repo).
* Create virtual environment using requirements.txt and update virtual environment after pull from remote repo.
* Folder raw_data is empty because files are too large for github. fill the folder only in your local repo from the [Google Drive folder data](https://drive.google.com/drive/u/0/folders/1IkIbwRA1dFFJGyGPFCmTpKO5LOPnoxR_). Georeferencing was done using QGIS software. 
* Do not push any large files to remote repo, especially any large files from local raw_data folder.
* Every folder contains a README.md for clear information.
* Folder raw_data is empty because files are too large for github. Fill the folder only in your local repo from the [Google Drive Ordner data](https://drive.google.com/drive/u/0/folders/1IkIbwRA1dFFJGyGPFCmTpKO5LOPnoxR_).

  
## Creating Virtual Environments:
[here using conda and pip]
1. Open a Anaconda prompt. Per default you are in your base environment (base). Using Power Shell requires running ''' conda init powershell''' first to set up conda.
2. Execute the following commands:
```
 cd path-to-your-project-folder
 conda create -n klima-kollektiv   # or whatever virtual environment name
 conda activate klima-kollektiv     # you are now in your virtual environment (klima-kollektiv)
 pip install -r requirements.txt       # installing via pip enables saving and updating dependencies using only requirements.txt, using conda requires also a exporting a .yml file
```
3. Select the environment in your project in your IDE.

## Updating Virtual Environments:

_Adding something to your virtual environment_

You have to do this in order to call the library in your project.
1. Open a prompt like Anaconda prompt. Per default you are in your base environment (base).
2. Execute the following commands:
 ```
 conda activate klima-kollektiv     # you are now in your virtual environment (klima-kollektiv)
 conda install new-library          # add other libraries to your virtual environment (if no virtual environment was activated they will be installed in the base environment, not recommended)
 cd path-to-your-project-folder     # in case you are not already in your project folder
 pip freeze > requirements.txt
```
3. Include requirements.txt file in your push.

_Updating versions, dependencies and additional libraries_

You should do this whenever the requirements.txt file has changed since your last commit.
1. Open a prompt like Anaconda prompt. Per default you are in your base environment (base).
2. Execute the following commands:
 ```
 conda activate klima-kollektiv     # you are now in your virtual environment (klima-kollektiv)
 cd path-to-your-project-folder     # in case you are not already in your project folder
 pip install -r requirements.txt --upgrade
```
3. Select the environment in your project in your IDE.
 

_About the Choice of the IDE_ 

* VS Code: outside of the virtual environment.
  * You can select the virtual environment using the shortcut ```CTRL + SHIFT + P ``` in VS Code.
  * Select the task "Python: Select Interpreter" and choose your virtual environment. (alternatively in VS Code in the right corner)

* In any other python IDE like Spyder, Jupyter notebook: the chosen IDE has to be inside the virtual environment.
* Another libary to add to the virtual environment: 
```
conda activate klima-kollektiv # your are now in your virtual environment (klima-kollektiv)
conda install jupyter notebook
jupyter notebook # will open jupyter notebook IDE
```

  
