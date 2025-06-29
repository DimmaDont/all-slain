LOCATIONS: dict[str, str | tuple[str, str]] = {
    "A18_HospitalInt_OC": "Empire Health Services, Area18, ArcCorp, Stanton",
    "ab_pyro_int_dung_001": ("in a", "Contested Zone"),  # SUPVISR 3-4 and 3-5
    "ab_pyro_int_dung_exec_002": "PYAM-EXHANG-0-1",
    "ab_pyro_int_dung_exec_004": "PYAM-EXHANG-0-1",
    "ab_pyro_int_dung_exec_005": "PYAM-EXHANG-0-1",
    "AEGS_Reclaimer_Interior_Platform": ("inside of an", "Aegis Reclaimer"),
    "Area18_central-001": "Area18 Central, Area18, ArcCorp, Stanton",
    "dealership_rundown_001": "Ship Dealer",
    "druglab_a_int": "Jumptown",
    "ellis3": "Green (Ellis III), Ellis",  # Arena Commander
    "int_s1_dc_cvlx_s1dc06": ("inside", "Covalex Distribution Center S1DC06"),
    "int_s1_dc_dpre_imf": ("inside", "Dupree Industrial Manufacturing Facility"),
    "int_s1_dc_grin_s1pcb": ("inside", "Greycat Stanton I Production Complex-B"),
    "int_s1_dc_hrst_cassillo": ("inside", "HDPC-Cassillo"),
    "int_s1_dc_hrst_farnesway": ("inside", "HDPC-Farnesway"),
    "int_s1_dc_sasu_magnolia": ("inside", "Sakura Sun Magnolia Workcenter"),
    "int_s4_dc_cras_pp19-02": ("inside", "Cry-Astro Processing Plant 19-02"),
    "int_s4_dc_cras_pp34-12": ("inside", "Cry-Astro Processing Plant 34-12"),
    "int_s4_dc_cvlx_s4dc05": ("inside", "Covalex Distribution Center S4DC05"),
    "int_s4_dc_grin_s4pca": ("inside", "Greycat Stanton IV Production Complex-A"),
    "int_s4_dc_mite_s4ld01": ("inside", "microTech Logistics Depot S4LD01"),
    "int_s4_dc_mite_s4ld13": ("inside", "microTech Logistics Depot S4LD13"),
    "int_s4_dc_sasu_goldenrod": ("inside", "Sakura Sun Goldenrod Workcenter"),
    "jumppoint_pyro_stanton": "Stanton Gateway, Pyro",
    "lorville_l19_int": ("in", "L19 Residences, Lorville"),
    "oc_a18_sp_int": ("inside", "Riker Memorial Spaceport"),
    "OOC_JumpPoint_stanton_magnus": "Magnus Gateway, Stanton",
    "OOC_JumpPoint_stanton_pyro": "Pyro Gateway, Stanton",
    "OOC_JumpPoint_stanton_terra": "Terra Gateway, Stanton",
    "OOC_Stanton1_L1": "HUR-L1 Green Glade Station",
    "OOC_Stanton1_L2": "HUR-L2 Faithful Dream Station",
    "OOC_Stanton1_L3": "HUR-L3 Thundering Express Station",
    "OOC_Stanton1_L4": "HUR-L4 Melodic Fields Station",
    "OOC_Stanton1_L5": "HUR-L5 High Course Station",
    "OOC_Stanton2_L1": "CRU-L1 Ambitious Dream Station",
    "OOC_Stanton2_L4": "CRU-L4 Shallow Fields Station",
    "OOC_Stanton2_L5": "CRU-L5 Beautiful Glen Station",
    "OOC_Stanton3_L1": "ARC-L1 Wide Forest Station",
    "OOC_Stanton3_L2": "ARC-L2 Lively Pathway Station",
    "OOC_Stanton3_L3": "ARC-L3 Modern Express Station",
    "OOC_Stanton3_L4": "ARC-L4 Faint Glen Station",
    "OOC_Stanton3_L5": "ARC-L5 Yellow Core Station",
    "OOC_Stanton4_L1": "MIC-L1 Shallow Frontier Station",
    "OOC_Stanton4_L2": "MIC-L2 Long Forest Station",
    "OOC_Stanton4_L3": "MIC-L3 Endless Odyssey Station",
    "OOC_Stanton4_L4": "MIC-L4 Red Crossroads Station",
    "OOC_Stanton4_L5": "MIC-L5 Modern Icarus Station",
    "OOC_Stanton_1_Hurston": ("on", "Hurston, Stanton"),
    "OOC_Stanton_1a_Ariel": ("on", "Ariel, Hurston, Stanton"),
    "OOC_Stanton_1b_Aberdeen": ("on", "Aberdeen, Hurston, Stanton"),
    "OOC_Stanton_1c_Magda": ("on", "Magda, Hurston, Stanton"),
    "OOC_Stanton_1d_Ita": ("on", "Ita, Hurston, Stanton"),
    "OOC_Stanton_2_Crusader": ("on", "Crusader, Stanton"),
    "OOC_Stanton_2a_Cellin": ("on", "Cellin, Crusader, Stanton"),
    "OOC_Stanton_2b_Daymar": ("on", "Daymar, Crusader, Stanton"),
    "OOC_Stanton_2c_Yela": ("on", "Yela, Crusader, Stanton"),
    "OOC_Stanton_3_ArcCorp": ("on", "ArcCorp, Stanton"),
    "OOC_Stanton_3a_Lyria": ("on", "Lyria, ArcCorp, Stanton"),
    "OOC_Stanton_3b_Wala": ("on", "Wala, ArcCorp, Stanton"),
    "OOC_Stanton_4_Microtech": ("on", "microTech, Stanton"),
    "OOC_Stanton_4a_Calliope": ("on", "Calliope, microTech, Stanton"),
    "OOC_Stanton_4b_Clio": ("on", "Clio, microTech, Stanton"),
    "OOC_Stanton_4c_Euterpe": ("on", "Euterpe, microTech, Stanton"),
    "P1_L1": "PYR1 L1",
    "P2_L4": "Checkmate Station, Monox, Pyro",
    "p2l4_contestedzone": "Contested Zone, Checkmate",
    "P3_L1": "Starlight Service Station",
    "P3_L3": "Patch City",
    "P3_L4": "PYAM-SUPVISR-3-4, Pyro",
    "P3_L5": "PYAM-SUPVISR-3-5, Pyro",
    "P5_L2": "Gaslight",
    "P5_L4": "Rod's Fuel 'N Supplies",
    "P5_L5": "Rat's Nest",
    "p5l2_contestedzone": "Contested Zone, Orbituary",
    "P6_L1": "PYR6 L1",
    "P6_L2": "PYR6 L2",
    "P6_L3": "Endgame",
    "P6_L4": "Dudley & Daughters",
    "P6_L5": "Megumi Refueling",
    "planet": ("on a", "Planet"),  # Arena Commander?
    "pyro1": ("on", "Pyro I, Pyro"),
    "pyro2": ("on", "Monox, Pyro"),
    "pyro3": ("on", "Bloom, Pyro"),
    "pyro4": ("on", "Pyro IV, Pyro"),
    "pyro5": ("on", "Pyro V, Pyro"),
    "pyro5a": ("on", "Ignis, Pyro V, Pyro"),
    "pyro5b": ("on", "Vatra, Pyro V, Pyro"),
    "pyro5c": ("on", "Adir, Pyro V, Pyro"),
    "pyro5d": ("on", "Fairo, Pyro V, Pyro"),
    "pyro5e": ("on", "Fuego, Pyro V, Pyro"),
    "pyro5f": ("on", "Vuur, Pyro V, Pyro"),
    "pyro6": ("on", "Terminus, Pyro"),
    "rs_cargo_001": "Cargo Center",
    "rs_cz_rewards_001": "CZ Rewards Area, Checkmate",
    "rs_cz_rewards_003": "CZ Rewards Area, Orbituary",
    "rs_entry_cru-leo1": ("inside", "Seraphim Station"),
    "rs_entry_pyro-stan_jp1": "Stanton Gateway, Pyro",
    "rs_ext_cru-leo1": ("outside", "Seraphim Station, Crusader"),
    "rs_int_p2l4": "Checkmate Station, Monox, Pyro",
    "rs_int_p3leo": "Orbituary Station, Bloom, Pyro",
    "rs_int_p6l3": "Endgame, Pyro",
    "rs_int_p6leo_ruinstation": "Ruin Station, Terminus, Pyro",
    "rs_opendungeon_rund_002": "Contested Zone, Ruin Station",
    "rs_refinery_pyro": "Refinery",
    "sand01_vlk_001_001_int": ("in a", "Cave"),  # OLP cave
    "stanton1": ("on", "Hurston"),
    "stanton1a": ("on", "Arial, Hurston, Stanton"),
    "stanton1b": ("on", "Aberdeen, Hurston, Stanton"),
    "stanton1c": ("on", "Magda, Hurston, Stanton"),
    "stanton1d": ("on", "Ita, Hurston, Stanton"),
    "stanton2": ("on", "Crusader, Stanton"),
    "stanton2a": ("on", "Cellin, Crusader, Stanton"),
    "stanton2b": ("on", "Daymar, Crusader, Stanton"),
    "stanton2c": ("on", "Yela, Crusader, Stanton"),
    "stanton3": ("on", "ArcCorp, Stanton"),
    "stanton3a": ("on", "Lyria, ArcCorp, Stanton"),
    "stanton3b": ("on", "Wala, ArcCorp, Stanton"),
    "stanton4": ("on", "microTech, Stanton"),
    "stanton4a": ("on", "Calliope, microTech, Stanton"),
    "stanton4b": ("on", "Clio, microTech, Stanton"),
    "stanton4c": ("on", "Euterpe, microTech, Stanton"),
    # OLPs
    "orbtl_002_plat_001_util_a_orbital_001_occu_a_final": ("at an", "OLP"),
    "util_a_orbital_001_occu_a_final-001": ("outside an", "OLP"),
    "util_a_orbital_001_occu_a_final_int": ("inside an", "OLP"),
    # Hathor facilities
    "util_cmpd_wrhse_lge_001_rund_a_final_int": ("in a", "Large Warehouse A"),
    "util_cmpd_wrhse_lge_001_rund_b_final_int": ("in a", "Large Warehouse B"),
    "util_cmpd_wrhse_sml_001_rund_a_final_int": ("in a", "Small Warehouse A"),
    "util_cmpd_wrhse_sml_001_rund_a_final_int-004": ("in a", "Small Warehouse A"),
    "util_cmpd_wrhse_sml_001_rund_b_final_int-001": ("in a", "Small Warehouse B"),
    "util_cmpd_wrhse_sml_001_rund_c_final_int-001": ("in a", "Small Warehouse C"),
    "util_dish_001_rund_a_final_int": ("in a", "PAF 01 Main Building"),
    "util_dish_001_rund_b_final_int": ("in a", "PAF 02 Main Building"),
    "util_dish_001_rund_c_final_int": ("in a", "PAF 03 Main Building"),
    # Pyro RABs and clusters don't have zones
    # 4.1.1 Mining Bases
    "ab_mine_pyro_regiona_med_001": "RMB-PURI, Pyro I",
    "ab_mine_pyro_regiona_med_002": "RMB-BALM, Pyro I",
    "ab_mine_pyro_regiona_med_003": "RMB-ONER, Pyro I",
    "ab_mine_pyro_regiona_med_004": "RMB-KAIN, Pyro I",
    "ab_mine_pyro_regiona_med_005": "RMB-MYAL, Pyro I",
    "ab_mine_pyro_regiona_med_006": "RMB-CEDI, PYR1 L5",
    "ab_mine_pyro_regiona_med_007": "RMB-BALE, PYR1 L5",
    "ab_mine_pyro_regiona_med_008": "RMB-RIGG, PYR1 L5",
    "ab_mine_pyro_regiona_med_009": "RMB-VOES, PYR1 L4",
    "ab_mine_pyro_regiona_med_010": "RMB-IKAN, PYR1 L4",
    "ab_mine_pyro_regiona_med_011": "RMB-DREG, PYR1 L4",
    "ab_mine_pyro_regiona_med_012": "RMB-ZARF, PYR2 L1",
    "ab_mine_pyro_regiona_med_013": "RMB-GREX, PYR2 L1",
    "ab_mine_pyro_regiona_med_014": "RMB-SHEW, PYR2 L1",
    "ab_mine_pyro_regiona_med_015": "RMB-NAIN, PYR2 L2",
    "ab_mine_pyro_regiona_med_016": "RMB-LAZO, PYR2 L2",
    "ab_mine_pyro_regiona_med_017": "RMB-ELMS, PYR2 L2",
    "ab_mine_pyro_regiona_med_018": "RMB-LIRE, PYR2 L5",
    "ab_mine_pyro_regiona_med_019": "RMB-HOWE, PYR2 L5",
    "ab_mine_pyro_regiona_sml_001": "RMB-SURD, Pyro I",
    "ab_mine_pyro_regiona_sml_002": "RMB-NIGH, PYR2 L1",
    "ab_mine_pyro_regiona_sml_003": "RMB-EVEN, PYR2 L2",
    "ab_mine_pyro_regiona_sml_004": "RMB-TIAN, PYR2 L5",
    "ab_mine_pyro_regionb_med_001": "RMB-LEST, PYR3 L1 Starlight Service Station, Bloom",
    "ab_mine_pyro_regionb_med_002": "RMB-JONG, PYR3 L1 Starlight Service Station, Bloom",
    "ab_mine_pyro_regionb_med_003": "RMB-KNAP, PYR3 L1 Starlight Service Station, Bloom",
    "ab_mine_pyro_regionb_med_004": "RMB-OXID, PYR3 L1 Starlight Service Station, Bloom",
    "ab_mine_pyro_regionb_med_005": "RMB-PALL, PYR3 L2, Bloom",
    "ab_mine_pyro_regionb_med_006": "RMB-HELM, PYR3 L2, Bloom",
    "ab_mine_pyro_regionb_med_007": "RMB-BASK, PYR3 L2, Bloom",
    "ab_mine_pyro_regionb_med_008": "RMB-BUCK, PYR3 L2, Bloom",
    "ab_mine_pyro_regionb_med_009": "RMB-LUNE, Cluster BGR-560, Bloom",
    "ab_mine_pyro_regionb_med_010": "RMB-GRAY, Cluster BGR-560, Bloom",
    "ab_mine_pyro_regionb_med_011": "RMB-MAGE, Cluster BGR-560, Bloom",
    "ab_mine_pyro_regionb_med_012": "RMB-GADE, Cluster BGR-560, Bloom",
    "ab_mine_pyro_regionb_med_013": "RMB-WARB, Cluster BGR-560, Bloom",
    "ab_mine_pyro_regionb_med_014": "RMB-HORN, Cluster CAJ-445, Bloom",
    "ab_mine_pyro_regionb_med_015": "RMB-KIFF, Cluster CAJ-445, Bloom",
    "ab_mine_pyro_regionb_med_016": "RMB-MUGG, Cluster CAJ-445, Bloom",
    "ab_mine_pyro_regionb_med_017": "RMB-PEKE, Cluster CAJ-445, Bloom",
    "ab_mine_pyro_regionb_sml_001": "RMB-TACK, PYR3 L1 Starlight Service Station, Bloom",
    "ab_mine_pyro_regionb_sml_002": "RMB-AXIL, PYR3 L2, Bloom",
    "ab_mine_pyro_regionb_sml_003": "RMB-DARI, Cluster BGR-560, Bloom",
    "ab_mine_pyro_regionb_sml_004": "RMB-YEAD, Cluster CAJ-445, Bloom",
    "ab_mine_pyro_regionc_med_001": "RMB-NARY, PYR5 L1, Pyro V",
    "ab_mine_pyro_regionc_med_002": "RMB-JUTE, PYR5 L1, Pyro V",
    "ab_mine_pyro_regionc_med_003": "RMB-TYRO, PYR5 L1, Pyro V",
    "ab_mine_pyro_regionc_med_004": "RMB-SPAW, PYR5 L2 Gaslight",
    "ab_mine_pyro_regionc_med_005": "RMB-MURK, PYR5 L2 Gaslight",
    "ab_mine_pyro_regionc_med_006": "RMB-OLLA, PYR5 L2 Gaslight",
    "ab_mine_pyro_regionc_med_007": "RMB-KYUS, Cluster RSC-340, Pyro V",
    "ab_mine_pyro_regionc_med_008": "RMB-DORY, Cluster RSC-340, Pyro V",
    "ab_mine_pyro_regionc_med_009": "RMB-RODE, Cluster RSC-340, Pyro V",
    "ab_mine_pyro_regionc_med_010": "RMB-VERD, Cluster KKE-717, Pyro V",
    "ab_mine_pyro_regionc_med_011": "RMB-FLAG, Cluster KKE-717, Pyro V",
    "ab_mine_pyro_regionc_med_012": "RMB-RINE, Pyro V",
    "ab_mine_pyro_regionc_med_013": "RMB-ALME, Pyro V",
    "ab_mine_pyro_regionc_med_014": "RMB-OAKS, Pyro V",
    "ab_mine_pyro_regionc_med_015": "RMB-NONG, Pyro V",
    "ab_mine_pyro_regionc_med_016": "RMB-LANX, Cluster GRP-839, Pyro V",
    "ab_mine_pyro_regionc_med_017": "RMB-SIJO, Cluster GRP-839, Pyro V",
    "ab_mine_pyro_regionc_med_018": "RMB-ARID, Pyro V",
    "ab_mine_pyro_regionc_sml_001": "RMB-BORS, Cluster KKE-717, Pyro V",
    "ab_mine_pyro_regionc_sml_002": "RMB-LYES, Pyro V",
    "ab_mine_pyro_regionc_sml_003": "RMB-HADE, Pyro V",
    "ab_mine_pyro_regiond_med_001": "RMB-UMUS, Terminus",
    "ab_mine_pyro_regiond_med_002": "RMB-MEFF, Terminus",
    "ab_mine_pyro_regiond_med_003": "RMB-SOWL, Terminus",
    "ab_mine_pyro_regiond_med_004": "RMB-PIZE, Terminus",
    "ab_mine_pyro_regiond_med_005": "RMB-QINS, Terminus",
    "ab_mine_pyro_regiond_med_006": "RMB-RAWN, Terminus",
    "ab_mine_pyro_regiond_med_007": "RMB-LOWN, Terminus",
    "ab_mine_pyro_regiond_med_008": "RMB-CRUE, Terminus",
    "ab_mine_pyro_regiond_med_009": "RMB-MARA, Terminus",
    "ab_mine_pyro_regiond_med_010": "RMB-CHAM, Terminus",
    "ab_mine_pyro_regiond_med_011": "RMB-RAIK, Terminus",
    "ab_mine_pyro_regiond_med_012": "RMB-KELT, Terminus",
    "ab_mine_pyro_regiond_med_013": "RMB-MOSK, Terminus",
    "ab_mine_pyro_regiond_med_014": "RMB-JADE, Terminus",
    "ab_mine_pyro_regiond_med_015": "RMB-NENE, Terminus",
    "ab_mine_pyro_regiond_med_016": "RMB-DIRK, Cluster DLO-486, Terminus",
    "ab_mine_pyro_regiond_med_017": "RMB-PLEX, Cluster DLO-486, Terminus",
    "ab_mine_pyro_regiond_med_018": "RMB-TIGS, Cluster DLO-486, Terminus",
    "ab_mine_pyro_regiond_sml_001": "RMB-HARK, Terminus",
    "ab_mine_pyro_regiond_sml_002": "RMB-SEER, Terminus",
    "ab_mine_pyro_regiond_sml_003": "RMB-SAIC, Cluster DLO-486, Terminus",
    "ab_mine_stanton1_med_001": "Mining Base #IGB-FXW, Hurston",
    "ab_mine_stanton1_med_002": "Mining Base #YTO-GLQ, Hurston",
    "ab_mine_stanton1_med_003": "Mining Base #LBP-UN5, Hurston",
    "ab_mine_stanton1_med_004": "Mining Base #6IN-P02, Hurston",
    "ab_mine_stanton1_med_005": "Mining Base #01K-I43, Hurston",
    "ab_mine_stanton1_med_006": "Mining Base #BBR-4JQ, Hurston",
    "ab_mine_stanton1_med_007": "Mining Base #365-YNZ, Hurston",
    "ab_mine_stanton1_med_008": "Mining Base #ODD-E9B, Hurston",
    "ab_mine_stanton1_med_009": "Mining Base #WUO-ZRU, Hurston",
    "ab_mine_stanton1_sml_001": "Mining Base #7LI-0OA, Hurston",
    "ab_mine_stanton1_sml_002": "Mining Base #6RU-55R, Hurston",
    "ab_mine_stanton1_sml_003": "Mining Base #R08-Y3K, Hurston",
    "ab_mine_stanton2_med_001": "Mining Base #UU6-1EI, Crusader",
    "ab_mine_stanton2_med_002": "Mining Base #Q4U-I20, Crusader",
    "ab_mine_stanton2_med_003": "Mining Base #Z48-013, Crusader",
    "ab_mine_stanton2_med_004": "Mining Base #E38-S5G, Crusader",
    "ab_mine_stanton2_med_005": "Mining Base #W79-2H7, Crusader",
    "ab_mine_stanton2_med_006": "Mining Base #QXS-NBS, Crusader",
    "ab_mine_stanton2_med_007": "Mining Base #URB-H3V, Crusader",
    "ab_mine_stanton2_med_008": "Mining Base #R75-5PZ, Crusader",
    "ab_mine_stanton2_med_009": "Mining Base #IO3-H1F, Crusader",
    "ab_mine_stanton2_med_010": "Mining Base #51F-OGH, Crusader",
    "ab_mine_stanton2_sml_001": "Mining Base #90O-0HA, Crusader",
    "ab_mine_stanton2_sml_002": "Mining Base #4PI-3YY, Crusader",
    "ab_mine_stanton3_med_001": "Mining Base #CZW-RRY, ArcCorp",
    "ab_mine_stanton3_med_002": "Mining Base #7IQ-29Q, ArcCorp",
    "ab_mine_stanton3_med_003": "Mining Base #INX-KPJ, ArcCorp",
    "ab_mine_stanton3_med_004": "Mining Base #ZHY-77G, ArcCorp",
    "ab_mine_stanton3_med_005": "Mining Base #OYV-JKE, ArcCorp",
    "ab_mine_stanton3_med_006": "Mining Base #8CG-OSA, ArcCorp",
    "ab_mine_stanton3_med_007": "Mining Base #A73-HTJ, ArcCorp",
    "ab_mine_stanton3_med_008": "Mining Base #74H-2DO, ArcCorp",
    "ab_mine_stanton3_med_009": "Mining Base #BRE-582, ArcCorp",
    "ab_mine_stanton3_med_010": "Mining Base #6DO-K6A, ArcCorp",
    "ab_mine_stanton3_med_011": "Mining Base #118-NA2, ArcCorp",
    "ab_mine_stanton3_med_012": "Mining Base #4R0-NVX, ArcCorp",
    "ab_mine_stanton3_med_013": "Mining Base #8PV-WNE, ArcCorp",
    "ab_mine_stanton3_sml_001": "Mining Base #N6J-XKH, ArcCorp",
    "ab_mine_stanton3_sml_002": "Mining Base #RSV-8HL, ArcCorp",
    "ab_mine_stanton3_sml_003": "Mining Base #BSK-IJ5, ArcCorp",
    "ab_mine_stanton3_sml_004": "Mining Base #0YX-O7Z, ArcCorp",
    "ab_mine_stanton3_sml_005": "Mining Base #7YH-JX7, ArcCorp",
    "ab_mine_stanton3_sml_006": "Mining Base #PHB-DYC, ArcCorp",
    "ab_mine_stanton4_med_001": "Mining Base #1XA-3GI, microTech",
    "ab_mine_stanton4_med_002": "Mining Base #GO4-CH0, microTech",
    "ab_mine_stanton4_med_003": "Mining Base #AL5-XPD, microTech",
    "ab_mine_stanton4_med_004": "Mining Base #CVF-T6H, microTech",
    "ab_mine_stanton4_med_005": "Mining Base #U5X-NGQ, microTech",
    "ab_mine_stanton4_med_006": "Mining Base #JUG-0KZ, microTech",
    "ab_mine_stanton4_med_007": "Mining Base #UDK-IJX, microTech",
    "ab_mine_stanton4_med_008": "Mining Base #X92-IVA, microTech",
    "ab_mine_stanton4_med_009": "Mining Base #DU4-XBU, microTech",
    "ab_mine_stanton4_med_010": "Mining Base #734-A26, microTech",
    "ab_mine_stanton4_med_011": "Mining Base #XJZ-JR2, microTech",
    "ab_mine_stanton4_med_012": "Mining Base #Q9Q-090, microTech",
    "ab_mine_stanton4_med_013": "Mining Base #5U5-TLC, microTech",
    "ab_mine_stanton4_med_014": "Mining Base #SAG-2UN, microTech",
    "ab_mine_stanton4_sml_001": "Mining Base #C6P-3KJ, microTech",
    "ab_mine_stanton4_sml_002": "Mining Base #851-81H, microTech",
    "ab_mine_stanton4_sml_003": "Mining Base #TP1-N76, microTech",
    "ab_mine_stanton4_sml_004": "Mining Base #R7J-WJ7, microTech",
    "ab_mine_stanton4_sml_005": "Mining Base #0Z9-SVV, microTech",
    "ab_mine_stanton4_sml_006": "Mining Base #RCD-OB3, microTech",
    # 4.2.0 Associated Science and Development
    # Farro Datacenters
    "asd_labdata_int_01a": "Farro Data Center",
    # Lazarus
    "asd_labresearch_int_01a": "ASD Lazarus Complex Research Lab",
    "ht_station_001_occu_a_final_int": "ASD Lazarus Transport Hub Shuttle Station",
    "ht_xs_001_occu_a_final_int": "ASD Lazarus Transport Hub Lab",  # sever [sic] room (server), data analysis, research rooms
}
