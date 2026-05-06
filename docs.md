# Documentation

## How the model works

The system uses a lightweight image-analysis heuristic to classify soil type using the uploaded soil image. It converts the image to HSV color space and compares average hue, saturation, and brightness to identify common soil categories such as sandy, clay, loamy, peaty, and silty.

Soil properties are then estimated from the predicted soil type, humidity, and temperature values.

## Data flow

1. User uploads a soil image.
2. The image is processed to derive a soil type.
3. Environmental inputs are combined with the soil type.
4. Soil metrics are estimated.
5. Crop recommendations are generated from soil and weather conditions.

## Model limitations

- The soil classifier is heuristic-based, not a trained deep neural network.
- Results are only approximations and meant for demonstration.
- The prototype does not use a real weather API.

## Assumptions

- The uploaded image represents soil ground surface.
- Humidity and temperature values are provided accurately.
- Land size is entered in hectares.
