from enrichsdk.lib.customer import find_usecase
from .models import *
from .forms import *

def get_spec():

    return {
        'name': 'Catalog',
        'description': "Catalog",
        'usecase': find_usecase(__file__),
        'models': {
            'catalog': Catalog,
            'attachment': Attachment,
            'datasource': DataSource,
            'column': Column,
            'role': Role,
            'visibilitymap': VisibilityMap
        },
        'forms': {
            'catalog': CatalogForm,
            'attachment': AttachmentForm,
            'datasource': DataSourceForm,
            'column': ColumnForm,
            'role': RoleForm,
            'roleselect': RoleSelectForm
        }
    }
