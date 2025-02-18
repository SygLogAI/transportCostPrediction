from model.transport_cost import TransportCost
from fastapi import APIRouter, Depends
import celery_app.tasks
from pydantic import BaseModel
from typing import List
import uuid
import pandas as pd
import pathlib
import numpy as np
from dependencies import model_path

MODEL_NAME = "transport_cost"

router = APIRouter()

class TransportTraningDataset(BaseModel):
    distances: List[float]
    time_periods: List[float]
    costs: List[float]

class FitResponse(BaseModel):
    model_id: str

@router.post("/transport_cost/fit")
async def fit_transport_cost(dataset: TransportTraningDataset):
    model_id = str(uuid.uuid4())
    model_dir = model_path(MODEL_NAME, model_id)

    pathlib.Path(model_dir).mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame({
            "distance": dataset.distances,
            "time_period": dataset.time_periods,
            "target": dataset.costs
        })

    TransportCost(model_dir).save_training_data(df)

    celery_app.tasks.train_transport_cost.delay(model_dir)

    return FitResponse(model_id=model_id)

class TransportPredictParams(BaseModel):
    model_id: str
    distances: List[float]
    time_periods: List[float]

class PredictResponse(BaseModel):
    costs: List[float]

@router.post("/transport_cost/predict", response_model=PredictResponse)
async def fit_transport_cost(params: TransportPredictParams):
    pred = TransportCost(model_path(MODEL_NAME, params.model_id)).predict(np.array([params.distances, params.time_periods]).T)

    return PredictResponse(costs=list(pred))
    
class StatusResponse(BaseModel):
    status: str

@router.get("/transport_cost/status", response_model=StatusResponse)
async def fit_transport_cost(model_id: str):
    status = TransportCost(model_path(MODEL_NAME, model_id)).status()

    return StatusResponse(status=status["status"])