# -*- coding: utf-8 -*-
import contextlib
import os
import unittest

from alembic import command
from alembic.config import Config
from pyramid.paster import get_appsettings
from skosprovider.providers import DictionaryProvider
from skosprovider.registry import Registry
from skosprovider.skos import ConceptScheme
from skosprovider.uri import UriPatternGenerator
from skosprovider_sqlalchemy.providers import SQLAlchemyProvider
from skosprovider_sqlalchemy.utils import import_provider
from sqlalchemy import engine_from_config
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

from atramhasis.cache import list_region
from atramhasis.cache import tree_region
from fixtures import data
from fixtures import materials as material_data

TEST_DIR = os.path.dirname(__file__)
SETTINGS = get_appsettings(os.path.join(TEST_DIR, '..', 'tests', 'conf_test.ini'))
db_setup = False
db_filled = False

# No test should want caching
tree_region.configure('dogpile.cache.null', replace_existing_backend=True)
list_region.configure('dogpile.cache.null', replace_existing_backend=True)


def get_alembic_config():
    alembic_config = Config(os.path.join(TEST_DIR, '..', 'alembic.ini'))
    alembic_config.set_main_option(
        "script_location",
        os.path.join(TEST_DIR, '..', 'atramhasis', 'alembic')
    )
    alembic_config.set_main_option(
        "ini_location",
        os.path.join(TEST_DIR, '..', 'tests', 'conf_test.ini')
    )
    return alembic_config


ALEMBIC_CONFIG = get_alembic_config()


def setup_db(guarantee_empty=False):
    global db_setup, db_filled
    if not db_setup or (guarantee_empty and db_filled):
        _reset_db()
        command.upgrade(ALEMBIC_CONFIG, 'head')
        db_setup = True
        db_filled = False


def _reset_db():
    engine = engine_from_config(SETTINGS, prefix='sqlalchemy.')
    try:
        engine.execute("DELETE FROM concept_note")
        engine.execute("DELETE FROM note")
        engine.execute("DELETE FROM concept_label")
        engine.execute("DELETE FROM label")
    except (ProgrammingError, OperationalError):
        """The tables may not exist if it's first time."""
    command.downgrade(ALEMBIC_CONFIG, 'base')
    engine.dispose()


def fill_db():
    global db_filled
    if not db_filled:
        from fixtures.data import trees
        from skosprovider_sqlalchemy.models import ConceptScheme
        with db_session() as session:
            import_provider(trees,
                            ConceptScheme(id=1, uri='urn:x-skosprovider:trees'),
                            session)
            import_provider(material_data.materials,
                            ConceptScheme(id=4, uri='urn:x-vioe:materials'),
                            session)
            import_provider(data.geo,
                            ConceptScheme(id=2, uri='urn:x-vioe:geography'),
                            session)
            import_provider(
                DictionaryProvider(
                    {'id': 'MISSING_LABEL', 'default_language': 'nl'},
                    [{'id': '1', 'uri': 'urn:x-skosprovider:test/1'},
                     {
                         'id': '2',
                         'uri': 'urn:x-skosprovider:test/2',
                         'labels': [
                             {'type': 'prefLabel', 'language': 'nl', 'label': 'label'}
                         ],
                     }]
                ),
                ConceptScheme(id=9, uri='urn:x-vioe:test'),
                session)
            session.add(ConceptScheme(id=3, uri='urn:x-vioe:styles'))
            for scheme_id in (5, 6, 7, 8):
                session.add(
                    ConceptScheme(id=scheme_id, uri='urn:dummy-{}'.format(scheme_id))
                )
        db_filled = True


class DbTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(DbTest, cls).setUpClass()
        cls.engine = engine_from_config(SETTINGS, prefix='sqlalchemy.')
        cls.connection = cls.engine.connect()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
        cls.engine.dispose()
        super(DbTest, cls).tearDownClass()

    def setUp(self):
        super(DbTest, self).setUp()
        self.transaction = self.connection.begin()
        self.session = sessionmaker(bind=self.connection)()

    def tearDown(self):
        self.session.close()
        self.transaction.rollback()

    def insert(self, db_object):
        self.session.add(db_object)
        self.session.flush()
        self.session.refresh(db_object)

    def update(self, db_object):
        self.session.merge(db_object)
        self.session.flush()
        self.session.refresh(db_object)


@contextlib.contextmanager
def db_session():
    engine = engine_from_config(SETTINGS, prefix='sqlalchemy.')
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_registry(request):
    registry = Registry(instance_scope='threaded_thread')
    trees = SQLAlchemyProvider(
        {'id': 'TREES', 'conceptscheme_id': 1},
        request.db
    )

    geo = SQLAlchemyProvider(
        {'id': 'GEOGRAPHY', 'conceptscheme_id': 2},
        request.db,
        uri_generator=UriPatternGenerator('urn:x-vioe:geography:%s')
    )

    styles = SQLAlchemyProvider(
        {'id': 'STYLES', 'conceptscheme_id': 3},
        request.db
    )

    materials = SQLAlchemyProvider(
        {'id': 'MATERIALS', 'conceptscheme_id': 4},
        request.db,
        uri_generator=UriPatternGenerator('urn:x-vioe:materials:%s')
    )
    test = DictionaryProvider(
        {
            'id': 'TEST',
            'default_language': 'nl',
            'subject': ['biology']
        },
        [data.larch, data.chestnut, data.species],
        concept_scheme=ConceptScheme('http://id.trees.org')
    )
    missing_label = SQLAlchemyProvider(
        {'id': 'MISSING_LABEL', 'conceptscheme_id': 9},
        request.db
    )

    registry.register_provider(trees)
    registry.register_provider(geo)
    registry.register_provider(styles)
    registry.register_provider(materials)
    registry.register_provider(test)
    registry.register_provider(missing_label)
    return registry
