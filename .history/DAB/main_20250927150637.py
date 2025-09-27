#!/usr/bin/env python3
import shutil
import subprocess
from pathlib import Path
import argparse
import sys
import re
import json

# ── paths ─────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent  # This sets ROOT to ...\Data-Archive-Book\DAB
SCRIPTS = ROOT / "DAB"/"scripts"
CONTENT_DIR = ROOT / "DAB"/"content"
IMAGES_DIR = CONTENT_DIR / "images"
BOOK_DIR = ROOT / "DAB"/"book"
BOOK_JSON = ROOT / "DAB" / "book.json"



# Standardised source content (absolute or relative to home)
STANDARDISED_CONTENT = Path.home() / "Desktop" / "Data-Archive" / "content" / "standardised" #TODO Fix due to categorisation
STANDARDISED_IMAGES  = Path.home() / "Desktop" / "Data-Archive" / "content" / "storage" / "images"
# ── functions ─────────────────────────────────────────────────────────────

def clean_and_prepare_directories():
    if CONTENT_DIR.exists():
        shutil.rmtree(CONTENT_DIR)
    CONTENT_DIR.mkdir(parents=True)
    IMAGES_DIR.mkdir(parents=True)
    print("✅ Cleaned and recreated content directories")

def copy_standardised_content():
    selector_file = ROOT / "DAB"/"selected_files_list.md"
    source_folder = STANDARDISED_CONTENT
    destination_folder = CONTENT_DIR

    print(f"🔍 ROOT resolved to: {ROOT}")
    print(f"📄 Looking for selector file at: {selector_file}")

    # Ensure destination folders exist
    destination_folder.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Check if the selector file exists
    if not selector_file.exists():
        raise FileNotFoundError(f"Selector file not found: {selector_file}")

    # Extract filenames from [[...]] notation
    with open(selector_file, "r", encoding="utf-8") as f:
        selected_files = []
        for line in f:
            match = re.search(r"\[\[(.*?)\]\]", line)
            if match:
                selected_files.append(match.group(1) + ".md")

    # Copy selected markdown files
    copied_count = 0
    for file_name in selected_files:
        source_path = source_folder / file_name
        destination_path = destination_folder / file_name

        if source_path.exists():
            shutil.copy(source_path, destination_path)
            print(f"📄 Copied: {file_name}")
            copied_count += 1
        else:
            print(f"⚠️  Warning: {file_name} not found in {source_folder}")

    print(f"{copied_count} markdown files copied to {destination_folder}")

    # Copy all images
    image_files = list(STANDARDISED_IMAGES.glob("*"))
    for image in image_files:
        shutil.copy(image, IMAGES_DIR)
    print(f"🖼️  Copied {len(image_files)} images to {IMAGES_DIR}")

def run_script(script_name):
    script_path = SCRIPTS / script_name
    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {script_name} completed successfully.")
        print(result.stdout)  # Prints the output of the script
    else:
        print(f"❌ Error running {script_name}:\n{result.stderr}")  # Prints any errors if the script fails


def update_book_json(new_title):
    if not BOOK_JSON.exists():
        print(f"❌ book.json not found at {BOOK_JSON}")
        return

    with open(BOOK_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    old_title = data.get("title", "(no title)")
    data["title"] = new_title

    with open(BOOK_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Updated book title from '{old_title}' to '{new_title}' in book.json")


def main(args):
    if args.clean:
        clean_and_prepare_directories()

    if args.copy:
        copy_standardised_content()

    if args.run:
        script_name = args.run  # script passed as argument (e.g., 'update.py')
        script_path = SCRIPTS / script_name
        if not script_path.exists():
            print(f"Script not found: {script_path}")
            return
        run_script(script_name)  # Use the new function here
    
    if args.update_title:
        update_book_json(args.update_title)

    # if args.fallback:
    #     fallback = input("Did an error occur in compiler.py? Run file_remover.py? (y/N): ")
    #     if fallback.strip().lower() == "y":
    #         run_script("file_remover.py")

# ── CLI entry ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build pipeline controller")
    parser.add_argument("--clean", action="store_true", help="Clean and recreate content directories")
    parser.add_argument("--copy", action="store_true", help="Copy standardised content and images")
    parser.add_argument('--run', type=str, help="Run a script by name (e.g. update.py, compiler.py)")
    parser.add_argument("--update-title", type=str, help="Update the title field in book.json")

    # PDF and EPUB generation
    parser.add_argument("--pdf", type=str, help="Generate PDF with the specified output filename")
    parser.add_argument("--epub", type=str, help="Generate EPUB with the specified output filename")


    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        main(args)

# Usage:
# python main.py --clean
# python main.py --copy
# python main.py --run update.py
# python main.py --run compiler.py
# python main.py --run latex.py
# python main.py --update-title "New Book Title"

