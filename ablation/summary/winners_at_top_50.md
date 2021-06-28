# Investigation of Top 50 Results

This document gives insight into which models, loss functions, etc. are consistently
appearing in the top 50 experiments rated by hits@10 for **all** datasets. The ones that appear in the top 50
experiments for every dataset are shown in **bold** in the index of each table. Note that not all tables
show that there are consistent best performers.

## Investigation of `model`

|             |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-------------|------------|------------|----------|-----------|
| TuckER      |          6 |         10 |        5 |         0 |
| **RotatE**  |          9 |          9 |       12 |         4 |
| ConvE       |          2 |          9 |        4 |         0 |
| DistMult    |          2 |          0 |        4 |         6 |
| MuRE        |         10 |          0 |       10 |         7 |
| **RESCAL**  |          2 |          1 |        2 |         3 |
| TransE      |          7 |          0 |        3 |         1 |
| **QuatE**   |          1 |          3 |        4 |         6 |
| KG2E        |          4 |          0 |        2 |         0 |
| ERMLP       |          2 |          0 |        0 |         5 |
| **ComplEx** |          1 |         10 |        1 |         8 |
| HolE        |          1 |          0 |        1 |         4 |
| TransD      |          1 |          0 |        0 |         0 |
| ProjE       |          2 |          0 |        1 |         0 |
| SE          |          0 |          1 |        0 |         0 |
| SimplE      |          0 |          7 |        1 |         0 |
| ConvKB      |          0 |          0 |        0 |         6 |


## Investigation of `loss`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **BCEL**  |         13 |         15 |       12 |        13 |
| **SPL**   |         14 |         11 |       14 |        15 |
| CEL       |         14 |         10 |       15 |         0 |
| **NSSAL** |          5 |          9 |        6 |        11 |
| **MRL**   |          4 |          5 |        3 |        11 |


## Investigation of `training_approach`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| LCWA      |         35 |         22 |       33 |         0 |
| **sLCWA** |         15 |         28 |       17 |        50 |


## Investigation of `inverse_relations`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **True**  |         30 |         37 |       25 |        25 |
| **False** |         20 |         13 |       25 |        25 |


## Investigation of `model` and `loss`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| TuckER and BCEL      |          2 |          3 |        1 |         0 |
| TuckER and SPL       |          2 |          3 |        2 |         0 |
| TuckER and CEL       |          2 |          2 |        2 |         0 |
| **RotatE and NSSAL** |          2 |          2 |        2 |         2 |
| ConvE and BCEL       |          1 |          2 |        2 |         0 |
| RotatE and BCEL      |          2 |          2 |        4 |         0 |
| DistMult and CEL     |          2 |          0 |        1 |         0 |
| MuRE and BCEL        |          4 |          0 |        3 |         2 |
| RotatE and CEL       |          2 |          2 |        2 |         0 |
| RESCAL and CEL       |          1 |          0 |        2 |         0 |
| TransE and MRL       |          2 |          0 |        0 |         1 |
| QuatE and CEL        |          1 |          1 |        2 |         0 |
| ConvE and CEL        |          1 |          2 |        1 |         0 |
| TransE and CEL       |          1 |          0 |        0 |         0 |
| KG2E and SPL         |          4 |          0 |        2 |         0 |
| RESCAL and BCEL      |          1 |          0 |        0 |         0 |
| TransE and SPL       |          2 |          0 |        1 |         0 |
| MuRE and SPL         |          4 |          0 |        4 |         2 |
| ERMLP and BCEL       |          1 |          0 |        0 |         2 |
| MuRE and NSSAL       |          2 |          0 |        2 |         1 |
| ComplEx and CEL      |          1 |          2 |        1 |         0 |
| TransE and BCEL      |          1 |          0 |        1 |         0 |
| RotatE and SPL       |          2 |          0 |        3 |         0 |
| **RotatE and MRL**   |          1 |          3 |        1 |         2 |
| HolE and CEL         |          1 |          0 |        1 |         0 |
| TransE and NSSAL     |          1 |          0 |        1 |         0 |
| TransD and MRL       |          1 |          0 |        0 |         0 |
| ProjE and BCEL       |          1 |          0 |        0 |         0 |
| ProjE and CEL        |          1 |          0 |        1 |         0 |
| ERMLP and CEL        |          1 |          0 |        0 |         0 |
| ConvE and NSSAL      |          0 |          1 |        0 |         0 |
| ComplEx and NSSAL    |          0 |          2 |        0 |         2 |
| SE and NSSAL         |          0 |          1 |        0 |         0 |
| SimplE and BCEL      |          0 |          3 |        0 |         0 |
| TuckER and NSSAL     |          0 |          1 |        0 |         0 |
| ComplEx and BCEL     |          0 |          4 |        0 |         2 |
| ConvE and SPL        |          0 |          3 |        1 |         0 |
| TuckER and MRL       |          0 |          1 |        0 |         0 |
| SimplE and SPL       |          0 |          2 |        0 |         0 |
| SimplE and CEL       |          0 |          1 |        1 |         0 |
| ComplEx and SPL      |          0 |          2 |        0 |         2 |
| SimplE and NSSAL     |          0 |          1 |        0 |         0 |
| QuatE and BCEL       |          0 |          1 |        0 |         2 |
| QuatE and NSSAL      |          0 |          1 |        0 |         1 |
| RESCAL and SPL       |          0 |          1 |        0 |         2 |
| ConvE and MRL        |          0 |          1 |        0 |         0 |
| MuRE and CEL         |          0 |          0 |        1 |         0 |
| DistMult and BCEL    |          0 |          0 |        1 |         1 |
| QuatE and MRL        |          0 |          0 |        1 |         1 |
| QuatE and SPL        |          0 |          0 |        1 |         2 |
| DistMult and NSSAL   |          0 |          0 |        1 |         1 |
| DistMult and MRL     |          0 |          0 |        1 |         2 |
| HolE and BCEL        |          0 |          0 |        0 |         2 |
| ConvKB and SPL       |          0 |          0 |        0 |         2 |
| ERMLP and SPL        |          0 |          0 |        0 |         1 |
| HolE and SPL         |          0 |          0 |        0 |         2 |
| ComplEx and MRL      |          0 |          0 |        0 |         2 |
| ConvKB and BCEL      |          0 |          0 |        0 |         2 |
| DistMult and SPL     |          0 |          0 |        0 |         2 |
| ERMLP and NSSAL      |          0 |          0 |        0 |         2 |
| ConvKB and NSSAL     |          0 |          0 |        0 |         1 |
| RESCAL and NSSAL     |          0 |          0 |        0 |         1 |
| MuRE and MRL         |          0 |          0 |        0 |         2 |
| ConvKB and MRL       |          0 |          0 |        0 |         1 |


## Investigation of `model` and `training_approach`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| TuckER and LCWA      |          6 |          7 |        5 |         0 |
| **RotatE and sLCWA** |          3 |          5 |        6 |         4 |
| ConvE and LCWA       |          2 |          6 |        4 |         0 |
| RotatE and LCWA      |          6 |          4 |        6 |         0 |
| DistMult and LCWA    |          2 |          0 |        1 |         0 |
| MuRE and LCWA        |          4 |          0 |        4 |         0 |
| RESCAL and LCWA      |          2 |          0 |        2 |         0 |
| TransE and sLCWA     |          3 |          0 |        1 |         1 |
| QuatE and LCWA       |          1 |          1 |        3 |         0 |
| TransE and LCWA      |          4 |          0 |        2 |         0 |
| KG2E and LCWA        |          2 |          0 |        2 |         0 |
| ERMLP and LCWA       |          2 |          0 |        0 |         0 |
| MuRE and sLCWA       |          6 |          0 |        6 |         7 |
| ComplEx and LCWA     |          1 |          2 |        1 |         0 |
| KG2E and sLCWA       |          2 |          0 |        0 |         0 |
| HolE and LCWA        |          1 |          0 |        1 |         0 |
| TransD and sLCWA     |          1 |          0 |        0 |         0 |
| ProjE and LCWA       |          2 |          0 |        1 |         0 |
| ConvE and sLCWA      |          0 |          3 |        0 |         0 |
| ComplEx and sLCWA    |          0 |          8 |        0 |         8 |
| SE and sLCWA         |          0 |          1 |        0 |         0 |
| SimplE and sLCWA     |          0 |          5 |        0 |         0 |
| TuckER and sLCWA     |          0 |          3 |        0 |         0 |
| SimplE and LCWA      |          0 |          2 |        1 |         0 |
| QuatE and sLCWA      |          0 |          2 |        1 |         6 |
| RESCAL and sLCWA     |          0 |          1 |        0 |         3 |
| DistMult and sLCWA   |          0 |          0 |        3 |         6 |
| HolE and sLCWA       |          0 |          0 |        0 |         4 |
| ERMLP and sLCWA      |          0 |          0 |        0 |         5 |
| ConvKB and sLCWA     |          0 |          0 |        0 |         6 |


## Investigation of `loss` and `training_approach`

|                     |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|---------------------|------------|------------|----------|-----------|
| BCEL and LCWA       |         11 |          8 |        7 |         0 |
| SPL and LCWA        |         10 |          4 |       11 |         0 |
| CEL and LCWA        |         14 |         10 |       15 |         0 |
| **NSSAL and sLCWA** |          5 |          9 |        6 |        11 |
| **MRL and sLCWA**   |          4 |          5 |        3 |        11 |
| **BCEL and sLCWA**  |          2 |          7 |        5 |        13 |
| **SPL and sLCWA**   |          4 |          7 |        3 |        15 |


## Investigation of `model`, `loss`, and `training_approach`

|                              |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|------------------------------|------------|------------|----------|-----------|
| TuckER, BCEL, and LCWA       |          2 |          3 |        1 |         0 |
| TuckER, SPL, and LCWA        |          2 |          2 |        2 |         0 |
| TuckER, CEL, and LCWA        |          2 |          2 |        2 |         0 |
| **RotatE, NSSAL, and sLCWA** |          2 |          2 |        2 |         2 |
| ConvE, BCEL, and LCWA        |          1 |          2 |        2 |         0 |
| RotatE, BCEL, and LCWA       |          2 |          2 |        2 |         0 |
| DistMult, CEL, and LCWA      |          2 |          0 |        1 |         0 |
| MuRE, BCEL, and LCWA         |          2 |          0 |        1 |         0 |
| RotatE, CEL, and LCWA        |          2 |          2 |        2 |         0 |
| RESCAL, CEL, and LCWA        |          1 |          0 |        2 |         0 |
| TransE, MRL, and sLCWA       |          2 |          0 |        0 |         1 |
| QuatE, CEL, and LCWA         |          1 |          1 |        2 |         0 |
| ConvE, CEL, and LCWA         |          1 |          2 |        1 |         0 |
| TransE, CEL, and LCWA        |          1 |          0 |        0 |         0 |
| KG2E, SPL, and LCWA          |          2 |          0 |        2 |         0 |
| RESCAL, BCEL, and LCWA       |          1 |          0 |        0 |         0 |
| TransE, SPL, and LCWA        |          2 |          0 |        1 |         0 |
| MuRE, SPL, and LCWA          |          2 |          0 |        2 |         0 |
| ERMLP, BCEL, and LCWA        |          1 |          0 |        0 |         0 |
| MuRE, NSSAL, and sLCWA       |          2 |          0 |        2 |         1 |
| ComplEx, CEL, and LCWA       |          1 |          2 |        1 |         0 |
| TransE, BCEL, and LCWA       |          1 |          0 |        1 |         0 |
| RotatE, SPL, and LCWA        |          2 |          0 |        2 |         0 |
| MuRE, BCEL, and sLCWA        |          2 |          0 |        2 |         2 |
| MuRE, SPL, and sLCWA         |          2 |          0 |        2 |         2 |
| **RotatE, MRL, and sLCWA**   |          1 |          3 |        1 |         2 |
| KG2E, SPL, and sLCWA         |          2 |          0 |        0 |         0 |
| HolE, CEL, and LCWA          |          1 |          0 |        1 |         0 |
| TransE, NSSAL, and sLCWA     |          1 |          0 |        1 |         0 |
| TransD, MRL, and sLCWA       |          1 |          0 |        0 |         0 |
| ProjE, BCEL, and LCWA        |          1 |          0 |        0 |         0 |
| ProjE, CEL, and LCWA         |          1 |          0 |        1 |         0 |
| ERMLP, CEL, and LCWA         |          1 |          0 |        0 |         0 |
| ConvE, NSSAL, and sLCWA      |          0 |          1 |        0 |         0 |
| ComplEx, NSSAL, and sLCWA    |          0 |          2 |        0 |         2 |
| SE, NSSAL, and sLCWA         |          0 |          1 |        0 |         0 |
| SimplE, BCEL, and sLCWA      |          0 |          2 |        0 |         0 |
| TuckER, NSSAL, and sLCWA     |          0 |          1 |        0 |         0 |
| ComplEx, BCEL, and sLCWA     |          0 |          4 |        0 |         2 |
| ConvE, SPL, and LCWA         |          0 |          2 |        1 |         0 |
| TuckER, MRL, and sLCWA       |          0 |          1 |        0 |         0 |
| SimplE, SPL, and sLCWA       |          0 |          2 |        0 |         0 |
| SimplE, CEL, and LCWA        |          0 |          1 |        1 |         0 |
| ComplEx, SPL, and sLCWA      |          0 |          2 |        0 |         2 |
| TuckER, SPL, and sLCWA       |          0 |          1 |        0 |         0 |
| SimplE, BCEL, and LCWA       |          0 |          1 |        0 |         0 |
| SimplE, NSSAL, and sLCWA     |          0 |          1 |        0 |         0 |
| ConvE, SPL, and sLCWA        |          0 |          1 |        0 |         0 |
| QuatE, BCEL, and sLCWA       |          0 |          1 |        0 |         2 |
| QuatE, NSSAL, and sLCWA      |          0 |          1 |        0 |         1 |
| RESCAL, SPL, and sLCWA       |          0 |          1 |        0 |         2 |
| ConvE, MRL, and sLCWA        |          0 |          1 |        0 |         0 |
| MuRE, CEL, and LCWA          |          0 |          0 |        1 |         0 |
| RotatE, BCEL, and sLCWA      |          0 |          0 |        2 |         0 |
| RotatE, SPL, and sLCWA       |          0 |          0 |        1 |         0 |
| DistMult, BCEL, and sLCWA    |          0 |          0 |        1 |         1 |
| QuatE, MRL, and sLCWA        |          0 |          0 |        1 |         1 |
| QuatE, SPL, and LCWA         |          0 |          0 |        1 |         0 |
| DistMult, NSSAL, and sLCWA   |          0 |          0 |        1 |         1 |
| DistMult, MRL, and sLCWA     |          0 |          0 |        1 |         2 |
| QuatE, SPL, and sLCWA        |          0 |          0 |        0 |         2 |
| HolE, BCEL, and sLCWA        |          0 |          0 |        0 |         2 |
| ERMLP, BCEL, and sLCWA       |          0 |          0 |        0 |         2 |
| ConvKB, SPL, and sLCWA       |          0 |          0 |        0 |         2 |
| ERMLP, SPL, and sLCWA        |          0 |          0 |        0 |         1 |
| HolE, SPL, and sLCWA         |          0 |          0 |        0 |         2 |
| ComplEx, MRL, and sLCWA      |          0 |          0 |        0 |         2 |
| ConvKB, BCEL, and sLCWA      |          0 |          0 |        0 |         2 |
| DistMult, SPL, and sLCWA     |          0 |          0 |        0 |         2 |
| ERMLP, NSSAL, and sLCWA      |          0 |          0 |        0 |         2 |
| ConvKB, NSSAL, and sLCWA     |          0 |          0 |        0 |         1 |
| RESCAL, NSSAL, and sLCWA     |          0 |          0 |        0 |         1 |
| MuRE, MRL, and sLCWA         |          0 |          0 |        0 |         2 |
| ConvKB, MRL, and sLCWA       |          0 |          0 |        0 |         1 |


