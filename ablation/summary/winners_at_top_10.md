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

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **NSSAL** |          2 |          1 |        2 |         4 |
| CEL       |          4 |          1 |        2 |         0 |
| **BCEL**  |          1 |          2 |        3 |         3 |
| **SPL**   |          2 |          2 |        3 |         3 |
| MRL       |          1 |          4 |        0 |         0 |


## Investigation of `training_approach`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **sLCWA** |          3 |          6 |        2 |        10 |
| LCWA      |          7 |          4 |        8 |         0 |


## Investigation of `inverse_relations`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **False** |          3 |          2 |        4 |         5 |
| **True**  |          7 |          8 |        6 |         5 |


## Investigation of `model` and `loss`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| **RotatE and NSSAL** |          2 |          1 |        2 |         2 |
| DistMult and CEL     |          1 |          0 |        0 |         0 |
| RotatE and BCEL      |          1 |          0 |        2 |         0 |
| RotatE and CEL       |          1 |          0 |        0 |         0 |
| TuckER and SPL       |          1 |          2 |        0 |         0 |
| RESCAL and CEL       |          1 |          0 |        0 |         0 |
| TransE and CEL       |          1 |          0 |        0 |         0 |
| RotatE and SPL       |          1 |          0 |        2 |         0 |
| TransE and MRL       |          1 |          0 |        0 |         0 |
| TuckER and CEL       |          0 |          1 |        1 |         0 |
| TuckER and MRL       |          0 |          3 |        0 |         0 |
| TuckER and BCEL      |          0 |          1 |        0 |         0 |
| RotatE and MRL       |          0 |          1 |        0 |         0 |
| SimplE and BCEL      |          0 |          1 |        0 |         0 |
| TransE and SPL       |          0 |          0 |        1 |         0 |
| ConvE and CEL        |          0 |          0 |        1 |         0 |
| TransE and BCEL      |          0 |          0 |        1 |         0 |
| ComplEx and BCEL     |          0 |          0 |        0 |         2 |
| ComplEx and SPL      |          0 |          0 |        0 |         2 |
| ComplEx and NSSAL    |          0 |          0 |        0 |         2 |
| ERMLP and SPL        |          0 |          0 |        0 |         1 |
| HolE and BCEL        |          0 |          0 |        0 |         1 |


## Investigation of `model` and `training_approach`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| **RotatE and sLCWA** |          2 |          2 |        2 |         2 |
| DistMult and LCWA    |          1 |          0 |        0 |         0 |
| RotatE and LCWA      |          3 |          0 |        4 |         0 |
| TuckER and LCWA      |          1 |          3 |        1 |         0 |
| RESCAL and LCWA      |          1 |          0 |        0 |         0 |
| TransE and LCWA      |          1 |          0 |        2 |         0 |
| TransE and sLCWA     |          1 |          0 |        0 |         0 |
| TuckER and sLCWA     |          0 |          4 |        0 |         0 |
| SimplE and LCWA      |          0 |          1 |        0 |         0 |
| ConvE and LCWA       |          0 |          0 |        1 |         0 |
| ComplEx and sLCWA    |          0 |          0 |        0 |         6 |
| ERMLP and sLCWA      |          0 |          0 |        0 |         1 |
| HolE and sLCWA       |          0 |          0 |        0 |         1 |


## Investigation of `loss` and `training_approach`

|                     |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|---------------------|------------|------------|----------|-----------|
| **NSSAL and sLCWA** |          2 |          1 |        2 |         4 |
| CEL and LCWA        |          4 |          1 |        2 |         0 |
| BCEL and LCWA       |          1 |          2 |        3 |         0 |
| SPL and LCWA        |          2 |          1 |        3 |         0 |
| MRL and sLCWA       |          1 |          4 |        0 |         0 |
| SPL and sLCWA       |          0 |          1 |        0 |         3 |
| BCEL and sLCWA      |          0 |          0 |        0 |         3 |


## Investigation of `model`, `loss`, and `training_approach`

|                              |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|------------------------------|------------|------------|----------|-----------|
| **RotatE, NSSAL, and sLCWA** |          2 |          1 |        2 |         2 |
| DistMult, CEL, and LCWA      |          1 |          0 |        0 |         0 |
| RotatE, BCEL, and LCWA       |          1 |          0 |        2 |         0 |
| RotatE, CEL, and LCWA        |          1 |          0 |        0 |         0 |
| TuckER, SPL, and LCWA        |          1 |          1 |        0 |         0 |
| RESCAL, CEL, and LCWA        |          1 |          0 |        0 |         0 |
| TransE, CEL, and LCWA        |          1 |          0 |        0 |         0 |
| RotatE, SPL, and LCWA        |          1 |          0 |        2 |         0 |
| TransE, MRL, and sLCWA       |          1 |          0 |        0 |         0 |
| TuckER, CEL, and LCWA        |          0 |          1 |        1 |         0 |
| TuckER, MRL, and sLCWA       |          0 |          3 |        0 |         0 |
| TuckER, BCEL, and LCWA       |          0 |          1 |        0 |         0 |
| RotatE, MRL, and sLCWA       |          0 |          1 |        0 |         0 |
| SimplE, BCEL, and LCWA       |          0 |          1 |        0 |         0 |
| TuckER, SPL, and sLCWA       |          0 |          1 |        0 |         0 |
| TransE, SPL, and LCWA        |          0 |          0 |        1 |         0 |
| ConvE, CEL, and LCWA         |          0 |          0 |        1 |         0 |
| TransE, BCEL, and LCWA       |          0 |          0 |        1 |         0 |
| ComplEx, BCEL, and sLCWA     |          0 |          0 |        0 |         2 |
| ComplEx, SPL, and sLCWA      |          0 |          0 |        0 |         2 |
| ComplEx, NSSAL, and sLCWA    |          0 |          0 |        0 |         2 |
| ERMLP, SPL, and sLCWA        |          0 |          0 |        0 |         1 |
| HolE, BCEL, and sLCWA        |          0 |          0 |        0 |         1 |


