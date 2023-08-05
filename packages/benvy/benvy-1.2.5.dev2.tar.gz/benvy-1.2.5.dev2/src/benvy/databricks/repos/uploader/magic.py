from benvy.databricks.repos.config.BootstrapConfig import BootstrapConfig
from benvy.container.dicontainer import Container


def uploader(line):
    parameters = BootstrapConfig().get_parameters()
    container = Container(parameters)
    repo_file_uploader = container.get_repo_file_uploader()
    arguments = line.split()
    repo_file_uploader.upload_files_to_repo(*arguments)


def load_ipython_extension(ipython):
    ipython.register_magic_function(uploader, "line")
