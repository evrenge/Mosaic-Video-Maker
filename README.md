# Mosaic Video Maker

A program that builds videos from desired pictures! Written in Python 3.9.2.

## Getting Started

Install the dependencies (Pillow, NumPy, OpenCV, SciPy) by running the following command:

```
pip3 install -r requirements.txt
```

If you want to create the videos with your own pictures, place your images in the `tiles` folder and then run `listBuilder.py` with the following command:

```
python3 listBuilder.py
```

This generates a JSON file with the information about the tiles into `out/data.json`.

Then you can run the GUI by running the `App.py` script:

```
python3 App.py
```

Enjoy the program!