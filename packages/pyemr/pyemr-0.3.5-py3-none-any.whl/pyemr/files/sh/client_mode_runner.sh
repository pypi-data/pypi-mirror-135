set -e
BUILD_S3_PATH=$1
BUILD_NAME=$(basename -- $BUILD_S3_PATH)
mkdir -p tmp/env
cd tmp
aws s3 cp $BUILD_S3_PATH .
chmod +x $BUILD_NAME;
tar -zxvf $BUILD_NAME -C ./env
shift;
eval "$@"
rm -r env

