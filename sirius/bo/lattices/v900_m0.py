from pyaccel import *

b_length_hedge     = 1.152 #[m]
b_length_segmented = 1.538 #[m]
half_model_diff    = (b_length_segmented - b_length_hedge)/2.0

lt       = Drift(fam_name = 'lt',      length = 2.146000)
lt2      = Drift(fam_name = 'lt2',     length = 2.146000-half_model_diff) 
l20      = Drift(fam_name = 'l20',     length = 0.200000)
l25      = Drift(fam_name = 'l25',     length = 0.250000)
l25_2    = Drift(fam_name = 'l25_2',   length = 0.250000-half_model_diff)
l30_2    = Drift(fam_name = 'l30_2',   length = 0.300000-half_model_diff)
l36      = Drift(fam_name = 'l36',     length = 0.360000)
l60      = Drift(fam_name = 'l60',     length = 0.600000)
l80      = Drift(fam_name = 'l80',     length = 0.800000)
l100     = Drift(fam_name = 'l100',    length = 1.000000)
lm25     = Drift(fam_name = 'lm25',    length = 1.896000)
lm30     = Drift(fam_name = 'lm30',    length = 1.846000)
lm40     = Drift(fam_name = 'lm40',    length = 1.746000)
lm45     = Drift(fam_name = 'lm45',    length = 1.696000)
lm60     = Drift(fam_name = 'lm60',    length = 1.546000)
lm66     = Drift(fam_name = 'lm66',    length = 1.486000)
lm70     = Drift(fam_name = 'lm70',    length = 1.446000)
lm120    = Drift(fam_name = 'lm120',   length = 0.946000)
lm105    = Drift(fam_name = 'lm105',   length = 1.096000)
lkk      = Drift(fam_name = 'lkk',     length = 0.741000)
lm60_kk  = Drift(fam_name = 'lm60_kk', length = 0.805000)

kick_in  = Marker(fam_name = 'kick_in')
kick_ex  = Marker(fam_name = 'kick_ex')
sept_in  = Marker(fam_name = 'sept_in')
sept_ex  = Marker(fam_name = 'sept_ex')
