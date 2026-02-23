# EconML

After completing my Ph.D. defense, I began to reflect on a fundamental question:

What is the true meaning of dedicating years to time-series forecasting and modeling research?

How can what we study in academia be translated vertically into real industrial impact?

In recent years, the field of time-series forecasting seems to have entered a peculiar loop. Many researchers are overwhelmingly focused on reducing loss values. If a model achieves slightly lower error than previous methods, it is declared state-of-the-art. To achieve this, increasingly complex attention mechanisms are designed, computational costs are escalated, and sometimes questionable model architectures or experimental settings are justified solely because they reduce loss.

But does this truly matter?

## Industrial Financial Time-Series Forecasting Projects

This project includes three parts:

1. [data_pipeline](data_pipeline)
2. model_pipeline
3. evaluation

Each part has its own README.

## About the main.py (Coming soon)

'''bash
python3 main.py
'''

A unified main.py orchestrates the entire workflow, connecting the data pipeline, model pipeline, and evaluation module.
Users can flexibly choose the dataset (e.g., SPX or N225), the model, and the task type (prediction or anomaly detection), with automated evaluation performed at the end of the process.
