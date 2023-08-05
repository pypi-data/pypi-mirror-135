from pydantic import BaseModel
from typing import Optional

from MLMetaRequest import ModelMetaRequest
from MLPredictRequest import ModelPredictRequest
from MLTrainRequest import ModelTrainRequest
from MLEvalRequest import ModelEvaluateRequest


class MLGatewayRequest(BaseModel):
    meta: Optional[ModelMetaRequest]
    predict: Optional[ModelPredictRequest]
    train: Optional[ModelTrainRequest]
    evaluate: Optional[ModelEvaluateRequest]


if __name__ == "__main__":
    print(MLGatewayRequest.schema_json(indent=2))
