echo "Installing package dependencies inside docker:"
echo ""
pip3 install pyemr -U --quiet
pyemr notebook --env=venv
