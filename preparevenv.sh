#!/bin/bash

echo "Let's prepare the virtual env!"


python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

if python3 -c "import sys; sys.exit(0 if sys.prefix == sys.base_prefix else 1)"; then
    echo "No Python virtual environment is active"
else
    echo "A Python virtual environment is active"
fi

pip3 install -r requirements.txt > /dev/null
pip3 install -e . > /dev/null

cp .env.example .env > /dev/null

cat .env

if [ -f "venv/bin/secora" ]; then
    echo "File exists"
    ./venv/bin/secora &

    # lsof -i -P -n | grep 8000 --- to find out the detail of the process associated with teh port
    # pkill Python --- for killing the background process
else
    echo "File does not exist"
    if deactivate; then
        echo "Deactivated the Python virtual environment!!!"; 

        rm -rf venv/
        if [ $? != 0 ]; then 
            echo "A Python virtual environment couln't be removed!!!";
        else 
            echo "A Python virtual environment removed!!!";
        fi
    else
        echo "Couldn't deactivate the Python virtual environment!!!"; 
    fi
fi





