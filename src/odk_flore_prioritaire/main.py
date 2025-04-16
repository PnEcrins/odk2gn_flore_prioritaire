import click
from odk_flore_prioritaire.odk_methods import update_priority_flora_db, upgrade_pf

import logging

log = logging.getLogger("app")


@click.command(name="flore-prio")
@click.option("--project_id", required=True, type=int)
@click.option("--form_id", required=True, type=str)
def synchronize(project_id, form_id):
    """synchronize the db for priority flora module

    Keyword arguments:
    project_id -- int, the id of the odk project
    form_id -- string, the form_id defined on the form

    """
    log.info(f"--- Start synchro for priority flora ---")
    update_priority_flora_db(project_id=project_id, form_id=form_id)
    log.info("--- Done ---")


@click.command(name="flore-prio")
@click.option("--project_id", required=True, type=int)
@click.option("--form_id", required=True, type=str)
def upgrade_odk_form(project_id, form_id):
    """update the csv files for priority flora module

    Keyword arguments:
    project_id -- int, the id of the odk project
    form_id -- string, the form_id defined on the form
    """
    upgrade_pf(project_id, form_id)
