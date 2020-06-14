# Investigation of Top 10 Results

This document gives insight into which models, loss functions, etc. are consistently
appearing in the top 10 experiments rated by hits@10 for **all** datasets. The ones that appear in the top 10
experiments for every dataset are shown in **bold** in the index of each table. Note that not all tables
show that there are consistent best performers.

## Investigation of `model`

|            |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|------------|------------|------------|----------|-----------|
| **RotatE** |          5 |          2 |        6 |         2 |
| DistMult   |          1 |          0 |        0 |         0 |
| TuckER     |          1 |          7 |        1 |         0 |
| RESCAL     |          1 |          0 |        0 |         0 |
| TransE     |          2 |          0 |        2 |         0 |
| SimplE     |          0 |          1 |        0 |         0 |
| ConvE      |          0 |          0 |        1 |         0 |
| ComplEx    |          0 |          0 |        0 |         6 |
| ERMLP      |          0 |          0 |        0 |         1 |
| HolE       |          0 |          0 |        0 |         1 |


## Investigation of `loss`

|              |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|--------------|------------|------------|----------|-----------|
| **NSSA**     |          2 |          1 |        2 |         4 |
| CE           |          4 |          1 |        2 |         0 |
| **BCE**      |          1 |          2 |        3 |         3 |
| **SoftPlus** |          2 |          2 |        3 |         3 |
| MR           |          1 |          4 |        0 |         0 |


## Investigation of `training_loop`

|         |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|---------|------------|------------|----------|-----------|
| **OWA** |          3 |          6 |        2 |        10 |
| LCWA    |          7 |          4 |        8 |         0 |


## Investigation of `create_inverse_triples`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **False** |          3 |          2 |        4 |         5 |
| **True**  |          7 |          8 |        6 |         5 |


## Investigation of `model` and `loss`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| **RotatE and NSSA**  |          2 |          1 |        2 |         2 |
| DistMult and CE      |          1 |          0 |        0 |         0 |
| RotatE and BCE       |          1 |          0 |        2 |         0 |
| RotatE and CE        |          1 |          0 |        0 |         0 |
| TuckER and SoftPlus  |          1 |          2 |        0 |         0 |
| RESCAL and CE        |          1 |          0 |        0 |         0 |
| TransE and CE        |          1 |          0 |        0 |         0 |
| RotatE and SoftPlus  |          1 |          0 |        2 |         0 |
| TransE and MR        |          1 |          0 |        0 |         0 |
| TuckER and CE        |          0 |          1 |        1 |         0 |
| TuckER and MR        |          0 |          3 |        0 |         0 |
| TuckER and BCE       |          0 |          1 |        0 |         0 |
| RotatE and MR        |          0 |          1 |        0 |         0 |
| SimplE and BCE       |          0 |          1 |        0 |         0 |
| TransE and SoftPlus  |          0 |          0 |        1 |         0 |
| ConvE and CE         |          0 |          0 |        1 |         0 |
| TransE and BCE       |          0 |          0 |        1 |         0 |
| ComplEx and BCE      |          0 |          0 |        0 |         2 |
| ComplEx and SoftPlus |          0 |          0 |        0 |         2 |
| ComplEx and NSSA     |          0 |          0 |        0 |         2 |
| ERMLP and SoftPlus   |          0 |          0 |        0 |         1 |
| HolE and BCE         |          0 |          0 |        0 |         1 |


## Investigation of `model` and `training_loop`

|                    |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|--------------------|------------|------------|----------|-----------|
| **RotatE and OWA** |          2 |          2 |        2 |         2 |
| DistMult and LCWA  |          1 |          0 |        0 |         0 |
| RotatE and LCWA    |          3 |          0 |        4 |         0 |
| TuckER and LCWA    |          1 |          3 |        1 |         0 |
| RESCAL and LCWA    |          1 |          0 |        0 |         0 |
| TransE and LCWA    |          1 |          0 |        2 |         0 |
| TransE and OWA     |          1 |          0 |        0 |         0 |
| TuckER and OWA     |          0 |          4 |        0 |         0 |
| SimplE and LCWA    |          0 |          1 |        0 |         0 |
| ConvE and LCWA     |          0 |          0 |        1 |         0 |
| ComplEx and OWA    |          0 |          0 |        0 |         6 |
| ERMLP and OWA      |          0 |          0 |        0 |         1 |
| HolE and OWA       |          0 |          0 |        0 |         1 |


## Investigation of `loss` and `training_loop`

|                   |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-------------------|------------|------------|----------|-----------|
| **NSSA and OWA**  |          2 |          1 |        2 |         4 |
| CE and LCWA       |          4 |          1 |        2 |         0 |
| BCE and LCWA      |          1 |          2 |        3 |         0 |
| SoftPlus and LCWA |          2 |          1 |        3 |         0 |
| MR and OWA        |          1 |          4 |        0 |         0 |
| SoftPlus and OWA  |          0 |          1 |        0 |         3 |
| BCE and OWA       |          0 |          0 |        0 |         3 |


## Investigation of `model`, `loss`, and `training_loop`

|                            |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------------|------------|------------|----------|-----------|
| **RotatE, NSSA, and OWA**  |          2 |          1 |        2 |         2 |
| DistMult, CE, and LCWA     |          1 |          0 |        0 |         0 |
| RotatE, BCE, and LCWA      |          1 |          0 |        2 |         0 |
| RotatE, CE, and LCWA       |          1 |          0 |        0 |         0 |
| TuckER, SoftPlus, and LCWA |          1 |          1 |        0 |         0 |
| RESCAL, CE, and LCWA       |          1 |          0 |        0 |         0 |
| TransE, CE, and LCWA       |          1 |          0 |        0 |         0 |
| RotatE, SoftPlus, and LCWA |          1 |          0 |        2 |         0 |
| TransE, MR, and OWA        |          1 |          0 |        0 |         0 |
| TuckER, CE, and LCWA       |          0 |          1 |        1 |         0 |
| TuckER, MR, and OWA        |          0 |          3 |        0 |         0 |
| TuckER, BCE, and LCWA      |          0 |          1 |        0 |         0 |
| RotatE, MR, and OWA        |          0 |          1 |        0 |         0 |
| SimplE, BCE, and LCWA      |          0 |          1 |        0 |         0 |
| TuckER, SoftPlus, and OWA  |          0 |          1 |        0 |         0 |
| TransE, SoftPlus, and LCWA |          0 |          0 |        1 |         0 |
| ConvE, CE, and LCWA        |          0 |          0 |        1 |         0 |
| TransE, BCE, and LCWA      |          0 |          0 |        1 |         0 |
| ComplEx, BCE, and OWA      |          0 |          0 |        0 |         2 |
| ComplEx, SoftPlus, and OWA |          0 |          0 |        0 |         2 |
| ComplEx, NSSA, and OWA     |          0 |          0 |        0 |         2 |
| ERMLP, SoftPlus, and OWA   |          0 |          0 |        0 |         1 |
| HolE, BCE, and OWA         |          0 |          0 |        0 |         1 |


