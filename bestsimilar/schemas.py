from schematics.models import Model
from schematics.types import ListType, StringType


class BestSimilarSchema(Model):
    title = StringType(required=True)
    tags = ListType(StringType)
    year = StringType(required=True)
