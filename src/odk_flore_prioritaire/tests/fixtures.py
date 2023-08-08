import pytest, csv
import uuid
import datetime
from odk_flore_prioritaire.odk_methods import to_wkb
from geonature.utils.env import db
from geonature import create_app
from geonature.core.gn_meta.models import TDatasets
from sqlalchemy.event import listen, remove
from geonature.core.gn_commons.models import TModules
from gn_module_monitoring.config.repositories import get_config
from pypnusershub.db.models import UserList, User
from pypnnomenclature.models import TNomenclatures, BibNomenclaturesTypes
from geonature.core.gn_monitoring.models import TBaseSites, corSiteModule
from gn_module_monitoring.monitoring.models import (
    TMonitoringModules,
    TMonitoringSites,
    TMonitoringSitesGroups,
)
from apptax.taxonomie.models import BibListes, CorNomListe, Taxref, BibNoms
from utils_flask_sqla.tests.utils import JSONClient


point = {"geometry": {"type": "Point", "coordinates": [6.0535113, 44.5754145]}}


@pytest.fixture(scope="function")
def type_nomenclature():
    with db.session.begin_nested():
        type_nom = BibNomenclaturesTypes(
            mnemonique="TEST", label_default="test", label_fr="Test"
        )
        db.session.add(type_nom)
    return type_nom


@pytest.fixture(scope="function")
def plant():
    with db.session.begin_nested():
        plant = Taxref(
            cd_nom=9999999,
            regne="Plantae",
            nom_complet="Plant Test",
            nom_vern="Plante test",
            nom_valide="Plante test",
        )
        db.session.add(plant)
    return plant


def create_nomenclature(nomenclature_type, cd_nomenclature, label_default, label_fr):
    nom = TNomenclatures(
        id_type=nomenclature_type.id_type,
        cd_nomenclature=cd_nomenclature,
        label_default=label_default,
        label_fr=label_fr,
    )
    return nom


@pytest.fixture(scope="function")
def nomenclature(type_nomenclature):
    with db.session.begin_nested():
        nomenclature = create_nomenclature(type_nomenclature, "test", "test", "test")
        nomenclature.active = True
        nomenclature.nomenclature_type = type_nomenclature
        db.session.add(nomenclature)
    return nomenclature


@pytest.fixture(scope="function")
def observers_and_list():
    with db.session.begin_nested():
        obs_list = UserList(code_liste="test_list", nom_liste="test_liste")
        obs = User(
            identifiant="test",
            groupe=False,
            active=True,
            nom_role="User",
            prenom_role="test",
        )
        obs_list.users.append(obs)
        db.session.add(obs)
        db.session.add(obs_list)
    return {"list": obs_list, "user_list": obs_list.users}


@pytest.fixture(scope="function")
def pf_sub(plant, observers_and_list, nomenclature):
    pf_sub = [
        {
            "__id": uuid.uuid4(),
            "zp_geom_4326": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [6.352753, 44.670053, 0, 0],
                        [6.354138, 44.647097, 0, 0],
                        [6.370172, 44.669491, 0, 0],
                        [6.352753, 44.670053, 0, 0],
                    ]
                ],
            },
            "cd_nom": plant.cd_nom,
            "date_min": datetime.date.today(),
            "zp_area": "1758888.79",
            "observers": "" + str(observers_and_list["user_list"][0].id_role),
            "aps": [
                {
                    "type_geom": "point",
                    "ap_geom_shape": None,
                    "ap_geom_point": {
                        "type": "Point",
                        "coordinates": [6.355671, 44.655574, 0, 0],
                    },
                    "situation": {
                        "id_nomenclature_incline": nomenclature.id_nomenclature,
                        "ap_area_shape": None,
                        "ap_area_point": "0",
                        "physiognomies": str(nomenclature.id_nomenclature),
                    },
                    "habitat": {
                        "id_nomenclature_habitat": nomenclature.id_nomenclature,
                        "threat_level": "0",
                        "favorable_status_percent": 0,
                        "perturbations": str(nomenclature.id_nomenclature),
                    },
                    "id_nomenclature_phenology": nomenclature.id_nomenclature,
                    "frequency_est": {
                        "id_nomenclature_frequency_method": nomenclature.id_nomenclature,
                        "frequency": 0,
                    },
                    "count": {
                        "counting_method": "1",
                        "total_min": None,
                        "total_max": None,
                        "num": 1,
                    },
                    "comment": None,
                },
                {
                    "type_geom": "point",
                    "ap_geom_shape": None,
                    "ap_geom_point": {
                        "type": "Point",
                        "coordinates": [6.355671, 44.655574, 0],
                    },
                    "situation": {
                        "id_nomenclature_incline": nomenclature.id_nomenclature,
                        "ap_area_shape": None,
                        "ap_area_point": "0",
                        "physiognomies": str(nomenclature.id_nomenclature),
                    },
                    "habitat": {
                        "id_nomenclature_habitat": nomenclature.id_nomenclature,
                        "threat_level": "0",
                        "favorable_status_percent": 0,
                        "perturbations": str(nomenclature.id_nomenclature),
                    },
                    "id_nomenclature_phenology": nomenclature.id_nomenclature,
                    "frequency_est": {
                        "id_nomenclature_frequency_method": nomenclature.id_nomenclature,
                        "frequency": 0,
                    },
                    "count": {
                        "counting_method": "2",
                        "total_min": 1,
                        "total_max": 1,
                        "num": None,
                    },
                    "comment": None,
                },
                {
                    "type_geom": "shape",
                    "ap_geom_point": None,
                    "ap_geom_shape": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [6.352753, 44.670053, 0],
                                [6.354138, 44.647097, 0],
                                [6.370172, 44.669491, 0],
                                [6.352753, 44.670053, 0],
                            ]
                        ],
                    },
                    "situation": {
                        "id_nomenclature_incline": nomenclature.id_nomenclature,
                        "ap_area_shape": "1758888.79",
                        "ap_area_point": None,
                        "physiognomies": str(nomenclature.id_nomenclature),
                    },
                    "habitat": {
                        "id_nomenclature_habitat": nomenclature.id_nomenclature,
                        "threat_level": "0",
                        "favorable_status_percent": 0,
                        "perturbations": str(nomenclature.id_nomenclature),
                    },
                    "id_nomenclature_phenology": nomenclature.id_nomenclature,
                    "frequency_est": {
                        "id_nomenclature_frequency_method": "mille",
                        "frequency": 0,
                    },
                    "count": {
                        "counting_method": "0",
                        "total_min": None,
                        "total_max": None,
                        "num": None,
                    },
                    "comment": None,
                },
            ],
        },
    ]
    return pf_sub
