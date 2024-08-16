from cv2 import COLOR_BGR2RGB, cvtColor, imwrite
from cv2.typing import MatLike
from imaginairy_normal_map.model import create_normal_map_pil_img
from numpy import array
from PIL import Image

from print_colored import print_colored


def create_macro_normal_map(input_image: str) -> MatLike:
    image = Image.open(input_image).convert("RGB")
    image = create_normal_map_pil_img(image)
    image = cvtColor(array(image), COLOR_BGR2RGB)
    return image


def save_macro_normal_map(input_image: str, output_image: str) -> bool:
    if macro_normal_map is None:
        return False
    macro_normal_map = create_macro_normal_map(input_image)
    return imwrite(output_image, macro_normal_map)


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_image", type=str, help="Input image")
    parser.add_argument(
        "-o", "--output_image", type=str, default="", help="Output image"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_image = args.input_image
    output_image = args.output_image
    if output_image == "":
        output_image = input_image.replace(
            "." + input_image.split(".")[-1], "_macro_n.png"
        )

    try:
        result = save_macro_normal_map(input_image, output_image)
        if not result:
            print_colored("red", "Failed to save macro normal map image")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
