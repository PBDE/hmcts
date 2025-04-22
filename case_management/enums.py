from enum import Enum, auto

class UserDetails(Enum):
    USERNAME = auto()
    PASSWORD = auto()
    EMAIL = auto()

class PatternNames(Enum):
    CASES_OVERVIEW = "case_management:cases_overview"
    LOGIN = "case_management:login"
