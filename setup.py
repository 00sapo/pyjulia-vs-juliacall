

def setup_pyjulia_env(path_to_project="."):
    """
    A function that installs all dependencies for current environment.

    This should be the same as what `juliacall` does at every import time.

    * `path_to_project` is the path to the project that will be instantiated.
    If `None`, no project will be instantiated. Defaults: to the current
    working directory.
    """
    import jill.install  # noqa: autoimport
    import os  # noqa: autoimport
    import shutil  # noqa: autoimport
    if shutil.which('julia') is None:
        print(
            "No Julia executable found, installing the latest version using `jill`")
        jill.install.install_julia("stable", confirm=True)
        if shutil.which('julia') is None:
            print(f"Please add {os.environ['JILL_SYMLINK_DIR']} to your path")
    import julia  # noqa: autoimport
    # the following installs dependencies for pyjulia
    julia.install()
    from julia.api import LibJulia  # noqa: autoimport

    if path_to_project is not None:
        api = LibJulia.load()
        api.init_julia([f"--project={path_to_project}"])

        from julia import Main  # noqa: autoimport

        Main.eval('using Pkg')
        Main.eval('Pkg.instantiate()')


setup_pyjulia_env()

# juliacall uses another custom json format... not very portable when switching
# between julia and python
__import__('juliacall')
