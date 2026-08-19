-- Cyberpunk total-conversion wartime AI tuning.
--
-- These values improve decisiveness after a war has begun. They do not change
-- war-goal generation or diplomatic aggression, and they do not add units.

NDefines.NAI.PLAN_VALUE_TO_EXECUTE = -0.70
NDefines.NAI.PLAN_AVG_PREPARATION_TO_EXECUTE = 0.35
NDefines.NAI.MAIN_ENEMY_FRONT_IMPORTANCE = 6.0
NDefines.NAI.AI_FRONT_MOVEMENT_FACTOR_FOR_READY = 0.35

-- Keep fewer divisions trapped in broad area-defense orders and make the AI
-- more willing to rebalance weak or empty fronts.
NDefines.NAI.MAX_UNITS_FACTOR_AREA_ORDER = 0.60
NDefines.NAI.REASSIGN_TO_ANOTHER_FRONT_FACTOR = 0.75
NDefines.NAI.REASSIGN_TO_ANOTHER_FRONT_IF_IN_COMBAT_FACTOR = 0.30

-- Encourage balanced offensives without forcing constant suicidal rush attacks.
NDefines.NAI.AGGRESSIVENESS_CHECK_BASE = 1.25
NDefines.NAI.AGGRESSIVENESS_CHECK_CAREFUL = 0.45

-- Make overseas powers use their fleets and invasion forces more consistently.
NDefines.NAI.MAX_DISTANCE_NAVAL_INVASION = 350.0
NDefines.NAI.MIN_INVASION_PLAN_VALUE_TO_EXECUTE = 0.15
NDefines.NAI.MIN_INVASION_ORG_FACTOR_TO_EXECUTE = 0.35
NDefines.NAI.INVASION_UNITS_READY_AT_MIN_PLAN = 0.60
NDefines.NAI.MAX_UNIT_RATIO_FOR_INVASIONS = 0.50

-- Air wings react to contested fronts sooner instead of remaining idle while
-- only a small part of an air region is under enemy control.
NDefines.NAI.AIR_AI_ENEMY_PROV_RATIO_FOR_COMBAT_REGION = 0.08
