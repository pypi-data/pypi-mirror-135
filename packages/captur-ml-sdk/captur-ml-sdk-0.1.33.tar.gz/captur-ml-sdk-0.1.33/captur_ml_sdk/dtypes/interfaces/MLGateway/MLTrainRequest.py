from pydantic import BaseModel, HttpUrl, validator, root_validator

from typing import Optional, List

from captur_ml_sdk.dtypes.exceptions import InvalidFilePathError
from captur_ml_sdk.dtypes.generics import Image
from captur_ml_sdk.dtypes.interfaces.validators import (
    check_model_exists,
    ensure_file_exists,
    check_images_or_imagesfile_is_included,
    enforce_mutual_exclusivity_between_images_and_imagesfile
)
from captur_ml_sdk.dtypes.utils import get_image_components


class TrainMeta(BaseModel):
    webhooks: Optional[HttpUrl]
    budget_milli_node_hours: Optional[int] = 8000


class BaseMdl(BaseModel):
    name: str
    version: Optional[str] = "HEAD"

    root_validator(check_model_exists)


class Model(BaseModel):
    name: str
    base_model: Optional[BaseMdl]


class Data(BaseModel):
    images: Optional[List[Image]] = None
    imagesfile: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    @ validator('imagesfile')
    def check_imagesfile_has_correct_components(cls, v):
        try:
            get_image_components(v, ".csv")
        except InvalidFilePathError as e:
            raise ValueError(str(e))
        return v

    validator("imagesfile")(ensure_file_exists)

    root_validator(check_images_or_imagesfile_is_included)

    root_validator(enforce_mutual_exclusivity_between_images_and_imagesfile)


class ModelTrainRequest(BaseModel):
    meta: Optional[TrainMeta]
    models: List[Model]
    data: Data
