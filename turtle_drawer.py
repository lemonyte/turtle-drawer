# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy~=2.2.6",
#     "pillow~=12.0.0",
#     "pyautotrace~=0.0.6",
# ]
# ///

import argparse
import time
from turtle import Screen, Turtle

import numpy as np
from autotrace import Bitmap, Path, Point, PolynomialDegree
from PIL import Image

Point2D = tuple[float, float]


def offset_point(point: Point, offset: Point2D, /) -> Point2D:
    return (point.x + offset[0], point.y + offset[1])


def move_to(turtle: Turtle, point: Point2D, /, *, draw: bool = True) -> None:
    wasdown = turtle.isdown()
    turtle.pen(pendown=draw)
    turtle.goto(point[0], point[1])
    turtle.pen(pendown=wasdown)


def draw_path(turtle: Turtle, path: Path, /, *, quality: int, offset: Point2D = (0, 0)) -> None:
    if path.color:
        turtle.color(
            (path.color.r, path.color.g, path.color.b),
            (path.color.r, path.color.g, path.color.b),
        )
    first_point = path.splines[0].points[0]
    move_to(turtle, offset_point(first_point, offset), draw=False)
    if not path.open:
        turtle.begin_fill()
    for spline in path.splines:
        if spline.degree == PolynomialDegree.LINEAR:
            points = [spline.points[0], spline.points[-1]]
        else:
            ts = [i / quality for i in range(quality)] + [1.0]
            points = [spline.evaluate(t) for t in ts]
        for point in points:
            move_to(turtle, offset_point(point, offset), draw=True)
    if not path.open:
        turtle.end_fill()


def main(*, file_path: str, loop: bool, quality: int, speed: int, size: int) -> None:
    image = Image.open(file_path).convert("RGB")
    if size > 0:
        image.thumbnail((size, size))
    vector = Bitmap(np.array(image)).trace(noise_removal=100, despeckle_level=500)
    offset = (-vector.width / 2, -vector.height / 2)
    turtle = Turtle()
    screen = Screen()
    screen.onkey(screen.bye, "q")
    screen.onkey(screen.bye, "Escape")
    screen.listen()
    screen.tracer(n=speed, delay=0)
    screen.screensize(vector.width, vector.height)
    screen.colormode(255)
    while True:
        turtle.reset()
        turtle.hideturtle()
        for path in vector.paths:
            draw_path(turtle, path, quality=quality, offset=offset)
        if not loop:
            break
        time.sleep(1)
    screen.update()
    screen.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("-l", "--loop", action="store_true")
    parser.add_argument("-q", "--quality", type=int, default=10)
    parser.add_argument("--speed", type=int, default=1000)
    parser.add_argument("--size", type=int, default=0)
    args = parser.parse_args()
    main(
        file_path=args.path,
        loop=args.loop,
        quality=args.quality,
        speed=args.speed,
        size=args.size,
    )
