import numpy as np

# copied from the MEED paper "MEED-An-Unsupervised-Multi-Environment-EventDetector-for-Non-Intrusive-Load-Monitoring", same author as CREAM, Daniel Jorde
class Electrical_Metrics():
    """
    Class that contains several functions to compute (approximately) diverse Electrical metrics:

    active_power
    apparent_power
    reative_power
    power_factor
    voltage_current_rms
    single_rms

    """
    def __init__(self):
        pass

    def active_power(self,instant_voltage, instant_current,period_length):
        """
        Active or Real power is the average of instantaneous power.
        P = Sum ( i[n] * v[n] ) / N )
        First we calculate the instantaneous power by multiplying the instantaneous
        voltage measurement by the instantaneous current measurement. We sum the
        instantaneous power measurement over a given number of samples and divide by
        that number of samples.


        Parameters
        ----------
        instant_voltage : ndarray
            Instantaneous Voltage, flat array
        instant_current : ndarray
            Instantaneous Current, flat array
        period_length : int
            Number of samples the features are computed over

        Returns
        -------
        active_power : ndarray
            Active Power array

        """

        instant_current = np.array(instant_current).flatten()
        instant_voltage = np.array(instant_voltage).flatten()

        if len(instant_current) == len(instant_voltage):
            instant_power = instant_voltage * instant_current
            period_length = int(period_length)

            active_power = []
            for i in range(0, len(instant_power), period_length):
                if i + period_length <= len(instant_power):
                    signal_one_period = instant_power[i:int(i + period_length)]
                    active_power_one_period = np.mean(signal_one_period )
                    active_power.append(active_power_one_period)
            active_power = np.array(active_power)
            return active_power

        else:
            raise ValueError("Signals need to have the same length")

    def apparent_power(self, instant_voltage,instant_current,period_length):
        """
        Compute apparent power:
        S = Vrms * Irms

        Parameters
        ----------
        instant_voltage : ndarray
            Instantaneous Voltage, flat array
        instant_current : ndarray
            Instantaneous Current, flat array
        period_length : int
            Number of samples the features are computed over

        Returns
        -------
        apparent_power : ndarray
            Apparent Power array

        """
        if len(instant_current) == len(instant_voltage):

            rms_voltage = self.compute_single_rms(instant_voltage,period_length)
            rms_current = self.compute_single_rms(instant_current,period_length)
            apparent_power = rms_voltage * rms_current
            return apparent_power

        else:
            raise ValueError("Signals need to have the same length")

    def reactive_power(self,apparent_power,active_power):
        """
        Compute reactive power:
        Q = sqrt(S^2 - P^2)

        Parameters
        ----------
        apparent_power : ndarray
            Apparent power, flat array
        active_power : ndarray
            Active power, flat array

        Returns
        -------
        reactive_power : ndarray
            Reactive power, flat array

        """

        if len(apparent_power) == len(active_power):
            reactive_power = np.sqrt((apparent_power * apparent_power) - (active_power * active_power))
            return reactive_power
        else:
            raise ValueError("Signals need to have the same length")


    def compute_power_factor(self,apparent_power,active_power):
        """
        Compute power factor:
        PF = P / S

        Parameters
        ----------
        apparent_power : ndarray
            Apparent power, flat array
        active_power : ndarray
            Active power, flat array

        Returns
        -------
        power_factor : float
            Power factor

        """

        power_factor = active_power / apparent_power
        return power_factor


    def compute_voltage_current_rms(self, voltage, current, period_length):
        """
        Compute Root-Mean-Square (RMS) values for the provided voltage and current.

        Parameters
        ----------
        voltage : ndarray
            Instantaneous Voltage, flat array
        current : ndarray
            Instantaneous Current, flat array
        period_length : int
            Number of samples the features are computed over

        Returns
        -------
        voltage_rms : ndarray
            Voltage RMS values
        current_rms : ndarray
            Current RMS values

        """
        period_length = int(period_length)
        voltage_rms = self.compute_single_rms(voltage, period_length)
        current_rms = self.compute_single_rms(current, period_length)
        return voltage_rms, current_rms


    def compute_single_rms(self,signal,period_length):
        """
        Compute Root-Mean-Square (RMS) values for the provided signal.

        Parameters
        ----------
        signal : ndarray
            Instantaneous Voltage OR Current flat array

        period_length : int
            Number of samples the features are computed over

        Returns
        -------
        signal_rms : ndarray
            RMS values of signal

        """
        rms_values = []
        period_length = int(period_length)
        for i in range(0, len(signal), period_length):
            if i + period_length <= len(signal):
                signal_one_period = signal[i:int(i + period_length)]
                rms_one_period = np.sqrt(np.mean(np.square(signal_one_period))) #rms
                rms_values.append(rms_one_period)
        return np.array(rms_values)