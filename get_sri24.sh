#!/bin/bash

# Set variables
URL="https://www.nitrc.org/frs/download.php/4841/sri24_spm8.zip?i_agree=1&download_now=1"
OUTPUT_DIR="$(dirname "$0")/data"
OUTPUT_FILE="${OUTPUT_DIR}/sri24.zip"
UNZIP_DIR="${OUTPUT_DIR}/sri24"

# Create necessary directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$UNZIP_DIR"

# Download the file
echo "Downloading ${URL}..."
curl -L -o "$OUTPUT_FILE" "$URL"
if [ $? -ne 0 ]; then
    echo "Error: Download failed!"
    exit 1
fi
echo "File downloaded to ${OUTPUT_FILE}"

# Unzip the file
echo "Unpacking ${OUTPUT_FILE} to ${UNZIP_DIR}..."
unzip -o "$OUTPUT_FILE" -d "$UNZIP_DIR"
if [ $? -ne 0 ]; then
    echo "Error: Unzipping failed!"
    exit 1
fi
echo "File unpacked successfully to ${UNZIP_DIR}"

# Remove the zip file
if [ -f "$OUTPUT_FILE" ]; then
    rm "$OUTPUT_FILE"
    echo "Removed zip file: ${OUTPUT_FILE}"
fi
