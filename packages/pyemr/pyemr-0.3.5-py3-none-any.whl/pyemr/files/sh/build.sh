BUILD_PATH=$1
BUILD_DIR=$(dirname $BUILD_PATH)

echo "Building package inside docker..."
echo "Installing package dependencies inside docker:"
echo ""

mkdir -p $BUILD_DIR
poetry run pip install .
rm -f $BUILD_PATH

echo "Packaging virtual environments"
poetry run venv-pack -o $BUILD_PATH --python-prefix /usr/bin/

