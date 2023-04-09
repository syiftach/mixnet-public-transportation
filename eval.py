import time
import os
import matplotlib.pyplot as plt

from mot_app import app_demo, MAX_N_MSGS, MAX_N_CLIENTS
from NetworkNode.utils import save_pickle, load_pickle
from NetworkNode import POOL_SIZE

# N_CLIENT = [2 ** n for n in range(5, 13)]
N_CLIENT = [32, 64, 128, 256, 512, 1024, 2048, 4096]
N_RELAYS = 3
DEFAULT_N_MSGS = 4
DEFAULT_N_CLIENTS = 16
POOL_SIZES = [16, 32, 64, 128]


def evaluate_performance_wrt_n_clients():
    throughput_arr = []
    latency_arr = []
    for n_clients in N_CLIENT:
        # measure th starting time
        start = time.time()
        # run the app
        app_demo(n_relays=N_RELAYS, n_clients=n_clients, n_msgs=DEFAULT_N_MSGS)
        # measure the end time
        end = time.time()
        # add the average to the throughput array
        throughput_arr.append((DEFAULT_N_MSGS * n_clients) / (end - start))
        latency_arr.append((end - start) / (DEFAULT_N_MSGS * n_clients))
        time.sleep(2)
        # save_pickle(f'pkl/thr_n_clients_pool={POOL_SIZE}.pkl', throughput_arr)
    return throughput_arr, latency_arr


def plot_throughput(eval_func: callable, save=False):
    thr_arr, lat_arr = eval_func()
    fig, axis = plt.subplots(1, 2)

    axis[0].set_title(f'Throughput (pool size={POOL_SIZE})')
    axis[0].set_xlabel('n_clients')
    axis[0].set_ylabel('msgs/second')
    axis[0].plot(N_CLIENT, thr_arr, marker='.', lw=1.5, color='orange')

    axis[1].set_title(f'Latency (pool size={POOL_SIZE})')
    axis[1].set_xlabel('n_clients')
    axis[1].set_ylabel('seconds')
    axis[1].plot(N_CLIENT, lat_arr, marker='.', lw=1.5, color='purple')

    fig.show()

    if save:
        i = 1
        filename = f'{eval_func.__name__}-pool={POOL_SIZE}-{{i}}'
        while os.path.exists(f'./png/{filename.format(i=i)}.png') and i < 100:
            i += 1
        filename = filename.format(i=i)
        fig.savefig(f'./png/{filename}.png')
        save_pickle(f'./pkl/{filename}-throughput.pkl', thr_arr)
        save_pickle(f'./pkl/{filename}-latency.pkl', lat_arr)


if __name__ == '__main__':
    plot_throughput(evaluate_performance_wrt_n_clients, save=True)
