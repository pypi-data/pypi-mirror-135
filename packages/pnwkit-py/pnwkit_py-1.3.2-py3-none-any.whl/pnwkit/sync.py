from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Literal,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
    overload,
)

import requests

from .base import KitBase
from .data import (
    Alliance,
    Color,
    Data,
    Nation,
    PaginatorInfo,
    Trade,
    Tradeprice,
    Treasure,
    War,
)
from .errors import GraphQLError
from .paginator import AlliancePaginator, NationPaginator, Paginator


class SyncKit(KitBase):
    def _query(
        self,
        endpoint: str,
        params: MutableMapping[str, Any],
        args: Sequence[Union[str, Any]],
        *,
        is_paginator: bool = False,
    ) -> Dict[str, Any]:
        query = query = self._format_query(endpoint, params, args, is_paginator)
        response = requests.request("GET", self.graphql_url(), json={"query": query})
        data: Any = response.json()
        try:
            if "errors" in data[0]:
                error = (
                    "\n".join(i["message"] for i in data[0]["errors"])
                    if len(data[0]["errors"]) > 1
                    else data[0]["errors"][0]["message"]
                )
                raise GraphQLError(error)
        except KeyError:
            pass
        try:
            if "errors" in data:
                error = (
                    "\n".join(i["message"] for i in data["errors"])
                    if len(data["errors"]) > 1
                    else data["errors"][0]["message"]
                )
                raise GraphQLError(error)
        except KeyError:
            pass
        return data

    def _data_query(
        self,
        endpoint: str,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        is_paginator: bool = False,
        type_: Type[Data],
        paginator_type: Optional[Type[Paginator]] = None,
        **kwargs: Any,
    ) -> Union[Tuple[Data, ...], Paginator]:
        args = (arg, *args)
        params = params or kwargs
        if "first" not in params and endpoint in {"alliance", "nations"}:
            params["first"] = 5
        response = self._query(endpoint, params, args, is_paginator=is_paginator)
        if is_paginator and paginator_type:
            data = tuple(type_(i) for i in response["data"][endpoint]["data"])
            if paginator:
                return paginator_type(
                    data, PaginatorInfo(response["data"][endpoint]["paginatorInfo"])
                )
            return data
        data = tuple(type_(i) for i in response["data"][endpoint])
        return data

    @overload
    def alliance_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = False,
        **kwargs: Any,
    ) -> Tuple[Alliance, ...]:
        ...

    @overload
    def alliance_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = True,
        **kwargs: Any,
    ) -> AlliancePaginator:
        ...

    def alliance_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **kwargs: Any,
    ) -> Union[Tuple[Alliance, ...], AlliancePaginator]:
        data = self._data_query(
            "alliances",
            params,
            arg,
            *args,
            **kwargs,
            type_=Alliance,
            paginator=paginator,
            is_paginator=True,
            paginator_type=AlliancePaginator,
        )
        if TYPE_CHECKING:
            if isinstance(data, tuple):
                data = cast(Tuple[Alliance, ...], data)
            else:
                data = cast(AlliancePaginator, data)
        return data

    def color_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[Color, ...]:
        data = self._data_query(
            "colors",
            params,
            arg,
            *args,
            **kwargs,
            type_=Color,
        )
        if TYPE_CHECKING:
            data = cast(Tuple[Color, ...], data)
        return data

    @overload
    def nation_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = False,
        **kwargs: Any,
    ) -> Tuple[Nation, ...]:
        ...

    @overload
    def nation_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = True,
        **kwargs: Any,
    ) -> NationPaginator:
        ...

    def nation_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **kwargs: Any,
    ) -> Union[Tuple[Nation, ...], NationPaginator]:
        data = self._data_query(
            "nations",
            params,
            arg,
            *args,
            **kwargs,
            type_=Nation,
            paginator=paginator,
            is_paginator=True,
            paginator_type=NationPaginator,
        )
        if TYPE_CHECKING:
            if isinstance(data, tuple):
                data = cast(Tuple[Nation, ...], data)
            else:
                data = cast(NationPaginator, data)
        return data

    def trade_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[Trade, ...]:
        data = self._data_query(
            "trades",
            params,
            arg,
            *args,
            **kwargs,
            type_=Trade,
        )
        if TYPE_CHECKING:
            data = cast(Tuple[Trade, ...], data)
        return data

    def trade_price_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[Tradeprice, ...]:
        data = self._data_query(
            "tradeprices",
            params,
            arg,
            *args,
            **kwargs,
            type_=Tradeprice,
        )
        if TYPE_CHECKING:
            data = cast(Tuple[Tradeprice, ...], data)
        return data

    def treasure_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[Treasure, ...]:
        data = self._data_query(
            "treasures",
            params,
            arg,
            *args,
            **kwargs,
            type_=Treasure,
        )
        if TYPE_CHECKING:
            data = cast(Tuple[Treasure, ...], data)
        return data

    def war_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[War, ...]:
        data = self._data_query(
            "wars",
            params,
            arg,
            *args,
            **kwargs,
            type_=War,
        )
        if TYPE_CHECKING:
            data = cast(Tuple[War, ...], data)
        return data
