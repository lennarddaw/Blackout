# Blackout

A wearable real-time person tracking system using ESP32-CAM and face embeddings to analyze social interactions based on proximity and duration.

## Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Configuration](#configuration)  
5. [Usage](#usage)  
6. [Directory Structure](#directory-structure)  
7. [Model Download](#model-download)  
8. [License](#license)  

## Features

- Detects and tracks faces in first-person video streams from an ESP32-CAM  
- Assigns names on first encounter, stores face embeddings locally  
- Logs contact start/end timestamps and duration per person  
- Simple Flask API backend on Raspberry Pi  
- Minimal dependencies, ONNX Runtime for embedding extraction  

## Prerequisites

- **Hardware**  
  - ESP32-CAM module  
  - Raspberry Pi (any model with network connectivity)  
- **Software**  
  - Python 3.7+  
  - Arduino IDE (for ESP32-CAM)  
  - Git  

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/lennarddaw/Blackout.git
   cd Blackout
