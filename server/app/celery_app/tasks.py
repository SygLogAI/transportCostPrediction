from model.transport_cost import TransportCost
from .worker import app

@app.task
def train_transport_cost(model_dir):
    TransportCost(model_dir).fit()
