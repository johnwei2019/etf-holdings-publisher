import os
import zipfile
import glob

def create_lambda_package(package_path, dependencies_path):
    print("Start to create lambda package")
    try:
        os.remove(package_path)
    except FileNotFoundError:
        pass
    try: 
        os.makedirs(os.path.dirname(package_path))
    except FileExistsError:
        pass
    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as package_file:
        [package_file.write(f) for f in glob.glob('src/**/*.py', recursive=True)]
        add_package_dependencies(package_file, dependencies_path)
    print("Lambda package created at {}".format(package_path))

def add_package_dependencies(package_file, dependencies_path):
    print("Adding package dependencies")
    os.environ['PIPENV_VENV_IN_PROJECT'] = '1'
    os.system('pipenv install')
    for f in glob.glob("{}/**/*".format(dependencies_path), recursive=True):
        package_file.write(f, f[len(dependencies_path)+1:])
    print("Package dependencies added")
