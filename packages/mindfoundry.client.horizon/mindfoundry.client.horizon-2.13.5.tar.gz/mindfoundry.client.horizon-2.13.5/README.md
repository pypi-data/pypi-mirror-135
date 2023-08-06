# Mind Foundry Horizon Client

This package contains a python client that can be used to interact with an instance of Mind Foundry Horizon. The client exposes a familiar interface that allows you to tackle forecasting problems with ease.

```python
from mindfoundry.client.horizon import Connection
from mindfoundry.client.horizon.models import HorizonForecaster

# Generate an API key in the Horizon dashboard
connection = Connection(
    base_url="your Horizon instance",
    api_key="your api key",
)

# Create a new forecasting model. See the complete documentation
# for a more in-depth explanation of each argument.
model = HorizonForecaster(
    connection=connection,
    name="My Forecaster",
    targets=["target1", "target2", ...],
    horizons=[1, 2, 3],
    refinement=False,
)

# Train a model on some training data (a pandas dataframe)
model.fit(training_data)

# Make a prediction on new data
prediction = model.predict(new_data)
print(prediction.as_df().head())

# Save the model for later use
model.save("/path/to/model/file")

# Re-load the model
model = HorizonForecaster.load("/path/to/model/file", connection=connection)

# The model can be updated with new data in the same format
model.update(new_data_2)
new_prediction = model.predict()
```
