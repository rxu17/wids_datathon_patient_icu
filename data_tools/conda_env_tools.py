
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
    ''' Returns str, path to current environment
    '''
    cur_env = os.environ['CONDA_PREFIX']
    return('/{}/environment.yml'.format(cur_env))


def get_env_path(env_name):
    ''' Returns str, path to selected env
    '''
    cur_env = os.environ['CONDA_PREFIX']
    env_path = os.path.dirname(get_current_env_path())
    envs = os.listdir("{}/envs/{}/".format(env_path, env_name))
    return(envs)


def package_options():
    ''' Returns dict, user input options for conda environment changes
    '''
    options = {"1":"Create environment",
               "2":"Add package",
               "3":"Remove package",
               "4":"Remove all",
               "5":"List environments",
               "6":"List packages",
               "7":"Activate environment"}
    return(options)


def get_envs():
    ''' Returns str, current conda environment path
    '''
    env_path = os.path.dirname(get_current_env_path())
    envs = os.listdir("{}/envs/".format(env_path))
    envs = {str(i):envs[i] for i in range(0, len(envs))}
    return(envs)


def validate_user_input(options, message):
    ''' Validation function for asking for user input

        Args: options - str, available options for user
              message - str, prompt for user

        Returns: str, user selected option
    '''
    user_input = ""
    while user_input not in options.keys():
        for key in options:
            print(key, ':', options[key])
        print("Enter 'q' anytime to quit\n")
        user_input = input(message)
        if user_input.lower() == "q": # exit
            sys.exit()
    return(user_input)


def options_select():
    ''' Main function for linking each user option to an
        actionable function
    '''
    op = package_options()
    user_input = validate_user_input(options = op, 
                                     message = "Please select an option from the above: \n")
    # option paths
    if user_input == "1":
        create_env()
    elif user_input == "5":
        os.system("conda env list")
    else:
        env_name = get_envs()[validate_user_input(options = get_envs(), 
                                       message = "Please select an environment to change: \n")]
        if user_input in ["2", "3"]:
            update_env_file(user_input, env_name)
        elif user_input == "4":
            remove_env(env_name)
        elif user_input == "6":
            os.system("conda list -n {}".format(env_name))
        elif user_input == "7":
            os.system("source activate {}".format(env_name))


def create_env():
    ''' Function that has the option of creating environment file from 
        another environment file, or creating blank env
    '''
    env_name = input("Please enter a name for your new env: \n")
    option = validate_user_input(options = {"a":"Create env from another env",
                                            "b":"Create blank env"}, 
                                 message = "Please select an option from the above: \n")

    # create from another env yaml file
    if option == "a":
        user_input = get_envs()[validate_user_input(options = get_envs(), 
                    message = "Please select an environment to copy: \n")]
        save_path = "{}/to_copy.yaml".format(os.getcwd())
        os.system("conda env export > {} -n {}".format(save_path, env_name))

        try:
            # open env file to copy
            with open(save_path, 'r+') as file:
                to_copy = yaml.full_load(file)
                # save to selected env file
                os.system("conda env create -f {}".format(save_path))
        except:
            print("Error with env creation from file")
        finally:
            # create default environment
            os.system("conda create -n {} python".format(env_name))

    elif option == "b":
        # create blank environment
        os.system("conda create -n {}".format(env_name))


def update_env_file(option, env_name):
    ''' Function for manually adding or removing packages from 
        environment file

        Args: option - str, option selected from package_options()
              env_name - str, env to update
    '''
    if option == "2": # add pkg
        pkg_name = input("Please enter package_name to add: \n")
        pkg_ver = input("Please enter package_version to add: \n") # optional
        if pkg_ver == "":
            pkg_name = "{}".format(pkg_name)
        else:
            pkg_name = "{}={}".format(pkg_name, pkg_ver)
        os.system("conda install {} -n {}".format(pkg_name, env_name))
    elif option == "3": # remove pkg
        pkg_name = input("Please enter package_name to remove: \n")
        os.system("conda remove {} -n {}".format(pkg_name, env_name))


def remove_env(env_name):
    ''' Functions takes in env name and removes it

        Args: env_name - str, name for envrionment
    '''
    try:
        os.system("conda remove --name {} --all".format(env_name))
    except:
        print("Trouble removing environment")
    finally:
        os.system("conda env remove -n {}".format(env_name))


def main():
    ''' Main function allows user to continue making 
        conda env choices
    '''
    cont = ""
    while cont != "n":
        cont = input("Continue? (y/n) \n")
        options_select()

if __name__ == "__main__":
    main()
