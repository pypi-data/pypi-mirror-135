# AIGrammar

## About
AIGrammar is all in one and easy to use package for model diagnostic and vulnerability checks. It enable with a simple line of code to check model metrics and prediction generalizability, feature contribution, and model vulnerability against adversarial attacks. 

**Data**
- Multicollinearity
- Data drift

**Model**
- Metric metric comparison
  - roc_auc vs average precision
- Optimal threshold vs 50% threshold

**Feature importance**
- Too high importance
- 0 impact
- Negative influence (FLOFO)
- Causes of overfitting

**Adversarial Attack**
- Model vulnerability identification based on one feature minimal change for getting opposite outcome.


**Usage**
Python 3.7+ required.
Installation: ``pip install AIGrammar``

Example:
``` from AIGrammar import AIGrammar
aig = AIGrammar(train, test, model, target_name)
aig.measure_all(X0_shap_values, X1_shap_values)

print(aig.diagnosis)
print(aig.warnings)
```


