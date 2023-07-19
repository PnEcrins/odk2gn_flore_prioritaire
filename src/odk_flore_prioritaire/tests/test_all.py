import pytest, csv, sys
from click.testing import CliRunner
import uuid
import flatdict

from odk_flore_prioritaire.tests.fixtures import (
    point,
    nomenclature,
    observers_and_list,
    plant,
    type_nomenclature,
)

from odk2gn.main import (
    synchronize,
    upgrade_odk_form,
)

from odk_flore_prioritaire.odk_methods import write_files

from odk2gn.gn2_utils import (
    get_observer_list,
)


@pytest.mark.usefixtures("temporary_transaction")
class TestCommand:
    def test_synchronize_flore_prio(self, mocker, app, pf_sub):
        mocker.patch("odk2gn.main.create_app", return_value=app)
        mocker.patch(
            "odk_flore_prioritaire.odk_methods.get_submissions",
            return_value=pf_sub,
        )
        mocker.patch("odk_flore_prioritaire.odk_methods.update_review_state")
        runner = CliRunner()
        result = runner.invoke(
            synchronize,
            ["flore-prio", "--project_id", 99, "--form_id", "bidon2"],
        )

        assert result.exit_code == 0

    def test_upgrade_priority_flora(self, mocker, app):
        mocker.patch("odk2gn.main.update_form_attachment")
        mocker.patch("odk2gn.main.create_app", return_value=app)
        runner = CliRunner()
        result = runner.invoke(
            upgrade_odk_form,
            ["flore-prio", "--project_id", 99, "--form_id", "bidon"],
        )
        assert result.exit_code == 0


@pytest.mark.usefixtures("temporary_transaction")
class TestUtilsFunctions:
    def test_get_observer_list1(self, observers_and_list):
        observers = get_observer_list(observers_and_list["list"].id_liste)
        assert type(observers) is list
        dict_cols = set(observers[0].keys())
        assert set(["id_role", "nom_complet"]).issubset(dict_cols)

    def test_pf_files(self):
        files = write_files()
        assert type(files) is dict
        files_names = set(files.keys())
        assert set(
            ["pf_nomenclatures.csv", "pf_observers.csv", "pf_taxons.csv"]
        ).issubset(files_names)
