# ArtiViz
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![build](https://img.shields.io/circleci/project/github/badges/shields/master)

A tool to automatically generate dynamic graphics as webm files using themes provided as natural language queries. Built using p5.js, powered by ChatGPT. 

## Setup

1) Clone this repository.  
   `git clone https://github.com/dv-fenix/ArtiViz.git`  
   `cd ArtiViz`
   
2) Install the requirements given in `requirements.txt`.  
   `python -m pip install -r requirements.txt`

3) Alias the python command for ease of use
    `alias artiviz='/usr/bin/python <path to animation_app.py>'`

## Usage

1) Generate and add your OpenAI API key in the `.env` file.

2) Add the input files to the root directory.

3) Call the ffmpeg_app. An example is provided below:
    ```
    artiviz --theme "Nachos"
    ```

## Example Output
The animator was asked to generate something around the theme "Nachos".

![Checkout the webm file provided in the samples folder](samples/output.webm)