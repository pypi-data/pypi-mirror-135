import datetime
import json
import logging
import pathlib
import re
import typing
from dataclasses import dataclass, field
from io import BytesIO

import appdirs
import aws_regions.endpoints
import boto3
import pydantic
from diskcache import Cache


def get_regions():
    cache_path = pathlib.Path(appdirs.user_cache_dir(appname="clatmenow"))
    logging.debug(cache_path)

    with Cache(cache_path) as reference:
        result = reference.get("regions")
        if not result:
            logging.debug("set cache")
            _regions = Regions.map_friendly_name()
            col = RegionCollection.from_dict(_regions)
            jsbin = col.json().encode("utf-8")

            expire = datetime.timedelta(days=1)
            reference.set("regions", BytesIO(jsbin), expire=expire.total_seconds())
        else:
            logging.debug("get cache")
            reader = result
            js = reader.read().decode()
            dct = json.loads(js)
            try:
                col = RegionCollection.parse_obj(dct)
            except pydantic.error_wrappers.ValidationError as ex:
                raise ex

        return col.regions


class Region(pydantic.BaseModel):
    name: str
    namefull: str
    namebroad: str
    namespecific: str


class RegionCollection(pydantic.BaseModel):
    regions: typing.List[Region]

    @classmethod
    def _extract_detail_fields(cls, name: str, namefull: str) -> dict:
        pat: typing.Pattern[str] = re.compile(
            f"""
        (?P<broad>[^\(]+)
        \(
        (?P<specific>[^\)]+)
        \)
        """,
            re.VERBOSE,
        )

        mo = pat.search(namefull)
        dct = {
            "name": name,
            "namefull": namefull,
            "namespecific": mo.group("specific").strip(),
            "namebroad": mo.group("broad").strip(),
        }
        return dct

    @classmethod
    def from_dict(cls, dct):
        lst = []
        for short, full in dct.items():
            dct = cls._extract_detail_fields(short, full)
            region = Region(**dct)
            lst.append(region)
        return cls(regions=lst)

    def __iter__(self):
        for region in self.regions:
            yield region


@dataclass
class Regions:
    cache: pathlib.Path = None
    lst: typing.List[Region] = field(init=False, default_factory=list)

    @classmethod
    def map_friendly_name(cls):
        regions = aws_regions.endpoints.get_regions()

        client = boto3.client("ssm", region_name="us-east-1")
        dct = {}
        for region in regions:
            response = client.get_parameter(
                Name=f"/aws/service/global-infrastructure/regions/{region}/longName"
            )

            region_name = response["Parameter"]["Value"]
            dct[region] = region_name

        return dct


def main():
    for region in get_regions():
        print(region)


if __name__ == "__main__":
    main()
