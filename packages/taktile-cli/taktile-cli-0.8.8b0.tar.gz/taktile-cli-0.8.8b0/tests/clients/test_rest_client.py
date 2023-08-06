import os
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_array_equal
from pandas.testing import assert_frame_equal, assert_series_equal
from taktile_types.enums.endpoint import EndpointKinds

from tktl.core.clients.future.endpoint import SDKRestEndpoint
from tktl.core.clients.http_client import API
from tktl.core.clients.rest import RestClient
from tktl.core.exceptions import TaktileSdkError
from tktl.core.future.t import ArrowFormatKinds
from tktl.core.managers.auth import AuthConfigManager
from tktl.core.schemas.future.service import EndpointInfoSchema


def _assert_equal(a, b):
    assert a == b


RETURN_VALUE = [0.88]


def test_instantiate_client():

    key = os.environ["TEST_USER_API_KEY"]
    AuthConfigManager.set_api_key(key)

    with pytest.raises(TaktileSdkError):
        RestClient(
            api_key=key,
            repository_name=f"{os.environ['TEST_USER']}/test-new",
            branch_name="master",
            endpoint_name="repayment",
        )

    client = RestClient(
        api_key=key,
        repository_name=f"{os.environ['TEST_USER']}/integ-testing",
        branch_name="master",
        endpoint_name="repayment",
    )
    assert client.location is not None


def test_instantiate_by_url(sample_deployed_url):
    key = os.environ["TEST_USER_API_KEY"]
    AuthConfigManager.set_api_key(key)
    client = RestClient.for_url(
        api_key=key, url=sample_deployed_url, endpoint_name="repayment"
    )
    assert client.location == f"https://{sample_deployed_url}/"


@pytest.mark.parametrize(
    "X,X_serialized",
    [(pd.DataFrame([1]), '[{"0":1}]'), (pd.Series([1]), "[1]"), (np.array([1]), "[1]")],
)
@pytest.mark.parametrize(
    "response_kind,result,assert_equal",
    [
        (None, RETURN_VALUE, _assert_equal),
        (ArrowFormatKinds.DATAFRAME, pd.DataFrame(RETURN_VALUE), assert_frame_equal),
        (ArrowFormatKinds.SERIES, pd.Series(RETURN_VALUE), assert_series_equal),
        (ArrowFormatKinds.ARRAY, np.array(RETURN_VALUE), assert_array_equal),
    ],
)
def test_rest_client_serialization(
    X, X_serialized, response_kind, result, assert_equal
):
    info: EndpointInfoSchema = EndpointInfoSchema(
        name="dummy",
        path="dummy",
        kind=EndpointKinds.ARROW,
        response_kind=response_kind,
    )
    api = API(api_url="dummy")
    rest_endpoint = SDKRestEndpoint(api=api, info=info)
    with patch("tktl.core.clients.future.endpoint.safe_post") as mock:
        mock.return_value = RETURN_VALUE
        return_val = rest_endpoint.__call__(X)
        mock.assert_called_with(
            api=api, url=info.path, retries=3, timeout=10.0, data=X_serialized
        )
        assert_equal(return_val, result)


RETURN_VALUE_DT = ["2015-12-31T00:00:00.000Z"]


@pytest.mark.parametrize(
    "response_kind,result,assert_equal",
    [
        (None, RETURN_VALUE_DT, _assert_equal),
        (ArrowFormatKinds.DATAFRAME, pd.DataFrame(RETURN_VALUE_DT), assert_frame_equal),
        (ArrowFormatKinds.SERIES, pd.Series(RETURN_VALUE_DT), assert_series_equal),
        (ArrowFormatKinds.ARRAY, np.array(RETURN_VALUE_DT), assert_array_equal),
    ],
)
def test_rest_client_datetime(response_kind, result, assert_equal):
    X = pd.DataFrame([pd.to_datetime(["2015-12-31"])], columns=["end_date"])
    X_ser = '[{"end_date":"2015-12-31T00:00:00.000Z"}]'
    info: EndpointInfoSchema = EndpointInfoSchema(
        name="dummy",
        path="dummy",
        kind=EndpointKinds.ARROW,
        response_kind=response_kind,
    )
    api = API(api_url="dummy")
    rest_endpoint = SDKRestEndpoint(api=api, info=info)
    with patch("tktl.core.clients.future.endpoint.safe_post") as mock:
        mock.return_value = RETURN_VALUE_DT
        return_val = rest_endpoint.__call__(X)
        mock.assert_called_with(
            api=api, url=info.path, retries=3, timeout=10.0, data=X_ser
        )
        assert_equal(return_val, result)
