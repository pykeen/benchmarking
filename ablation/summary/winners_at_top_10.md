# Investigation of Top 10 Results

This document gives insight into which models, loss functions, etc. are consistently
appearing in the top 10 experiments rated by hits@10 for **all** datasets. The ones that appear in the top 10
experiments for every dataset are shown in **bold** in the index of each table. Note that not all tables
show that there are consistent best performers.

## Investigation of `model`

|            |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|------------|------------|------------|----------|-----------|
| TuckER     |          3 |          4 |        0 |         0 |
| **RotatE** |          4 |          3 |        6 |         2 |
| ConvE      |          1 |          2 |        0 |         0 |
| DistMult   |          1 |          0 |        0 |         0 |
| MuRE       |          1 |          0 |        3 |         3 |
| ComplEx    |          0 |          1 |        0 |         5 |
| TransE     |          0 |          0 |        1 |         0 |


## Investigation of `loss`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **BCEL**  |          4 |          2 |        3 |         2 |
| **SPL**   |          1 |          2 |        5 |         4 |
| CEL       |          3 |          2 |        0 |         0 |
| **NSSAL** |          2 |          3 |        2 |         4 |
| MRL       |          0 |          1 |        0 |         0 |


## Investigation of `training_approach`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| LCWA      |          8 |          6 |        6 |         0 |
| **sLCWA** |          2 |          4 |        4 |        10 |


## Investigation of `inverse_relations`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **True**  |          8 |          9 |        5 |         5 |
| **False** |          2 |          1 |        5 |         5 |


## Investigation of `model` and `loss`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| TuckER and BCEL      |          1 |          1 |        0 |         0 |
| TuckER and SPL       |          1 |          2 |        0 |         0 |
| TuckER and CEL       |          1 |          1 |        0 |         0 |
| **RotatE and NSSAL** |          2 |          2 |        2 |         2 |
| ConvE and BCEL       |          1 |          1 |        0 |         0 |
| RotatE and BCEL      |          1 |          0 |        2 |         0 |
| DistMult and CEL     |          1 |          0 |        0 |         0 |
| MuRE and BCEL        |          1 |          0 |        1 |         1 |
| RotatE and CEL       |          1 |          0 |        0 |         0 |
| ConvE and NSSAL      |          0 |          1 |        0 |         0 |
| RotatE and MRL       |          0 |          1 |        0 |         0 |
| ComplEx and CEL      |          0 |          1 |        0 |         0 |
| RotatE and SPL       |          0 |          0 |        2 |         0 |
| MuRE and SPL         |          0 |          0 |        2 |         2 |
| TransE and SPL       |          0 |          0 |        1 |         0 |
| ComplEx and BCEL     |          0 |          0 |        0 |         1 |
| ComplEx and SPL      |          0 |          0 |        0 |         2 |
| ComplEx and NSSAL    |          0 |          0 |        0 |         2 |


## Investigation of `model` and `training_approach`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| TuckER and LCWA      |          3 |          4 |        0 |         0 |
| **RotatE and sLCWA** |          2 |          3 |        2 |         2 |
| ConvE and LCWA       |          1 |          1 |        0 |         0 |
| RotatE and LCWA      |          2 |          0 |        4 |         0 |
| DistMult and LCWA    |          1 |          0 |        0 |         0 |
| MuRE and LCWA        |          1 |          0 |        1 |         0 |
| ConvE and sLCWA      |          0 |          1 |        0 |         0 |
| ComplEx and LCWA     |          0 |          1 |        0 |         0 |
| MuRE and sLCWA       |          0 |          0 |        2 |         3 |
| TransE and LCWA      |          0 |          0 |        1 |         0 |
| ComplEx and sLCWA    |          0 |          0 |        0 |         5 |


## Investigation of `loss` and `training_approach`

|                     |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|---------------------|------------|------------|----------|-----------|
| BCEL and LCWA       |          4 |          2 |        2 |         0 |
| SPL and LCWA        |          1 |          2 |        4 |         0 |
| CEL and LCWA        |          3 |          2 |        0 |         0 |
| **NSSAL and sLCWA** |          2 |          3 |        2 |         4 |
| MRL and sLCWA       |          0 |          1 |        0 |         0 |
| BCEL and sLCWA      |          0 |          0 |        1 |         2 |
| SPL and sLCWA       |          0 |          0 |        1 |         4 |


## Investigation of `model`, `loss`, and `training_approach`

|                              |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|------------------------------|------------|------------|----------|-----------|
| TuckER, BCEL, and LCWA       |          1 |          1 |        0 |         0 |
| TuckER, SPL, and LCWA        |          1 |          2 |        0 |         0 |
| TuckER, CEL, and LCWA        |          1 |          1 |        0 |         0 |
| **RotatE, NSSAL, and sLCWA** |          2 |          2 |        2 |         2 |
| ConvE, BCEL, and LCWA        |          1 |          1 |        0 |         0 |
| RotatE, BCEL, and LCWA       |          1 |          0 |        2 |         0 |
| DistMult, CEL, and LCWA      |          1 |          0 |        0 |         0 |
| MuRE, BCEL, and LCWA         |          1 |          0 |        0 |         0 |
| RotatE, CEL, and LCWA        |          1 |          0 |        0 |         0 |
| ConvE, NSSAL, and sLCWA      |          0 |          1 |        0 |         0 |
| RotatE, MRL, and sLCWA       |          0 |          1 |        0 |         0 |
| ComplEx, CEL, and LCWA       |          0 |          1 |        0 |         0 |
| RotatE, SPL, and LCWA        |          0 |          0 |        2 |         0 |
| MuRE, SPL, and LCWA          |          0 |          0 |        1 |         0 |
| MuRE, BCEL, and sLCWA        |          0 |          0 |        1 |         1 |
| TransE, SPL, and LCWA        |          0 |          0 |        1 |         0 |
| MuRE, SPL, and sLCWA         |          0 |          0 |        1 |         2 |
| ComplEx, BCEL, and sLCWA     |          0 |          0 |        0 |         1 |
| ComplEx, SPL, and sLCWA      |          0 |          0 |        0 |         2 |
| ComplEx, NSSAL, and sLCWA    |          0 |          0 |        0 |         2 |


