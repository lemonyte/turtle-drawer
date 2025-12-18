# Turtle Drawer

Draw raster images using Python's Turtle library.

This script is a demo of my [pyautotrace](https://github.com/lemonyte/pyautotrace) library.

![turtle-drawer-demo](https://github.com/user-attachments/assets/7ece9e28-1985-402b-8f25-97e703b716f6)

## Usage

First, choose a regular JPEG or PNG image to draw. Simple 2D images like clipart vectorize best.

If you don't have [uv](https://docs.astral.sh/uv/) yet, install it.

No need to download or install anything else! You can run the script directly with uv:

```bash
uv run https://raw.githubusercontent.com/lemonyte/turtle-drawer/refs/heads/main/turtle_drawer.py image.png
```

## Reference

Command syntax:

```bash
uv run turtle_drawer.py [-h] [-l] [-q QUALITY] [--speed SPEED] [--size SIZE] path
```

### Options

Option|Type|Default|Description
--|--|--|--
`-h`, `--help`|Flag|None|Show a help message.
`-l`, `--loop`|Flag|`False`|Continuously draw and erase the image on repeat.
`-q`, `--quality`|Integer|`10`|Set the quality of the drawing, higher value equals higher quality.
`--speed`|Integer|`1000`|Number of actions before a screen update is called, higher value equals faster drawing. Set to `0` for instant drawing. See the [Turtle docs](https://docs.python.org/3/library/turtle.html#turtle.tracer).
`--size`|Integer|`0`|Set the max size of the image to draw, in pixels. Set to `0` to use the original image size.

Example:

```bash
uv run turtle_drawer.py --loop --quality 50 --speed 100 --size 900 serpent.png
```

When run, the program will take some time to vectorize the raster image. The time it takes to vectorize and draw the image depends on the complexity of the image and the performance of your system. Experiment with the `--speed` option to find a value that works well. For complex images a value of `1000` or greater is recommended.

## License

[MIT License](license.txt)
