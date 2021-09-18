import pathlib
import shutil

import click
import yaml
from jinja2 import Environment, FileSystemLoader

@click.group()
def cli():
    pass


def _err_message(message: str) -> str:
    return click.style(message, fg='red')


@cli.command()
@click.option('--path', 'path_', prompt='Where should be template setting directory gonna created.')
def init(path_: str):
    boilerplate_dir_path = pathlib.Path(__file__).parent / 'template_boilerplate'
    d_path = pathlib.Path(path_)
    if d_path.exists():
        click.echo(_err_message(f"The directory {d_path.absolute()} already exists."), err=True)
        raise click.Abort()
    shutil.copytree(boilerplate_dir_path, d_path)
    print(f"Done. template dir is {d_path.absolute()}")


@cli.command()
@click.option('--setting_path', 'path_', prompt='The Path of template setting Yaml file.')
def out(path_: str):
    setting_yml_path = pathlib.Path(path_)
    if not setting_yml_path.exists():
        click.echo(_err_message(f"Not Found the setting Yaml. Path: {setting_yml_path.absolute()}"), err=True)
        raise click.Abort()

    with open(path_) as f:
        settings = yaml.load(f, Loader=yaml.SafeLoader)
    env = Environment(loader=FileSystemLoader(setting_yml_path.parent, encoding='utf8'))
    tpl = env.get_template(settings['template_path'])
    rendered_text = tpl.render(settings['variables'])
    print(rendered_text)
    dist_file_path = setting_yml_path.parent / settings['dist_file_path']
    with open(dist_file_path, 'w') as f:
        f.write(rendered_text)

if __name__ == '__main__':
    cli()
