from cv2 import COLOR_BGR2RGB, cvtColor, imread, imwrite
from cv2.typing import MatLike
from numpy import float32, uint8, zeros_like

from print_colored import print_colored


def blend_normals(
    base_img: MatLike, overlay_img: MatLike, alpha: float = 0.5
) -> MatLike:
    base_image = base_img.astype(float32) / 255.0
    overlay_image = overlay_img.astype(float32) / 255.0

    overlay_image = overlay_image * alpha + base_image * (1 - alpha)

    result = zeros_like(base_image)
    mask = base_image <= 0.5

    result[mask] = 2 * base_image[mask] * overlay_image[mask]
    result[~mask] = 1 - 2 * (1 - base_image[~mask]) * (1 - overlay_image[~mask])

    result = (result * 255).astype(uint8)

    return result


def save_blended_image(
    input_img_path: str, overlay_img_path: str, output_img_path: str, alpha: float = 0.5
) -> bool:
    base_img = imread(input_img_path)
    overlay_img = imread(overlay_img_path)

    blended_img = blend_normals(base_img, overlay_img, alpha=0.5)
    blended_img = cvtColor(blended_img, COLOR_BGR2RGB)

    return imwrite(output_img_path, blended_img)


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("base_img_path", type=str)
    parser.add_argument("overlay_img_path", type=str)
    parser.add_argument("-o", "--output_img_path", type=str, default="")
    parser.add_argument("-a", "--alpha", type=float, default=0.5)
    return parser.parse_args()


def main():
    args = parse_args()
    base_img_path = args.base_img_path
    overlay_img_path = args.overlay_img_path
    output_img_path = args.output_img_path
    alpha = args.alpha
    if output_img_path == "":
        output_img_path = base_img_path.replace(
            "." + base_img_path.split(".")[-1], "_blended.png"
        )

    try:
        result = save_blended_image(
            base_img_path, overlay_img_path, output_img_path, alpha=alpha
        )
        if not result:
            print_colored("red", "Failed to save blended image")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
