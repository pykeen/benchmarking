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

|              |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|--------------|------------|------------|----------|-----------|
| **NSSA**     |          6 |          7 |        6 |        12 |
| CE           |         10 |         13 |       17 |         0 |
| **BCE**      |         10 |         14 |       11 |        12 |
| **SoftPlus** |         14 |          9 |       11 |        12 |
| **MR**       |         10 |          7 |        5 |        14 |


## Investigation of `training_loop`

|         |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|---------|------------|------------|----------|-----------|
| **OWA** |         17 |         26 |       17 |        50 |
| LCWA    |         33 |         24 |       33 |         0 |


## Investigation of `create_inverse_triples`

|           |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------|------------|------------|----------|-----------|
| **False** |         24 |          5 |       26 |        26 |
| **True**  |         26 |         45 |       24 |        24 |


## Investigation of `model` and `loss`

|                       |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------------------|------------|------------|----------|-----------|
| **RotatE and NSSA**   |          2 |          2 |        2 |         2 |
| DistMult and CE       |          1 |          0 |        2 |         0 |
| RotatE and BCE        |          2 |          0 |        4 |         0 |
| RotatE and CE         |          2 |          1 |        2 |         0 |
| TuckER and SoftPlus   |          1 |          2 |        2 |         0 |
| RESCAL and CE         |          1 |          0 |        2 |         0 |
| TransE and CE         |          1 |          0 |        0 |         0 |
| RotatE and SoftPlus   |          2 |          0 |        4 |         0 |
| TransE and MR         |          8 |          0 |        2 |         2 |
| TransE and SoftPlus   |          8 |          0 |        1 |         0 |
| TuckER and CE         |          2 |          5 |        2 |         0 |
| RESCAL and BCE        |          1 |          0 |        0 |         1 |
| KG2E and SoftPlus     |          3 |          0 |        2 |         0 |
| TransE and BCE        |          4 |          0 |        1 |         0 |
| ComplEx and CE        |          1 |          3 |        1 |         0 |
| ERMLP and BCE         |          1 |          0 |        0 |         4 |
| TransE and NSSA       |          4 |          0 |        2 |         2 |
| HolE and CE           |          1 |          0 |        1 |         0 |
| ProjE and CE          |          1 |          0 |        2 |         0 |
| ProjE and BCE         |          1 |          0 |        0 |         0 |
| TransD and MR         |          1 |          0 |        0 |         0 |
| **RotatE and MR**     |          1 |          2 |        1 |         2 |
| SimplE and BCE        |          1 |          4 |        0 |         0 |
| TuckER and MR         |          0 |          5 |        1 |         0 |
| TuckER and BCE        |          0 |          4 |        2 |         0 |
| ConvE and CE          |          0 |          2 |        2 |         0 |
| ConvE and BCE         |          0 |          5 |        2 |         0 |
| ComplEx and NSSA      |          0 |          1 |        0 |         2 |
| TuckER and NSSA       |          0 |          2 |        0 |         0 |
| ConvE and NSSA        |          0 |          2 |        0 |         0 |
| SimplE and CE         |          0 |          2 |        2 |         0 |
| ComplEx and BCE       |          0 |          1 |        0 |         2 |
| ConvE and SoftPlus    |          0 |          3 |        2 |         0 |
| SimplE and SoftPlus   |          0 |          3 |        0 |         0 |
| ComplEx and SoftPlus  |          0 |          1 |        0 |         2 |
| DistMult and NSSA     |          0 |          0 |        2 |         2 |
| DistMult and BCE      |          0 |          0 |        2 |         2 |
| KG2E and CE           |          0 |          0 |        1 |         0 |
| TransH and MR         |          0 |          0 |        1 |         0 |
| ERMLP and SoftPlus    |          0 |          0 |        0 |         2 |
| HolE and BCE          |          0 |          0 |        0 |         2 |
| ConvKB and SoftPlus   |          0 |          0 |        0 |         2 |
| ComplEx and MR        |          0 |          0 |        0 |         2 |
| ConvKB and BCE        |          0 |          0 |        0 |         1 |
| HolE and SoftPlus     |          0 |          0 |        0 |         2 |
| RESCAL and SoftPlus   |          0 |          0 |        0 |         2 |
| DistMult and MR       |          0 |          0 |        0 |         2 |
| DistMult and SoftPlus |          0 |          0 |        0 |         2 |
| ERMLP and NSSA        |          0 |          0 |        0 |         2 |
| ConvKB and NSSA       |          0 |          0 |        0 |         1 |
| ConvKB and MR         |          0 |          0 |        0 |         2 |
| RESCAL and MR         |          0 |          0 |        0 |         1 |
| RESCAL and NSSA       |          0 |          0 |        0 |         1 |
| HolE and MR           |          0 |          0 |        0 |         2 |
| ERMLP and MR          |          0 |          0 |        0 |         1 |


## Investigation of `model` and `training_loop`

|                    |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|--------------------|------------|------------|----------|-----------|
| **RotatE and OWA** |          3 |          4 |        7 |         4 |
| DistMult and LCWA  |          1 |          0 |        2 |         0 |
| RotatE and LCWA    |          6 |          1 |        6 |         0 |
| TuckER and LCWA    |          3 |          7 |        6 |         0 |
| RESCAL and LCWA    |          2 |          0 |        2 |         0 |
| TransE and LCWA    |         13 |          0 |        2 |         0 |
| TransE and OWA     |         12 |          0 |        4 |         4 |
| KG2E and LCWA      |          2 |          0 |        3 |         0 |
| ComplEx and LCWA   |          1 |          3 |        1 |         0 |
| ERMLP and LCWA     |          1 |          0 |        0 |         0 |
| HolE and LCWA      |          1 |          0 |        1 |         0 |
| KG2E and OWA       |          1 |          0 |        0 |         0 |
| ProjE and LCWA     |          2 |          0 |        2 |         0 |
| TransD and OWA     |          1 |          0 |        0 |         0 |
| SimplE and LCWA    |          1 |          3 |        2 |         0 |
| TuckER and OWA     |          0 |         11 |        1 |         0 |
| ConvE and LCWA     |          0 |         10 |        6 |         0 |
| ComplEx and OWA    |          0 |          3 |        0 |         8 |
| ConvE and OWA      |          0 |          2 |        0 |         0 |
| SimplE and OWA     |          0 |          6 |        0 |         0 |
| DistMult and OWA   |          0 |          0 |        4 |         8 |
| TransH and OWA     |          0 |          0 |        1 |         0 |
| ERMLP and OWA      |          0 |          0 |        0 |         9 |
| HolE and OWA       |          0 |          0 |        0 |         6 |
| ConvKB and OWA     |          0 |          0 |        0 |         6 |
| RESCAL and OWA     |          0 |          0 |        0 |         5 |


## Investigation of `loss` and `training_loop`

|                      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------------------|------------|------------|----------|-----------|
| **NSSA and OWA**     |          6 |          7 |        6 |        12 |
| CE and LCWA          |         10 |         13 |       17 |         0 |
| BCE and LCWA         |         10 |          7 |        7 |         0 |
| SoftPlus and LCWA    |         13 |          4 |        9 |         0 |
| **MR and OWA**       |         10 |          7 |        5 |        14 |
| **SoftPlus and OWA** |          1 |          5 |        2 |        12 |
| BCE and OWA          |          0 |          7 |        4 |        12 |


## Investigation of `model`, `loss`, and `training_loop`

|                             |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------------------------|------------|------------|----------|-----------|
| **RotatE, NSSA, and OWA**   |          2 |          2 |        2 |         2 |
| DistMult, CE, and LCWA      |          1 |          0 |        2 |         0 |
| RotatE, BCE, and LCWA       |          2 |          0 |        2 |         0 |
| RotatE, CE, and LCWA        |          2 |          1 |        2 |         0 |
| TuckER, SoftPlus, and LCWA  |          1 |          1 |        2 |         0 |
| RESCAL, CE, and LCWA        |          1 |          0 |        2 |         0 |
| TransE, CE, and LCWA        |          1 |          0 |        0 |         0 |
| RotatE, SoftPlus, and LCWA  |          2 |          0 |        2 |         0 |
| TransE, MR, and OWA         |          8 |          0 |        2 |         2 |
| TransE, SoftPlus, and LCWA  |          8 |          0 |        1 |         0 |
| TuckER, CE, and LCWA        |          2 |          5 |        2 |         0 |
| RESCAL, BCE, and LCWA       |          1 |          0 |        0 |         0 |
| KG2E, SoftPlus, and LCWA    |          2 |          0 |        2 |         0 |
| TransE, BCE, and LCWA       |          4 |          0 |        1 |         0 |
| ComplEx, CE, and LCWA       |          1 |          3 |        1 |         0 |
| ERMLP, BCE, and LCWA        |          1 |          0 |        0 |         0 |
| TransE, NSSA, and OWA       |          4 |          0 |        2 |         2 |
| HolE, CE, and LCWA          |          1 |          0 |        1 |         0 |
| KG2E, SoftPlus, and OWA     |          1 |          0 |        0 |         0 |
| ProjE, CE, and LCWA         |          1 |          0 |        2 |         0 |
| ProjE, BCE, and LCWA        |          1 |          0 |        0 |         0 |
| TransD, MR, and OWA         |          1 |          0 |        0 |         0 |
| **RotatE, MR, and OWA**     |          1 |          2 |        1 |         2 |
| SimplE, BCE, and LCWA       |          1 |          1 |        0 |         0 |
| TuckER, MR, and OWA         |          0 |          5 |        1 |         0 |
| TuckER, BCE, and LCWA       |          0 |          1 |        2 |         0 |
| TuckER, SoftPlus, and OWA   |          0 |          1 |        0 |         0 |
| ConvE, CE, and LCWA         |          0 |          2 |        2 |         0 |
| ConvE, BCE, and LCWA        |          0 |          5 |        2 |         0 |
| ComplEx, NSSA, and OWA      |          0 |          1 |        0 |         2 |
| TuckER, BCE, and OWA        |          0 |          3 |        0 |         0 |
| TuckER, NSSA, and OWA       |          0 |          2 |        0 |         0 |
| ConvE, NSSA, and OWA        |          0 |          2 |        0 |         0 |
| SimplE, BCE, and OWA        |          0 |          3 |        0 |         0 |
| SimplE, CE, and LCWA        |          0 |          2 |        2 |         0 |
| ComplEx, BCE, and OWA       |          0 |          1 |        0 |         2 |
| ConvE, SoftPlus, and LCWA   |          0 |          3 |        2 |         0 |
| SimplE, SoftPlus, and OWA   |          0 |          3 |        0 |         0 |
| ComplEx, SoftPlus, and OWA  |          0 |          1 |        0 |         2 |
| RotatE, SoftPlus, and OWA   |          0 |          0 |        2 |         0 |
| RotatE, BCE, and OWA        |          0 |          0 |        2 |         0 |
| DistMult, NSSA, and OWA     |          0 |          0 |        2 |         2 |
| DistMult, BCE, and OWA      |          0 |          0 |        2 |         2 |
| KG2E, CE, and LCWA          |          0 |          0 |        1 |         0 |
| TransH, MR, and OWA         |          0 |          0 |        1 |         0 |
| ERMLP, SoftPlus, and OWA    |          0 |          0 |        0 |         2 |
| HolE, BCE, and OWA          |          0 |          0 |        0 |         2 |
| ERMLP, BCE, and OWA         |          0 |          0 |        0 |         4 |
| ConvKB, SoftPlus, and OWA   |          0 |          0 |        0 |         2 |
| ComplEx, MR, and OWA        |          0 |          0 |        0 |         2 |
| ConvKB, BCE, and OWA        |          0 |          0 |        0 |         1 |
| HolE, SoftPlus, and OWA     |          0 |          0 |        0 |         2 |
| RESCAL, SoftPlus, and OWA   |          0 |          0 |        0 |         2 |
| DistMult, MR, and OWA       |          0 |          0 |        0 |         2 |
| DistMult, SoftPlus, and OWA |          0 |          0 |        0 |         2 |
| ERMLP, NSSA, and OWA        |          0 |          0 |        0 |         2 |
| ConvKB, NSSA, and OWA       |          0 |          0 |        0 |         1 |
| ConvKB, MR, and OWA         |          0 |          0 |        0 |         2 |
| RESCAL, MR, and OWA         |          0 |          0 |        0 |         1 |
| RESCAL, BCE, and OWA        |          0 |          0 |        0 |         1 |
| RESCAL, NSSA, and OWA       |          0 |          0 |        0 |         1 |
| HolE, MR, and OWA           |          0 |          0 |        0 |         2 |
| ERMLP, MR, and OWA          |          0 |          0 |        0 |         1 |


