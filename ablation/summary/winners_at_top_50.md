## Top 50 Results for `model`

|          |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------|------------|------------|----------|-----------|
| RotatE   |          9 |          5 |       13 |         4 |
| DistMult |          1 |          0 |        6 |         8 |
| TuckER   |          3 |         18 |        7 |         0 |
| RESCAL   |          2 |          0 |        2 |         5 |
| TransE   |         25 |          0 |        6 |         4 |
| KG2E     |          3 |          0 |        3 |         0 |
| ComplEx  |          1 |          6 |        1 |         8 |
| ERMLP    |          1 |          0 |        0 |         9 |
| HolE     |          1 |          0 |        1 |         6 |
| ProjE    |          2 |          0 |        2 |         0 |
| TransD   |          1 |          0 |        0 |         0 |
| SimplE   |          1 |          9 |        2 |         0 |
| ConvE    |          0 |         12 |        6 |         0 |
| TransH   |          0 |          0 |        1 |         0 |
| ConvKB   |          0 |          0 |        0 |         6 |

Winner at N=50: RotatE
Winner at N=50: ComplEx

## Top 50 Results for `loss`

|          |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|----------|------------|------------|----------|-----------|
| NSSA     |          6 |          7 |        6 |        12 |
| CE       |         10 |         13 |       17 |         0 |
| BCE      |         10 |         14 |       11 |        12 |
| SoftPlus |         14 |          9 |       11 |        12 |
| MR       |         10 |          7 |        5 |        14 |

Winner at N=50: NSSA
Winner at N=50: BCE
Winner at N=50: SoftPlus
Winner at N=50: MR

## Top 50 Results for `training_loop`

|      |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|------|------------|------------|----------|-----------|
| OWA  |         17 |         26 |       17 |        50 |
| LCWA |         33 |         24 |       33 |         0 |

Winner at N=50: OWA

## Top 50 Results for `create_inverse_triples`

|       |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-------|------------|------------|----------|-----------|
| False |         24 |          5 |       26 |        26 |
| True  |         26 |         45 |       24 |        24 |

Winner at N=50: False
Winner at N=50: True

## Top 50 Results for `model-loss`

|                   |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-------------------|------------|------------|----------|-----------|
| RotatE_NSSA       |          2 |          2 |        2 |         2 |
| DistMult_CE       |          1 |          0 |        2 |         0 |
| RotatE_BCE        |          2 |          0 |        4 |         0 |
| RotatE_CE         |          2 |          1 |        2 |         0 |
| TuckER_SoftPlus   |          1 |          2 |        2 |         0 |
| RESCAL_CE         |          1 |          0 |        2 |         0 |
| TransE_CE         |          1 |          0 |        0 |         0 |
| RotatE_SoftPlus   |          2 |          0 |        4 |         0 |
| TransE_MR         |          8 |          0 |        2 |         2 |
| TransE_SoftPlus   |          8 |          0 |        1 |         0 |
| TuckER_CE         |          2 |          5 |        2 |         0 |
| RESCAL_BCE        |          1 |          0 |        0 |         1 |
| KG2E_SoftPlus     |          3 |          0 |        2 |         0 |
| TransE_BCE        |          4 |          0 |        1 |         0 |
| ComplEx_CE        |          1 |          3 |        1 |         0 |
| ERMLP_BCE         |          1 |          0 |        0 |         4 |
| TransE_NSSA       |          4 |          0 |        2 |         2 |
| HolE_CE           |          1 |          0 |        1 |         0 |
| ProjE_CE          |          1 |          0 |        2 |         0 |
| ProjE_BCE         |          1 |          0 |        0 |         0 |
| TransD_MR         |          1 |          0 |        0 |         0 |
| RotatE_MR         |          1 |          2 |        1 |         2 |
| SimplE_BCE        |          1 |          4 |        0 |         0 |
| TuckER_MR         |          0 |          5 |        1 |         0 |
| TuckER_BCE        |          0 |          4 |        2 |         0 |
| ConvE_CE          |          0 |          2 |        2 |         0 |
| ConvE_BCE         |          0 |          5 |        2 |         0 |
| ComplEx_NSSA      |          0 |          1 |        0 |         2 |
| TuckER_NSSA       |          0 |          2 |        0 |         0 |
| ConvE_NSSA        |          0 |          2 |        0 |         0 |
| SimplE_CE         |          0 |          2 |        2 |         0 |
| ComplEx_BCE       |          0 |          1 |        0 |         2 |
| ConvE_SoftPlus    |          0 |          3 |        2 |         0 |
| SimplE_SoftPlus   |          0 |          3 |        0 |         0 |
| ComplEx_SoftPlus  |          0 |          1 |        0 |         2 |
| DistMult_NSSA     |          0 |          0 |        2 |         2 |
| DistMult_BCE      |          0 |          0 |        2 |         2 |
| KG2E_CE           |          0 |          0 |        1 |         0 |
| TransH_MR         |          0 |          0 |        1 |         0 |
| ERMLP_SoftPlus    |          0 |          0 |        0 |         2 |
| HolE_BCE          |          0 |          0 |        0 |         2 |
| ConvKB_SoftPlus   |          0 |          0 |        0 |         2 |
| ComplEx_MR        |          0 |          0 |        0 |         2 |
| ConvKB_BCE        |          0 |          0 |        0 |         1 |
| HolE_SoftPlus     |          0 |          0 |        0 |         2 |
| RESCAL_SoftPlus   |          0 |          0 |        0 |         2 |
| DistMult_MR       |          0 |          0 |        0 |         2 |
| DistMult_SoftPlus |          0 |          0 |        0 |         2 |
| ERMLP_NSSA        |          0 |          0 |        0 |         2 |
| ConvKB_NSSA       |          0 |          0 |        0 |         1 |
| ConvKB_MR         |          0 |          0 |        0 |         2 |
| RESCAL_MR         |          0 |          0 |        0 |         1 |
| RESCAL_NSSA       |          0 |          0 |        0 |         1 |
| HolE_MR           |          0 |          0 |        0 |         2 |
| ERMLP_MR          |          0 |          0 |        0 |         1 |

Winner at N=50: RotatE_NSSA
Winner at N=50: RotatE_MR

## Top 50 Results for `model-training_loop`

|               |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|---------------|------------|------------|----------|-----------|
| RotatE_OWA    |          3 |          4 |        7 |         4 |
| DistMult_LCWA |          1 |          0 |        2 |         0 |
| RotatE_LCWA   |          6 |          1 |        6 |         0 |
| TuckER_LCWA   |          3 |          7 |        6 |         0 |
| RESCAL_LCWA   |          2 |          0 |        2 |         0 |
| TransE_LCWA   |         13 |          0 |        2 |         0 |
| TransE_OWA    |         12 |          0 |        4 |         4 |
| KG2E_LCWA     |          2 |          0 |        3 |         0 |
| ComplEx_LCWA  |          1 |          3 |        1 |         0 |
| ERMLP_LCWA    |          1 |          0 |        0 |         0 |
| HolE_LCWA     |          1 |          0 |        1 |         0 |
| KG2E_OWA      |          1 |          0 |        0 |         0 |
| ProjE_LCWA    |          2 |          0 |        2 |         0 |
| TransD_OWA    |          1 |          0 |        0 |         0 |
| SimplE_LCWA   |          1 |          3 |        2 |         0 |
| TuckER_OWA    |          0 |         11 |        1 |         0 |
| ConvE_LCWA    |          0 |         10 |        6 |         0 |
| ComplEx_OWA   |          0 |          3 |        0 |         8 |
| ConvE_OWA     |          0 |          2 |        0 |         0 |
| SimplE_OWA    |          0 |          6 |        0 |         0 |
| DistMult_OWA  |          0 |          0 |        4 |         8 |
| TransH_OWA    |          0 |          0 |        1 |         0 |
| ERMLP_OWA     |          0 |          0 |        0 |         9 |
| HolE_OWA      |          0 |          0 |        0 |         6 |
| ConvKB_OWA    |          0 |          0 |        0 |         6 |
| RESCAL_OWA    |          0 |          0 |        0 |         5 |

Winner at N=50: RotatE_OWA

## Top 50 Results for `loss-training_loop`

|               |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|---------------|------------|------------|----------|-----------|
| NSSA_OWA      |          6 |          7 |        6 |        12 |
| CE_LCWA       |         10 |         13 |       17 |         0 |
| BCE_LCWA      |         10 |          7 |        7 |         0 |
| SoftPlus_LCWA |         13 |          4 |        9 |         0 |
| MR_OWA        |         10 |          7 |        5 |        14 |
| SoftPlus_OWA  |          1 |          5 |        2 |        12 |
| BCE_OWA       |          0 |          7 |        4 |        12 |

Winner at N=50: NSSA_OWA
Winner at N=50: MR_OWA
Winner at N=50: SoftPlus_OWA

## Top 50 Results for `model-loss-training_loop`

|                       |   FB15k237 |   Kinships |   WN18RR |   YAGO310 |
|-----------------------|------------|------------|----------|-----------|
| RotatE_NSSA_OWA       |          2 |          2 |        2 |         2 |
| DistMult_CE_LCWA      |          1 |          0 |        2 |         0 |
| RotatE_BCE_LCWA       |          2 |          0 |        2 |         0 |
| RotatE_CE_LCWA        |          2 |          1 |        2 |         0 |
| TuckER_SoftPlus_LCWA  |          1 |          1 |        2 |         0 |
| RESCAL_CE_LCWA        |          1 |          0 |        2 |         0 |
| TransE_CE_LCWA        |          1 |          0 |        0 |         0 |
| RotatE_SoftPlus_LCWA  |          2 |          0 |        2 |         0 |
| TransE_MR_OWA         |          8 |          0 |        2 |         2 |
| TransE_SoftPlus_LCWA  |          8 |          0 |        1 |         0 |
| TuckER_CE_LCWA        |          2 |          5 |        2 |         0 |
| RESCAL_BCE_LCWA       |          1 |          0 |        0 |         0 |
| KG2E_SoftPlus_LCWA    |          2 |          0 |        2 |         0 |
| TransE_BCE_LCWA       |          4 |          0 |        1 |         0 |
| ComplEx_CE_LCWA       |          1 |          3 |        1 |         0 |
| ERMLP_BCE_LCWA        |          1 |          0 |        0 |         0 |
| TransE_NSSA_OWA       |          4 |          0 |        2 |         2 |
| HolE_CE_LCWA          |          1 |          0 |        1 |         0 |
| KG2E_SoftPlus_OWA     |          1 |          0 |        0 |         0 |
| ProjE_CE_LCWA         |          1 |          0 |        2 |         0 |
| ProjE_BCE_LCWA        |          1 |          0 |        0 |         0 |
| TransD_MR_OWA         |          1 |          0 |        0 |         0 |
| RotatE_MR_OWA         |          1 |          2 |        1 |         2 |
| SimplE_BCE_LCWA       |          1 |          1 |        0 |         0 |
| TuckER_MR_OWA         |          0 |          5 |        1 |         0 |
| TuckER_BCE_LCWA       |          0 |          1 |        2 |         0 |
| TuckER_SoftPlus_OWA   |          0 |          1 |        0 |         0 |
| ConvE_CE_LCWA         |          0 |          2 |        2 |         0 |
| ConvE_BCE_LCWA        |          0 |          5 |        2 |         0 |
| ComplEx_NSSA_OWA      |          0 |          1 |        0 |         2 |
| TuckER_BCE_OWA        |          0 |          3 |        0 |         0 |
| TuckER_NSSA_OWA       |          0 |          2 |        0 |         0 |
| ConvE_NSSA_OWA        |          0 |          2 |        0 |         0 |
| SimplE_BCE_OWA        |          0 |          3 |        0 |         0 |
| SimplE_CE_LCWA        |          0 |          2 |        2 |         0 |
| ComplEx_BCE_OWA       |          0 |          1 |        0 |         2 |
| ConvE_SoftPlus_LCWA   |          0 |          3 |        2 |         0 |
| SimplE_SoftPlus_OWA   |          0 |          3 |        0 |         0 |
| ComplEx_SoftPlus_OWA  |          0 |          1 |        0 |         2 |
| RotatE_SoftPlus_OWA   |          0 |          0 |        2 |         0 |
| RotatE_BCE_OWA        |          0 |          0 |        2 |         0 |
| DistMult_NSSA_OWA     |          0 |          0 |        2 |         2 |
| DistMult_BCE_OWA      |          0 |          0 |        2 |         2 |
| KG2E_CE_LCWA          |          0 |          0 |        1 |         0 |
| TransH_MR_OWA         |          0 |          0 |        1 |         0 |
| ERMLP_SoftPlus_OWA    |          0 |          0 |        0 |         2 |
| HolE_BCE_OWA          |          0 |          0 |        0 |         2 |
| ERMLP_BCE_OWA         |          0 |          0 |        0 |         4 |
| ConvKB_SoftPlus_OWA   |          0 |          0 |        0 |         2 |
| ComplEx_MR_OWA        |          0 |          0 |        0 |         2 |
| ConvKB_BCE_OWA        |          0 |          0 |        0 |         1 |
| HolE_SoftPlus_OWA     |          0 |          0 |        0 |         2 |
| RESCAL_SoftPlus_OWA   |          0 |          0 |        0 |         2 |
| DistMult_MR_OWA       |          0 |          0 |        0 |         2 |
| DistMult_SoftPlus_OWA |          0 |          0 |        0 |         2 |
| ERMLP_NSSA_OWA        |          0 |          0 |        0 |         2 |
| ConvKB_NSSA_OWA       |          0 |          0 |        0 |         1 |
| ConvKB_MR_OWA         |          0 |          0 |        0 |         2 |
| RESCAL_MR_OWA         |          0 |          0 |        0 |         1 |
| RESCAL_BCE_OWA        |          0 |          0 |        0 |         1 |
| RESCAL_NSSA_OWA       |          0 |          0 |        0 |         1 |
| HolE_MR_OWA           |          0 |          0 |        0 |         2 |
| ERMLP_MR_OWA          |          0 |          0 |        0 |         1 |

Winner at N=50: RotatE_NSSA_OWA
Winner at N=50: RotatE_MR_OWA

