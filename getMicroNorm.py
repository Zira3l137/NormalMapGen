from argparse import ArgumentParser, Namespace

from cv2 import (COLOR_BGR2GRAY, COLOR_BGR2RGB, CV_32F, NORM_MINMAX, Sobel,
                 cvtColor, imread, imwrite, normalize)
from cv2.typing import MatLike
from numpy import float32, uint8, zeros

from print_colored import print_colored


def create_micro_normal_map(image: MatLike, strength=1.0) -> MatLike:
    grayscale_image: MatLike = cvtColor(image, COLOR_BGR2GRAY)

    x_normal_direction = Sobel(grayscale_image, CV_32F, 1, 0, ksize=3)
    y_normal_direction = Sobel(grayscale_image, CV_32F, 0, 1, ksize=3)

    x_normal_direction = normalize(x_normal_direction, None, 0, 1, NORM_MINMAX)
    y_normal_direction = normalize(y_normal_direction, None, 0, 1, NORM_MINMAX)

    normal_map = zeros((image.shape[0], image.shape[1], 3), dtype=float32)

    normal_map[..., 0] = x_normal_direction * 2 - 1
    normal_map[..., 1] = y_normal_direction * 2 - 1
    normal_map[..., 2] = strength

    normal_map = normalize(normal_map, None, 0, 1, NORM_MINMAX)
    normal_map_8bit = (normal_map * 255).astype(uint8)
    normal_map_rgb = cvtColor(normal_map_8bit, COLOR_BGR2RGB)

    return normal_map_rgb


def save_normal_map_image(
    input_image: str, output_image: str, normal_map_strength: float
) -> bool:
    image = imread(input_image)
    normal_map = create_micro_normal_map(image, strength=normal_map_strength)
    return imwrite(output_image, normal_map)


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("input_image", type=str)
    parser.add_argument("-s", "--strength", type=float, default=1.0)
    parser.add_argument("-o", "--output", type=str, default="")
    return parser.parse_args()


def main():
    args = parse_args()
    normal_map_strength = args.strength
    input_image = args.input_image
    output_image = args.output
    if output_image == "":
        output_image = input_image.replace(
            "." + input_image.split(".")[-1], "_micro_n.png"
        )

    try:
        result = save_normal_map_image(input_image, output_image, normal_map_strength)
        if not result:
            print_colored("red", "Failed to save micro normal map image")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
