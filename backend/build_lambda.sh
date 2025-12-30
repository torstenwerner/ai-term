#!/bin/bash

set -e

# Configuration
PACKAGE_DIR="lambda_package"
ZIP_FILE="lambda_function.zip"

# Clean up previous builds
echo "Cleaning up previous builds..."
rm -rf "$PACKAGE_DIR" "$ZIP_FILE"

# Create package directory
echo "Creating package directory..."
mkdir -p "$PACKAGE_DIR"

# Install dependencies into package directory
echo "Installing dependencies..."
uv pip install --quiet --target "$PACKAGE_DIR" \
    --python-platform aarch64-manylinux2014 \
    --python-version 3.13 \
    --quiet \
    "dotenv>=0.9.9" \
    "google-genai>=1.56.0"

# Copy Python files
echo "Copying Python files..."
cp *.py "$PACKAGE_DIR/"

# Create zip file
echo "Creating zip file..."
cd "$PACKAGE_DIR"
zip -r -q "../$ZIP_FILE" .
cd ..

# Clean up package directory
echo "Cleaning up..."
#rm -rf "$PACKAGE_DIR"

echo "Lambda package created successfully: $ZIP_FILE"
