# Soil Health & Crop Recommendation Prototype

This project is a prototype for soil image analysis, soil property estimation, and crop recommendation using a Gradio web interface.

## Features

- Upload a soil image for type prediction
- Estimate soil metrics: moisture, texture, organic content, pH
- Enter environmental values: humidity, temperature, land size
- Generate crop recommendations with reasoning
- View documentation and about pages within the interface

## Installation

1. Create a Python environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the app

```bash
python app.py
```

Open the local Gradio URL shown in the terminal to use the prototype.

## Notes

- This prototype uses heuristic soil classification and rule-based recommendations.
- It is designed as a working end-to-end demo for the project requirements.
