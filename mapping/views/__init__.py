# from .views_classic import *
# from .views_api import *
from .update_codesystems import *
from .taskmanager import *
from .release_candidate import *
from .progressreport import *
from .projects import *
from .tasks import *
from .taskeditor import *
from .mappings import *
from .mapping_targets import (  # noqa: F401
    MappingTaskECLPartsView,
    MappingTaskExclusionsView,
    MappingTaskTargetsView,
    MappingECLConceptsView,
)
from .audits import *
from .status import *
from .users import *
from .comments import *
from .snomed_failback_import import *
from .server_status import *
from .test_createRules import *
from .abstract_export import *
