import numpy as np
import os

def read_files(path):
    print(path)
    fname = ''.join(path + '/FINITE_VOLUME_CENTROID_COORDINATES.TXT')
    with open(fname, 'r') as f:
        fin_volcentr_coord = np.array([float(line) for line in f])
    f.close()
    fname = ''.join(path + '/CHEMICAL_POTENTIALS.TXT')
    with open(fname, 'r') as f:
        chem_potentials = np.array([float(line) for line in f])
    f.close()
    fname = ''.join(path + '/DOMAIN_SIZE.TXT')
    with open(fname, 'r') as f:
        domain_size = np.array([float(line) for line in f])
    f.close()
    fname = ''.join(path + '/GRADIENT_ENERGY_CONTRIBUTION.TXT')
    with open(fname, 'r') as f:
        grad_energy_contr = np.array([float(line) for line in f])
    f.close()
    fname = ''.join(path + '/MOLE_FRACTIONS.TXT')
    with open(fname, 'r') as f:
        mole_fractions = np.array([float(line) for line in f])
    f.close()
    fname = ''.join(path + '/NUMBER_OF_ELEMENTS.TXT')
    with open(fname, 'r') as f:
        n_elements= np.array([int(line) for line in f])
    f.close()
    fname = ''.join(path + '/NUMBER_OF_GRID_POINTS.TXT')
    with open(fname, 'r') as f:
        n_gridpoints= np.array([int(line) for line in f])
    f.close()
    fname = ''.join(path + '/NUMBER_OF_PHASES.TXT')
    with open(fname, 'r') as f:
        n_phases = np.array([int(line) for line in f])
    f.close()
    fname = ''.join(path + '/PERMEABILITIES.TXT')
    with open(fname, 'r') as f:
        permeabilities = np.array([float(line) for line in f])

    f.close()
    fname = ''.join(path + '/PHASE_FIELD.TXT')
    with open(fname, 'r') as f:
        ph_field = np.array([float(line) for line in f])
    f.close()
    fname = ''.join(path + '/PHASE_FRACTIONS.TXT')
    with open(fname, 'r') as f:
        ph_fractions = np.array([float(line) for line in f])
    f.close()
    fname = ''.join(path + '/TIME.TXT')
    with open(fname, 'r') as f:
        time = np.array([float(line) for line in f])
    f.close()
    fname = ''.join(path + '/ELEMENT_NAMES.TXT')
    with open(fname, 'r') as f:
        el_names = f.read().split()
    f.close()	
    fname = ''.join(path + '/PHASE_NAMES.TXT')
    with open(fname, 'r') as f:
        ph_names = f.read().split()
    f.close()
    fname = ''.join(path + '/DIMENSIONALITY.TXT')
    with open(fname, 'r') as f:
        n_dimensions = np.array([int(line) for line in f])
    f.close()
    hcc = {}
    k1c = {}
    hccexist = os.path.exists(path + '/HCC.TXT')
    k1cexist = os.path.exists(path + '/K1C.TXT')
    if hccexist:
        fname = ''.join(path + '/HCC.TXT')
        with open(fname, 'r') as f:
            hcc = np.array([float(line) for line in f])
        f.close()
    if k1cexist:
        fname = ''.join(path + '/K1C.TXT')
        with open(fname, 'r') as f:
            k1c = np.array([float(line) for line in f])
        f.close()
    ntstp, nel, nph, n_dim = np.size(time), n_elements[0],  n_phases[0],  n_dimensions[0]

    return fin_volcentr_coord, chem_potentials, domain_size, mole_fractions, nel, n_gridpoints, nph, ph_fractions, \
           time, el_names, ph_names, n_dim, hcc, k1c, ntstp



#grad_energy_contr, permeabilities, ph_field,
# for line in f:
#    numbers.append(float(line.strip()))
# fin_volcentr_coord = map(float, f)
# fin_volcentr_coord = float(f.read().splitlines())