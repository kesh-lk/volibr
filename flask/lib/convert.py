import os
import subprocess


def convert_pdf_to_html(pdf_path, page_from, page_to, output_dir="/tmp"):
    os.makedirs(output_dir, exist_ok=True)

    output_filename = "pdf.html"

    command = [
        "pdf2htmlEX",
        f"--first-page={page_from}",
        f"--last-page={page_to}",
        "--split-pages", "0",  # single HTML file
        "--process-outline", "0",
        "--dest-dir", output_dir,
        pdf_path,
        output_filename
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Converted pages {page_from}–{page_to} to HTML")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e}")
