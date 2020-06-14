# Investigation of Top 5 Results

This document gives insight into which models, loss functions, etc. are consistently
appearing in the top 5 experiments rated by hits@10 for **all** datasets. The ones that appear in the top 5
experiments for every dataset are shown in **bold** in the index of each table. Note that not all tables
show that there are consistent best performers.

## Investigation of `model`

|            |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|------------|------------|------------|----------|-----------|
| **RotatE** |          4 |          1 |        5 |         1 |
| DistMult   |          1 |          0 |        0 |         0 |
| TuckER     |          0 |          4 |        0 |         0 |
| ComplEx    |          0 |          0 |        0 |         4 |


## Investigation of `loss`

|          |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------|------------|------------|----------|-----------|
| NSSA     |          2 |          0 |        1 |         2 |
| CE       |          2 |          1 |        0 |         0 |
| **BCE**  |          1 |          1 |        2 |         1 |
| SoftPlus |          0 |          1 |        2 |         2 |
| MR       |          0 |          2 |        0 |         0 |


## Investigation of `training_loop`

|         |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|---------|------------|------------|----------|-----------|
| **OWA** |          2 |          2 |        1 |         5 |
| LCWA    |          3 |          3 |        4 |         0 |


## Investigation of `create_inverse_triples`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **False** |          2 |          1 |        2 |         2 |
| **True**  |          3 |          4 |        3 |         3 |


## Investigation of `model-loss`

|                  |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|------------------|------------|------------|----------|-----------|
| RotatE_NSSA      |          2 |          0 |        1 |         1 |
| DistMult_CE      |          1 |          0 |        0 |         0 |
| RotatE_BCE       |          1 |          0 |        2 |         0 |
| RotatE_CE        |          1 |          0 |        0 |         0 |
| TuckER_SoftPlus  |          0 |          1 |        0 |         0 |
| TuckER_CE        |          0 |          1 |        0 |         0 |
| TuckER_MR        |          0 |          1 |        0 |         0 |
| TuckER_BCE       |          0 |          1 |        0 |         0 |
| RotatE_MR        |          0 |          1 |        0 |         0 |
| RotatE_SoftPlus  |          0 |          0 |        2 |         0 |
| ComplEx_BCE      |          0 |          0 |        0 |         1 |
| ComplEx_SoftPlus |          0 |          0 |        0 |         2 |
| ComplEx_NSSA     |          0 |          0 |        0 |         1 |


## Investigation of `model-training_loop`

|                |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------|------------|------------|----------|-----------|
| **RotatE_OWA** |          2 |          1 |        1 |         1 |
| DistMult_LCWA  |          1 |          0 |        0 |         0 |
| RotatE_LCWA    |          2 |          0 |        4 |         0 |
| TuckER_LCWA    |          0 |          3 |        0 |         0 |
| TuckER_OWA     |          0 |          1 |        0 |         0 |
| ComplEx_OWA    |          0 |          0 |        0 |         4 |


## Investigation of `loss-training_loop`

|               |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|---------------|------------|------------|----------|-----------|
| NSSA_OWA      |          2 |          0 |        1 |         2 |
| CE_LCWA       |          2 |          1 |        0 |         0 |
| BCE_LCWA      |          1 |          1 |        2 |         0 |
| SoftPlus_LCWA |          0 |          1 |        2 |         0 |
| MR_OWA        |          0 |          2 |        0 |         0 |
| BCE_OWA       |          0 |          0 |        0 |         1 |
| SoftPlus_OWA  |          0 |          0 |        0 |         2 |


## Investigation of `model-loss-training_loop`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| RotatE_NSSA_OWA      |          2 |          0 |        1 |         1 |
| DistMult_CE_LCWA     |          1 |          0 |        0 |         0 |
| RotatE_BCE_LCWA      |          1 |          0 |        2 |         0 |
| RotatE_CE_LCWA       |          1 |          0 |        0 |         0 |
| TuckER_SoftPlus_LCWA |          0 |          1 |        0 |         0 |
| TuckER_CE_LCWA       |          0 |          1 |        0 |         0 |
| TuckER_MR_OWA        |          0 |          1 |        0 |         0 |
| TuckER_BCE_LCWA      |          0 |          1 |        0 |         0 |
| RotatE_MR_OWA        |          0 |          1 |        0 |         0 |
| RotatE_SoftPlus_LCWA |          0 |          0 |        2 |         0 |
| ComplEx_BCE_OWA      |          0 |          0 |        0 |         1 |
| ComplEx_SoftPlus_OWA |          0 |          0 |        0 |         2 |
| ComplEx_NSSA_OWA     |          0 |          0 |        0 |         1 |


