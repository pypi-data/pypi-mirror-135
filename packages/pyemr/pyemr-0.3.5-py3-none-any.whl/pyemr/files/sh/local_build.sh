rm -f -r pyemr/dist
poetry build
cp -r dist pyemr/dist
poetry build
rm -f -r pyemr/dist

build_path=$(ls ./dist/*.tar.gz | head -n1)
