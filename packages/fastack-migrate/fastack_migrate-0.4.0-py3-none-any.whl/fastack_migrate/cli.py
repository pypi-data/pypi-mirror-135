from typing import List

from fastack.decorators import enable_context
from typer import Argument, Context, Option, Typer

from fastack_migrate import branches as _branches
from fastack_migrate import current as _current
from fastack_migrate import downgrade as _downgrade
from fastack_migrate import edit as _edit
from fastack_migrate import heads as _heads
from fastack_migrate import history as _history
from fastack_migrate import init as _init
from fastack_migrate import list_templates as _list_templates
from fastack_migrate import merge as _merge
from fastack_migrate import migrate as _migrate
from fastack_migrate import revision as _revision
from fastack_migrate import show as _show
from fastack_migrate import stamp as _stamp
from fastack_migrate import upgrade as _upgrade

db = Typer(name="db", help="Perform database migrations.")


@db.command()
def list_templates():
    """List available templates."""
    _list_templates()


@db.command()
@enable_context()
def init(
    ctx: Context,
    directory: str = Option(
        "migrations", "-d", "--directory", help="Migration script directory"
    ),
    # multidb: bool = Option(False, "--multidb", is_flag=True),
    template: str = Option(
        "fastack", "-t", "--template", help="Repository template to use"
    ),
    package: bool = Option(
        False,
        "--package",
        help="Write empty __init__.py files to the environment and version locations",
    ),
):
    """Creates a new migration repository."""
    _init(ctx.obj, directory, False, template, package)


@db.command()
@enable_context()
def revision(
    ctx: Context,
    directory: str = Option(
        "migrations", "-d", "--directory", help="Migration script directory"
    ),
    message: str = Option(None, "-m", "--message", help="Revision message"),
    autogenerate: bool = Option(
        False,
        "--autogenerate",
        is_flag=True,
        help=(
            "Populate revision script with candidate migration "
            "operations, based on comparison of database to model"
        ),
    ),
    sql: bool = Option(
        False,
        "--sql",
        is_flag=True,
        help=("Don't emit SQL to database - dump to standard output instead"),
    ),
    head: str = Option(
        "head",
        "--head",
        help=("Specify head revision or <branchname>@head to base new " "revision on"),
    ),
    splice: bool = Option(
        False,
        "--splice",
        is_flag=True,
        help=('Allow a non-head revision as the "head" to splice onto'),
    ),
    branch_label: str = Option(
        None,
        "--branch-label",
        help=("Specify a branch label to apply to the new revision"),
    ),
    version_path: str = Option(
        None,
        "--version-path",
        help=("Specify specific path from config for version file"),
    ),
    rev_id: str = Option(
        None,
        "--rev-id",
        help=("Specify a hardcoded revision id instead of generating one"),
    ),
):
    """Create a new revision file."""
    _revision(
        ctx.obj,
        directory,
        message,
        autogenerate,
        sql,
        head,
        splice,
        branch_label,
        version_path,
        rev_id,
    )


@db.command()
@enable_context()
def migrate(
    ctx: Context,
    directory: str = Option(
        "migrations",
        "-d",
        "--directory",
        help=('Migration script directory (default is "migrations")'),
    ),
    message: str = Option(None, "-m", "--message", help="Revision message"),
    sql: bool = Option(
        False,
        "--sql",
        is_flag=True,
        help=("Don't emit SQL to database - dump to standard output " "instead"),
    ),
    head: str = Option(
        "head",
        "--head",
        help=("Specify head revision or <branchname>@head to base new " "revision on"),
    ),
    splice: bool = Option(
        False,
        "--splice",
        is_flag=True,
        help=('Allow a non-head revision as the "head" to splice onto'),
    ),
    branch_label: str = Option(
        None,
        "--branch-label",
        help=("Specify a branch label to apply to the new revision"),
    ),
    version_path: str = Option(
        None,
        "--version-path",
        help=("Specify specific path from config for version file"),
    ),
    rev_id: str = Option(
        None,
        "--rev-id",
        help=("Specify a hardcoded revision id instead of generating one"),
    ),
    x_arg: List[str] = Option(
        None,
        "-x",
        "--x-arg",
        help="Additional arguments consumed by custom env.py scripts",
    ),
):
    """Autogenerate a new revision file (Alias for
    'revision --autogenerate')"""
    _migrate(
        ctx.obj,
        directory,
        message,
        sql,
        head,
        splice,
        branch_label,
        version_path,
        rev_id,
        x_arg,
    )


@db.command()
@enable_context()
def edit(
    ctx: Context,
    directory: str = Option(
        "migrations",
        "-d",
        "--directory",
        help=('Migration script directory (default is "migrations")'),
    ),
    revision: str = Argument("head"),
):
    """Edit a revision file"""
    _edit(ctx.obj, directory, revision)


@db.command()
@enable_context()
def merge(
    ctx: Context,
    directory: str = Option(
        "migrations",
        "-d",
        "--directory",
        help=('Migration script directory (default is "migrations")'),
    ),
    message: str = Option(None, "-m", "--message", help="Merge revision message"),
    branch_label: str = Option(
        None,
        "--branch-label",
        help=("Specify a branch label to apply to the new revision"),
    ),
    rev_id: str = Option(
        None,
        "--rev-id",
        help=("Specify a hardcoded revision id instead of generating one"),
    ),
    revisions: List[str] = Argument(None, max=-1),
):
    """Merge two revisions together, creating a new revision file"""
    _merge(ctx.obj, directory, revisions, message, branch_label, rev_id)


@db.command()
@enable_context()
def upgrade(
    ctx: Context,
    directory: str = Option(
        "migrations",
        "-d",
        "--directory",
        help=('Migration script directory (default is "migrations")'),
    ),
    sql: bool = Option(
        False,
        "--sql",
        is_flag=True,
        help=("Don't emit SQL to database - dump to standard output " "instead"),
    ),
    tag: str = Option(
        None,
        "--tag",
        help=('Arbitrary "tag" name - can be used by custom env.py ' "scripts"),
    ),
    x_arg: List[str] = Option(
        None,
        "-x",
        "--x-arg",
        help="Additional arguments consumed by custom env.py scripts",
    ),
    revision: str = Argument("head"),
):
    """Upgrade to a later version"""
    _upgrade(ctx.obj, directory, revision, sql, tag, x_arg)


@db.command()
@enable_context()
def downgrade(
    ctx: Context,
    directory: str = Option(
        "migrations",
        "-d",
        "--directory",
        help=('Migration script directory (default is "migrations")'),
    ),
    sql: bool = Option(
        False,
        "--sql",
        is_flag=True,
        help=("Don't emit SQL to database - dump to standard output " "instead"),
    ),
    tag: str = Option(
        None,
        "--tag",
        help=('Arbitrary "tag" name - can be used by custom env.py ' "scripts"),
    ),
    x_arg: List[str] = Option(
        None,
        "-x",
        "--x-arg",
        help="Additional arguments consumed by custom env.py scripts",
    ),
    revision: str = Argument("-1"),
):
    """Revert to a previous version"""
    _downgrade(ctx.obj, directory, revision, sql, tag, x_arg)


@db.command()
@enable_context()
def show(
    ctx: Context,
    directory: str = Option(
        "migrations",
        "-d",
        "--directory",
        help=('Migration script directory (default is "migrations")'),
    ),
    revision: str = Argument("head"),
):
    """Show the revision denoted by the given symbol."""
    _show(ctx.obj, directory, revision)


@db.command()
@enable_context()
def history(
    ctx: Context,
    directory: str = Option(
        "migrations",
        "-d",
        "--directory",
        help=('Migration script directory (default is "migrations")'),
    ),
    rev_range: str = Option(
        None,
        "-r",
        "--rev-range",
        help="Specify a revision range; format is [start]:[end]",
    ),
    verbose: bool = Option(
        False, "-v", "--verbose", is_flag=True, help="Use more verbose output"
    ),
    indicate_current: bool = Option(
        False,
        "-i",
        "--indicate-current",
        is_flag=True,
        help=("Indicate current version (Alembic 0.9.9 or greater is " "required)"),
    ),
):
    """List changeset scripts in chronological order."""
    _history(ctx.obj, directory, rev_range, verbose, indicate_current)


@db.command()
@enable_context()
def heads(
    ctx: Context,
    directory: str = Option(
        "migrations",
        "-d",
        "--directory",
        help=('Migration script directory (default is "migrations")'),
    ),
    verbose: bool = Option(
        False, "-v", "--verbose", is_flag=True, help="Use more verbose output"
    ),
    resolve_dependencies: bool = Option(
        False,
        "--resolve-dependencies",
        is_flag=True,
        help="Treat dependency versions as down revisions",
    ),
):
    """Show current available heads in the script directory"""
    _heads(ctx.obj, directory, verbose, resolve_dependencies)


@db.command()
@enable_context()
def branches(
    ctx: Context,
    directory: str = Option(
        "migrations",
        "-d",
        "--directory",
        help=('Migration script directory (default is "migrations")'),
    ),
    verbose: bool = Option(
        False, "-v", "--verbose", is_flag=True, help="Use more verbose output"
    ),
):
    """Show current branch points"""
    _branches(ctx.obj, directory, verbose)


@db.command()
@enable_context()
def current(
    ctx: Context,
    directory: str = Option(
        "migrations",
        "-d",
        "--directory",
        help=('Migration script directory (default is "migrations")'),
    ),
    verbose: bool = Option(
        False, "-v", "--verbose", is_flag=True, help="Use more verbose output"
    ),
):
    """Display the current revision for each database."""
    _current(ctx.obj, directory, verbose)


@db.command()
@enable_context()
def stamp(
    ctx: Context,
    directory: str = Option(
        "migrations",
        "-d",
        "--directory",
        help=('Migration script directory (default is "migrations")'),
    ),
    sql: bool = Option(
        False,
        "--sql",
        is_flag=True,
        help=("Don't emit SQL to database - dump to standard output " "instead"),
    ),
    tag: str = Option(
        None,
        "--tag",
        help=('Arbitrary "tag" name - can be used by custom env.py ' "scripts"),
    ),
    revision: str = Argument("head"),
):
    """'stamp' the revision table with the given revision; don't run any
    migrations"""
    _stamp(ctx.obj, directory, revision, sql, tag)
