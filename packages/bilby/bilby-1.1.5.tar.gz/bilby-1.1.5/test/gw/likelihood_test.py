import unittest
from copy import deepcopy
import os

import numpy as np
import bilby
from bilby.gw.likelihood import BilbyROQParamsRangeError


class TestBasicGWTransient(unittest.TestCase):
    def setUp(self):
        np.random.seed(500)
        self.parameters = dict(
            mass_1=31.0,
            mass_2=29.0,
            a_1=0.4,
            a_2=0.3,
            tilt_1=0.0,
            tilt_2=0.0,
            phi_12=1.7,
            phi_jl=0.3,
            luminosity_distance=4000.0,
            theta_jn=0.4,
            psi=2.659,
            phase=1.3,
            geocent_time=1126259642.413,
            ra=1.375,
            dec=-1.2108,
        )
        self.interferometers = bilby.gw.detector.InterferometerList(["H1"])
        self.interferometers.set_strain_data_from_power_spectral_densities(
            sampling_frequency=2048, duration=4
        )
        self.waveform_generator = bilby.gw.waveform_generator.WaveformGenerator(
            duration=4,
            sampling_frequency=2048,
            frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
        )

        self.likelihood = bilby.gw.likelihood.BasicGravitationalWaveTransient(
            interferometers=self.interferometers,
            waveform_generator=self.waveform_generator,
        )
        self.likelihood.parameters = self.parameters.copy()

    def tearDown(self):
        del self.parameters
        del self.interferometers
        del self.waveform_generator
        del self.likelihood

    def test_noise_log_likelihood(self):
        """Test noise log likelihood matches precomputed value"""
        self.likelihood.noise_log_likelihood()
        self.assertAlmostEqual(
            -4037.0994372143414, self.likelihood.noise_log_likelihood(), 3
        )

    def test_log_likelihood(self):
        """Test log likelihood matches precomputed value"""
        self.likelihood.log_likelihood()
        self.assertAlmostEqual(self.likelihood.log_likelihood(), -4054.047229508672, 3)

    def test_log_likelihood_ratio(self):
        """Test log likelihood ratio returns the correct value"""
        self.assertAlmostEqual(
            self.likelihood.log_likelihood() - self.likelihood.noise_log_likelihood(),
            self.likelihood.log_likelihood_ratio(),
            3,
        )

    def test_likelihood_zero_when_waveform_is_none(self):
        """Test log likelihood returns np.nan_to_num(-np.inf) when the
        waveform is None"""
        self.likelihood.waveform_generator.frequency_domain_strain = lambda x: None
        self.assertEqual(self.likelihood.log_likelihood_ratio(), np.nan_to_num(-np.inf))

    def test_repr(self):
        expected = "BasicGravitationalWaveTransient(interferometers={},\n\twaveform_generator={})".format(
            self.interferometers, self.waveform_generator
        )
        self.assertEqual(expected, repr(self.likelihood))


class TestGWTransient(unittest.TestCase):
    def setUp(self):
        np.random.seed(500)
        self.duration = 4
        self.sampling_frequency = 2048
        self.parameters = dict(
            mass_1=31.0,
            mass_2=29.0,
            a_1=0.4,
            a_2=0.3,
            tilt_1=0.0,
            tilt_2=0.0,
            phi_12=1.7,
            phi_jl=0.3,
            luminosity_distance=4000.0,
            theta_jn=0.4,
            psi=2.659,
            phase=1.3,
            geocent_time=1126259642.413,
            ra=1.375,
            dec=-1.2108,
        )
        self.interferometers = bilby.gw.detector.InterferometerList(["H1"])
        self.interferometers.set_strain_data_from_power_spectral_densities(
            sampling_frequency=self.sampling_frequency, duration=self.duration
        )
        self.waveform_generator = bilby.gw.waveform_generator.WaveformGenerator(
            duration=self.duration,
            sampling_frequency=self.sampling_frequency,
            frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
        )

        self.prior = bilby.gw.prior.BBHPriorDict()
        self.prior["geocent_time"] = bilby.prior.Uniform(
            minimum=self.parameters["geocent_time"] - self.duration / 2,
            maximum=self.parameters["geocent_time"] + self.duration / 2,
        )

        self.likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
            interferometers=self.interferometers,
            waveform_generator=self.waveform_generator,
            priors=self.prior.copy(),
        )
        self.likelihood.parameters = self.parameters.copy()

    def tearDown(self):
        del self.parameters
        del self.interferometers
        del self.waveform_generator
        del self.prior
        del self.likelihood

    def test_noise_log_likelihood(self):
        """Test noise log likelihood matches precomputed value"""
        self.likelihood.noise_log_likelihood()
        self.assertAlmostEqual(
            -4037.0994372143414, self.likelihood.noise_log_likelihood(), 3
        )

    def test_log_likelihood(self):
        """Test log likelihood matches precomputed value"""
        self.likelihood.log_likelihood()
        self.assertAlmostEqual(self.likelihood.log_likelihood(),
                               -4054.047229508673, 3)

    def test_log_likelihood_ratio(self):
        """Test log likelihood ratio returns the correct value"""
        self.assertAlmostEqual(
            self.likelihood.log_likelihood() - self.likelihood.noise_log_likelihood(),
            self.likelihood.log_likelihood_ratio(),
            3,
        )

    def test_likelihood_zero_when_waveform_is_none(self):
        """Test log likelihood returns np.nan_to_num(-np.inf) when the
        waveform is None"""
        self.likelihood.waveform_generator.frequency_domain_strain = lambda x: None
        self.assertEqual(self.likelihood.log_likelihood_ratio(), np.nan_to_num(-np.inf))

    def test_repr(self):
        expected = (
            "GravitationalWaveTransient(interferometers={},\n\twaveform_generator={},\n\t"
            "time_marginalization={}, distance_marginalization={}, phase_marginalization={}, "
            "calibration_marginalization={}, priors={})".format(
                self.interferometers,
                self.waveform_generator,
                False,
                False,
                False,
                False,
                self.prior,
            )
        )
        self.assertEqual(expected, repr(self.likelihood))

    def test_interferometers_setting_list(self):
        ifos = [
            bilby.gw.detector.get_empty_interferometer(name=name)
            for name in ["H1", "L1"]
        ]
        self.likelihood.interferometers = ifos
        self.assertListEqual(
            bilby.gw.detector.InterferometerList(ifos), self.likelihood.interferometers
        )
        self.assertTrue(
            type(self.likelihood.interferometers)
            == bilby.gw.detector.InterferometerList
        )

    def test_interferometers_setting_interferometer_list(self):
        ifos = bilby.gw.detector.InterferometerList(
            [
                bilby.gw.detector.get_empty_interferometer(name=name)
                for name in ["H1", "L1"]
            ]
        )
        self.likelihood.interferometers = ifos
        self.assertListEqual(
            bilby.gw.detector.InterferometerList(ifos), self.likelihood.interferometers
        )
        self.assertTrue(
            type(self.likelihood.interferometers)
            == bilby.gw.detector.InterferometerList
        )

    def test_meta_data(self):
        expected = dict(
            interferometers=self.interferometers.meta_data,
            time_marginalization=False,
            phase_marginalization=False,
            distance_marginalization=False,
            calibration_marginalization=False,
            waveform_generator_class=self.waveform_generator.__class__,
            waveform_arguments=self.waveform_generator.waveform_arguments,
            frequency_domain_source_model=self.waveform_generator.frequency_domain_source_model,
            parameter_conversion=self.waveform_generator.parameter_conversion,
            sampling_frequency=self.waveform_generator.sampling_frequency,
            duration=self.waveform_generator.duration,
            start_time=self.waveform_generator.start_time,
            time_reference="geocent",
            reference_frame="sky",
            lal_version=self.likelihood.lal_version,
            lalsimulation_version=self.likelihood.lalsimulation_version,
        )
        self.assertDictEqual(expected, self.likelihood.meta_data)

    def test_reference_frame_agrees_with_default(self):
        new_likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
            interferometers=self.interferometers,
            waveform_generator=self.waveform_generator,
            priors=self.prior.copy(),
            reference_frame="H1L1"
        )
        parameters = self.parameters.copy()
        del parameters["ra"], parameters["dec"]
        parameters["zenith"] = 1.0
        parameters["azimuth"] = 1.0
        parameters["ra"], parameters["dec"] = bilby.gw.utils.zenith_azimuth_to_ra_dec(
            zenith=parameters["zenith"],
            azimuth=parameters["azimuth"],
            geocent_time=parameters["geocent_time"],
            ifos=bilby.gw.detector.InterferometerList(["H1", "L1"])
        )
        new_likelihood.parameters.update(parameters)
        self.likelihood.parameters.update(parameters)
        self.assertEqual(
            new_likelihood.log_likelihood_ratio(),
            self.likelihood.log_likelihood_ratio()
        )

    def test_time_reference_agrees_with_default(self):
        new_likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
            interferometers=self.interferometers,
            waveform_generator=self.waveform_generator,
            priors=self.prior.copy(),
            time_reference="H1"
        )
        ifo = bilby.gw.detector.get_empty_interferometer("H1")
        time_delay = ifo.time_delay_from_geocenter(
            ra=self.parameters["ra"],
            dec=self.parameters["dec"],
            time=self.parameters["geocent_time"]
        )
        parameters = self.parameters.copy()
        parameters["H1_time"] = parameters["geocent_time"] + time_delay
        new_likelihood.parameters.update(parameters)
        self.likelihood.parameters.update(parameters)
        self.assertEqual(
            new_likelihood.log_likelihood_ratio(),
            self.likelihood.log_likelihood_ratio()
        )


class TestMarginalizedLikelihood(unittest.TestCase):
    def setUp(self):
        np.random.seed(500)
        self.duration = 4
        self.sampling_frequency = 2048
        self.parameters = dict(
            mass_1=31.0,
            mass_2=29.0,
            a_1=0.4,
            a_2=0.3,
            tilt_1=0.0,
            tilt_2=0.0,
            phi_12=1.7,
            phi_jl=0.3,
            luminosity_distance=4000.0,
            theta_jn=0.4,
            psi=2.659,
            phase=1.3,
            geocent_time=1126259642.413,
            ra=1.375,
            dec=-1.2108,
        )

        self.interferometers = bilby.gw.detector.InterferometerList(["H1"])
        self.interferometers.set_strain_data_from_power_spectral_densities(
            sampling_frequency=self.sampling_frequency,
            duration=self.duration,
            start_time=self.parameters["geocent_time"] - self.duration / 2,
        )

        self.waveform_generator = bilby.gw.waveform_generator.WaveformGenerator(
            duration=self.duration,
            sampling_frequency=self.sampling_frequency,
            frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
        )

        self.prior = bilby.gw.prior.BBHPriorDict()
        self.prior["geocent_time"] = bilby.prior.Uniform(
            minimum=self.parameters["geocent_time"] - self.duration / 2,
            maximum=self.parameters["geocent_time"] + self.duration / 2,
        )

    def test_cannot_instantiate_marginalised_likelihood_without_prior(self):
        self.assertRaises(
            ValueError,
            lambda: bilby.gw.likelihood.GravitationalWaveTransient(
                interferometers=self.interferometers,
                waveform_generator=self.waveform_generator,
                phase_marginalization=True,
            ),
        )

    def test_generating_default_time_prior(self):
        temp = self.prior.pop("geocent_time")
        new_prior = self.prior.copy()
        like = bilby.gw.likelihood.GravitationalWaveTransient(
            interferometers=self.interferometers,
            waveform_generator=self.waveform_generator,
            priors=new_prior,
            time_marginalization=True,
        )
        same = all(
            [
                temp.minimum == like.priors["geocent_time"].minimum,
                temp.maximum == like.priors["geocent_time"].maximum,
                new_prior["geocent_time"] == temp.minimum,
            ]
        )
        self.assertTrue(same)
        self.prior["geocent_time"] = temp

    def test_generating_default_phase_prior(self):
        temp = self.prior.pop("phase")
        new_prior = self.prior.copy()
        like = bilby.gw.likelihood.GravitationalWaveTransient(
            interferometers=self.interferometers,
            waveform_generator=self.waveform_generator,
            priors=new_prior,
            phase_marginalization=True,
        )
        same = all(
            [
                temp.minimum == like.priors["phase"].minimum,
                temp.maximum == like.priors["phase"].maximum,
                new_prior["phase"] == float(0),
            ]
        )
        self.assertTrue(same)
        self.prior["phase"] = temp

    def test_run_sampler_flags_if_marginalized_phase_is_sampled(self):
        like = bilby.gw.likelihood.GravitationalWaveTransient(
            interferometers=self.interferometers,
            waveform_generator=self.waveform_generator,
            priors=self.prior,
            phase_marginalization=True,
        )
        new_prior = self.prior.copy()
        new_prior["phase"] = bilby.prior.Uniform(minimum=0, maximum=2 * np.pi)
        for key, param in dict(
            mass_1=31.0,
            mass_2=29.0,
            a_1=0.4,
            a_2=0.3,
            tilt_1=0.0,
            tilt_2=0.0,
            phi_12=1.7,
            phi_jl=0.3,
            theta_jn=0.4,
            psi=2.659,
            ra=1.375,
            dec=-1.2108,
        ).items():
            new_prior[key] = param
        with self.assertRaises(bilby.core.sampler.SamplingMarginalisedParameterError):
            bilby.run_sampler(like, new_prior)

    def test_run_sampler_flags_if_marginalized_time_is_sampled(self):
        like = bilby.gw.likelihood.GravitationalWaveTransient(
            interferometers=self.interferometers,
            waveform_generator=self.waveform_generator,
            priors=self.prior,
            time_marginalization=True,
        )
        new_prior = self.prior.copy()
        new_prior["geocent_time"] = bilby.prior.Uniform(minimum=0, maximum=1)
        for key, param in dict(
            mass_1=31.0,
            mass_2=29.0,
            a_1=0.4,
            a_2=0.3,
            tilt_1=0.0,
            tilt_2=0.0,
            phi_12=1.7,
            phi_jl=0.3,
            theta_jn=0.4,
            psi=2.659,
            ra=1.375,
            dec=-1.2108,
        ).items():
            new_prior[key] = param
        with self.assertRaises(bilby.core.sampler.SamplingMarginalisedParameterError):
            bilby.run_sampler(like, new_prior)


class TestMarginalizations(unittest.TestCase):
    """
    Test all marginalised likelihoods matches brute force version.

    For time, this is strongly dependent on the specific time grid used.
    The `time_jitter` parameter makes this a weaker dependence during sampling.
    """

    def setUp(self):
        np.random.seed(500)
        self.duration = 4
        self.sampling_frequency = 2048
        self.parameters = dict(
            mass_1=31.0,
            mass_2=29.0,
            a_1=0.4,
            a_2=0.3,
            tilt_1=0.0,
            tilt_2=0.0,
            phi_12=1.7,
            phi_jl=0.3,
            luminosity_distance=4000.0,
            theta_jn=0.4,
            psi=2.659,
            phase=1.3,
            geocent_time=1126259642.413,
            ra=1.375,
            dec=-1.2108,
            time_jitter=0,
        )

        self.interferometers = bilby.gw.detector.InterferometerList(["H1"])
        self.interferometers.set_strain_data_from_power_spectral_densities(
            sampling_frequency=self.sampling_frequency,
            duration=self.duration,
            start_time=1126259640,
        )

        self.waveform_generator = bilby.gw.waveform_generator.WaveformGenerator(
            duration=self.duration,
            sampling_frequency=self.sampling_frequency,
            frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
            start_time=1126259640,
        )
        self.interferometers.inject_signal(
            parameters=self.parameters, waveform_generator=self.waveform_generator
        )

        self.priors = bilby.gw.prior.BBHPriorDict()
        self.priors["geocent_time"] = bilby.prior.Uniform(
            minimum=self.interferometers.start_time,
            maximum=self.interferometers.start_time + self.interferometers.duration,
        )

    def tearDown(self):
        del self.duration
        del self.sampling_frequency
        del self.parameters
        del self.interferometers
        del self.waveform_generator
        del self.priors

    def get_likelihood(
        self,
        time_marginalization=False,
        phase_marginalization=False,
        distance_marginalization=False,
        priors=None
    ):
        if priors is None:
            priors = self.priors.copy()
        if distance_marginalization and phase_marginalization:
            lookup = "distance_lookup_phase.npz"
        elif distance_marginalization:
            lookup = "distance_lookup_no_phase.npz"
        else:
            lookup = None
        like = bilby.gw.likelihood.GravitationalWaveTransient(
            interferometers=self.interferometers,
            waveform_generator=self.waveform_generator,
            distance_marginalization=distance_marginalization,
            phase_marginalization=phase_marginalization,
            time_marginalization=time_marginalization,
            distance_marginalization_lookup_table=lookup,
            priors=priors,
        )
        like.parameters = self.parameters.copy()
        if time_marginalization:
            like.parameters["geocent_time"] = self.interferometers.start_time
        return like

    def _template(self, marginalized, non_marginalized, key, prior=None, values=None):
        if prior is None:
            prior = self.priors[key]
        if values is None:
            values = np.linspace(prior.minimum, prior.maximum, 1000)
        prior_values = prior.prob(values)
        ln_likes = np.empty(values.shape)
        for ii, value in enumerate(values):
            non_marginalized.parameters[key] = value
            ln_likes[ii] = non_marginalized.log_likelihood_ratio()
        like = np.exp(ln_likes - max(ln_likes))

        marg_like = np.log(np.trapz(like * prior_values, values)) + max(ln_likes)
        self.assertAlmostEqual(
            marg_like, marginalized.log_likelihood_ratio(), delta=0.5
        )

    def test_distance_marginalisation(self):
        self._template(
            self.get_likelihood(distance_marginalization=True),
            self.get_likelihood(),
            key="luminosity_distance",
        )

    def test_distance_phase_marginalisation(self):
        self._template(
            self.get_likelihood(distance_marginalization=True, phase_marginalization=True),
            self.get_likelihood(phase_marginalization=True),
            key="luminosity_distance",
        )

    def test_distance_time_marginalisation(self):
        self._template(
            self.get_likelihood(distance_marginalization=True, time_marginalization=True),
            self.get_likelihood(time_marginalization=True),
            key="luminosity_distance",
        )

    def test_distance_phase_time_marginalisation(self):
        """
        Test phase marginalised likelihood matches brute force version when
        also marginalising over time.
        """
        self._template(
            self.get_likelihood(distance_marginalization=True, phase_marginalization=True, time_marginalization=True),
            self.get_likelihood(phase_marginalization=True, time_marginalization=True),
            key="luminosity_distance",
        )

    def test_phase_marginalisation(self):
        self._template(
            self.get_likelihood(phase_marginalization=True),
            self.get_likelihood(),
            key="phase",
        )

    def test_phase_distance_marginalisation(self):
        self._template(
            self.get_likelihood(distance_marginalization=True, phase_marginalization=True),
            self.get_likelihood(distance_marginalization=True),
            key="phase",
        )

    def test_phase_time_marginalisation(self):
        self._template(
            self.get_likelihood(time_marginalization=True, phase_marginalization=True),
            self.get_likelihood(time_marginalization=True),
            key="phase",
        )

    def test_phase_distance_time_marginalisation(self):
        self._template(
            self.get_likelihood(time_marginalization=True, distance_marginalization=True, phase_marginalization=True),
            self.get_likelihood(time_marginalization=True, distance_marginalization=True),
            key="phase",
        )

    def test_time_marginalisation(self):
        times = self.waveform_generator.time_array
        self._template(
            self.get_likelihood(time_marginalization=True),
            self.get_likelihood(),
            key="geocent_time",
            values=times,
        )

    def test_time_distance_marginalisation(self):
        times = self.waveform_generator.time_array
        self._template(
            self.get_likelihood(time_marginalization=True, distance_marginalization=True),
            self.get_likelihood(distance_marginalization=True),
            key="geocent_time",
            values=times
        )

    def test_time_phase_marginalisation(self):
        times = self.waveform_generator.time_array
        self._template(
            self.get_likelihood(time_marginalization=True, phase_marginalization=True),
            self.get_likelihood(phase_marginalization=True),
            key="geocent_time",
            values=times
        )

    def test_time_distance_phase_marginalisation(self):
        times = self.waveform_generator.time_array
        self._template(
            self.get_likelihood(time_marginalization=True, phase_marginalization=True, distance_marginalization=True),
            self.get_likelihood(phase_marginalization=True, distance_marginalization=True),
            key="geocent_time",
            values=times
        )

    def test_time_marginalisation_partial_segment(self):
        """
        Test time marginalised likelihood matches brute force version over
        just part of a segment.
        """
        priors = self.priors.copy()
        prior = bilby.prior.Uniform(
            minimum=self.parameters["geocent_time"] - 0.1,
            maximum=self.parameters["geocent_time"] + 0.1,
        )
        priors["geocent_time"] = prior
        self._template(
            self.get_likelihood(time_marginalization=True, priors=priors.copy()),
            self.get_likelihood(priors=priors.copy()),
            key="geocent_time",
            values=self.waveform_generator.time_array,
            prior=prior,
        )


class TestROQLikelihood(unittest.TestCase):
    def setUp(self):
        self.duration = 4
        self.sampling_frequency = 2048

        # Possible locations for the ROQ: in the docker image, local, or on CIT
        trial_roq_paths = [
            "/roq_basis",
            os.path.join(os.path.expanduser("~"), "ROQ_data/IMRPhenomPv2/4s"),
            "/home/cbc/ROQ_data/IMRPhenomPv2/4s",
        ]
        roq_dir = None
        for path in trial_roq_paths:
            if os.path.isdir(path):
                roq_dir = path
                break
        if roq_dir is None:
            raise Exception("Unable to load ROQ basis: cannot proceed with tests")

        linear_matrix_file = "{}/B_linear.npy".format(roq_dir)
        quadratic_matrix_file = "{}/B_quadratic.npy".format(roq_dir)

        fnodes_linear_file = "{}/fnodes_linear.npy".format(roq_dir)
        fnodes_linear = np.load(fnodes_linear_file).T
        fnodes_quadratic_file = "{}/fnodes_quadratic.npy".format(roq_dir)
        fnodes_quadratic = np.load(fnodes_quadratic_file).T
        self.linear_matrix_file = "{}/B_linear.npy".format(roq_dir)
        self.quadratic_matrix_file = "{}/B_quadratic.npy".format(roq_dir)
        self.params_file = "{}/params.dat".format(roq_dir)

        self.test_parameters = dict(
            mass_1=36.0,
            mass_2=36.0,
            a_1=0.0,
            a_2=0.0,
            tilt_1=0.0,
            tilt_2=0.0,
            phi_12=1.7,
            phi_jl=0.3,
            luminosity_distance=1000.0,
            theta_jn=0.4,
            psi=0.659,
            phase=1.3,
            geocent_time=1.2,
            ra=1.3,
            dec=-1.2,
        )

        ifos = bilby.gw.detector.InterferometerList(["H1"])
        ifos.set_strain_data_from_power_spectral_densities(
            sampling_frequency=self.sampling_frequency, duration=self.duration
        )

        self.priors = bilby.gw.prior.BBHPriorDict()
        self.priors.pop("mass_1")
        self.priors.pop("mass_2")
        # Testing is done with the 4s IMRPhenomPV2 ROQ basis
        self.priors["chirp_mass"] = bilby.core.prior.Uniform(12.299703, 45)
        self.priors["mass_ratio"] = bilby.core.prior.Uniform(0.125, 1)
        self.priors["geocent_time"] = bilby.core.prior.Uniform(1.19, 1.21)

        non_roq_wfg = bilby.gw.WaveformGenerator(
            duration=self.duration,
            sampling_frequency=self.sampling_frequency,
            frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
            waveform_arguments=dict(
                reference_frequency=20.0,
                minimum_frequency=20.0,
                approximant="IMRPhenomPv2",
            ),
        )

        ifos.inject_signal(
            parameters=self.test_parameters, waveform_generator=non_roq_wfg
        )

        self.ifos = ifos

        roq_wfg = bilby.gw.waveform_generator.WaveformGenerator(
            duration=self.duration,
            sampling_frequency=self.sampling_frequency,
            frequency_domain_source_model=bilby.gw.source.binary_black_hole_roq,
            waveform_arguments=dict(
                frequency_nodes_linear=fnodes_linear,
                frequency_nodes_quadratic=fnodes_quadratic,
                reference_frequency=20.0,
                minimum_frequency=20.0,
                approximant="IMRPhenomPv2",
            ),
        )

        self.roq_wfg = roq_wfg

        self.non_roq = bilby.gw.likelihood.GravitationalWaveTransient(
            interferometers=ifos, waveform_generator=non_roq_wfg
        )

        self.non_roq_phase = bilby.gw.likelihood.GravitationalWaveTransient(
            interferometers=ifos,
            waveform_generator=non_roq_wfg,
            phase_marginalization=True,
            priors=self.priors.copy(),
        )

        self.roq = bilby.gw.likelihood.ROQGravitationalWaveTransient(
            interferometers=ifos,
            waveform_generator=roq_wfg,
            linear_matrix=linear_matrix_file,
            quadratic_matrix=quadratic_matrix_file,
            priors=self.priors,
        )

        self.roq_phase = bilby.gw.likelihood.ROQGravitationalWaveTransient(
            interferometers=ifos,
            waveform_generator=roq_wfg,
            linear_matrix=linear_matrix_file,
            quadratic_matrix=quadratic_matrix_file,
            phase_marginalization=True,
            priors=self.priors.copy(),
        )

    def tearDown(self):
        del (
            self.roq,
            self.non_roq,
            self.non_roq_phase,
            self.roq_phase,
            self.ifos,
            self.priors,
        )

    def test_matches_non_roq(self):
        self.non_roq.parameters.update(self.test_parameters)
        self.roq.parameters.update(self.test_parameters)
        self.assertLess(
            abs(self.non_roq.log_likelihood_ratio() - self.roq.log_likelihood_ratio())
            / self.non_roq.log_likelihood_ratio(),
            1e-3,
        )

    def test_time_prior_out_of_bounds_returns_zero(self):
        self.roq.parameters.update(self.test_parameters)
        self.roq.parameters["geocent_time"] = -5
        self.assertEqual(self.roq.log_likelihood_ratio(), np.nan_to_num(-np.inf))

    def test_phase_marginalisation_roq(self):
        """Test phase marginalised likelihood matches brute force version"""
        self.non_roq_phase.parameters = self.test_parameters.copy()
        self.roq_phase.parameters = self.test_parameters.copy()
        self.assertLess(
            abs(
                self.non_roq_phase.log_likelihood_ratio()
                - self.roq_phase.log_likelihood_ratio()
            )
            / self.non_roq_phase.log_likelihood_ratio(),
            1e-3,
        )

    def test_create_roq_weights_with_params(self):
        roq = bilby.gw.likelihood.ROQGravitationalWaveTransient(
            interferometers=self.ifos,
            waveform_generator=self.roq_wfg,
            linear_matrix=self.linear_matrix_file,
            roq_params=self.params_file,
            quadratic_matrix=self.quadratic_matrix_file,
            priors=self.priors,
        )
        roq.parameters.update(self.test_parameters)
        self.roq.parameters.update(self.test_parameters)
        self.assertEqual(roq.log_likelihood_ratio(), self.roq.log_likelihood_ratio())

    def test_create_roq_weights_frequency_mismatch_works_with_params(self):

        self.ifos[0].maximum_frequency = self.ifos[0].maximum_frequency / 2
        bilby.gw.likelihood.ROQGravitationalWaveTransient(
            interferometers=self.ifos,
            waveform_generator=self.roq_wfg,
            linear_matrix=self.linear_matrix_file,
            roq_params=self.params_file,
            quadratic_matrix=self.quadratic_matrix_file,
            priors=self.priors,
        )

    def test_create_roq_weights_frequency_mismatch_fails_without_params(self):
        self.ifos[0].maximum_frequency = self.ifos[0].maximum_frequency / 2
        with self.assertRaises(ValueError):
            bilby.gw.likelihood.ROQGravitationalWaveTransient(
                interferometers=self.ifos,
                waveform_generator=self.roq_wfg,
                linear_matrix=self.linear_matrix_file,
                quadratic_matrix=self.quadratic_matrix_file,
                priors=self.priors,
            )

    def test_create_roq_weights_fails_with_min_chirp_mass_outside_bounds(self):
        self.ifos[0].maximum_frequency = self.ifos[0].maximum_frequency / 2
        self.priors["chirp_mass"] = bilby.core.prior.Uniform(10, 45)
        with self.assertRaises(BilbyROQParamsRangeError):
            bilby.gw.likelihood.ROQGravitationalWaveTransient(
                interferometers=self.ifos,
                waveform_generator=self.roq_wfg,
                linear_matrix=self.linear_matrix_file,
                roq_params=self.params_file,
                quadratic_matrix=self.quadratic_matrix_file,
                priors=self.priors,
            )

    def test_create_roq_weights_fails_with_max_chirp_mass_outside_bounds(self):
        self.ifos[0].maximum_frequency = self.ifos[0].maximum_frequency / 2
        self.priors["chirp_mass"] = bilby.core.prior.Uniform(12.299703, 50)
        with self.assertRaises(BilbyROQParamsRangeError):
            bilby.gw.likelihood.ROQGravitationalWaveTransient(
                interferometers=self.ifos,
                waveform_generator=self.roq_wfg,
                linear_matrix=self.linear_matrix_file,
                roq_params=self.params_file,
                quadratic_matrix=self.quadratic_matrix_file,
                priors=self.priors,
            )

    def test_create_roq_weights_fails_with_min_component_mass_outside_bounds(self):
        self.ifos[0].maximum_frequency = self.ifos[0].maximum_frequency / 2
        self.priors["chirp_mass"] = bilby.core.prior.Uniform(12.299703, 45)
        self.priors["mass_ratio"] = bilby.core.prior.Uniform(1e-5, 1)
        with self.assertRaises(BilbyROQParamsRangeError):
            bilby.gw.likelihood.ROQGravitationalWaveTransient(
                interferometers=self.ifos,
                waveform_generator=self.roq_wfg,
                linear_matrix=self.linear_matrix_file,
                roq_params=self.params_file,
                quadratic_matrix=self.quadratic_matrix_file,
                priors=self.priors,
            )

    def test_create_roq_weights_fails_with_max_frequency(self):
        ifos = bilby.gw.detector.InterferometerList(["H1"])
        ifos.set_strain_data_from_power_spectral_densities(
            sampling_frequency=2 ** 14, duration=4
        )
        ifos[0].maximum_frequency = 2 ** 13
        with self.assertRaises(BilbyROQParamsRangeError):
            bilby.gw.likelihood.ROQGravitationalWaveTransient(
                interferometers=ifos,
                waveform_generator=self.roq_wfg,
                linear_matrix=self.linear_matrix_file,
                roq_params=self.params_file,
                quadratic_matrix=self.quadratic_matrix_file,
                priors=self.priors,
            )

    def test_create_roq_weights_fails_due_to_min_frequency(self):
        self.ifos[0].minimum_frequency = 15
        with self.assertRaises(BilbyROQParamsRangeError):
            bilby.gw.likelihood.ROQGravitationalWaveTransient(
                interferometers=self.ifos,
                waveform_generator=self.roq_wfg,
                linear_matrix=self.linear_matrix_file,
                roq_params=self.params_file,
                quadratic_matrix=self.quadratic_matrix_file,
                priors=self.priors,
            )

    def test_create_roq_weights_fails_due_to_duration(self):
        ifos = bilby.gw.detector.InterferometerList(["H1"])
        ifos.set_strain_data_from_power_spectral_densities(
            sampling_frequency=self.sampling_frequency, duration=16
        )
        with self.assertRaises(BilbyROQParamsRangeError):
            bilby.gw.likelihood.ROQGravitationalWaveTransient(
                interferometers=ifos,
                waveform_generator=self.roq_wfg,
                linear_matrix=self.linear_matrix_file,
                roq_params=self.params_file,
                quadratic_matrix=self.quadratic_matrix_file,
                priors=self.priors,
            )


class TestRescaledROQLikelihood(unittest.TestCase):
    def test_rescaling(self):

        # Possible locations for the ROQ: in the docker image, local, or on CIT
        trial_roq_paths = [
            "/roq_basis",
            os.path.join(os.path.expanduser("~"), "ROQ_data/IMRPhenomPv2/4s"),
            "/home/cbc/ROQ_data/IMRPhenomPv2/4s",
        ]
        roq_dir = None
        for path in trial_roq_paths:
            if os.path.isdir(path):
                roq_dir = path
                break
        if roq_dir is None:
            raise Exception("Unable to load ROQ basis: cannot proceed with tests")

        linear_matrix_file = "{}/B_linear.npy".format(roq_dir)
        quadratic_matrix_file = "{}/B_quadratic.npy".format(roq_dir)

        fnodes_linear_file = "{}/fnodes_linear.npy".format(roq_dir)
        fnodes_linear = np.load(fnodes_linear_file).T
        fnodes_quadratic_file = "{}/fnodes_quadratic.npy".format(roq_dir)
        fnodes_quadratic = np.load(fnodes_quadratic_file).T
        self.linear_matrix_file = "{}/B_linear.npy".format(roq_dir)
        self.quadratic_matrix_file = "{}/B_quadratic.npy".format(roq_dir)
        self.params_file = "{}/params.dat".format(roq_dir)

        scale_factor = 0.5
        params = np.genfromtxt(self.params_file, names=True)

        self.duration = 4 / scale_factor
        self.sampling_frequency = 2048 * scale_factor

        ifos = bilby.gw.detector.InterferometerList(["H1"])
        ifos.set_strain_data_from_power_spectral_densities(
            sampling_frequency=self.sampling_frequency, duration=self.duration
        )
        self.ifos = ifos

        self.priors = bilby.gw.prior.BBHPriorDict()
        self.priors.pop("mass_1")
        self.priors.pop("mass_2")
        # Testing is done with the 4s IMRPhenomPV2 ROQ basis
        self.priors["chirp_mass"] = bilby.core.prior.Uniform(
            12.299703 / scale_factor, 45 / scale_factor
        )
        self.priors["mass_ratio"] = bilby.core.prior.Uniform(0.125, 1)
        self.priors["geocent_time"] = bilby.core.prior.Uniform(1.19, 1.21)

        self.roq_wfg = bilby.gw.waveform_generator.WaveformGenerator(
            duration=self.duration,
            sampling_frequency=self.sampling_frequency,
            frequency_domain_source_model=bilby.gw.source.binary_black_hole_roq,
            waveform_arguments=dict(
                frequency_nodes_linear=fnodes_linear,
                frequency_nodes_quadratic=fnodes_quadratic,
                reference_frequency=20.0,
                minimum_frequency=20.0,
                approximant="IMRPhenomPv2",
            ),
        )

        self.roq = bilby.gw.likelihood.ROQGravitationalWaveTransient(
            interferometers=ifos,
            waveform_generator=self.roq_wfg,
            linear_matrix=linear_matrix_file,
            roq_params=params,
            roq_scale_factor=scale_factor,
            quadratic_matrix=quadratic_matrix_file,
            priors=self.priors,
        )


class TestBBHLikelihoodSetUp(unittest.TestCase):
    def setUp(self):
        self.ifos = bilby.gw.detector.InterferometerList(["H1"])

    def tearDown(self):
        del self.ifos

    def test_instantiation(self):
        self.like = bilby.gw.likelihood.get_binary_black_hole_likelihood(self.ifos)


class TestMBLikelihood(unittest.TestCase):
    def setUp(self):
        duration = 16
        fmin = 20.
        sampling_frequency = 2048.
        self.test_parameters = dict(
            chirp_mass=6.0,
            mass_ratio=0.5,
            a_1=0.0,
            a_2=0.0,
            tilt_1=0.0,
            tilt_2=0.0,
            phi_12=0.0,
            phi_jl=0.0,
            luminosity_distance=200.0,
            theta_jn=0.4,
            psi=0.659,
            phase=1.3,
            geocent_time=1187008882,
            ra=1.3,
            dec=-1.2
        )  # Network SNR is ~50

        ifos = bilby.gw.detector.InterferometerList(["H1", "L1", "V1"])
        np.random.seed(170817)
        ifos.set_strain_data_from_power_spectral_densities(
            sampling_frequency=sampling_frequency, duration=duration,
            start_time=self.test_parameters['geocent_time'] - duration + 2.
        )
        for ifo in ifos:
            ifo.minimum_frequency = fmin

        priors = bilby.gw.prior.BBHPriorDict()
        priors.pop("mass_1")
        priors.pop("mass_2")
        priors["chirp_mass"] = bilby.core.prior.Uniform(5.5, 6.5)
        priors["mass_ratio"] = bilby.core.prior.Uniform(0.125, 1)
        priors["geocent_time"] = bilby.core.prior.Uniform(
            self.test_parameters['geocent_time'] - 0.1,
            self.test_parameters['geocent_time'] + 0.1)

        approximant_22 = "IMRPhenomD"
        approximant_homs = "IMRPhenomHM"
        non_mb_wfg_22 = bilby.gw.WaveformGenerator(
            duration=duration, sampling_frequency=sampling_frequency,
            frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
            waveform_arguments=dict(
                reference_frequency=fmin, minimum_frequency=fmin, approximant=approximant_22)
        )
        mb_wfg_22 = bilby.gw.waveform_generator.WaveformGenerator(
            duration=duration, sampling_frequency=sampling_frequency,
            frequency_domain_source_model=bilby.gw.source.binary_black_hole_frequency_sequence,
            waveform_arguments=dict(
                reference_frequency=fmin, approximant=approximant_22)
        )
        non_mb_wfg_homs = bilby.gw.WaveformGenerator(
            duration=duration, sampling_frequency=sampling_frequency,
            frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
            waveform_arguments=dict(
                reference_frequency=fmin, minimum_frequency=fmin, approximant=approximant_homs)
        )
        mb_wfg_homs = bilby.gw.waveform_generator.WaveformGenerator(
            duration=duration, sampling_frequency=sampling_frequency,
            frequency_domain_source_model=bilby.gw.source.binary_black_hole_frequency_sequence,
            waveform_arguments=dict(
                reference_frequency=fmin, approximant=approximant_homs)
        )

        ifos_22 = deepcopy(ifos)
        ifos_22.inject_signal(
            parameters=self.test_parameters, waveform_generator=non_mb_wfg_22
        )
        ifos_homs = deepcopy(ifos)
        ifos_homs.inject_signal(
            parameters=self.test_parameters, waveform_generator=non_mb_wfg_homs
        )

        self.non_mb_22 = bilby.gw.likelihood.GravitationalWaveTransient(
            interferometers=ifos_22, waveform_generator=non_mb_wfg_22
        )
        self.non_mb_homs = bilby.gw.likelihood.GravitationalWaveTransient(
            interferometers=ifos_homs, waveform_generator=non_mb_wfg_homs
        )

        self.mb_22 = bilby.gw.likelihood.MBGravitationalWaveTransient(
            interferometers=ifos_22, waveform_generator=deepcopy(mb_wfg_22),
            reference_chirp_mass=self.test_parameters['chirp_mass'],
            priors=priors.copy()
        )
        self.mb_ifftfft_22 = bilby.gw.likelihood.MBGravitationalWaveTransient(
            interferometers=ifos_22, waveform_generator=deepcopy(mb_wfg_22),
            reference_chirp_mass=self.test_parameters['chirp_mass'],
            priors=priors.copy(), linear_interpolation=False
        )
        self.mb_homs = bilby.gw.likelihood.MBGravitationalWaveTransient(
            interferometers=ifos_homs, waveform_generator=deepcopy(mb_wfg_homs),
            reference_chirp_mass=self.test_parameters['chirp_mass'],
            priors=priors.copy(), linear_interpolation=False, highest_mode=4
        )
        self.mb_more_accurate = bilby.gw.likelihood.MBGravitationalWaveTransient(
            interferometers=ifos_22, waveform_generator=deepcopy(mb_wfg_22),
            reference_chirp_mass=self.test_parameters['chirp_mass'],
            priors=priors.copy(), accuracy_factor=50
        )

    def tearDown(self):
        del (
            self.non_mb_22,
            self.non_mb_homs,
            self.mb_22,
            self.mb_ifftfft_22,
            self.mb_homs,
            self.mb_more_accurate
        )

    def test_matches_non_mb(self):
        self.non_mb_22.parameters.update(self.test_parameters)
        self.mb_22.parameters.update(self.test_parameters)
        self.assertLess(
            abs(self.non_mb_22.log_likelihood_ratio() - self.mb_22.log_likelihood_ratio()),
            1e-2
        )

    def test_ifft_fft(self):
        """
        Check if multi-banding likelihood with (h, h) computed with the
        IFFT-FFT algorithm matches the original likelihood.
        """
        self.non_mb_22.parameters.update(self.test_parameters)
        self.mb_ifftfft_22.parameters.update(self.test_parameters)
        self.assertLess(
            abs(self.non_mb_22.log_likelihood_ratio() - self.mb_ifftfft_22.log_likelihood_ratio()),
            5e-3
        )

    def test_homs(self):
        """
        Check if multi-banding likelihood matches the original likelihood for higher-order moments.
        """
        self.non_mb_homs.parameters.update(self.test_parameters)
        self.mb_homs.parameters.update(self.test_parameters)
        self.assertLess(
            abs(self.non_mb_homs.log_likelihood_ratio() - self.mb_homs.log_likelihood_ratio()),
            1e-3
        )

    def test_large_accuracy_factor(self):
        """
        Check if larger accuracy factor increases the accuracy.
        """
        self.non_mb_22.parameters.update(self.test_parameters)
        self.mb_22.parameters.update(self.test_parameters)
        self.mb_more_accurate.parameters.update(self.test_parameters)
        self.assertLess(
            abs(self.non_mb_22.log_likelihood_ratio() - self.mb_more_accurate.log_likelihood_ratio()),
            abs(self.non_mb_22.log_likelihood_ratio() - self.mb_22.log_likelihood_ratio()) / 2
        )


if __name__ == "__main__":
    unittest.main()
