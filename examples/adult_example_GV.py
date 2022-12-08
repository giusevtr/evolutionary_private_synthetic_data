from examples.run_example import generate_private_SD, run_experiment
from models import PrivGA, RelaxedProjection
from stats import Marginals, TwoWayPrefix
from utils.utils_data import get_data

import pdb

if __name__ == "__main__":

    # Get Data
    data = get_data('adult', 'adult-mini', root_path='../data_files/')

    get_gen_list = [
        # RelaxedProjection.get_generator(learning_rate=0.01),
        PrivGA.get_generator(popsize=10000,
                             top_k=10,
                             num_generations=200,
                             stop_loss_time_window=50,
                             print_progress=True)
    ]

    stat_module_list = [
        Marginals.get_all_kway_combinations(data.domain, k=2),
    ]
    run_experiment(data,
                   data_name='adult',
                   generators=get_gen_list,
                   stat_modules=stat_module_list,
                   epsilon_list=[1.0],
                   # epsilon_list=[0.07, 0.15, 0.23, 0.41, 0.52, 0.62, 0.74, 0.87, 1.0],
                   seed_list=[0],
                   plot_results=True,
                   data_size=100)

