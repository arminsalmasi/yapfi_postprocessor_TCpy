from tc_python import *
import itertools as itertool

def eq_calc_array(database, tempera, press, element_names, phase_names, ngd, mf_in):
    mf_out, wf_out, vpv_out, npm_out, x_ph_out, y_ph_out = [], [], [], [], [], []
    with TCPython() as tcp:
        system_int = tcp.select_database_and_elements(database, element_names).without_default_phases()
        for phase in phase_names:
            system_int.select_phase(phase)
        system = system_int.get_system()
        calc = system.with_single_equilibrium_calculation()
        calc.set_condition(ThermodynamicQuantity.temperature(), tempera)
        calc.set_condition(ThermodynamicQuantity.pressure(), press)
        for gp in range(ngd):
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" + " grid point= ", str(gp))
            #for i in range(len(element_names) - 1):
            cnt = 1
            for element in element_names[0:-1]:
                #calc.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component((element_names[i])), mf_in[i][gp])
                calc.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component((element)), mf_in[cnt][gp])
                cnt += 1
            calc_res = calc.calculate()
            stable_phases = calc_res.get_stable_phases()
            ''' vlaue holders of the time step '''
            #calc_mf, wf, x_in_phase, y_in_phase, vpv, npm, wf, y_in_phase = [], [], [], [], [], [], [], []
            ''' Binary (phase, element) pairs'''
            binary_list = list(itertool.product(stable_phases, element_names))
            for element in element_names:
                #calc_mf.append(calc_res.get_value_of('x({})'.format(element)))
                mf_out.append(calc_res.get_value_of('x({})'.format(element)))
                #wf.append(calc_res.get_value_of('w({})'.format(element)))
                wf_out.append(calc_res.get_value_of('w({})'.format(element)))
            for phase in stable_phases:
                vpv_out.append(calc_res.get_value_of('vpv({})'.format(phase)))
                npm_out.append(calc_res.get_value_of('npm({})'.format(phase)))
            for binary in binary_list:
                x_ph_out.append(calc_res.get_value_of('x({},{})'.format(binary[0], binary[1])))
            for binary in binary_list:
                try:
                    y_ph_out.append(calc_res.get_value_of('y({},{})'.format(binary[0], binary[1])))
                except Exception as error:
                    print('y({},{})=error'.format(binary[0], binary[1]))
                    y_ph_out.append(-1)
            '''print(vpv_out)
            print(npm_out)
            print(x_ph_out)
            print(y_ph_out)
            print(mf_out)
            print(wf_out)'''
    return mf_out, wf_out, vpv_out, npm_out, y_ph_out, x_ph_out
