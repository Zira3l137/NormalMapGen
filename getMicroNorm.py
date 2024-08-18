from argparse import ArgumentParser, Namespace
from os import scandir
from pathlib import Path

from cv2 import (COLOR_BGR2GRAY, COLOR_BGR2RGB, COLOR_RGB2BGR, CV_32F,
                 NORM_MINMAX, Sobel, cvtColor, imwrite, normalize)
from cv2.typing import MatLike
from numpy import array, float32, uint8, zeros
from PIL import Image

from print_colored import print_colored


def create_micro_normal_map(input_image: str, strength=1.0) -> MatLike:
    input_image_obj = Image.open(input_image).convert("RGB")
    cv2_image: MatLike = cvtColor(array(input_image_obj), COLOR_RGB2BGR)

    grayscale_image = cvtColor(cv2_image, COLOR_BGR2GRAY)

    x_normal_direction = Sobel(grayscale_image, CV_32F, 1, 0, ksize=3)
    y_normal_direction = Sobel(grayscale_image, CV_32F, 0, 1, ksize=3)

    x_normal_direction = normalize(x_normal_direction, None, 0, 1, NORM_MINMAX)
    y_normal_direction = normalize(y_normal_direction, None, 0, 1, NORM_MINMAX)

    normal_map = zeros((cv2_image.shape[0], cv2_image.shape[1], 3), dtype=float32)

    normal_map[..., 0] = x_normal_direction * 2 - 1
    normal_map[..., 1] = y_normal_direction * 2 - 1
    normal_map[..., 2] = strength

    normal_map = normalize(normal_map, None, 0, 1, NORM_MINMAX)
    normal_map_8bit = (normal_map * 255).astype(uint8)
    normal_map_rgb = cvtColor(normal_map_8bit, COLOR_BGR2RGB)

    return normal_map_rgb


def save_micro_normal_map_image(
    image_obj: MatLike, output_path: str
) -> bool | tuple[bool, str]:
    try:
        imwrite(output_path, image_obj)
    except Exception as e:
        return False, str(e)
    return True


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("input_image", type=str, help="Input image")
    parser.add_argument(
        "-o", "--output_image", type=str, default="", help="Output image"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_image = args.input_image
    output_image = args.output_image

    input_image_path = Path(input_image)
    if input_image_path.is_file():
        if input_image_path.suffix in [".png", ".jpg", ".jpeg", ".tga"]:
            if output_image == "":
                output_image = input_image_path.with_suffix(".png")
            normal = create_micro_normal_map(input_image)
            success = save_micro_normal_map_image(normal, str(output_image))
            if isinstance(success, tuple):
                print_colored("red", f"Failed to create macro normal map: {success[1]}")
    else:
        for file in scandir(input_image):
            if Path(file.path).suffix in [".png", ".jpg", ".jpeg", ".tga"]:
                if output_image == "":
                    output_image = Path(file.path).with_suffix(".png")
                normal = create_micro_normal_map(file.path)
                success = save_micro_normal_map_image(normal, str(output_image))
                if isinstance(success, tuple):
                    print_colored(
                        "red", f"Failed to create macro normal map: {success[1]}"
                    )
                    print_colored("red", "Aborting...")
                    break


if __name__ == "__main__":
    main()
