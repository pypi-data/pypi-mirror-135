from typing import TYPE_CHECKING, List, Optional

import pandas as pd

from .utils import nested_dict_to_frame

if TYPE_CHECKING:
    from infima_client.client import InfimaClient


def check_cohort_coverage(
    *, client: "InfimaClient", cohorts: List[str]
) -> Optional[pd.DataFrame]:
    resp = client.api.cohort_v1.check_coverage(cohorts=cohorts)
    return nested_dict_to_frame(
        resp.to_dict(),
        "summary->cohort(*)->summary->cusip(*)",
    )


def check_coverage(
    *, client: "InfimaClient", cusips: List[str]
) -> Optional[pd.DataFrame]:
    resp = client.api.pool_v1.check_coverage(cusips=cusips)
    return nested_dict_to_frame(resp.to_dict(), "summary->cusip(*)")
