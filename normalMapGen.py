from argparse import ArgumentParser
from os import scandir
from pathlib import Path
from time import time
from traceback import format_exc

from cv2 import COLOR_BGR2RGB, cvtColor
from PIL import Image

from blendNorms import blend_normals
from getMacroNorm import create_macro_normal_map
from getMicroNorm import create_micro_normal_map
from print_colored import (enable_ansi_escape_sequences, print_colored,
                           print_mixed)

enable_ansi_escape_sequences()


def generate_normal(
    input_image: str, output_path: str, output_format: str, blending_factor: float
) -> bool:
    print_mixed("blue", text="Processing image: ", colored_text=(input_image))
    input_image_path = Path(input_image).absolute()

    try:
        print_colored("blue", "Generating normal map (1/2)...")
        micro_normal_map = create_micro_normal_map(str(input_image_path))

        print_colored("blue", "Generating normal map (2/2)...")
        macro_normal_map = create_macro_normal_map(str(input_image_path))

        print_colored("blue", "Blending details...")
        normal_map = blend_normals(micro_normal_map, macro_normal_map, blending_factor)

        print_mixed("green", text="Saving as: ", colored_text=output_path)
        output_rgb = cvtColor(normal_map, COLOR_BGR2RGB)
        Image.fromarray(output_rgb).save(output_path, format=output_format)
    except Exception as e:
        traceback_str = format_exc()
        print_mixed("red", text=traceback_str + "\n", colored_text=str(e))
        return False

    return True


def process_directory(
    input_directory: str,
    output_directory: str,
    output_format: str,
    blending_factor: float,
) -> bool:
    for image in scandir(input_directory):
        if image.is_dir():
            continue
        if True not in [
            Path(image.name).suffix.lower() == ext for ext in [".png", ".jpg", ".tga"]
        ]:
            continue
        output_path = Path(
            output_directory, Path(image.name).with_suffix("." + output_format)
        )
        if not generate_normal(
            image.path, str(output_path), output_format, blending_factor
        ):
            return False
    return True


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "input_directory", type=str, help="Input directory with the images"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Specify the output directory (default: same as input directory)",
    )
    parser.add_argument(
        "-b",
        "--blend",
        type=float,
        default=0.5,
        help="Set the blending factor between micro and macro normal maps (default: 0.5)",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="dds",
        help="Set the output format for the final normal map (default: dds)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_dir = args.input_directory
    output_dir = args.output
    blending_factor = args.blend
    output_format = args.format

    if output_dir is None:
        output_dir = input_dir
    if not Path(output_dir).exists():
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    start_time = time()
    if not process_directory(input_dir, output_dir, output_format, blending_factor):
        print_colored("red", "Generation process interrupted due to an error")
    else:
        print_colored(
            "green",
            f"Generation process finished in {time() - start_time:.2f} seconds",
        )


if __name__ == "__main__":
    main()
