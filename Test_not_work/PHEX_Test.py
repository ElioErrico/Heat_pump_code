from __future__ import division, print_function, absolute_import
import CoolProp as CP
from CoolProp.CoolProp import PropsSI
from ACHP.PHEHX import PHEHXClass
from math import pi
import matplotlib.pyplot as plt

def test_WyattPHEHX():
    """
    Test case for Plate Heat Exchanger based on WyattPHEHX example
    """
    # Abstract State        
    Ref_c = 'R134a'
    Backend_c = 'HEOS'
    AS_c = CP.AbstractState(Backend_c, Ref_c)
    Ref_h = 'Water'
    Backend_h = 'HEOS'
    AS_h = CP.AbstractState(Backend_h, Ref_h)
    
    Tdew = PropsSI('T', 'P', 962833, 'Q', 1.0, Ref_c)
    params = {
        'AS_c': AS_c,
        'mdot_c': 0.073,
        'pin_c': 962833,
        'hin_c': PropsSI('H', 'T', Tdew, 'Q', 0.0, Ref_c),  # [J/kg-K]
        'xin_c': 0.0,
        
        'AS_h': AS_h,
        'mdot_h': 100.017,
        'pin_h': PropsSI('P', 'T', 115.5+273.15, 'Q', 1, Ref_h),
        'hin_h': PropsSI('H', 'T', 115.5+273.15, 'Q', 1, Ref_h),  # [J/kg-K]
        
        # Geometric parameters
        'HXType': 'Plate-HX',  # choose the type of IHX
        'Bp': 0.119,
        'Lp': 0.526,  # Center-to-center distance between ports
        'Nplates': 110,
        'PlateAmplitude': 0.00102,  # [m]
        'PlateThickness': 0.0003,  # [m]
        'PlateWavelength': 0.0066,  # [m]
        'InclinationAngle': pi/3,  # [rad]
        'PlateConductivity': 15.0,  # [W/m-K]
        'Rp': 1.0,  # [microns] Surface roughness
        'MoreChannels': 'Hot',  # Which stream gets the extra channel, 'Hot' or 'Cold'
    
        'Verbosity': 10,
        
        'h_tp_cold_tuning': 1,
        'h_tp_hot_tuning': 1,
        'DP_hot_tuning': 1,
        'DP_cold_tuning': 1
    }
    
    # Create and calculate the heat exchanger
    PHE = PHEHXClass(**params)
    PHE.Calculate()
    
    # Print some key results
    print("Heat transfer rate [W]:", PHE.Q)
    print("Hot side outlet temperature [K]:", PHE.Tout_h)
    print("Cold side outlet temperature [K]:", PHE.Tout_c)
    print("Hot side pressure drop [kPa]:", -PHE.DP_h/1000)
    print("Cold side pressure drop [kPa]:", -PHE.DP_c/1000)
    
    # Return the full output list for detailed inspection
    return PHE.OutputList()

def test_SWEPVariedmdot():
    """
    Test case for SWEP heat exchanger with varied mass flow rates
    """
    # Abstract State        
    Ref_c = 'R290'
    Backend_c = 'HEOS'
    AS_c = CP.AbstractState(Backend_c, Ref_c)
    Ref_h = 'Water'
    Backend_h = 'HEOS'
    AS_h = CP.AbstractState(Backend_h, Ref_h)
    
    Tin = 8+273.15
    results = []
    
    for mdot_h in [0.4176, 0.5013, 0.6267, 0.8357, 1.254, 2.508]:
        params = {
            'AS_c': AS_c,
            'mdot_c': 0.03312,
            'pin_c': PropsSI('P', 'T', Tin, 'Q', 1.0, Ref_c),
            'hin_c': PropsSI('H', 'T', Tin, 'Q', 0.15, Ref_c),  # [J/kg-K]
            
            'AS_h': AS_h,
            'mdot_h': mdot_h,
            'pin_h': 200000,
            'hin_h': PropsSI('H', 'T', 15+273.15, 'P', 200000, Ref_h),  # [J/kg-K]
            
            # Geometric parameters
            'HXType': 'Plate-HX',  # choose the type of IHX
            'Bp': 0.101,
            'Lp': 0.455,  # Center-to-center distance between ports
            'Nplates': 46,
            'PlateAmplitude': 0.00102,  # [m]
            'PlateThickness': 0.0003,  # [m]
            'PlateWavelength': 0.00626,  # [m]
            'InclinationAngle': 65/180*pi,  # [rad]
            'PlateConductivity': 15.0,  # [W/m-K]
            'Rp': 1.0,  # [microns] Surface roughness
            'MoreChannels': 'Hot',  # Which stream gets the extra channel, 'Hot' or 'Cold'
        
            'Verbosity': 0,
            
            'h_tp_cold_tuning': 1,
            'h_tp_hot_tuning': 1,
            'DP_hot_tuning': 1,
            'DP_cold_tuning': 1
        }
        
        PHE = PHEHXClass(**params)
        PHE.Calculate()
        
        print(f"Mass flow rate: {mdot_h} kg/s")
        print(f"Heat transfer: {PHE.Q} W, HTC: {PHE.h_subcooled_h} W/m²K, DP: {-PHE.DP_h/1000} kPa")
        
        results.append((mdot_h, PHE.Q, PHE.h_subcooled_h, -PHE.DP_h/1000))
    
    # Plot results
    mdot_values = [r[0] for r in results]
    Q_values = [r[1] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(mdot_values, Q_values, 'o-')
    plt.xlabel('Mass Flow Rate [kg/s]')
    plt.ylabel('Heat Transfer Rate [W]')
    plt.title('Heat Transfer vs Mass Flow Rate')
    plt.grid(True)
    plt.savefig('SWEP_HeatTransfer.png')
    plt.close()
    
    return results


def test_SamplePHEHX():
    """
    Test case for Plate Heat Exchanger based on SamplePHEHX example
    """
    # Abstract State        
    Ref_c = 'R290'
    Backend_c = 'HEOS'
    AS_c = CP.AbstractState(Backend_c, Ref_c)
    Ref_h = 'Water'
    Backend_h = 'HEOS'
    AS_h = CP.AbstractState(Backend_h, Ref_h)
    
    TT = []
    QQ = []
    Q1 = []
    Tin = 8+273.15
    results = []
    
    for mdot_h in [0.4176, 0.5013, 0.6267, 0.8357, 1.254, 2.508]:
        params = {
            'AS_c': AS_c,
            'mdot_c': 0.03312,
            'pin_c': PropsSI('P', 'T', Tin, 'Q', 1.0, Ref_c),
            'hin_c': PropsSI('H', 'T', Tin, 'Q', 0.15, Ref_c),  # [J/kg-K]
            
            'AS_h': AS_h,
            'mdot_h': mdot_h,
            'pin_h': 200000,
            'hin_h': PropsSI('H', 'T', 15+273.15, 'P', 200000, Ref_h),  # [J/kg-K]
            
            # Geometric parameters
            'HXType': 'Plate-HX',  # choose the type of IHX
            'Bp': 0.101,
            'Lp': 0.455,  # Center-to-center distance between ports
            'Nplates': 46,
            'PlateAmplitude': 0.00102,  # [m]
            'PlateThickness': 0.0003,  # [m]
            'PlateWavelength': 0.00626,  # [m]
            'InclinationAngle': 65/180*pi,  # [rad]
            'PlateConductivity': 15.0,  # [W/m-K]
            'Rp': 1.0,  # [microns] Surface roughness
            'MoreChannels': 'Hot',  # Which stream gets the extra channel, 'Hot' or 'Cold'
            'Verbosity': 0,
            
            'h_tp_cold_tuning': 1,
            'h_tp_hot_tuning': 1,
            'DP_hot_tuning': 1,
            'DP_cold_tuning': 1
        }
        
        PHE = PHEHXClass(**params)
        PHE.Calculate()
        
        TT.append(Tin)
        QQ.append(PHE.h_2phase_c)  # Heat transfer coefficient for two-phase cold side
        Q1.append(PHE.q_flux)  # Heat flux
        
        print(f"Mass flow rate: {mdot_h} kg/s")
        print(f"Heat transfer: {PHE.Q} W, HTC: {PHE.h_subcooled_h} W/m²K, DP: {-PHE.DP_h/1000} kPa")
        
        results.append((mdot_h, PHE.Q, PHE.h_subcooled_h, -PHE.DP_h/1000))
        
        # Print the output list for detailed inspection
        output_list = PHE.OutputList()
        for item in output_list:
            print(f"{item[0]}: {item[2]} {item[1]}")
    
    # Plot results - Heat transfer coefficient vs mass flow rate
    plt.figure(figsize=(10, 6))
    plt.plot([r[0] for r in results], QQ, 'o-')
    plt.xlabel('Mass Flow Rate [kg/s]')
    plt.ylabel('Heat Transfer Coefficient [W/m²K]')
    plt.title('Heat Transfer Coefficient vs Mass Flow Rate')
    plt.grid(True)
    plt.savefig('PHEHX_HTC.png')
    
    # Plot results - Heat flux vs mass flow rate
    plt.figure(figsize=(10, 6))
    plt.plot([r[0] for r in results], Q1, 'o-')
    plt.xlabel('Mass Flow Rate [kg/s]')
    plt.ylabel('Heat Flux [W/m²]')
    plt.title('Heat Flux vs Mass Flow Rate')
    plt.grid(True)
    plt.savefig('PHEHX_HeatFlux.png')
    
    return results

if __name__ == '__main__':
    # print("Running Wyatt PHEHX test case...")
    # test_WyattPHEHX()
    
    # print("\nRunning SWEP varied mass flow rate test case...")
    # test_SWEPVariedmdot()

    print("\nRunning SamplePHEHX varied mass flow rate test case...")
    test_SamplePHEHX()
