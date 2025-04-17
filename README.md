# ENPM611 Project 📊 GitHub Issue Analysis - Team 5

### Introduction:
Welcome to our data-driven analysis of GitHub issues using the open-source Poetry [poetry](https://github.com/python-poetry/poetry/issues) project. This repository explores issue resolution patterns, contributor behavior, and community interactions by processing GitHub issue data.

### Project Overview:
This project was developed as part of the ENPM611 Software Engineering class. The goal is to extract meaningful insights from GitHub Issues (not commits), visualizing patterns around labels, contributors, and reactions.
This is the template for the ENPM611 class project.

### Objective:
Investigate how issues are labeled, discussed, and resolved
Identify top contributors and common bottlenecks
Visualize trends in issue handling using matplotlib

### Features Implemented:

Feature 1: Contributor and Reaction Analysis
1. Identifies the top issue creators and closers
2. Counts all reactions (e.g., thumbs up, heart, rocket)
3. Visualizes results using a three-panel bar chart

Feature 2: Label Frequency and Resolution Time
1. Analyzes most-used labels across all issues
2. Calculates average resolution time per label (in days)
3. Visualized with bar chart + annotations

Feature 3: Label-Based Deep Dive (User Input Required)
1. Input a label like bug, status/triage, or kind/feature
Outputs:
1. Total number of issues
2. Average comments
3. Average close time
4. Most active contributor and resolved count
5. Visualization: histogram of close times + annotations

### Files Description:

- `scripts/fetch_issues.py`: Implements the functionality to fetch all the issues by using GITHUB_TOKEN and returns a json file called poetry_data.json that has all the issues.
- `data/poetry_data.json`: A Json file with all the issues.
- `config.py`: Supports configuring the application via the `config.json` file.
- `config.json`: Stores key project settings such as the dataset path and GitHub repository details (owner and repo), allowing consistent and centralized configuration access across your ENPM611 analysis scripts.
- `run.py`: This is the module that will be invoked to run your application. Based on the `--feature` command line parameter, one of the three analyses implemented will be run. Below you can see how to run features.
- `ClassDiagram/`: This folder contains the Class Diagram and its code.
- `EntityRelationshipDiagram/`: This folder contains the Entity Relationship Diagram and its code.
- `Analysis/analysisOne`: This shows the graphical representation of the Top Issue creators, Top Issue closers and the Emoji Reactions Summary.
- `Analysis/analysisTwo`: The graphical representation of the No of issues vs kind of label with their average resolution time.
- `Analysis/analysisThree`: This accepts a user-input label and returns graphical represenation  of the metrics like Average close time of the label, No of issues, Top contributor, Resolved issues by Top contributor, Time to close, and Total issues.
- `Figures/Analysis 1 Figure.png`: Resultant figure for the Analysis One.
- `Figures/Analysis 2 Figure.png`: Resultant figure for the Analysis Two.
- `Figures/Analysis 3 Figure.png`: Resultant figure for the Analysis Three.
- `ENPM611 Project Charter - Team 5.pdf`: A project file of our project.

### Not Used Files:
- `data_loader.py`: Utility to load the issues from the provided data file and returns the issues in a runtime data structure (e.g., objects)
- `model.py`: Implements the data model into which the data file is loaded. The data can then be accessed by accessing the fields of objects.


### File Types Used:
.py — Python scripts for feature logic and CLI execution
.json.gz — Gzipped JSON file containing GitHub issues
.png — Visualization outputs (e.g., charts)
.md — Markdown file for documentation (this README)

## Setup

To get started, Clone this repository to on your local computer. 

### Install dependencies

In the root directory of the application, create a virtual environment, activate that environment, and install the dependencies like so:

```
pip install -r requirements.txt
```

### How to Run fetch_issues.py in VS Code
 1. Open VS Code
    a. Launch Visual Studio Code.
    b. Open your ENPM611 project folder where fetch_issues.py is located.

 2. Set Your GitHub Token
    a. In config.json, make sure the "GITHUB_TOKEN" key is filled with a valid GitHub Personal Access Token to avoid rate limits:

3. Open fetch_issues.py
  a. In the Explorer sidebar, click fetch_issues.py to open the script.

4. Run the File
```
python fetch_issues.py
```

### Run an analysis

With everything set up, you should be able to run the analysis:

```
python run.py --feature 0
```

If you want to run feature 1 : Which shows the graphical representation of the Top Issue creators, Top Issue closers and the Emoji Reactions Summary :

```
python run.py --feature 1
```

If you want to run feature 2 : Which shows the graphical representation of the No of issues vs kind of label with their average resolution time :

```
python run.py --feature 2
```
If you want to run feature 3 : This accepts a user-input label and returns graphical represenation  of the metrics like Average close time of the label, No of issues, Top contributor, Resolved issues by Top contributor, Time to close, and Total issues: 

```
python run.py --feature 3 --label kind/feature
```

That will output basic information about the issues to the command line.


## VSCode run configuration

To make the application easier to debug, runtime configurations are provided to run each of the analyses you are implementing. When you click on the run button in the left-hand side toolbar, you can select to run one of the three analyses or run the file you are currently viewing. That makes debugging a little easier. This run configuration is specified in the `.vscode/launch.json` if you want to modify it.

The `.vscode/settings.json` also customizes the VSCode user interface sligthly to make navigation and debugging easier. But that is a matter of preference and can be turned off by removing the appropriate settings.

## Team Members
1. Bhavna Kumari, bhavna@umd.edu
2. Bolla Sai Saketh, sakethb@umd.edu
3. Souhardya Pal, spal05@umd.edu
4. Palak Gupta, pgupta13@umd.edu

