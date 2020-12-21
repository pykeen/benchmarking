# Investigation of Top 50 Results

This document gives insight into which models, loss functions, etc. are consistently
appearing in the top 50 experiments rated by hits@10 for **all** datasets. The ones that appear in the top 50
experiments for every dataset are shown in **bold** in the index of each table. Note that not all tables
show that there are consistent best performers.

## Investigation of `model`

|             |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-------------|------------|------------|----------|-----------|
| **RotatE**  |         10 |          8 |       13 |         4 |
| DistMult    |          6 |          0 |        7 |         7 |
| TuckER      |          5 |         15 |        7 |         0 |
| **RESCAL**  |          2 |          1 |        2 |         6 |
| TransE      |          9 |          0 |        6 |         3 |
| KG2E        |          5 |          0 |        3 |         0 |
| ERMLP       |          3 |          0 |        0 |         8 |
| **ComplEx** |          2 |         11 |        1 |         8 |
| HolE        |          3 |          0 |        1 |         6 |
| ProjE       |          2 |          0 |        2 |         0 |
| TransD      |          1 |          0 |        0 |         0 |
| SimplE      |          1 |          7 |        2 |         0 |
| TransR      |          1 |          0 |        0 |         0 |
| ConvE       |          0 |          6 |        6 |         0 |
| SE          |          0 |          2 |        0 |         0 |
| ConvKB      |          0 |          0 |        0 |         8 |


## Investigation of `loss`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **NSSAL** |          4 |          8 |        6 |        13 |
| CEL       |         16 |         10 |       17 |         0 |
| **BCEL**  |         11 |         15 |       11 |        13 |
| **SPL**   |         13 |         11 |       11 |        12 |
| **MRL**   |          6 |          6 |        5 |        12 |


## Investigation of `training_approach`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **sLCWA** |         13 |         31 |       17 |        50 |
| LCWA      |         37 |         19 |       33 |         0 |


## Investigation of `inverse_relations`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **False** |         18 |         17 |       26 |        24 |
| **True**  |         32 |         33 |       24 |        26 |


## Investigation of `model` and `loss`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| **RotatE and NSSAL** |          2 |          2 |        2 |         2 |
| DistMult and CEL     |          2 |          0 |        2 |         0 |
| RotatE and BCEL      |          2 |          1 |        4 |         0 |
| RotatE and CEL       |          2 |          2 |        2 |         0 |
| TuckER and SPL       |          2 |          3 |        2 |         0 |
| RESCAL and CEL       |          1 |          0 |        2 |         0 |
| RotatE and SPL       |          3 |          0 |        4 |         0 |
| TransE and CEL       |          1 |          0 |        0 |         0 |
| TransE and MRL       |          2 |          0 |        2 |         2 |
| RESCAL and BCEL      |          1 |          0 |        0 |         1 |
| TransE and SPL       |          2 |          0 |        1 |         0 |
| TuckER and CEL       |          2 |          2 |        2 |         0 |
| KG2E and SPL         |          4 |          0 |        2 |         0 |
| ERMLP and BCEL       |          1 |          0 |        0 |         4 |
| TransE and BCEL      |          2 |          0 |        1 |         0 |
| ComplEx and CEL      |          2 |          2 |        1 |         0 |
| **RotatE and MRL**   |          1 |          3 |        1 |         2 |
| TransE and NSSAL     |          2 |          0 |        2 |         1 |
| HolE and CEL         |          1 |          0 |        1 |         0 |
| TuckER and BCEL      |          1 |          6 |        2 |         0 |
| ProjE and CEL        |          1 |          0 |        2 |         0 |
| ProjE and BCEL       |          1 |          0 |        0 |         0 |
| ERMLP and CEL        |          1 |          0 |        0 |         0 |
| TransD and MRL       |          1 |          0 |        0 |         0 |
| SimplE and CEL       |          1 |          1 |        2 |         0 |
| DistMult and BCEL    |          1 |          0 |        2 |         2 |
| ERMLP and SPL        |          1 |          0 |        0 |         2 |
| DistMult and MRL     |          2 |          0 |        1 |         2 |
| TransR and CEL       |          1 |          0 |        0 |         0 |
| DistMult and SPL     |          1 |          0 |        0 |         2 |
| HolE and BCEL        |          2 |          0 |        0 |         2 |
| KG2E and CEL         |          1 |          0 |        1 |         0 |
| TuckER and MRL       |          0 |          3 |        1 |         0 |
| ConvE and NSSAL      |          0 |          1 |        0 |         0 |
| SimplE and BCEL      |          0 |          3 |        0 |         0 |
| ConvE and BCEL       |          0 |          2 |        2 |         0 |
| SE and NSSAL         |          0 |          1 |        0 |         0 |
| ConvE and CEL        |          0 |          2 |        2 |         0 |
| SimplE and NSSAL     |          0 |          1 |        0 |         0 |
| ComplEx and BCEL     |          0 |          3 |        0 |         2 |
| ConvE and SPL        |          0 |          1 |        2 |         0 |
| ComplEx and NSSAL    |          0 |          2 |        0 |         2 |
| ComplEx and SPL      |          0 |          4 |        0 |         2 |
| SimplE and SPL       |          0 |          2 |        0 |         0 |
| TuckER and NSSAL     |          0 |          1 |        0 |         0 |
| RESCAL and SPL       |          0 |          1 |        0 |         2 |
| SE and CEL           |          0 |          1 |        0 |         0 |
| DistMult and NSSAL   |          0 |          0 |        2 |         1 |
| ConvKB and SPL       |          0 |          0 |        0 |         2 |
| ConvKB and BCEL      |          0 |          0 |        0 |         2 |
| HolE and SPL         |          0 |          0 |        0 |         2 |
| ComplEx and MRL      |          0 |          0 |        0 |         2 |
| RESCAL and NSSAL     |          0 |          0 |        0 |         2 |
| ERMLP and NSSAL      |          0 |          0 |        0 |         2 |
| ConvKB and MRL       |          0 |          0 |        0 |         2 |
| ConvKB and NSSAL     |          0 |          0 |        0 |         2 |
| HolE and NSSAL       |          0 |          0 |        0 |         1 |
| RESCAL and MRL       |          0 |          0 |        0 |         1 |
| HolE and MRL         |          0 |          0 |        0 |         1 |


## Investigation of `model` and `training_approach`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| **RotatE and sLCWA** |          4 |          5 |        7 |         4 |
| DistMult and LCWA    |          4 |          0 |        2 |         0 |
| RotatE and LCWA      |          6 |          3 |        6 |         0 |
| TuckER and LCWA      |          5 |          6 |        6 |         0 |
| RESCAL and LCWA      |          2 |          0 |        2 |         0 |
| TransE and LCWA      |          5 |          0 |        2 |         0 |
| TransE and sLCWA     |          4 |          0 |        4 |         3 |
| KG2E and LCWA        |          3 |          0 |        3 |         0 |
| ERMLP and LCWA       |          3 |          0 |        0 |         0 |
| ComplEx and LCWA     |          2 |          2 |        1 |         0 |
| HolE and LCWA        |          3 |          0 |        1 |         0 |
| ProjE and LCWA       |          2 |          0 |        2 |         0 |
| KG2E and sLCWA       |          2 |          0 |        0 |         0 |
| TransD and sLCWA     |          1 |          0 |        0 |         0 |
| SimplE and LCWA      |          1 |          2 |        2 |         0 |
| DistMult and sLCWA   |          2 |          0 |        5 |         7 |
| TransR and LCWA      |          1 |          0 |        0 |         0 |
| TuckER and sLCWA     |          0 |          9 |        1 |         0 |
| ConvE and sLCWA      |          0 |          1 |        0 |         0 |
| SimplE and sLCWA     |          0 |          5 |        0 |         0 |
| ConvE and LCWA       |          0 |          5 |        6 |         0 |
| SE and sLCWA         |          0 |          1 |        0 |         0 |
| ComplEx and sLCWA    |          0 |          9 |        0 |         8 |
| RESCAL and sLCWA     |          0 |          1 |        0 |         6 |
| SE and LCWA          |          0 |          1 |        0 |         0 |
| ERMLP and sLCWA      |          0 |          0 |        0 |         8 |
| HolE and sLCWA       |          0 |          0 |        0 |         6 |
| ConvKB and sLCWA     |          0 |          0 |        0 |         8 |


## Investigation of `loss` and `training_approach`

|                     |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|---------------------|------------|------------|----------|-----------|
| **NSSAL and sLCWA** |          4 |          8 |        6 |        13 |
| CEL and LCWA        |         16 |         10 |       17 |         0 |
| BCEL and LCWA       |         11 |          7 |        7 |         0 |
| SPL and LCWA        |         10 |          2 |        9 |         0 |
| **MRL and sLCWA**   |          6 |          6 |        5 |        12 |
| **SPL and sLCWA**   |          3 |          9 |        2 |        12 |
| BCEL and sLCWA      |          0 |          8 |        4 |        13 |


## Investigation of `model`, `loss`, and `training_approach`

|                              |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|------------------------------|------------|------------|----------|-----------|
| **RotatE, NSSAL, and sLCWA** |          2 |          2 |        2 |         2 |
| DistMult, CEL, and LCWA      |          2 |          0 |        2 |         0 |
| RotatE, BCEL, and LCWA       |          2 |          1 |        2 |         0 |
| RotatE, CEL, and LCWA        |          2 |          2 |        2 |         0 |
| TuckER, SPL, and LCWA        |          2 |          1 |        2 |         0 |
| RESCAL, CEL, and LCWA        |          1 |          0 |        2 |         0 |
| RotatE, SPL, and LCWA        |          2 |          0 |        2 |         0 |
| TransE, CEL, and LCWA        |          1 |          0 |        0 |         0 |
| TransE, MRL, and sLCWA       |          2 |          0 |        2 |         2 |
| RESCAL, BCEL, and LCWA       |          1 |          0 |        0 |         0 |
| TransE, SPL, and LCWA        |          2 |          0 |        1 |         0 |
| TuckER, CEL, and LCWA        |          2 |          2 |        2 |         0 |
| KG2E, SPL, and LCWA          |          2 |          0 |        2 |         0 |
| ERMLP, BCEL, and LCWA        |          1 |          0 |        0 |         0 |
| TransE, BCEL, and LCWA       |          2 |          0 |        1 |         0 |
| ComplEx, CEL, and LCWA       |          2 |          2 |        1 |         0 |
| **RotatE, MRL, and sLCWA**   |          1 |          3 |        1 |         2 |
| TransE, NSSAL, and sLCWA     |          2 |          0 |        2 |         1 |
| HolE, CEL, and LCWA          |          1 |          0 |        1 |         0 |
| TuckER, BCEL, and LCWA       |          1 |          3 |        2 |         0 |
| ProjE, CEL, and LCWA         |          1 |          0 |        2 |         0 |
| KG2E, SPL, and sLCWA         |          2 |          0 |        0 |         0 |
| ProjE, BCEL, and LCWA        |          1 |          0 |        0 |         0 |
| ERMLP, CEL, and LCWA         |          1 |          0 |        0 |         0 |
| TransD, MRL, and sLCWA       |          1 |          0 |        0 |         0 |
| SimplE, CEL, and LCWA        |          1 |          1 |        2 |         0 |
| DistMult, BCEL, and LCWA     |          1 |          0 |        0 |         0 |
| ERMLP, SPL, and LCWA         |          1 |          0 |        0 |         0 |
| DistMult, MRL, and sLCWA     |          2 |          0 |        1 |         2 |
| TransR, CEL, and LCWA        |          1 |          0 |        0 |         0 |
| DistMult, SPL, and LCWA      |          1 |          0 |        0 |         0 |
| HolE, BCEL, and LCWA         |          2 |          0 |        0 |         0 |
| KG2E, CEL, and LCWA          |          1 |          0 |        1 |         0 |
| RotatE, SPL, and sLCWA       |          1 |          0 |        2 |         0 |
| TuckER, MRL, and sLCWA       |          0 |          3 |        1 |         0 |
| ConvE, NSSAL, and sLCWA      |          0 |          1 |        0 |         0 |
| SimplE, BCEL, and sLCWA      |          0 |          2 |        0 |         0 |
| ConvE, BCEL, and LCWA        |          0 |          2 |        2 |         0 |
| TuckER, BCEL, and sLCWA      |          0 |          3 |        0 |         0 |
| SimplE, BCEL, and LCWA       |          0 |          1 |        0 |         0 |
| SE, NSSAL, and sLCWA         |          0 |          1 |        0 |         0 |
| TuckER, SPL, and sLCWA       |          0 |          2 |        0 |         0 |
| ConvE, CEL, and LCWA         |          0 |          2 |        2 |         0 |
| SimplE, NSSAL, and sLCWA     |          0 |          1 |        0 |         0 |
| ComplEx, BCEL, and sLCWA     |          0 |          3 |        0 |         2 |
| ConvE, SPL, and LCWA         |          0 |          1 |        2 |         0 |
| ComplEx, NSSAL, and sLCWA    |          0 |          2 |        0 |         2 |
| ComplEx, SPL, and sLCWA      |          0 |          4 |        0 |         2 |
| SimplE, SPL, and sLCWA       |          0 |          2 |        0 |         0 |
| TuckER, NSSAL, and sLCWA     |          0 |          1 |        0 |         0 |
| RESCAL, SPL, and sLCWA       |          0 |          1 |        0 |         2 |
| SE, CEL, and LCWA            |          0 |          1 |        0 |         0 |
| RotatE, BCEL, and sLCWA      |          0 |          0 |        2 |         0 |
| DistMult, BCEL, and sLCWA    |          0 |          0 |        2 |         2 |
| DistMult, NSSAL, and sLCWA   |          0 |          0 |        2 |         1 |
| ERMLP, SPL, and sLCWA        |          0 |          0 |        0 |         2 |
| ERMLP, BCEL, and sLCWA       |          0 |          0 |        0 |         4 |
| HolE, BCEL, and sLCWA        |          0 |          0 |        0 |         2 |
| ConvKB, SPL, and sLCWA       |          0 |          0 |        0 |         2 |
| ConvKB, BCEL, and sLCWA      |          0 |          0 |        0 |         2 |
| HolE, SPL, and sLCWA         |          0 |          0 |        0 |         2 |
| ComplEx, MRL, and sLCWA      |          0 |          0 |        0 |         2 |
| RESCAL, NSSAL, and sLCWA     |          0 |          0 |        0 |         2 |
| ERMLP, NSSAL, and sLCWA      |          0 |          0 |        0 |         2 |
| DistMult, SPL, and sLCWA     |          0 |          0 |        0 |         2 |
| ConvKB, MRL, and sLCWA       |          0 |          0 |        0 |         2 |
| ConvKB, NSSAL, and sLCWA     |          0 |          0 |        0 |         2 |
| HolE, NSSAL, and sLCWA       |          0 |          0 |        0 |         1 |
| RESCAL, MRL, and sLCWA       |          0 |          0 |        0 |         1 |
| RESCAL, BCEL, and sLCWA      |          0 |          0 |        0 |         1 |
| HolE, MRL, and sLCWA         |          0 |          0 |        0 |         1 |


