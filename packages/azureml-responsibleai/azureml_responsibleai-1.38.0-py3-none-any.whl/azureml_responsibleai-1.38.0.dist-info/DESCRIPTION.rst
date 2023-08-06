Microsoft Azure Machine Learning Responsible AI for Python
==========================================================

This package has been tested with Python 3.6 and 3.7.
=====================================================


The azureml-responsibleai package provides classes for Responsible AI in Azure Machine Learning and includes the following:

- Model explanations including aggregate and individual feature importance.
- Causal inference, estimates the causal effect each feature has on the outcome and recommends a policy for when to apply treatments in order to optimize the outcome.
- Counterfactual analysis, generates diverse counterfactual examples of existing datapoints to achieve a desired model output.
- Error analysis, a more robust analysis of a model's performance by identifying which cohorts of your data have disproportionately higher error rate.  For example, a cohort of your data specifying gender or race.

This package is experimental and may be subject to future change or removal.

*****************
Setup
*****************

Follow these `instructions <https://docs.microsoft.com/azure/machine-learning/how-to-configure-environment#local>`_ to install the Azure ML SDK on your local machine, create an Azure ML workspace, and set up your notebook environment, which is required for the next step.
Once you have set up your environment, install the AzureML Responsible AI package:

.. code-block:: python

   pip install azureml-responsibleai




