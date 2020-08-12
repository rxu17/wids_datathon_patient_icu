
'''
Description: Tools to update
How To Use: import db_tools and call functions
Contributors: rxu17
'''
import sys
import os

# test for yaml
if 'yaml' not in sys.modules:
    os.system("conda install yaml")
    import yaml
else:
    import yaml

def get_current_env_path():
    '''
    '''
    cur_env = os.environ['CONDA_PREFIX']
    return('/{}/environment.yml'.format(cur_env))


def package_options():
    '''
    '''
    options = {"1":"Add package",
               "2":"Remove package",
               "3":"Remove all",
               "4":"Copy over yml",
               "5":"Update environment"}
    return(options)


def options_select():
    '''
    '''
    op = package_options()
    for key in op:
        print(key, ': ', op[key])
    user_input = ""
    while user_input not in op.keys():
        if user_input.lower() == "q":
            sys.exit()
        user_input = input("Please select an option from the above: \n")
    if user_input in ["1", "2"]:
        update_env_file(user_input)
    elif user_input == "3":
        os.remove(get_current_env_path())
    elif user_input == "4":
        create_env_file()
    elif user_input == "5":
        create_env_from_file(get_current_env_path())
    return()


def create_env_file():
    '''
    '''
    # current environment path
    user_input = input("Please select from following environments to copy yml from:{}".format())
    save_path = "{}/to_copy.yml".format(os.getcwd())
    os.system("conda env export > {}".format(save_path))

    with open(save_path, 'w') as file:
        to_copy = yaml.full_load(file)

    with open(get_current_env_path(), 'w') as file:
        documents = yaml.dump(to_copy, file)
        print(documents)


def update_env_file(option):
    with open(get_current_env_path(), 'w') as file:
        documents = yaml.full_load(file)
        if option == "1":
            pkg_name = input("Please enter package_name to add")
            pkg_ver = input("Please enter package_version to add")
            pkg_name = "{}={}".format(pkg_name, pkg_ver)
            documents['dependencies'].append(pkg_name)
        elif option == "2":
            pkg_name = input("Please enter package_name to remove")
            pkg_to_remove = [pkg for pkg in documents['dependencies'] if pkg_name in pkg][0]
            documents['dependencies'].remove(pkg_to_remove)
        yaml.dump(documents, file)


def create_env_from_file(file):
    os.system("conda env create -f {}".format(file))
    #os.system("conda env update --prefix ./env --file {}  --prune".format(file))


def main():
    options_select()

if __name__ == "__main__":
    main()

'''
function cenv() {
    # Usage and help message
    read -r -d '' CENV_HELP <<-'EOF'
    Usage: cenv [COMMAND] [FILE]

    Detect, activate, delete, and update conda environments.
    FILE should be a conda .yml environment file.
    If FILE is not given, assumes it is environment.yml.
    Automatically finds the environment name from FILE.

    Commands:

    None     Activates the environment
    rm       Delete the environment
    up       Update the environment

    EOF

    envfile="environment.yml"

    # Parse the command line arguments
    if [[ $# -gt 2 ]]; then
        errcho "Invalid argument(s): $@";
        return 1;
    elif [[ $# == 0 ]]; then
        cmd="activate"
    elif [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
        echo "$CENV_HELP";
        return 0;
    elif [[ "$1" == "rm" ]]; then
        cmd="delete"
        if [[ $# == 2 ]]; then
            envfile="$2"
        fi
    elif [[ "$1" == "up" ]]; then
        cmd="update"
        if [[ $# == 2 ]]; then
            envfile="$2"
        fi
    elif [[ $# == 1 ]]; then
        envfile="$1"
        cmd="activate"
    else
        errcho "Invalid argument(s): $@";
        return 1;
    fi

    # Check if the file exists
    if [[ ! -e "$envfile" ]]; then
        errcho "Environment file not found:" $envfile;
        return 1;
    fi

    # Get the environment name from the yaml file
    envname=$(grep "name: *" $envfile | sed -n -e 's/name: //p')

    # Execute one of these actions: activate, update, delete
    if [[ $cmd == "activate" ]]; then
        source activate "$envname";
    elif [[ $cmd == "update" ]]; then
        errcho "Updating environment:" $envname;
        source activate "$envname";
        conda env update -f "$envfile"
    elif [[ $cmd == "delete" ]]; then
        errcho "Removing environment:" $envname;
        source deactivate;
        conda env remove --name "$envname";
    fi
}
'''