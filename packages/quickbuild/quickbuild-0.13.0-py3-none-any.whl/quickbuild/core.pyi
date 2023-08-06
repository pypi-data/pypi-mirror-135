from quickbuild.endpoints import Agents as Agents, Audits as Audits, Builds as Builds, Changes as Changes, Configurations as Configurations, Dashboards as Dashboards, Groups as Groups, Identifiers as Identifiers, Issues as Issues, Measurements as Measurements, Memberships as Memberships, Reports as Reports, Requests as Requests, Resources as Resources, Shares as Shares, System as System, Tokens as Tokens, Users as Users
from quickbuild.exceptions import QBError as QBError, QBForbiddenError as QBForbiddenError, QBNotFoundError as QBNotFoundError, QBProcessingError as QBProcessingError, QBServerError as QBServerError
from quickbuild.helpers import ContentType as ContentType
from typing import Any, NamedTuple, Optional

CONTENT_JSON: str

class Response(NamedTuple):
    status: Any
    headers: Any
    body: Any

class QuickBuild:
    agents: Any
    audits: Any
    builds: Any
    changes: Any
    configurations: Any
    dashboards: Any
    groups: Any
    identifiers: Any
    issues: Any
    measurements: Any
    memberships: Any
    reports: Any
    requests: Any
    resources: Any
    shares: Any
    system: Any
    tokens: Any
    users: Any
    def __init__(self, content_type: Optional[ContentType]) -> None: ...
