import argparse
import turtle as t
from math import ceil
from svgpathtools import svg2paths


def parse_styles(attrs: list[dict]) -> list[dict]:
    for d in attrs:
        try:
            style = d['style'].replace(' ', '')
        except KeyError:
            continue
        x = style.rstrip(';').split(';')
        for i in x:
            k, v = i.split(':')
            if v == 'none':
                v = None
            d[k] = v
    return attrs


def parse_paths(paths: list, quality: int = 8, offset: list = [0, 0]) -> list[list]:
    new_paths = []
    for path in paths:
        new_path = []
        for subpaths in path.continuous_subpaths():
            points = []
            for segment in subpaths:
                interp_num = ceil(segment.length() / quality)
                p = [x / interp_num for x in range(interp_num)]
                points.extend([segment.point(x) for x in p])
            new_path.append([(point.real + offset[0], -point.imag - offset[1]) for point in points])
        new_paths.append(new_path)
    return new_paths


def move_to(coords: tuple[float, float], draw: bool = True):
    wasdown = t.isdown()
    t.pen(pendown=draw)
    t.goto(coords[0], coords[1])
    t.pen(pendown=wasdown)


def draw_path(path, color: str = None, fill: str = None):
    if color:
        t.color(color)
    for segment in path:
        move_to(segment[0], False)
        if fill:
            t.color(fill)
            t.begin_fill()
        for point in segment[1:]:
            move_to(point, True)
        if fill:
            t.end_fill()


def main(image_path: str, loop: bool = False, quality: int = 1, n: int = 1):
    paths, attrs, svg_attrs = svg2paths(image_path, return_svg_attributes=True)
    attrs = parse_styles(attrs)
    width, height = int(float(svg_attrs['width'])), int(float(svg_attrs['height']))
    offset = [-width / 2, -height / 2]
    paths = parse_paths(paths, quality, offset)
    t.tracer(n=n, delay=0)
    t.screensize(width, height)
    while True:
        t.reset()
        t.hideturtle()
        for path, attr in zip(paths, attrs):
            draw_path(path, attr.get('stroke'), attr.get('fill'))
        if not loop:
            break
    t.update()
    t.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path')
    parser.add_argument('-l', '--loop', action='store_true')
    parser.add_argument('-q', '--quality', type=int, default=1)
    parser.add_argument('-n', type=int, default=1)
    args = parser.parse_args()
    main(args.image_path, args.loop, args.quality, args.n)
