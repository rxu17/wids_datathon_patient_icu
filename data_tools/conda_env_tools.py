
'''
Description: Tool to update conda environment with desired packages
             Generally used before running rest of data pipeline
Dependencies: Requires installation of command line anaconda distribution
How To Use: 1) Activate desired conda environment
            2) python conda_env_tools.py
Contributors: rxu17
'''

import sys
import os

# test for yaml package in current env
if 'yaml' not in sys.modules:
    os.system("conda install yaml")
    import yaml
else:
    import yaml


def get_current_env_path():
    ''' Returns path to current environment
    '''
    cur_env = os.environ['CONDA_PREFIX']
    return('/{}/environment.yml'.format(cur_env))


def package_options():
    ''' Returns user input options for conda environment changes
    '''
    options = {"1":"Add package",
               "2":"Remove package",
               "3":"Remove all",
               "4":"Copy over yml",
               "5":"Update environment"
               "6":"Create environment"}
    return(options)


def options_select():
    ''' Main function for linking each user option to an
        actionable function
    '''
    op = package_options()
    for key in op:
        print(key, ': ', op[key])

    user_input = ""
    # continues user input until option is selected
    while user_input not in op.keys():
        if user_input.lower() == "q": # exit
            sys.exit()
        user_input = input("Please select an option from the above: \n")

    # option paths
    if user_input in ["1", "2"]:
        update_env_file(user_input)
    elif user_input == "3":
        os.remove(get_current_env_path())
    elif user_input == "4":
        create_env_file()
    elif user_input in ["5", "6"]:
        if user_input == "6":
            env_name = input("Please enter a name for your new env: \n")
        create_env_from_file(user_input, get_current_env_path(), env_name)


def create_env_file():
    ''' Function that creates environment file from 
        another environment file
    '''
    # current environment path
    user_input = input("Please select from following environments to copy yml from:{}".format())
    save_path = "{}/to_copy.yml".format(os.getcwd())
    os.system("conda env export > {}".format(save_path))

    # open env file to copy
    with open(save_path, 'w') as file:
        to_copy = yaml.full_load(file)

    # save to current env file
    with open(get_current_env_path(), 'w') as file:
        documents = yaml.dump(to_copy, file)
        print(documents)


def update_env_file(option):
    ''' Function for manually adding or removing packages from 
        environment file

        Args: option - str, option selected from package_options()
    '''
    with open(get_current_env_path(), 'w') as file:
        documents = yaml.full_load(file)
        if option == "1": # add pkg
            pkg_name = input("Please enter package_name to add")
            pkg_ver = input("Please enter package_version to add")
            pkg_name = "{}={}".format(pkg_name, pkg_ver)
            documents['dependencies'].append(pkg_name)
        elif option == "2": # remove pkg
            pkg_name = input("Please enter package_name to remove")
            pkg_to_remove = [pkg for pkg in documents['dependencies'] if pkg_name in pkg][0]
            documents['dependencies'].remove(pkg_to_remove)
        yaml.dump(documents, file)


def create_env_from_file(option, file, env_name):
    ''' Functions takes in filepath for environmental
        yaml file and creates/updates conda env using it

        Args: option - str, option selected from package_options()
              file - str, filepath of current env yaml file
              env_name - str, name for envrionment
    '''
    if option == "5":
        os.system("conda env update --prefix ./env --file {}  --prune".format(file))
    elif option == "6":
        try:
            os.system("conda env create -f {}".format(file))
        except:
            print("Error with env creation from file")
        finally:
            # create default environment
            os.system("conda env create -n {}".format(env_name))


def main():
    options_select()

if __name__ == "__main__":
    main()
