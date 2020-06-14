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


## Investigation of `model` and `loss`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| RotatE and NSSA      |          2 |          0 |        1 |         1 |
| DistMult and CE      |          1 |          0 |        0 |         0 |
| RotatE and BCE       |          1 |          0 |        2 |         0 |
| RotatE and CE        |          1 |          0 |        0 |         0 |
| TuckER and SoftPlus  |          0 |          1 |        0 |         0 |
| TuckER and CE        |          0 |          1 |        0 |         0 |
| TuckER and MR        |          0 |          1 |        0 |         0 |
| TuckER and BCE       |          0 |          1 |        0 |         0 |
| RotatE and MR        |          0 |          1 |        0 |         0 |
| RotatE and SoftPlus  |          0 |          0 |        2 |         0 |
| ComplEx and BCE      |          0 |          0 |        0 |         1 |
| ComplEx and SoftPlus |          0 |          0 |        0 |         2 |
| ComplEx and NSSA     |          0 |          0 |        0 |         1 |


## Investigation of `model` and `training_loop`

|                    |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|--------------------|------------|------------|----------|-----------|
| **RotatE and OWA** |          2 |          1 |        1 |         1 |
| DistMult and LCWA  |          1 |          0 |        0 |         0 |
| RotatE and LCWA    |          2 |          0 |        4 |         0 |
| TuckER and LCWA    |          0 |          3 |        0 |         0 |
| TuckER and OWA     |          0 |          1 |        0 |         0 |
| ComplEx and OWA    |          0 |          0 |        0 |         4 |


## Investigation of `loss` and `training_loop`

|                   |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-------------------|------------|------------|----------|-----------|
| NSSA and OWA      |          2 |          0 |        1 |         2 |
| CE and LCWA       |          2 |          1 |        0 |         0 |
| BCE and LCWA      |          1 |          1 |        2 |         0 |
| SoftPlus and LCWA |          0 |          1 |        2 |         0 |
| MR and OWA        |          0 |          2 |        0 |         0 |
| BCE and OWA       |          0 |          0 |        0 |         1 |
| SoftPlus and OWA  |          0 |          0 |        0 |         2 |


## Investigation of `model`, `loss`, and `training_loop`

|                            |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------------|------------|------------|----------|-----------|
| RotatE, NSSA, and OWA      |          2 |          0 |        1 |         1 |
| DistMult, CE, and LCWA     |          1 |          0 |        0 |         0 |
| RotatE, BCE, and LCWA      |          1 |          0 |        2 |         0 |
| RotatE, CE, and LCWA       |          1 |          0 |        0 |         0 |
| TuckER, SoftPlus, and LCWA |          0 |          1 |        0 |         0 |
| TuckER, CE, and LCWA       |          0 |          1 |        0 |         0 |
| TuckER, MR, and OWA        |          0 |          1 |        0 |         0 |
| TuckER, BCE, and LCWA      |          0 |          1 |        0 |         0 |
| RotatE, MR, and OWA        |          0 |          1 |        0 |         0 |
| RotatE, SoftPlus, and LCWA |          0 |          0 |        2 |         0 |
| ComplEx, BCE, and OWA      |          0 |          0 |        0 |         1 |
| ComplEx, SoftPlus, and OWA |          0 |          0 |        0 |         2 |
| ComplEx, NSSA, and OWA     |          0 |          0 |        0 |         1 |


