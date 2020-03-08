# TODO
# 1. Provide sets input as tuple where index 0 contains the reps for set 1, index 1 contains the reps for set 2, and so on
# 2. Calculate set fatigue as the product of the fatigue rate and rep factor where the rep factor
#   for set n is calculated as sum(reps(1):reps(n-1)) / reps(n))
# 3. Eventually calculate set fatigue to account for changes in weight AND reps
# 4. Pass named arguments
# 5. Specify which formula is desired when calling r_rm()
#   5a. set default to average

# TERMS
# blind - unweighted
# group - collection of sets

import math

# 1x1 FORMULAS
# Lombardi = w*r^(1/10)
# Brzycki = w*(36/(37 - r))
# Epley = w*(1 + (r/30))
# Mayhew = (w*100) / (52.2 + (41.9 * e^(-0.055*r)))
# O'Conner = w * (1 + 0.025*r)
# Wathan = (w*100) / (48.8 + (53.8 * e^(-0.075*r)))
# Lander = (w*100) / (101.3 - 2.67123*r)

# 1xR FORMULAS
# Lombardi_R = Lombardi / (R^(1/10))
# Brzycki_R = Brzycki / (36/(37 - R))
# Epley_R = Epley / (1 + (R/30))
# Mayhew_R = Mayhew * (52.2 + (41.9^(-0.055*R))) / 100
# O'Conner_R = O'Conner / (1 + 0.025*R)
# Wathan_R = Wathan * (48.8 + (53.8^(-0.075*R))) / 100
# Lander_R = Lander * (101.3 - 2.67123*R) / 100

# SET FATIGUE FORMULA (1xR max)
# RM(reps=3, sets=1) = RM(reps=3, set=3)*(1+(3-1)*set_fatigue_rate)

## Auxiliary Functions

def round_precision(num_to_round, precision):
    if precision:
        return precision * round(num_to_round / precision)
    else:
        return num_to_round

## Individual R Rep Max Formulas

def lombardi_rm(weight_lifted, reps_completed, reps_estimate):
    if reps_completed == 1:
        return weight_lifted
    else:
        lombardi_r1 = weight_lifted * reps_completed ** (1/10)
        if reps_estimate == 1:
            return lombardi_r1
        else:
            return lombardi_r1 / (reps_estimate ** (1/10))

def bryzcki_rm(weight_lifted, reps_completed, reps_estimate):
    if reps_completed == 1:
        return weight_lifted
    else:
        bryzcki_r1 = weight_lifted * (36 / (37 - reps_completed))
        if reps_estimate == 1:
            return bryzcki_r1
        else:
            return bryzcki_r1 / (36 / (37 - reps_estimate))

def epley_rm(weight_lifted, reps_completed, reps_estimate):
    if reps_completed == 1:
        return weight_lifted
    else:    
        epley_r1 = weight_lifted * (1 + (reps_completed/30))
        if reps_estimate == 1:
            return epley_r1
        else:
            return epley_r1 / (1 + (reps_estimate/30))

def mayhew_rm(weight_lifted, reps_completed, reps_estimate):
    if reps_completed == 1:
        return weight_lifted
    else:
        mayhew_r1 = (weight_lifted * 100) / (52.2 + (41.9 * math.exp(-0.055 * reps_completed)))
        if reps_estimate == 1:
            return mayhew_r1
        else:
            return mayhew_r1 * (52.2 + (41.9 * math.exp((-0.055 * reps_estimate)))) / 100

def oconner_rm(weight_lifted, reps_completed, reps_estimate):
    if reps_completed == 1:
        return weight_lifted
    else:
        oconner_r1 = weight_lifted * (1 + 0.025 * reps_completed)
        if reps_estimate == 1:
            return oconner_r1
        else:
            return oconner_r1 / (1 + 0.025 * reps_estimate)

def wathan_rm(weight_lifted, reps_completed, reps_estimate):
    if reps_completed == 1:
        return weight_lifted
    else:
        wathan_r1 = (weight_lifted * 100) / (48.8 + (53.8 * math.exp((-0.075 * reps_completed))))
        if reps_estimate == 1:
            return wathan_r1
        else:
            return wathan_r1 * (48.8 + (53.8 * math.exp(-0.075 * reps_estimate))) / 100

def lander_rm(weight_lifted, reps_completed, reps_estimate):
    if reps_completed == 1:
        return weight_lifted
    else:
        lander_r1 = (weight_lifted * 100) / (101.3 - 2.67123 * reps_completed)
        if reps_estimate == 1:
            return lander_r1
        else:
            return lander_r1 * (101.3 - 2.67123 * reps_estimate) / 100

def average_rm(weight_lifted, reps_completed, reps_estimate):
    average = (lombardi_rm(weight_lifted, reps_completed, reps_estimate) + \
                bryzcki_rm(weight_lifted, reps_completed, reps_estimate) + \
                epley_rm(weight_lifted, reps_completed, reps_estimate) + \
                mayhew_rm(weight_lifted, reps_completed, reps_estimate) + \
                oconner_rm(weight_lifted, reps_completed, reps_estimate) + \
                wathan_rm(weight_lifted, reps_completed, reps_estimate) + \
                lander_rm(weight_lifted, reps_completed, reps_estimate)) / 7
    return average

## 1xR Rep Max Calculators

# 1xR rep max without regard for sets - 1xR Blind Calculator

def blind_r_rm(seed_set, reps_estimate, use_method='Average', precision=0.01):
    weight_lifted, reps_completed = seed_set

    methods = {
        'Average': average_rm(weight_lifted, reps_completed, reps_estimate),
        'Bryzcki': bryzcki_rm(weight_lifted, reps_completed, reps_estimate),
        'Epley': epley_rm(weight_lifted, reps_completed, reps_estimate),
        'Lander': lander_rm(weight_lifted, reps_completed, reps_estimate),
        'Lombardi': lombardi_rm(weight_lifted, reps_completed, reps_estimate),
        'Mayhew': mayhew_rm(weight_lifted, reps_completed, reps_estimate),
        'OConner': oconner_rm(weight_lifted, reps_completed, reps_estimate),
        'Wathan': wathan_rm(weight_lifted, reps_completed, reps_estimate),
    }

    if type(use_method) is str:
        return (round_precision(methods.get(use_method), precision), reps_estimate)
    else:
        return {key: value for (key, value) in ((method, (round_precision(methods.get(method), precision), reps_estimate)) for method in use_method)}


if __name__ == "__main__":
    # 1xR rep max weighting function - 1xR Weighter
    # Takes set fatigue into consideration and returns weighted max estimates

    # def r_rm_weighter(blind_rm_group, fatigue_rate='0.015', precision=0.01):
    #     for  in blind_rm_group:

    print(blind_r_rm((175, 5), 1, precision=1, use_method=('Average', 'Bryzcki', 'Epley', 'Lander', 'Lombardi', 'Mayhew', 'OConner', 'Wathan')))