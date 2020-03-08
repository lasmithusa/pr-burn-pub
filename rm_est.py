import math

## BASE 1RM METHODS ##

# TODO
# change base 1RM estimate methods to use seed set as first args

## Auxiliary Functions

def round_precision(num_to_round, precision):
    if precision:
        return precision * round(num_to_round / precision)
    else:
        return num_to_round

## Base R Rep Max Estimate Methods

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

## Master R Rep Max Estimate Function

def blind_r_rm(seed_set, reps_estimate, use_method='Average', precision=0.01, return_set=True):
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

    if return_set:
        if type(use_method) is str:
            return (round_precision(methods.get(use_method), precision), reps_estimate)
        else:
            return {key: value for (key, value) in ((method, (round_precision(methods.get(method), precision), reps_estimate)) for method in use_method)}
    else:
        if type(use_method) is str:
            return (round_precision(methods.get(use_method), precision))
        else:
            return {key: value for (key, value) in ((method, (round_precision(methods.get(method), precision))) for method in use_method)}