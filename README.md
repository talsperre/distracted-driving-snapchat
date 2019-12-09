# Driving the Last Mile: Characterizing and Understanding Distracted Driving Posts on Social Networks

#### [Hemank Lamba](https://sites.google.com/site/hemanklamba/home), [Shashank Srikanth *](https://talsperre.github.io/), [Dheeraj Reddy *](https://scholar.google.co.in/citations?user=WMjvetsAAAAJ&hl=en), [Shwetanshu Singh](https://in.linkedin.com/in/shwetanshus), [Karandeep Juneja](https://www.linkedin.com/in/karandeepsj/?originalSubdomain=in), [Ponnurangam Kumaraguru](https://www.iiitd.ac.in/pk)

Drinking & Driving | Passenger Distraction | Distracted Driving on Bikes
:----------------------:|:-------------------------:|:-------------------------:|
![video1](./sample_videos/distracted-1.gif)  |  ![video2](./sample_videos/distracted-2.gif) |  ![video2](./sample_videos/distracted-3.gif)

This repository contains code and data required to reproduce the results of **"Driving the Last Mile: Characterizing and Understanding Distracted Driving Posts on Social Networks"**. ([**Paper link**](http://precog.iiitd.edu.in/pubs/Distracted-Driving-Pre-Print-Paper-ICWSM-2020.pdf))

### Introduction

Our work deals with identifying distracted driving content on social media (Snapchat) using computer vision methods and analyzing the data for spatio-temporal patterns and charecterizing the users demographics.  

A few examples of distracted driving content on Snapchat are given in the figure above. 

### Installation

The code has been tested with `python3` and `PyTorch 0.4.1`. The codebase can also support `PyTorch 1.0` with slight modifications. 

```
virtualenv -p python3.5 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the code

The codebase is divided into the following major portions:

1. [Annotation Portal](./annotation-portal/README.md)
2. [Scraper](./scraper/README.md)
3. [Data collection Pipeline](./data-collection-pipeline/README.md)
4. [Classification](./classifier_code/README.md)
5. [Analysis](./analysis/README.md)

### Pre-trained Models and Scraper code
All the pretrained models and the Snapchat scraper code are available on request via email at `pk [at] iiitd [dot] ac [dot] in`.

### Project Page
For additional details, plots, and discussions, refer to the project page [here](http://precog.iiitd.edu.in/research/distracted_driving/).

### Citation

If you are using this code or the pre-trained models, please cite our paper as follows:

```tex
@article{lambadistracteddriving,
  author={Hemank Lamba, Shashank Srikanth, Dheeraj Reddy Pailla, Shwetanshu Singh, Karandeep Juneja, and Ponnurangam Kumaraguru},
  title={Driving the Last Mile: Characterizing and Understanding Distracted Driving Posts on Social Networks},
  booktitle={Proceedings of the International AAAI Conference on Web and Social Media (ICWSM) 2020},
  year={2020},
}
```