import numpy, scipy
from scipy.constants import k as k_B

NUM_SPIN  = 100
NUM_STEP  = 20000
NUM_FIELD = 51

def get_ene_diff(config, i : int, ising_h : float, ising_j : float):
    """Return the energy difference of flipping spin i.
    Args:
        config (numpy.ndarray): The current configuration.
        i (int): The index of the spin to flip.
        ising_h (float): The external field.
        ising_j (float): The coupling constant.

    Returns:
        ene_diff (float): The energy difference of flipping spin i.
    """

    ene_diff  = 2.0 * config[i % 100] * ising_h
    ene_diff += 2.0 * config[i % 100] * config[(i-1) % 100] * ising_j
    ene_diff += 2.0 * config[i % 100] * config[(i+1) % 100] * ising_j
    return ene_diff

def kernel(config: numpy.ndarray, ising_h: float, ising_j: float, beta: float, max_sweep: int):
    """Perform a Monte Carlo sweep.
    Args:
        config (numpy.ndarray): The current configuration.
        ising_h (float): The external field.
        ising_j (float): The coupling constant.
        beta (float): The inverse temperature.
        nsteps (int): The number of Monte Carlo steps to perform.

    Returns:
        config (numpy.ndarray): The new configuration.
    """

    m_list = []

    isweep = 0
    print("\nSetting up Ising model.", flush=True)
    print("num_spin = ", config.shape[0], flush=True)
    print("beta     = % 6.4f" % beta, flush=True)
    print("ising_h  = % 6.4f" % ising_h, flush=True)
    print("ising_j  = % 6.4f" % ising_j, flush=True)

    print("\nPerforming sweep...")
    while isweep < max_sweep:
        for i in range(NUM_SPIN):
            ene_diff = get_ene_diff(config, i, ising_h, ising_j)
            if ene_diff <= 0.0:
                config[i] *= -1
            elif numpy.random.rand() < numpy.exp(-beta * ene_diff):
                config[i] *= -1
        
        if isweep / max_sweep * 100 % 10 == 0:
            print(f"MC progress: {(isweep / max_sweep * 100): 8.4f}%", flush=True)

        m_list.append(numpy.sum(config))
        isweep += 1
        
    return m_list

if __name__ == "__main__":
    import sys
    temp = float(sys.argv[1])

    mm = []
    
    for h in numpy.linspace(-2.0, 2.0, NUM_FIELD):
        config0 = numpy.ones(NUM_SPIN, dtype = int)
        config0[numpy.random.choice(NUM_SPIN, NUM_SPIN//2, replace = False)] = -1
        m_list = kernel(config0.copy(), h, 1.0, 1.0/temp, NUM_STEP)
        mm.append(m_list)

    mm = numpy.asarray(mm)
    mm.reshape((NUM_FIELD, NUM_STEP))

    numpy.savetxt(f"./data/ising_1d_temp_{temp:6.4f}.csv", mm, fmt = "%12.8f", delimiter = ", ")
