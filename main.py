import argparse
from pathlib import Path
from lensify import lensify_photo

def main():
    parser = argparse.ArgumentParser(description="Apply sunglasses animation to a face image.")
    parser.add_argument("input_image", type=Path, help="Path to input face image (jpg, png, etc.)")
    parser.add_argument("output_gif", type=Path, help="Path to save the output animated GIF")
    args = parser.parse_args()

    lensify_photo(args.input_image, args.output_gif)
    print(f"Saved animated GIF to {args.output_gif}")

if __name__ == "__main__":
    main()