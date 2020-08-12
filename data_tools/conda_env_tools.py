
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
    '''
    '''
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
