# Turtle Drawer

Draw SVG images using Python's Turtle library.

## Requirements

### Python File

- [Python 3.9](https://www.python.org/downloads/) or higher
- Packages listed in [`requirements.txt`](requirements.txt)

### Windows Systems

Optional executable file for Windows users. Python and the required packages are included in the executable.

- 36 MB of free space for the executable
- 45 MB of free space for temporary files

## Usage

Download the executable file `turtle-drawer.exe` from the [latest release](https://github.com/lemonyte/turtle-drawer/releases/latest). If you are not using Windows, download the source code and use the Python file.

### Preparing an Image

First, choose a regular image to draw. Simple 2D images like clipart vectorize best. Once you have an image, go to <https://autotracer.org> and convert it to an SVG image. Save the SVG image on your computer. You may also use an SVG image from another source, but keep in mind this program is meant to be used with SVG images in the format provided by <https://autotracer.org>, and not all SVG images are in this format. To start drawing, run the program from a terminal.

Command syntax:

```bash
./turtle-drawer.exe [-h] [-l] [-q QUALITY] [-n N] image_path
```

### Options

Option|Parameters|Default|Description
--|--|--|--
`-h`, `--help`|None|None|Show this help message
`-l`, `--loop`|None|`False`|Continuously draw and erase the image on repeat
`-q`, `--quality`|Integer|`1`|Set the quality of the drawing, lower value equals higher quality
`-n`|Integer|`1`|Number of actions before a screen update is called, higher value equals faster drawing. Set to `0` for instant drawing. See the [Turtle docs](https://docs.python.org/3/library/turtle.html#turtle.tracer)

Example:

```bash
./turtle-drawer.exe -l -q 8 -n 1000 path/to/image.svg
```

If you are using the Python file, replace `./turtle-drawer.exe` with `python turtle-drawer.py`. When run, the program will take some time to first unpack all the necessary resources if the `.exe` file is being used, and then parse the SVG image. The time it takes to parse and draw the image depends on the complexity of the image and the performance of your system. Experiment with the `-n` option to find a value that works well. For complex images a value of `100` or greater is recommended.

## License

[MIT License](license.txt)
