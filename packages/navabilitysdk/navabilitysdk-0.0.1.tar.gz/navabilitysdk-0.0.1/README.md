# NavAbilitySDK.py
Access NavAbility Cloud factor graph features from Python.

# Installation

Create a Python 3 virtual environment in the folder `venv`:

```bash
python3 -m venv venv
```

Activate the environment:

```bash
source ./venv/bin/activate
```

Install the NavAbilitySDK:

```bash
pip install wheel
pip install git+ssh://git@github.com/NavAbility/NavAbilitySDK.py.git
```

# Example

This script will create variables and factors, and demonstrate how to check the status one the way:

```python
import time
from navability.entities.Variable import Variable
from navability.entities.Factor import Factor, FactorPrior
from navability.entities.StatusMessage import StatusMessage
from navability.services.NavAbilityClient import NavAbilityClient
from pprint import pprint

navi = NavAbilityClient()
result = navi.addVariable(Variable("x0", "Pose2"))
time.sleep(1)
statuses = navi.getStatusMessages(result['addVariable'])
pprint(statuses)
result = navi.addVariable(Variable("x1", "Pose2"))
time.sleep(1)
statuses = navi.getStatusMessages(result['addVariable'])
pprint(statuses)

# Add a prior
result = navi.addFactor(FactorPrior("x0f1", "PriorPose2", ["x0"]))
time.sleep(1)
statuses = navi.getStatusMessages(result['addFactor'])
pprint(statuses)

# Add a factor
result = navi.addFactor(Factor("x0x1f1", "Pose2Pose2", ["x0", "x1"]))
time.sleep(1)
statuses = navi.getStatusMessages(result['addFactor'])
pprint(statuses)

# WIP
result = navi.solveSession()
```
