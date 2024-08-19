# NormalMapGen

This tool generates normal maps from input images, blending micro and macro details to create high-quality normal maps for texturing purposes.

## Features

- Generates micro and macro normal maps from input images
- Blends micro and macro normal maps with adjustable blending factor
- Converts output to specified format
- Supports PNG, JPG, and TGA input formats

![image](https://github.com/user-attachments/assets/33f66674-ebb0-47cb-af8f-968661bc7b3a)
![image](https://github.com/user-attachments/assets/ff8f045a-23f5-4728-b8f4-e5ab2b5dde90)

Fire mage robe texture by [Vurt](https://next.nexusmods.com/profile/vurt/about-me)

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- [imaginairy_normal_map](https://github.com/brycedrennan/imaginairy-normal-map)

## Installation

There are two ways to install this tool:

### Using virtual environments (Recommended)

To use this tool in a virtual environment, you can follow the steps below:

0. Install virtual environements with `pip install virtualenv`

1. Clone this repository:
  
  ```
  git clone https://github.com/Zira3l137/NormalMapGen
  ```


2. Navigate inro the cloned repository directory and create a virtual environment with the following commands:

  ```
  cd normalmapgen
  python -m venv .
  ```

3. Activate the virtual environment:

  ```
  scripts\activate
  ```

4. Install the required packages (you can use `requirements.txt`):
  
  ```
  pip install -r requirements.txt
  ```

### Manually

1. Download scripts from this repository as a zip file.

2. Extract the zip file anywhere you want.

3. Install the required packages (you can use `requirements.txt`):

  ```
  pip install -r requirements.txt
  ```

## Usage

1. Run the script from the command line with the following syntax:

  ```
  python normalMapGen.py <input_directory> [options]
  ```

First execution of this script will take some time as it will download and setup necessary dependencies. Further executions will be faster.

Each script in this repository can be used separetely as a command line tool for better flexibility and control. Use `-h` to see the available options.

### Options

- `-o`, `--output`: Specify the output directory (default: same as input directory)
- `-b`, `--blend`: Set the blending factor between micro and macro normal maps (default: 0.5)
- `-f`, `--format`: Set the output format for the final normal map (default: dds)
- `-h`, `--help`: Show this help message

### Example

```
python normalMapGen.py ./input_images -o ./output_normals -s 1.2 -b 0.6 -f tga
```

This command will process all compatible images in the `./input_images` directory, generate 2 normal maps for each image with a strength of 1.2, blend them with a factor of 0.6, and save the results in the `./output_normals` directory in `.tga` format.

## How it works

1. The script scans the input directory for compatible image files (PNG, JPG, TGA).
2. For each image:
   - Generates a micro details normal map
   - Generates a macro details normal map
   - Blends the micro and macro normal maps
   - Saves the blended normal map as a image in a specified format

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 (see [link to GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)).

## Disclaimer

The source code is provided as-is, without warranty of any kind. It is not intended for use in production environments and is provided for free use for everyone.

## Acknowledgements

This project uses the following open source projects:
- [imaginairy_normal_map](https://github.com/brycedrennan/imaginairy-normal-map)

This project uses the following external scripts (included in this repository):
- `blendNorms.py`
- `getMacroNorm.py`
- `getMicroNorm.py`
- `print_colored.py`

## Credits

- [brycedrennan](https://github.com/brycedrennan)
