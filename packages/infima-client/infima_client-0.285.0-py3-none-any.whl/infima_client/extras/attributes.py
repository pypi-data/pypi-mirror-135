from typing import TYPE_CHECKING, List, Optional

import pandas as pd

from infima_client.core.types import Unset

from .utils import DateT, handle_factor_date, simple_dict_to_frame

if TYPE_CHECKING:
    from infima_client.client import InfimaClient


def get_cohort_summary(
    *,
    client: "InfimaClient",
    cohorts: List[str],
    factor_date: Optional[DateT] = None,
) -> Optional[pd.DataFrame]:
    resp = client.api.cohort_v1.get_cohort_summary(
        cohorts=cohorts,
        factor_date=handle_factor_date(factor_date)
        if factor_date is not None
        else None,
    )
    if isinstance(resp.summary, Unset):
        return None
    return simple_dict_to_frame(resp.summary.to_dict(), index_name="cohort")


def get_pool_attributes(
    *,
    client: "InfimaClient",
    cusips: List[str],
) -> Optional[pd.DataFrame]:
    resp = client.api.pool_v1.get(
        cusips=cusips,
    )
    if isinstance(resp.pools, Unset):
        return None
    return simple_dict_to_frame(resp.pools.to_dict(), index_name="cusip")
