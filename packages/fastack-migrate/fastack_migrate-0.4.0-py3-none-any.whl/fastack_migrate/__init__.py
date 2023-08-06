import argparse
import logging
import os
import sys
from functools import wraps
from typing import Callable, Sequence

from alembic import __version__ as __alembic_version__
from alembic import command
from alembic.config import Config as AlembicConfig
from alembic.util import CommandError
from fastack import Fastack
from fastack_sqlmodel import DatabaseState

alembic_version = tuple([int(v) for v in __alembic_version__.split(".")[0:3]])
log = logging.getLogger(__name__)


class Config(AlembicConfig):
    def __init__(self, *args, **kwargs):
        self.template_directory = kwargs.pop("template_directory", None)
        super().__init__(*args, **kwargs)

    def get_template_directory(self):
        if self.template_directory:
            return self.template_directory
        package_dir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(package_dir, "templates")


class Migrate(object):
    def __init__(
        self,
        app: Fastack = None,
        db: DatabaseState = None,
        directory: str = "migrations",
        **kwargs,
    ):
        self.configure_callbacks = []
        self.db = db
        self.directory = str(directory)
        self.alembic_ctx_kwargs = kwargs
        if app is not None and db is not None:
            self.init_app(app, db, directory)

    def init_app(
        self, app: Fastack, db: DatabaseState = None, directory: str = None, **kwargs
    ):
        self.db = db or app.state.db
        self.directory = str(directory or self.directory)
        self.alembic_ctx_kwargs.update(kwargs)
        app.state.migrate = MigrateConfig(self, self.db, **self.alembic_ctx_kwargs)

    def configure(self, f: Callable) -> Callable:
        self.configure_callbacks.append(f)
        return f

    def call_configure_callbacks(self, config: Config) -> Config:
        for f in self.configure_callbacks:
            config = f(config)
        return config

    def get_config(
        self, directory: str = None, x_arg: Sequence = None, opts: Sequence = None
    ) -> Config:
        if directory is None:
            directory = self.directory
        directory = str(directory)
        config = Config(os.path.join(directory, "alembic.ini"))
        config.set_main_option("script_location", directory)
        if config.cmd_opts is None:
            config.cmd_opts = argparse.Namespace()
        for opt in opts or []:
            setattr(config.cmd_opts, opt, True)
        if not hasattr(config.cmd_opts, "x"):
            if x_arg is not None:
                setattr(config.cmd_opts, "x", [])
                if isinstance(x_arg, list) or isinstance(x_arg, tuple):
                    for x in x_arg:
                        config.cmd_opts.x.append(x)
                else:
                    config.cmd_opts.x.append(x_arg)
            else:
                setattr(config.cmd_opts, "x", None)
        return self.call_configure_callbacks(config)


class MigrateConfig(object):
    def __init__(self, migrate: Migrate, db: DatabaseState, **kwargs):
        self.migrate = migrate
        self.db = db
        self.directory = migrate.directory
        self.configure_args = kwargs

    @property
    def metadata(self):
        """
        Backwards compatibility, in old releases app.state.migrate
        was set to db, and env.py accessed app.state.migrate.metadata
        """
        return self.db.engine.metadata


def setup(app: Fastack):
    def on_startup():
        try:
            db: DatabaseState = app.state.db
            Migrate(app, db)
        except AttributeError as e:
            raise RuntimeError(
                "Make sure ``fastack-sqlmodel`` plugin is installed in your project"
            ) from e

    app.add_event_handler("startup", on_startup)


def catch_errors(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except (CommandError, RuntimeError) as exc:
            log.error("Error: " + str(exc))
            sys.exit(1)

    return wrapped


@catch_errors
def list_templates():
    """List available templates."""
    config = Config()
    config.print_stdout("Available templates:\n")
    for tempname in sorted(os.listdir(config.get_template_directory())):
        with open(
            os.path.join(config.get_template_directory(), tempname, "README")
        ) as readme:
            synopsis = next(readme).strip()
        config.print_stdout("%s - %s", tempname, synopsis)


@catch_errors
def init(app: Fastack, directory=None, multidb=False, template=None, package=False):
    """Creates a new migration repository"""
    if directory is None:
        directory = app.state.migrate.directory
    template_directory = None
    if template is not None and ("/" in template or "\\" in template):
        template_directory, template = os.path.split(template)
    config = Config(template_directory=template_directory)
    config.set_main_option("script_location", directory)
    config.config_file_name = os.path.join(directory, "alembic.ini")
    config = app.state.migrate.migrate.call_configure_callbacks(config)
    if multidb and template is None:
        template = "fastack-multidb"
    elif template is None:
        template = "fastack"
    command.init(config, directory, template=template, package=package)


@catch_errors
def revision(
    app: Fastack,
    directory=None,
    message=None,
    autogenerate=False,
    sql=False,
    head="head",
    splice=False,
    branch_label=None,
    version_path=None,
    rev_id=None,
):
    """Create a new revision file."""
    config = app.state.migrate.migrate.get_config(directory)
    command.revision(
        config,
        message,
        autogenerate=autogenerate,
        sql=sql,
        head=head,
        splice=splice,
        branch_label=branch_label,
        version_path=version_path,
        rev_id=rev_id,
    )


@catch_errors
def migrate(
    app: Fastack,
    directory=None,
    message=None,
    sql=False,
    head="head",
    splice=False,
    branch_label=None,
    version_path=None,
    rev_id=None,
    x_arg=None,
):
    """Alias for 'revision --autogenerate'"""
    config = app.state.migrate.migrate.get_config(
        directory, opts=["autogenerate"], x_arg=x_arg
    )
    command.revision(
        config,
        message,
        autogenerate=True,
        sql=sql,
        head=head,
        splice=splice,
        branch_label=branch_label,
        version_path=version_path,
        rev_id=rev_id,
    )


@catch_errors
def edit(app: Fastack, directory=None, revision="current"):
    """Edit current revision."""
    if alembic_version >= (0, 8, 0):
        config = app.state.migrate.migrate.get_config(directory)
        command.edit(config, revision)
    else:
        raise RuntimeError("Alembic 0.8.0 or greater is required")


@catch_errors
def merge(
    app: Fastack,
    directory=None,
    revisions="",
    message=None,
    branch_label=None,
    rev_id=None,
):
    """Merge two revisions together.  Creates a new migration file"""
    config = app.state.migrate.migrate.get_config(directory)
    command.merge(
        config, revisions, message=message, branch_label=branch_label, rev_id=rev_id
    )


@catch_errors
def upgrade(
    app: Fastack, directory=None, revision="head", sql=False, tag=None, x_arg=None
):
    """Upgrade to a later version"""
    config = app.state.migrate.migrate.get_config(directory, x_arg=x_arg)
    command.upgrade(config, revision, sql=sql, tag=tag)


@catch_errors
def downgrade(
    app: Fastack, directory=None, revision="-1", sql=False, tag=None, x_arg=None
):
    """Revert to a previous version"""
    config = app.state.migrate.migrate.get_config(directory, x_arg=x_arg)
    if sql and revision == "-1":
        revision = "head:-1"
    command.downgrade(config, revision, sql=sql, tag=tag)


@catch_errors
def show(app: Fastack, directory=None, revision="head"):
    """Show the revision denoted by the given symbol."""
    config = app.state.migrate.migrate.get_config(directory)
    command.show(config, revision)


@catch_errors
def history(
    app: Fastack, directory=None, rev_range=None, verbose=False, indicate_current=False
):
    """List changeset scripts in chronological order."""
    config = app.state.migrate.migrate.get_config(directory)
    if alembic_version >= (0, 9, 9):
        command.history(
            config, rev_range, verbose=verbose, indicate_current=indicate_current
        )
    else:
        command.history(config, rev_range, verbose=verbose)


@catch_errors
def heads(app: Fastack, directory=None, verbose=False, resolve_dependencies=False):
    """Show current available heads in the script directory"""
    config = app.state.migrate.migrate.get_config(directory)
    command.heads(config, verbose=verbose, resolve_dependencies=resolve_dependencies)


@catch_errors
def branches(app: Fastack, directory=None, verbose=False):
    """Show current branch points"""
    config = app.state.migrate.migrate.get_config(directory)
    command.branches(config, verbose=verbose)


@catch_errors
def current(app: Fastack, directory=None, verbose=False):
    """Display the current revision for each database."""
    config = app.state.migrate.migrate.get_config(directory)
    command.current(config, verbose=verbose)


@catch_errors
def stamp(app: Fastack, directory=None, revision="head", sql=False, tag=None):
    """'stamp' the revision table with the given revision; don't run any
    migrations"""
    config = app.state.migrate.migrate.get_config(directory)
    command.stamp(config, revision, sql=sql, tag=tag)
