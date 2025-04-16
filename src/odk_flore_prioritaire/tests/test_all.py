import pytest
from click.testing import CliRunner

from odk_flore_prioritaire.tests.fixtures import *

from odk2gn.blueprint import (
    synchronize,
    upgrade_odk_form,
)

from odk_flore_prioritaire.odk_methods import write_files, update_priority_flora_db, upgrade_pf

from odk2gn.gn2_utils import (
    get_observer_list,
)


@pytest.mark.usefixtures("temporary_transaction")
class TestCommand:
    def test_synchronize_flore_prio(self, mocker, pf_sub):
        mocker.patch(
            "odk_flore_prioritaire.odk_methods.get_submissions",
            return_value=pf_sub,
        )
        mocker.patch("odk_flore_prioritaire.odk_methods.update_review_state")
        update_priority_flora_db(project_id=1, form_id="bidon")
        

    def test_upgrade_priority_flora(self, mocker):
        print("LAAAAAAAA??????????")
        mocker.patch("odk_flore_prioritaire.odk_methods.update_form_attachment")
        upgrade_pf(1, "bidon")
        

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
