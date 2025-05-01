# ENPM611 Project 📊 GitHub Issue Analysis - Team 5

### Introduction:
Welcome to our data-driven analysis of GitHub issues using the open-source Poetry [poetry](https://github.com/python-poetry/poetry/issues) project. This repository explores issue resolution patterns, contributor behavior, and community interactions by processing GitHub issue data.

### Project Overview:
This project was developed as part of the ENPM611 Software Engineering class. The goal is to extract meaningful insights from GitHub Issues (not commits), visualizing patterns around labels, contributors, and reactions.

### Objective:
Investigate how issues are labeled, discussed, and resolved
Identify top contributors and common bottlenecks
Visualize trends in issue handling using matplotlib

### Features Implemented:

#### Feature 1: Contributor and Reaction Analysis
1. Identifies the top issue creators and closers
2. Counts all reactions (e.g., thumbs up, heart, rocket)
3. Visualizes results using a three-panel bar chart

#### Feature 2: Label Frequency and Resolution Time
1. Analyzes most-used labels across all issues
2. Calculates average resolution time per label (in days)
3. Visualized with bar chart + annotations

#### Feature 3: Label-Based Deep Dive (User Input Required)
1. Input a label like bug, status/triage, or kind/feature
Outputs:
1. Total number of issues
2. Average comments
3. Average close time
4. Most active contributor and resolved count
5. Visualization: histogram of close times + annotations

```
enpm611-team5/
├── analysis/                        # Core analysis scripts
│   ├── contributorAndReactionAnalysis.py         # Visualizes top issue creators, closers, and reactions
│   ├── frequentLabelAndResolutionTimeAnalysis.py # Shows label frequency vs. resolution time
│   ├── labelBasedDeepDiveAnalysis.py             # Deep dive for a specific label's metrics
│
├── classDiagram/                   # Class diagram and source
│   ├── team_5_class_diagram.svg
│   ├── team_5_class_diagram
│
├── data/
│   ├── poetry_data.json            # GitHub issues dataset
│
├── entityRelationshipDiagrams/     # ER diagram files
│   ├── team_5_erd.svg
│   ├── team_5_erd.txt
│   ├── team_5_erd_explaination.txt
│
├── figures/                         # Generated analysis plots
│   ├── Analysis_One_Contributor_and_Reaction_Analysis.png
│   ├── Analysis_Two_Label_Frequency_and_Resolution_Time.png
│   ├── Analysis_Three_Label_Based_Deep_Dive.png
│
├── scripts/
│   ├── fetch_issues.py             # Pulls GitHub issues using GITHUB_TOKEN
│
├── tests/                          # Unit tests
│   ├── testAnalysis/
│   │   ├── test_contributorAndReactionAnalysis.py
│   │   ├── test_frequentLabelAndResolutionTimeAnalysis.py
│   │   ├── test_labelBasedDeepDiveAnalysis.py
│   ├── testScript/
│   │   ├── test_fetch_issues.py
│   ├── test_config.py
│   └── test_run.py
│
├── testsCoverageReports/           # Module-wise test coverage reports
│   ├── config_Test_Coverage_Report.txt
│   ├── run_Test_Coverage_Report.txt
│   ├── ContributorAndReactionAnalysis_Test_Coverage_Report.txt
│   ├── FrequentLabelAndResolutionTimeAnalysis_Test_Coverage_Report.txt
│   ├── LabelBasedDeepDiveAnalysis_Test_Coverage_Report.txt
│   ├── enpm-611-team5-projectTestCoverageReport.txt
│   ├── enpm611-Team5-testCoverageReport.pdf
│
├── run.py                          # Main CLI entry point (`--feature` required)
├── config.json                     # GitHub repo & dataset config
├── config.py                       # Loads config.json and supports env overrides
├── ENPM611 Project Charter - Team 5
└── requirements.txt                # Python dependencies

```


### File Types Used:
- .py — Python scripts for feature logic and CLI execution
-  .json.gz — Gzipped JSON file containing GitHub issues
-   .png — Visualization outputs (e.g., charts)
-  md — Markdown file for documentation (this README)

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

 3. Set Your GitHub Personal Access Token in the Run Configuration as Environment Variable as below:
 a. GITHUB_TOKEN

4. Open fetch_issues.py
a. In the Explorer sidebar, click fetch_issues.py to open the script.

5. Run the File
```
python fetch_issues.py
```

### Run an analysis

With everything set up, you should be able to run the analysis:

If you want to run feature 1 : Which shows the graphical representation of the Top Issue creators, Top Issue closers and the Emoji Reactions Summary

```
python run.py --feature 1
```

If you want to run feature 2 : Which shows the graphical representation of the No of issues vs kind of label with their average resolution time

```
python run.py --feature 2
```
If you want to run feature 3 : This accepts a user-input label and returns graphical represenation  of the metrics like Average close time of the label, No of issues, Top contributor, Resolved issues by Top contributor, Time to close, and Total issues

```
python run.py --feature 3 --label kind/feature
```

That will output basic information about the issues to the command line.


### Run Tests

```
python -m coverage run --source=. -m unittest discover -s tests
python -m coverage report --omit="*/tests/*,*/__init__.py"
```

### Generate an HTML Test Coverage report of the whole Project

```
python -m coverage run --source=. -m unittest discover -s tests
```
```
python -m coverage html
```
```
open htmlcov/index.html
```


## VSCode run configuration

To make the application easier to debug, runtime configurations are provided to run each of the analyses you are implementing. When you click on the run button in the left-hand side toolbar, you can select to run one of the three analyses or run the file you are currently viewing. That makes debugging a little easier. This run configuration is specified in the `.vscode/launch.json` if you want to modify it.

The `.vscode/settings.json` also customizes the VSCode user interface sligthly to make navigation and debugging easier. But that is a matter of preference and can be turned off by removing the appropriate settings.

## Team Members
1. Bhavna Kumari, bhavna@umd.edu
2. Bolla Sai Saketh, sakethb@umd.edu
3. Souhardya Pal, spal05@umd.edu
4. Palak Gupta, pgupta13@umd.edu

