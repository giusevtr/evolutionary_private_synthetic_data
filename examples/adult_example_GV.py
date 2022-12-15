import jax.random
import itertools
from examples.run_example import generate_private_SD, run_experiment
from models_v2 import PrivGA, RelaxedProjection
from stats_v2 import Marginals, TwoWayPrefix
from utils.utils_data import get_data
import jax.numpy as jnp

import pdb

if __name__ == "__main__":

    # Get Data
    # ROUNDS=4
    # data = get_data('adult', 'adult-small', root_path='../data_files/')
    ROUNDS=15
    data_name = 'folktables_income_2018_NY-cat'
    data = get_data('folktables_income_2018_NY-mixed', data_name, root_path='../data_files/')
    # data = get_data('adult', 'adult', root_path='../data_files/')

    # Create statistics and evaluate
    marginal_module = Marginals.get_all_kway_combinations(data.domain, k=3)
    # marginal_module = Marginals(data.domain, [('capital-gain', 'capital-loss'), ])
    marginal_module.fit(data)
    # reg_marginal_module = Marginals.get_all_kway_combinations(data.domain, k=1)
    # print(f'num queries = {marginal_module.get_num_queries()}')
    #
    print(marginal_module.get_num_queries())
    # rap = RelaxedProjection(domain=data.domain,
    #                         data_size=1000,
    #                         iterations=5000,
    #                         learning_rate=0.005,
    #                         print_progress=False,
    #                         )
    #
    # key = jax.random.PRNGKey(0)
    # sync_data_2 = rap.fit_dp_adaptive(key, stat_module=marginal_module,
    #                  rounds=ROUNDS, epsilon=1, delta=1e-6)
    # errros = marginal_module.get_sync_data_errors(sync_data_2.to_numpy())
    # print(f'RAP: max error = {errros.max():.5f}')


    # Choose algorithm parameters
    priv_ga = PrivGA(domain=data.domain,
                     popsize=100,
                    top_k=2,
                    num_generations=15000,
                    stop_loss_time_window=500,
                    print_progress=True,
                    start_mutations=32,
                     data_size=1000,
                     regularization_statistics=None
                     )
    epsilon_list = []
    seed_list = [0,1,2,3,4]
    # Generate differentially private synthetic data with ADAPTIVE mechanism
    for epsilon, seed in itertools.product(epsilon_list, seed_list):
        key = jax.random.PRNGKey(seed)
        sync_data_2 = priv_ga.fit_dp(key, stat_module=marginal_module,
                         # rounds=ROUNDS,
                                     epsilon=epsilon, delta=1e-6)
        true_stats = marginal_module.true_stats
        fn = marginal_module.get_stats_fn()
        sync_stats = fn(sync_data_2)
        errors = jnp.abs(true_stats - sync_stats)
        error = jnp.linalg.norm(errors, ord=1)
        error_l2 = jnp.linalg.norm(errors, ord=2)
        max_error = errors.max()
        print(f'Final L1 error = {error:.5f}, L2 error = {error_l2:.5f},  max error ={max_error:.5f}\n')
        # errros = marginal_module.get_sync_data_errors(sync_data_2.to_numpy())
        print(f'PrivGA: max error = {errros.max():.5f}')


