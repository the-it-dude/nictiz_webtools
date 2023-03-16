import enum

class MappingGroups:
    """Collection of Mapping Group Names."""

    project_access = "mapping | access"


class ProjectTypes(enum.Enum):
    """Mapping Project types."""

    one_to_many = '1'
    many_to_one = '2'
    many_to_many = '3'
    snomed_ecl_to_one = '4'

    @classmethod
    def choices(cls):
        return [
            # (code, readable)
            (cls.one_to_many.value, 'One to Many'),
            (cls.many_to_one.value, 'Many to One'),
            (cls.many_to_many.value, 'Many to Many'),
            (cls.snomed_ecl_to_one.value, 'Snomed ECL to one'),
        ]


class RuleCorrelations(enum.Enum):
    """Rule Correlations."""

    broad_to_narrow = '447559001'
    exact_match = '447557004'
    narrow_to_broad = '447558009'
    partial_overlap = '447560006'
    not_mappable = '447556008'
    not_specified = '447561005'

    @classmethod
    def choices(cls):
        return [
            # (code, readable)
            (cls.broad_to_narrow.value, 'Broad to narrow'),
            (cls.exact_match.value, 'Exact match'),
            (cls.narrow_to_broad.value, 'Narrow to broad'),
            (cls.partial_overlap.value, 'Partial overlap'),
            (cls.not_mappable.value, 'Not mappable'),
            (cls.not_specified.value, 'Not specified'),
        ]


class EventActionOptions(enum.Enum):
    status_change = 'status_change'
    user_change = 'user_change'

    @classmethod
    def choices(cls):
        return [
            (cls.status_change.value, 'Status wijzigen'),
            (cls.user_change.value, 'Toegewezen aan gebruiker'),
        ]


class RCStatus(enum.Enum):
    draft = '0'
    active = '1'
    retired = '2'
    unknown = '3'

    @classmethod
    def choices(cls):
        return [
            (RCStatus.draft.value, 'Draft'),
            (RCStatus.active.value, 'Active'),
            (RCStatus.retired.value, 'Retired'),
            (RCStatus.unknown.value, 'Unknown'),
        ]
