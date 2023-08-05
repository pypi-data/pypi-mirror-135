from __future__ import unicode_literals
from django.db import models
import jsonfield
from enrichapp.dashboard.catalog.modellib import *
from enrichapp.dashboard.marketplace.modellib import *

# Rename/add/delete
from enrichapp.dashboard.persona.modellib import *
class ComplexSearchRecord(SearchRecordBase):
    pass

##################################################
# Regular Models
##################################################
class Catalog(CatalogBase):
    pass

class Attachment(AttachmentBase):
    pass

class DataSource(DataSourceBase):
    pass

class Column(ColumnBase):
    pass

class Role(RoleBase):
    pass

class VisibilityMap(VisibilityMapBase):
    pass


class Comment(CommentBase):
    pass

class FeatureRequest(FeatureRequestBase):
    pass

class Experiment(ExperimentBase):
    pass

class ExperimentRun(ExperimentRunBase):
    pass

class Feature(FeatureBase):
    pass
