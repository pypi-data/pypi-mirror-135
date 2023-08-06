echo "Test spark script"
echo ""
poetry install
POETRY_ENV=$(poetry env info -p)

export PYTHONPATH=$PYTHONPATH:$POETRY_ENV/lib/python3.6/site-packages
export PYTHONPATH=$PYTHONPATH:$POETRY_ENV/lib64/python3.6/site-packages
export PYTHONPATH=$PYTHONPATH:$POETRY_ENV/lib/python3.7/site-packages
export PYTHONPATH=$PYTHONPATH:$POETRY_ENV/lib64/python3.7/site-packages
export PYTHONPATH=$PYTHONPATH:$POETRY_ENV/lib/python3.8/site-packages
export PYTHONPATH=$PYTHONPATH:$POETRY_ENV/lib64/python3.8/site-packages
export PYTHONPATH=$PYTHONPATH:$POETRY_ENV/lib/python3.9/site-packages
export PYTHONPATH=$PYTHONPATH:$POETRY_ENV/lib64/python3.9/site-packages

spark-submit $@


