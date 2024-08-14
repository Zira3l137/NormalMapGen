# NormalMapGenerator

This tool generates normal maps from input images, blending micro and macro details to create high-quality normal maps for texturing purposes.

## Features

- Generates micro and macro normal maps from input images
- Blends micro and macro normal maps with adjustable strength and blending factor
- Converts output to DDS format
- Supports PNG, JPG, and TGA input formats

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- ImageIO
- NumPy
- Pillow
- [imaginairy_normal_map](https://github.com/brycedrennan/imaginairy-normal-map)


## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Zira3l137/NormalMapGenerator
   cd normal-map-generator
   ```

2. Install the required packages (you can use `requirements.txt`):
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line with the following syntax:

```
python normal_map_generator.py <input_directory> [options]
```

### Options

- `-o`, `--output`: Specify the output directory (default: same as input directory)
- `-s`, `--strength`: Set the normal map strength (default: 1.0)
- `-b`, `--blend`: Set the blending factor between micro and macro normal maps (default: 0.5)

### Example

```
python normal_map_generator.py ./input_images -o ./output_normals -s 1.2 -b 0.6
```

This command will process all compatible images in the `./input_images` directory, generate 2 normal maps for each image with a strength of 1.2, blend them with a factor of 0.6, and save the results in the `./output_normals` directory.

## How it works

1. The script scans the input directory for compatible image files (PNG, JPG, TGA).
2. For each image:
   - Generates a micro details normal map
   - Generates a macro details normal map
   - Blends the micro and macro normal maps
   - Saves the blended normal map as a PNG
3. Converts all generated normal maps to DDS format
4. Removes the intermediate PNG files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 (see [link to GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)).

## Disclaimer

The source code is provided as-is, without warranty of any kind.

## Acknowledgements

This project uses the following open source projects:
- [imaginairy_normal_map](https://github.com/brycedrennan/imaginairy-normal-map)

This project uses the following external scripts (included in this repository):
- `blendNorms.py`
- `getMacroNorm.py`
- `getMicroNorm.py`
- `print_colored.py`

Credit: [brycedrennan](https://github.com/brycedrennan)
