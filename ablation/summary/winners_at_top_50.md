# Investigation of Top 50 Results

This document gives insight into which models, loss functions, etc. are consistently
appearing in the top 50 experiments rated by hits@10 for **all** datasets. The ones that appear in the top 50
experiments for every dataset are shown in **bold** in the index of each table. Note that not all tables
show that there are consistent best performers.

## Investigation of `model`

|             |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-------------|------------|------------|----------|-----------|
| **RotatE**  |          9 |          5 |       13 |         4 |
| DistMult    |          1 |          0 |        6 |         8 |
| TuckER      |          3 |         18 |        7 |         0 |
| RESCAL      |          2 |          0 |        2 |         5 |
| TransE      |         25 |          0 |        6 |         4 |
| KG2E        |          3 |          0 |        3 |         0 |
| **ComplEx** |          1 |          6 |        1 |         8 |
| ERMLP       |          1 |          0 |        0 |         9 |
| HolE        |          1 |          0 |        1 |         6 |
| ProjE       |          2 |          0 |        2 |         0 |
| TransD      |          1 |          0 |        0 |         0 |
| SimplE      |          1 |          9 |        2 |         0 |
| ConvE       |          0 |         12 |        6 |         0 |
| TransH      |          0 |          0 |        1 |         0 |
| ConvKB      |          0 |          0 |        0 |         6 |


## Investigation of `loss`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **NSSAL** |          6 |          7 |        6 |        12 |
| CEL       |         10 |         13 |       17 |         0 |
| **BCEL**  |         10 |         14 |       11 |        12 |
| **SPL**   |         14 |          9 |       11 |        12 |
| **MRL**   |         10 |          7 |        5 |        14 |


## Investigation of `training_approach`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **sLCWA** |         17 |         26 |       17 |        50 |
| LCWA      |         33 |         24 |       33 |         0 |


## Investigation of `inverse_relations`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **False** |         24 |          5 |       26 |        26 |
| **True**  |         26 |         45 |       24 |        24 |


## Investigation of `model` and `loss`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| **RotatE and NSSAL** |          2 |          2 |        2 |         2 |
| DistMult and CEL     |          1 |          0 |        2 |         0 |
| RotatE and BCEL      |          2 |          0 |        4 |         0 |
| RotatE and CEL       |          2 |          1 |        2 |         0 |
| TuckER and SPL       |          1 |          2 |        2 |         0 |
| RESCAL and CEL       |          1 |          0 |        2 |         0 |
| TransE and CEL       |          1 |          0 |        0 |         0 |
| RotatE and SPL       |          2 |          0 |        4 |         0 |
| TransE and MRL       |          8 |          0 |        2 |         2 |
| TransE and SPL       |          8 |          0 |        1 |         0 |
| TuckER and CEL       |          2 |          5 |        2 |         0 |
| RESCAL and BCEL      |          1 |          0 |        0 |         1 |
| KG2E and SPL         |          3 |          0 |        2 |         0 |
| TransE and BCEL      |          4 |          0 |        1 |         0 |
| ComplEx and CEL      |          1 |          3 |        1 |         0 |
| ERMLP and BCEL       |          1 |          0 |        0 |         4 |
| TransE and NSSAL     |          4 |          0 |        2 |         2 |
| HolE and CEL         |          1 |          0 |        1 |         0 |
| ProjE and CEL        |          1 |          0 |        2 |         0 |
| ProjE and BCEL       |          1 |          0 |        0 |         0 |
| TransD and MRL       |          1 |          0 |        0 |         0 |
| **RotatE and MRL**   |          1 |          2 |        1 |         2 |
| SimplE and BCEL      |          1 |          4 |        0 |         0 |
| TuckER and MRL       |          0 |          5 |        1 |         0 |
| TuckER and BCEL      |          0 |          4 |        2 |         0 |
| ConvE and CEL        |          0 |          2 |        2 |         0 |
| ConvE and BCEL       |          0 |          5 |        2 |         0 |
| ComplEx and NSSAL    |          0 |          1 |        0 |         2 |
| TuckER and NSSAL     |          0 |          2 |        0 |         0 |
| ConvE and NSSAL      |          0 |          2 |        0 |         0 |
| SimplE and CEL       |          0 |          2 |        2 |         0 |
| ComplEx and BCEL     |          0 |          1 |        0 |         2 |
| ConvE and SPL        |          0 |          3 |        2 |         0 |
| SimplE and SPL       |          0 |          3 |        0 |         0 |
| ComplEx and SPL      |          0 |          1 |        0 |         2 |
| DistMult and NSSAL   |          0 |          0 |        2 |         2 |
| DistMult and BCEL    |          0 |          0 |        2 |         2 |
| KG2E and CEL         |          0 |          0 |        1 |         0 |
| TransH and MRL       |          0 |          0 |        1 |         0 |
| ERMLP and SPL        |          0 |          0 |        0 |         2 |
| HolE and BCEL        |          0 |          0 |        0 |         2 |
| ConvKB and SPL       |          0 |          0 |        0 |         2 |
| ComplEx and MRL      |          0 |          0 |        0 |         2 |
| ConvKB and BCEL      |          0 |          0 |        0 |         1 |
| HolE and SPL         |          0 |          0 |        0 |         2 |
| RESCAL and SPL       |          0 |          0 |        0 |         2 |
| DistMult and MRL     |          0 |          0 |        0 |         2 |
| DistMult and SPL     |          0 |          0 |        0 |         2 |
| ERMLP and NSSAL      |          0 |          0 |        0 |         2 |
| ConvKB and NSSAL     |          0 |          0 |        0 |         1 |
| ConvKB and MRL       |          0 |          0 |        0 |         2 |
| RESCAL and MRL       |          0 |          0 |        0 |         1 |
| RESCAL and NSSAL     |          0 |          0 |        0 |         1 |
| HolE and MRL         |          0 |          0 |        0 |         2 |
| ERMLP and MRL        |          0 |          0 |        0 |         1 |


## Investigation of `model` and `training_approach`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| **RotatE and sLCWA** |          3 |          4 |        7 |         4 |
| DistMult and LCWA    |          1 |          0 |        2 |         0 |
| RotatE and LCWA      |          6 |          1 |        6 |         0 |
| TuckER and LCWA      |          3 |          7 |        6 |         0 |
| RESCAL and LCWA      |          2 |          0 |        2 |         0 |
| TransE and LCWA      |         13 |          0 |        2 |         0 |
| TransE and sLCWA     |         12 |          0 |        4 |         4 |
| KG2E and LCWA        |          2 |          0 |        3 |         0 |
| ComplEx and LCWA     |          1 |          3 |        1 |         0 |
| ERMLP and LCWA       |          1 |          0 |        0 |         0 |
| HolE and LCWA        |          1 |          0 |        1 |         0 |
| KG2E and sLCWA       |          1 |          0 |        0 |         0 |
| ProjE and LCWA       |          2 |          0 |        2 |         0 |
| TransD and sLCWA     |          1 |          0 |        0 |         0 |
| SimplE and LCWA      |          1 |          3 |        2 |         0 |
| TuckER and sLCWA     |          0 |         11 |        1 |         0 |
| ConvE and LCWA       |          0 |         10 |        6 |         0 |
| ComplEx and sLCWA    |          0 |          3 |        0 |         8 |
| ConvE and sLCWA      |          0 |          2 |        0 |         0 |
| SimplE and sLCWA     |          0 |          6 |        0 |         0 |
| DistMult and sLCWA   |          0 |          0 |        4 |         8 |
| TransH and sLCWA     |          0 |          0 |        1 |         0 |
| ERMLP and sLCWA      |          0 |          0 |        0 |         9 |
| HolE and sLCWA       |          0 |          0 |        0 |         6 |
| ConvKB and sLCWA     |          0 |          0 |        0 |         6 |
| RESCAL and sLCWA     |          0 |          0 |        0 |         5 |


## Investigation of `loss` and `training_approach`

|                     |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|---------------------|------------|------------|----------|-----------|
| **NSSAL and sLCWA** |          6 |          7 |        6 |        12 |
| CEL and LCWA        |         10 |         13 |       17 |         0 |
| BCEL and LCWA       |         10 |          7 |        7 |         0 |
| SPL and LCWA        |         13 |          4 |        9 |         0 |
| **MRL and sLCWA**   |         10 |          7 |        5 |        14 |
| **SPL and sLCWA**   |          1 |          5 |        2 |        12 |
| BCEL and sLCWA      |          0 |          7 |        4 |        12 |


## Investigation of `model`, `loss`, and `training_approach`

|                              |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|------------------------------|------------|------------|----------|-----------|
| **RotatE, NSSAL, and sLCWA** |          2 |          2 |        2 |         2 |
| DistMult, CEL, and LCWA      |          1 |          0 |        2 |         0 |
| RotatE, BCEL, and LCWA       |          2 |          0 |        2 |         0 |
| RotatE, CEL, and LCWA        |          2 |          1 |        2 |         0 |
| TuckER, SPL, and LCWA        |          1 |          1 |        2 |         0 |
| RESCAL, CEL, and LCWA        |          1 |          0 |        2 |         0 |
| TransE, CEL, and LCWA        |          1 |          0 |        0 |         0 |
| RotatE, SPL, and LCWA        |          2 |          0 |        2 |         0 |
| TransE, MRL, and sLCWA       |          8 |          0 |        2 |         2 |
| TransE, SPL, and LCWA        |          8 |          0 |        1 |         0 |
| TuckER, CEL, and LCWA        |          2 |          5 |        2 |         0 |
| RESCAL, BCEL, and LCWA       |          1 |          0 |        0 |         0 |
| KG2E, SPL, and LCWA          |          2 |          0 |        2 |         0 |
| TransE, BCEL, and LCWA       |          4 |          0 |        1 |         0 |
| ComplEx, CEL, and LCWA       |          1 |          3 |        1 |         0 |
| ERMLP, BCEL, and LCWA        |          1 |          0 |        0 |         0 |
| TransE, NSSAL, and sLCWA     |          4 |          0 |        2 |         2 |
| HolE, CEL, and LCWA          |          1 |          0 |        1 |         0 |
| KG2E, SPL, and sLCWA         |          1 |          0 |        0 |         0 |
| ProjE, CEL, and LCWA         |          1 |          0 |        2 |         0 |
| ProjE, BCEL, and LCWA        |          1 |          0 |        0 |         0 |
| TransD, MRL, and sLCWA       |          1 |          0 |        0 |         0 |
| **RotatE, MRL, and sLCWA**   |          1 |          2 |        1 |         2 |
| SimplE, BCEL, and LCWA       |          1 |          1 |        0 |         0 |
| TuckER, MRL, and sLCWA       |          0 |          5 |        1 |         0 |
| TuckER, BCEL, and LCWA       |          0 |          1 |        2 |         0 |
| TuckER, SPL, and sLCWA       |          0 |          1 |        0 |         0 |
| ConvE, CEL, and LCWA         |          0 |          2 |        2 |         0 |
| ConvE, BCEL, and LCWA        |          0 |          5 |        2 |         0 |
| ComplEx, NSSAL, and sLCWA    |          0 |          1 |        0 |         2 |
| TuckER, BCEL, and sLCWA      |          0 |          3 |        0 |         0 |
| TuckER, NSSAL, and sLCWA     |          0 |          2 |        0 |         0 |
| ConvE, NSSAL, and sLCWA      |          0 |          2 |        0 |         0 |
| SimplE, BCEL, and sLCWA      |          0 |          3 |        0 |         0 |
| SimplE, CEL, and LCWA        |          0 |          2 |        2 |         0 |
| ComplEx, BCEL, and sLCWA     |          0 |          1 |        0 |         2 |
| ConvE, SPL, and LCWA         |          0 |          3 |        2 |         0 |
| SimplE, SPL, and sLCWA       |          0 |          3 |        0 |         0 |
| ComplEx, SPL, and sLCWA      |          0 |          1 |        0 |         2 |
| RotatE, SPL, and sLCWA       |          0 |          0 |        2 |         0 |
| RotatE, BCEL, and sLCWA      |          0 |          0 |        2 |         0 |
| DistMult, NSSAL, and sLCWA   |          0 |          0 |        2 |         2 |
| DistMult, BCEL, and sLCWA    |          0 |          0 |        2 |         2 |
| KG2E, CEL, and LCWA          |          0 |          0 |        1 |         0 |
| TransH, MRL, and sLCWA       |          0 |          0 |        1 |         0 |
| ERMLP, SPL, and sLCWA        |          0 |          0 |        0 |         2 |
| HolE, BCEL, and sLCWA        |          0 |          0 |        0 |         2 |
| ERMLP, BCEL, and sLCWA       |          0 |          0 |        0 |         4 |
| ConvKB, SPL, and sLCWA       |          0 |          0 |        0 |         2 |
| ComplEx, MRL, and sLCWA      |          0 |          0 |        0 |         2 |
| ConvKB, BCEL, and sLCWA      |          0 |          0 |        0 |         1 |
| HolE, SPL, and sLCWA         |          0 |          0 |        0 |         2 |
| RESCAL, SPL, and sLCWA       |          0 |          0 |        0 |         2 |
| DistMult, MRL, and sLCWA     |          0 |          0 |        0 |         2 |
| DistMult, SPL, and sLCWA     |          0 |          0 |        0 |         2 |
| ERMLP, NSSAL, and sLCWA      |          0 |          0 |        0 |         2 |
| ConvKB, NSSAL, and sLCWA     |          0 |          0 |        0 |         1 |
| ConvKB, MRL, and sLCWA       |          0 |          0 |        0 |         2 |
| RESCAL, MRL, and sLCWA       |          0 |          0 |        0 |         1 |
| RESCAL, BCEL, and sLCWA      |          0 |          0 |        0 |         1 |
| RESCAL, NSSAL, and sLCWA     |          0 |          0 |        0 |         1 |
| HolE, MRL, and sLCWA         |          0 |          0 |        0 |         2 |
| ERMLP, MRL, and sLCWA        |          0 |          0 |        0 |         1 |


