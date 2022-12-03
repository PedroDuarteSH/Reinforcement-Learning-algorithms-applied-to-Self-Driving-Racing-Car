# Reinforcement Learning algorithms applied to Self Driving Racing Car

## About the project

Artificial Intelligence(AI) is currently one of the most researched themes on the context of Computer Science, even though it has a lot of past research~\cite{haenlein2019brief}, and in that field, Reinforcement Learning is one of the most studied areas being used in a lot of applications like Industry automation, healthcare and Autonomous Driving, on the other hand motorsport is one of the fastest growing competitive sporting events worldwide, for example in Formula 1 (F1), the most watched race of the 2020 season, the Hungarian Grand Prix in Budapest had an incredible 110 million spectators.

In this context, this project aims to study how different RI algorithms can interfere in the performance of an automated vehicle, in the racing context, measuring the order of magnitude of the changes. Using the simulator "The Open Racing Car Simulator" (TORCS), comparing deeply discretized and continuous types of algorithms, by measuring track and agent performance variables, like best lap times, median speed around track and number of steps to reach a state that can complete a certain number of laps without getting out of track.

### Used Platforms

[![Python][Python.logo]][Python-url]
[![Numpy][Numpy.logo]][Windows-url]
[![Windows][Windows.logo]][Windows-url]
[![LaTeX][LaTeX.com]][LaTeX-url]

## How to execute

### Prerequisites

- Python installed
- Torcs should be installed, with <a href="https://arxiv.org/pdf/1304.1672.pdf">SRC Plugin</a> in the project folder
- Open AI Gym frameword `pip install gym`
- Stable-baselines3 `pip install stable-baselines3`
- Dependecies present at file `Torcs.yml`, that represents a conda environment, can be installed with `conda env create -f Torcs.yml`

## Execution

To execute, the user should activate the Torcs conda enviroment and execute through console with `python main.py`, with console opened in project folder.

Also, the user can see the diferent tags for code execution using `python main.py -h`

The different network parameters can be changed with help of stable baselines framework in this file, as well as training timesteps and different algorithms

## Contacts

David Ressurreição

ressurreicao@student.dei.uc.pt

[![GitHub][GitHub.com]][GitHub-David][![Gmail][Gmail.com]][Gmail-David]

Fábio Vaqueiro

fabiovaqueiro@student.dei.uc.pt

[![GitHub][GitHub.com]][GitHub-Fabio][![Gmail][Gmail.com]][Gmail-Fabio]

Pedro Henriques

pedrohenriques@student.dei.uc.pt

[![GitHub][GitHub.com]][GitHub-Duarte][![Gmail][Gmail.com]][Gmail-Duarte]

[Python.logo]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/

[LaTeX.com]: https://img.shields.io/badge/latex-%23008080.svg?style=for-the-badge&logo=latex&logoColor=white
[LaTeX-url]: https://www.latex-project.org/

[Windows.logo]: https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white~
[Windows-url]: https://www.microsoft.com/en-us/windows?wa=wsignin1.0

[NumPy.logo]: https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white

[GitHub.com]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white
[GitHub-Duarte]: https://github.com/PedroDuarteSH
[GitHub-David]: https://github.com/David-Forte
[GitHub-Fabio]: https://github.com/FabioVaqueiro

[Gmail.com]:https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white
[Gmail-David]: mailto:ressurreicao@student.dei.uc.pt
[Gmail-Fabio]: mailto:fabiovaqueiro@student.dei.uc.pt
[Gmail-Duarte]: mailto:pedrohenriques@student.dei.uc.pt
