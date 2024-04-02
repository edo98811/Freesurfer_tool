update_settings() {
    # echo "$1"
    # echo "python3 update_settings.py $1 $2 $3"
    python3 "update_settings.py" "$1" "$2" "$3"
}

fstool(){
    # create conda env if it does not exist
    if ! conda env list | grep -q MRIs; then    
        create_env
    fi

    # activate conda env if it is not activated
    if [ "$CONDA_DEFAULT_ENV" == "MRIs" ]; then
        conda activate MRIs
    fi



    if [ $# -eq 1 ]; then
        python3 "main.py" "$1" 
    else 
        python3 "main.py" "$1" --N1 "$2" --N2 "$3"
    fi
}

print_settings() {
    # echo "$1"
    python3 "print_settings.py" "$1"
}

# update_settings $1
create_env(){
    echo create env not yet implemented 
}