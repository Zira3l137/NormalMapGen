from argparse import ArgumentParser, Namespace
from os import scandir
from pathlib import Path

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


def save_macro_normal_map_image(
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
            normal = create_macro_normal_map(input_image)
            success = save_macro_normal_map_image(normal, str(output_image))
            if isinstance(success, tuple):
                print_colored("red", f"Failed to create macro normal map: {success[1]}")
    else:
        for file in scandir(input_image):
            if Path(file.path).suffix in [".png", ".jpg", ".jpeg", ".tga"]:
                if output_image == "":
                    output_image = Path(file.path).with_suffix(".png")
                normal = create_macro_normal_map(file.path)
                success = save_macro_normal_map_image(normal, str(output_image))
                if isinstance(success, tuple):
                    print_colored(
                        "red", f"Failed to create macro normal map: {success[1]}"
                    )
                    print_colored("red", "Aborting...")
                    break


if __name__ == "__main__":
    main()
