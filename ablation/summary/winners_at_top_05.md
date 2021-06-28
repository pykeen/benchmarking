# Investigation of Top 5 Results

This document gives insight into which models, loss functions, etc. are consistently
appearing in the top 5 experiments rated by hits@10 for **all** datasets. The ones that appear in the top 5
experiments for every dataset are shown in **bold** in the index of each table. Note that not all tables
show that there are consistent best performers.

## Investigation of `model`

|            |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|------------|------------|------------|----------|-----------|
| TuckER     |          3 |          1 |        0 |         0 |
| **RotatE** |          1 |          3 |        5 |         1 |
| ConvE      |          1 |          1 |        0 |         0 |
| MuRE       |          0 |          0 |        0 |         3 |
| ComplEx    |          0 |          0 |        0 |         1 |


## Investigation of `loss`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| BCEL      |          2 |          0 |        2 |         2 |
| **SPL**   |          1 |          1 |        2 |         2 |
| CEL       |          1 |          0 |        0 |         0 |
| **NSSAL** |          1 |          3 |        1 |         1 |
| MRL       |          0 |          1 |        0 |         0 |


## Investigation of `training_approach`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| LCWA      |          4 |          1 |        4 |         0 |
| **sLCWA** |          1 |          4 |        1 |         5 |


## Investigation of `inverse_relations`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **True**  |          4 |          4 |        2 |         3 |
| **False** |          1 |          1 |        3 |         2 |


## Investigation of `model` and `loss`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| TuckER and BCEL      |          1 |          0 |        0 |         0 |
| TuckER and SPL       |          1 |          1 |        0 |         0 |
| TuckER and CEL       |          1 |          0 |        0 |         0 |
| **RotatE and NSSAL** |          1 |          2 |        1 |         1 |
| ConvE and BCEL       |          1 |          0 |        0 |         0 |
| ConvE and NSSAL      |          0 |          1 |        0 |         0 |
| RotatE and MRL       |          0 |          1 |        0 |         0 |
| RotatE and BCEL      |          0 |          0 |        2 |         0 |
| RotatE and SPL       |          0 |          0 |        2 |         0 |
| MuRE and SPL         |          0 |          0 |        0 |         2 |
| MuRE and BCEL        |          0 |          0 |        0 |         1 |
| ComplEx and BCEL     |          0 |          0 |        0 |         1 |


## Investigation of `model` and `training_approach`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| TuckER and LCWA      |          3 |          1 |        0 |         0 |
| **RotatE and sLCWA** |          1 |          3 |        1 |         1 |
| ConvE and LCWA       |          1 |          0 |        0 |         0 |
| ConvE and sLCWA      |          0 |          1 |        0 |         0 |
| RotatE and LCWA      |          0 |          0 |        4 |         0 |
| MuRE and sLCWA       |          0 |          0 |        0 |         3 |
| ComplEx and sLCWA    |          0 |          0 |        0 |         1 |


## Investigation of `loss` and `training_approach`

|                     |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|---------------------|------------|------------|----------|-----------|
| BCEL and LCWA       |          2 |          0 |        2 |         0 |
| SPL and LCWA        |          1 |          1 |        2 |         0 |
| CEL and LCWA        |          1 |          0 |        0 |         0 |
| **NSSAL and sLCWA** |          1 |          3 |        1 |         1 |
| MRL and sLCWA       |          0 |          1 |        0 |         0 |
| SPL and sLCWA       |          0 |          0 |        0 |         2 |
| BCEL and sLCWA      |          0 |          0 |        0 |         2 |


## Investigation of `model`, `loss`, and `training_approach`

|                              |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|------------------------------|------------|------------|----------|-----------|
| TuckER, BCEL, and LCWA       |          1 |          0 |        0 |         0 |
| TuckER, SPL, and LCWA        |          1 |          1 |        0 |         0 |
| TuckER, CEL, and LCWA        |          1 |          0 |        0 |         0 |
| **RotatE, NSSAL, and sLCWA** |          1 |          2 |        1 |         1 |
| ConvE, BCEL, and LCWA        |          1 |          0 |        0 |         0 |
| ConvE, NSSAL, and sLCWA      |          0 |          1 |        0 |         0 |
| RotatE, MRL, and sLCWA       |          0 |          1 |        0 |         0 |
| RotatE, BCEL, and LCWA       |          0 |          0 |        2 |         0 |
| RotatE, SPL, and LCWA        |          0 |          0 |        2 |         0 |
| MuRE, SPL, and sLCWA         |          0 |          0 |        0 |         2 |
| MuRE, BCEL, and sLCWA        |          0 |          0 |        0 |         1 |
| ComplEx, BCEL, and sLCWA     |          0 |          0 |        0 |         1 |


