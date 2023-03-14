import argparse
import math
from turtle import Screen, Turtle
from typing import Optional

from svgpathtools import svg2paths

turtle = Turtle()
screen = Screen()


def parse_styles(attrs: list[dict]) -> list[dict]:
    for dictionary in attrs:
        try:
            pairs = dictionary['style'].replace(' ', '')
        except KeyError:
            continue
        pairs = pairs.rstrip(';').split(';')
        for pair in pairs:
            key, value = pair.split(':')
            if value == 'none':
                value = None
            dictionary[key] = value
    return attrs


def parse_paths(paths: list, quality: int = 8, offset: tuple[float, float] = (0, 0)) -> list[list]:
    new_paths = []
    for path in paths:
        new_path = []
        for subpaths in path.continuous_subpaths():
            points = []
            for segment in subpaths:
                interp_num = math.ceil(segment.length() / quality)
                positions = [x / interp_num for x in range(interp_num)]
                points.extend([segment.point(position) for position in positions])
            new_path.append([(point.real + offset[0], -point.imag - offset[1]) for point in points])
        new_paths.append(new_path)
    return new_paths


def move_to(coords: tuple[float, float], draw: bool = True):
    wasdown = turtle.isdown()
    turtle.pen(pendown=draw)
    turtle.goto(coords[0], coords[1])
    turtle.pen(pendown=wasdown)


def draw_path(path, color: Optional[str] = None, fill: Optional[str] = None):
    if color:
        turtle.color(color)
    for segment in path:
        move_to(segment[0], False)
        if fill:
            turtle.color(fill)
            turtle.begin_fill()
        for point in segment[1:]:
            move_to(point, True)
        if fill:
            turtle.end_fill()


def main(file_path: str, loop: bool = False, quality: int = 1, n: int = 0):  # pylint: disable=invalid-name
    paths, attrs, svg_attrs = svg2paths(file_path, return_svg_attributes=True)  # type: ignore
    attrs = parse_styles(attrs)
    width, height = int(float(svg_attrs['width'])), int(float(svg_attrs['height']))
    offset = (-width / 2, -height / 2)
    paths = parse_paths(paths, quality, offset)
    screen.tracer(n=n, delay=0)
    screen.screensize(width, height)
    while True:
        turtle.reset()
        turtle.hideturtle()
        for path, attr in zip(paths, attrs):
            draw_path(path, attr.get('stroke'), attr.get('fill'))
        if not loop:
            break
    screen.update()
    screen.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-l', '--loop', action='store_true')
    parser.add_argument('-q', '--quality', type=int, default=1)
    parser.add_argument('-n', type=int, default=0)
    args = parser.parse_args()
    main(args.path, args.loop, args.quality, args.n)
