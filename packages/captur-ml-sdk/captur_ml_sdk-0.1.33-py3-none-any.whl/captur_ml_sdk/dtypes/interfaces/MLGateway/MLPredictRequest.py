from captur_ml_sdk.dtypes.generics import Image
from captur_ml_sdk.dtypes.exceptions import (
    ModelNotFoundError,
    InvalidFilePathError,
    VersionNotFoundError,
    ModelHasNoLiveVersionsError,
)
from captur_ml_sdk.utils import get_image_components

from pydantic import (
    BaseModel, validator, root_validator, HttpUrl
)
from typing import Optional, List


class PredictMeta(BaseModel):
    webhooks: Optional[HttpUrl]


class Data(BaseModel):
    images: Optional[List[Image]] = None
    imagesfile: Optional[str] = None
    labelsfile: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    @validator('imagesfile')
    def check_imagesfile_has_correct_components(cls, v):
        try:
            get_image_components(v, ".jsonl")
        except InvalidFilePathError as e:
            raise ValueError(str(e))
        return v

    @root_validator
    def enforce_mutual_exclusivity_between_images_and_imagesfile(cls, values):
        images = values.get("images")
        imagesfile = values.get("imagesfile")

        if images and imagesfile:
            raise ValueError(
                "Only one of predict:data.images or predict:data.imagesfile"
                "can be used"
            )
        return values


class Model(BaseModel):
    name: str
    version: Optional[str] = "HEAD"

    class Config:
        arbitrary_types_allowed = True


class ModelPredictRequest(BaseModel):
    meta: Optional[PredictMeta] = None
    models: List[Model]
    data: Data
