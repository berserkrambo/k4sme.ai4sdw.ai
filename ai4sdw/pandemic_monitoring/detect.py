import numpy as np

def get_distance_matrix(center_points_plan):
    number_of_peds = len(center_points_plan)
    distance_matrix = np.zeros((number_of_peds, number_of_peds)) + np.nan
    starting_j = 0

    for i in range(number_of_peds):
        for j in range(starting_j, number_of_peds):
            if i == j:
                continue
            point3d_1 = center_points_plan[i]
            point3d_2 = center_points_plan[j]
            distance_pred = np.linalg.norm(point3d_1 - point3d_2)
            distance_matrix[i, j] = distance_pred
            distance_matrix[j, i] = distance_pred
        starting_j += 1

    return distance_matrix


def get_individual_risk(distance_matrix, eta, beta, tau):
    number_of_peds = distance_matrix.shape[0]
    if number_of_peds <= 1:
        return 0
    individual_risks = np.zeros((number_of_peds,))

    for i in range(number_of_peds):
        conditioned_risks = []
        for j in range(number_of_peds):
            if i != j:
                p = eta * np.exp(-beta * np.maximum(0, distance_matrix[i, j] - tau))
                conditioned_risks.append(p)
        individual_risks[i] = np.max(conditioned_risks)

    return individual_risks


def get_global_risk(individual_risks, capacity=4):
    return np.minimum(1, np.sum(individual_risks) / capacity)


def get_dynamic_global_risk(global_risks):
    return np.mean(global_risks)


def get_distance_level(center_points, eta, beta, tau, area_capacity, worker):
    distance_matrix = get_distance_matrix(center_points)

    individual_risks = get_individual_risk(
        distance_matrix,
        eta=eta,
        beta=beta,
        tau=tau
    )
    global_risk = get_global_risk(individual_risks, capacity=area_capacity) * 100

    risk_table = [i*10 for i in range(11)]
    risk_cmp = [np.linalg.norm(i*10 - global_risk) for i in range(11)]
    id_cmp = np.argmin(risk_cmp)

    return risk_table[id_cmp]

