import os
import numpy as np
import re
from read_file import read_files
from load_data import get_itemwise_scalars
from write_vtk import write_vtk
from add_bcs import add_scalars_limits
from add_bcs import add_coords_limits
from eq_calc import eq_calc_array

def main():
    #path = os.getcwd() + '\\10-2D-F2275-TCFE-AIMD-FittedWithYapfi'
    path = os.getcwd() + '\\10point_2Dtest'
    if not os.path.exists(path + '\\BCvtk'):
        os.makedirs(path + '\\BCvtk')
    [fvcc, mu, dmsize, mf, nel, ngd, nph, phf, time, el_names, ph_names,
     n_dim, hcc, k1c, ntp] = read_files(path)
    ngd_tot = np.prod(ngd)
    # Reshaping
    mf = np.reshape(mf, (ntp, ngd_tot*nel))
    mu = np.reshape(mu, (ntp, ngd_tot*nel))
    phf = np.reshape(phf, (ntp, ngd_tot*nph))
    coords_limits, ngd_ternary = np.zeros(3), np.zeros(3, dtype=int)
    for i in range(n_dim):
        coords_limits[i], ngd_ternary[i] = dmsize[i], ngd[i]
    fvcc_wl = add_coords_limits(fvcc, ngd_ternary, coords_limits, n_dim)
    ngd_bc = np.array([], dtype=int)
    for i in range(n_dim):
        ngd_bc = np.append(ngd_bc, ngd[i]+2)
    strtemp = 'total number of timesteps: '
    print(strtemp + str(ntp))
    strtemp = 'Enter timestep/s to post process(integers between 0 and '
    tstp_to_postprocess = [int(i) for i in input(strtemp +str(ntp-1) + '): /all/').split()]
    if not tstp_to_postprocess:
        tstp_to_postprocess = range(ntp-1)

    strtemp = 'Enter timestep/s to calculate HV and KIC (integers between 0 and '
    tstp_eq_calc = [int(i) for i in input(strtemp + str(ntp) + '):').split()]
    for i in tstp_to_postprocess:
        mf_ts = get_itemwise_scalars(mf[i][:], nel, ngd_tot)
        mu_ts = get_itemwise_scalars(mu[i][:], nel, ngd_tot)
        phf_ts = get_itemwise_scalars(phf[i][:], nph, ngd_tot)
        mf_bc = add_scalars_limits(mf_ts[0, :], ngd)
        mu_bc = add_scalars_limits(mu_ts[0, :], ngd)
        phf_bc = add_scalars_limits(phf_ts[0, :], ngd)
        for elidx in range(1, nel):
            app_temp = []
            app_temp = add_scalars_limits(mf_ts[elidx, :], ngd)
            mf_bc = np.vstack((mf_bc, app_temp))
            app_temp = []
            app_temp = add_scalars_limits(mu_ts[elidx, :], ngd)
            mu_bc = np.vstack((mu_bc, app_temp))
        for phidx in range(1, nph):
            app_temp = []
            app_temp = add_scalars_limits(phf_ts[phidx, :], ngd)
            phf_bc = np.vstack((phf_bc, app_temp))
        header_str = write_vtk(fvcc_wl, ngd_bc, i, el_names, ph_names, mf_bc, mu_bc, phf_bc)
        out_file_name = path + '\\BCvtk\\ts_bc_' + str(i) + '.vtk'
        fout = open(out_file_name, "w")
        fout.write(header_str)
        fout.close()
    '''%%%%%%%%%%%%%%%%%%
    KIC HV Eq calc ....
    %%%%%%%%%%%%%%%%%%'''
    thermodata = "TCFE8"
    kindata = ""
    temperature =1723.15
    pressure = 1e5
    '''Strip string after # '''
    ph_names_tmp = ph_names
    ph_names = []
    for phase in ph_names_tmp:
        ph_names.append(phase.split("#")[0])
    ''' calculate equilibrium for each times step '''
    ''' merge all calculations to one long string and submit to eq calc)'''
    for tstp in tstp_eq_calc:
        mf_tss = get_itemwise_scalars(mf[tstp][:], nel, ngd_tot)
        # equilibrium calc mf-tss
        [mf_str, wf_str, vpv_str, npm_str, y_str, x_ph_str] = \
            eq_calc_array(thermodata, temperature, pressure, el_names, ph_names, ngd_tot, mf_tss)
        print(mf_str)


"""                print('phases are: {}'.format(stable_phases))
                for phase, vpv_val, npm_val in zip(stable_phases, vpv, npm):
                    print('vpv({})'.format(phase), "=", vpv_val)
                    print(' npm({})'.format(phase), "=", npm_val)
#                    vpv_final.append([tstp, gp, phase, vpv_val])
#                    npm_final.append([tstp, gp, phase, vpv_val])
                for element, calc_mf_val in zip(el_names, calc_mf):
                    print('m-f({})'.format(element), "=", calc_mf_val)
#                    m_f_final.append([tstp, gp, element, calc_mf_val])
                for binary, x_in_phase_val in zip(binary_list, x_in_phase):
                    print('x({},{})='.format(binary[0], binary[1]), x_in_phase_val)
#                    x_ph_final.append([tstp, gp, binary[0], binary[1], x_in_phase_val])
                for binary, y_in_phase_val in zip(binary_list, y_in_phase):
                    print('y({},{})='.format(binary[0], binary[1]), y_in_phase_val)
#                    y_ph_final.append([tstp, gp, binary[0], binary[1], y_in_phase_val])"""



      # # hcc = np.reshape(hcc, (1, ngd_tot))
      # # k1c = np.reshape(k1c, (1, ngd_tot))
      # # header_str = write_vtk(fvcc_wl, ngd_bc, i, el_names, ph_names, mf_bc, mu_bc, phf_bc)
      # # hcc_bc = add_scalars_limits(hcc[0][:], ngd)
      # # k1c_bc = add_scalars_limits(k1c[0][:], ngd)
      # # header_str = header_str + 'SCALARS ' + 'HCC' + ' Double 1' + '\n' + 'LOOKUP_TABLE default' + '\n' \
      # #              + re.sub('[\[\]]', '', np.array_str(hcc_bc[0][:])) + '\n'
      # # header_str = header_str + 'SCALARS ' + 'K1C' + ' Double 1' + '\n' + 'LOOKUP_TABLE default' + '\n' \
      # #              + re.sub('[\[\]]', '', np.array_str(k1c_bc[0][:])) + '\n'
      # # out_file_name = path + '\\BCvtk\\ts_bc_' + str(i) + '.vtk'
      # # fout = open(out_file_name, "w")
      # # fout.write(header_str)

      # # fout.close()

if __name__ == "__main__":
    main()







## without boundary limits
# header_str = write_vtk(fvcc, ngd, i, el_names, ph_names, mf_ts, mu_ts, phf_ts)
# if i == ntp:
#    HCC = np.array(HCC)
#    header_str = header_str + 'SCALARS ' + 'HCC' + ' Double 1' + '\n' + 'LOOKUP_TABLE default' + '\n' + re.sub('[\[\]]', '', np.array_str(HCC[0][:])) + '\n'
# out_file_name = path + '\\vtk\\ts_' + str(i) + '.vtk'
# fout = open(out_file_name, "w")
# fout.write(header_str)
# fout.close()
# if not os.path.exists(path + '\\vtk'):
#   os.makedirs(path + '\\vtk')