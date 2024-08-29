"""
Configuration settings for Grapher gui
"""

import pyqtgraph as pg
from PyQt5.QtGui import *

pg.setConfigOption("background", "k")
pg.setConfigOption("foreground", "y")


class TraceListConfig:
    def __init__(self, background_color="white", use_trace_color=True):
        self.use_trace_color = use_trace_color
        self.background_color = background_color


class GraphConfig:
    def __init__(
            self,
            name,
            ylim=(0, 1),
            is_scrolling=False,
            max_datasets=10,
            show_points=False,
            grid_on=True,
            is_images=False,
            scatter_plot="all",
            is_hist=False,
            vline=None,
            hline=None,
            vline_param=None,
            hline_param=None,
    ):
        self.vline_param = vline_param
        self.hline_param = hline_param
        self.name = name
        self.ylim = ylim
        self.is_scrolling = is_scrolling
        self.max_datasets = max_datasets
        self.graphs = 1  # just a single graph
        self.show_points = show_points
        self.grid_on = grid_on
        self.is_images = is_images
        self.scatter_plot = scatter_plot
        self.is_hist = is_hist
        self.vline = vline
        self.hline = hline


class GridGraphConfig:
    def __init__(self, tab, config_list):
        self.tab = tab
        self.config_list = config_list[0::3]
        self.row_list = config_list[1::3]
        self.column_list = config_list[2::3]

        self.graphs = len(self.config_list)


# colors were selected using vis pallette to be unambiguous
colors = {
    "red": QColor(255, 0, 58),
    "green": QColor(60, 180, 75),
    "yellow": QColor(255, 255, 25),
    "blue": QColor(0, 130, 200),
    "orange": QColor(245, 130, 48),
    "purple": QColor(197, 85, 231),
    "cyan": QColor(70, 240, 240),
    "magenta": QColor(240, 50, 230),
    "lime": QColor(153, 255, 0),
    "pink": QColor(250, 190, 212),
    "teal": QColor(0, 128, 128),
    "lavender": QColor(176, 135, 229),
}

tabs = [
    GridGraphConfig(
        "pmt",
        [
            GraphConfig(
                "pmt",
                hline="ion discriminator: ",
                hline_param=("Loading", "ion_threshold"),
                ylim=[0, 30],
                is_scrolling=True,
                max_datasets=1,
            ),
            0,
            0,
        ],
    ),
    #    gridGraphConfig('MM reduction',
    #                    [graphConfig('MM reduction',
    #                                 ylim=[0, 30], isScrolling=True,
    #                                 max_datasets=1),
    #                     0, 0]),
    #    gridGraphConfig('Drift Tracker',
    #                    [graphConfig('Drift Tracker'),
    #                     0, 0]),
    #    gridGraphConfig('Off Resonant Shelving Measurement',
    #                    [graphConfig('Off Resonant Shelving Measurement'),
    #                     0, 0]),
    #    gridGraphConfig('TD fluorescence',
    #                    [graphConfig('TD fluorescence'),
    #                     0, 0]),
    GridGraphConfig("tickle_scan", [GraphConfig("tickle_scan"), 0, 0]),
    GridGraphConfig(
        "Interleaved Linescan", [GraphConfig("Interleaved Linescan"), 0, 0]
    ),
    GridGraphConfig(
        "Wavemeter Linescan",
        [
            GraphConfig(
                "935_linescan",
                vline="935 Line center: ",
                vline_param=("Transitions", "repump_935"),
            ),
            0,
            0,
            GraphConfig(
                "822_linescan",
                vline="411 Line center: ",
                vline_param=("Transitions", "shelving_411"),
            ),
            1,
            1,
            GraphConfig(
                "760_linescan",
                vline="760 Line center: ",
                vline_param=("Transitions", "repump_760"),
            ),
            1,
            0,
            GraphConfig(
                "976_linescan",
                vline="976 Line center:",
                vline_param=("Transitions", "repump_976"),
            ),
            0,
            1,
        ],
    ),
    GridGraphConfig(
        "State Readout",
        [
            GraphConfig(
                "Histogram",
                is_hist=True,
                vline="StateReadout Threshold: ",
                vline_param=("StandardStateDetection", "state_readout_threshold"),
                max_datasets=2,
            ),
            0,
            0,
            GraphConfig(
                "Fidelity", is_scrolling=True, max_datasets=1, show_points=True
            ),
            1,
            0,
        ],
    ),
    #   gridGraphConfig('Quadrupole Linescan',
    #                    [graphConfig('Quadrupole Linescan',
    #                                 vline='Quadrupole Line center: ',
    #                                 vline_param=('Transitions', 'quadrupole')),
    #                     0, 0]),
    #    gridGraphConfig('DopplerCoolingLeakthroughTest',
    #                    [graphConfig('DopplerCoolingLeakthroughTest',
    #                                 max_datasets=5),
    #                     0, 0]),
    #    gridGraphConfig('Rabi Point Tracker',
    #                    [graphConfig('Rabi Point Tracker', isScrolling=True),
    #                     0, 0]),
    #    gridGraphConfig('Quadrupole Rabi Flopping',
    #                    [graphConfig('Quadrupole Rabi Flopping',
    #                                 vline='Quadrupole Pi time: ',
    #                                 vline_param=('QuadrupoleRabiFlopping', 'pi_time')),
    #                     0, 0]),
    GridGraphConfig(
        "Microwave Linescan",
        [
            GraphConfig(
                "Microwave Linescan qubit_0",
                vline="qubit_0 Line center: ",
                vline_param=("Transitions", "qubit_0"),
            ),
            0,
            0,
            GraphConfig(
                "Microwave Linescan qubit_plus",
                vline="qubit_plus Line center: ",
                vline_param=("Transitions", "qubit_plus"),
            ),
            1,
            1,
            GraphConfig(
                "Microwave Linescan qubit_minus",
                vline="qubit_minus Line center: ",
                vline_param=("Transitions", "qubit_minus"),
            ),
            1,
            0,
            GraphConfig(
                "Metastable Microwave Linescan",
                vline="Metastable Line center: ",
                vline_param=("Transitions", "qubit_minus"),
            ),
            0,
            1,
        ],
    ),
    GridGraphConfig(
        "Microwave Ramsey Experiment",
        [GraphConfig("Microwave Ramsey Experiment", show_points=True), 0, 0],
    ),
    # gridGraphConfig('Metastable Microwave Ramsey Experiment',
    #                 [graphConfig('Metastable Microwave Ramsey Experiment'),
    #                 0, 0]),
    GridGraphConfig(
        "Optical Pumping Rate",
        [GraphConfig("OpticalPumpingRate", show_points=True), 0, 0],
    ),
    #  gridGraphConfig('MeasurementDrivenRabiFlop',
    #                  [graphConfig('MeasurementDrivenRabiFlop', show_points=True),
    #                   0, 0]),
    #    gridGraphConfig('QuadrupoleOpticalPumpingLinescan',
    #                    [graphConfig('QuadrupoleOpticalPumpingLinescan',
    #                                 vline='Quadrupole Optical Pumping Line: ',
    #                                 vline_param=('OpticalPumping', 'quadrupole_op_detuning')),
    #                     0, 0]),
    GridGraphConfig(
        "Rabi Flopping",
        [
            GraphConfig(
                "Rabi Flopping qubit_0",
                vline="qubit_0 Pi time: ",
                vline_param=("Pi_times", "qubit_0"),
                show_points=True,
            ),
            0,
            0,
            GraphConfig(
                "Rabi Flopping qubit_plus",
                vline="qubit_plus Pi time: ",
                vline_param=("Pi_times", "qubit_plus"),
                show_points=True,
            ),
            1,
            1,
            GraphConfig(
                "Rabi Flopping qubit_minus",
                vline="qubit minus Pi time: ",
                vline_param=("Pi_times", "qubit_minus"),
                show_points=True,
            ),
            1,
            0,
            GraphConfig(
                "Metastable Qubit Rabi Flopping",
                vline="metastable Pi time: ",
                vline_param=("Pi_times", "qubit_minus"),
                show_points=True,
            ),
            0,
            1,
        ],
    ),
    #    gridGraphConfig('Randomized Benchmarking', [graphConfig('Randomized Benchmarking', show_points=True), 0, 0]),
    #    gridGraphConfig('ML Piezo Scan',
    #                    [graphConfig('ML Piezo Scan'),
    #                     0, 0]),
    #    gridGraphConfig('Images',
    #                    [graphConfig('Images', isImages=True), 0, 0]),
    #    gridGraphConfig('Ramsey Delay Stage Piezo Scan',
    #                    [graphConfig('Ramsey Delay Stage Piezo Scan'),
    #                     0, 0]),
    #    gridGraphConfig('ML_decoherence',
    #                    [graphConfig('ML_decoherence', max_datasets=3),
    #                     0, 0]),
    #    gridGraphConfig('PMT FFT',
    #                    [graphConfig('PMT FFT', max_datasets=5),
    #                     0, 0]),
    #   gridGraphConfig('Manifold Measurement',
    #                    [graphConfig('Manifolds', isScrolling=True, max_datasets=1),
    #                     1, 0]),
    GridGraphConfig(
        "Shelving", [GraphConfig("Shelving", max_datasets=5, show_points=True), 0, 0]
    ),
    #    gridGraphConfig('Hudson_linescan',
    #                    [graphConfig('Hudson_linescan',
    #                                 max_datasets=5),
    #                     0, 0]),
    #    gridGraphConfig('bf_fluorescence',
    #                    [graphConfig('bf_fluorescence', isScrolling=True,
    #                                 max_datasets=5),
    #                     0, 0]),
    # ,
    GridGraphConfig(
        "Frequency Monitor", [GraphConfig("Frequency Monitor", max_datasets=5), 0, 0]
    ),
    # gridGraphConfig('Image Fluorescence',
    #                [graphConfig('Image Fluorescence',
    #                             max_datasets=5),
    #                 0, 0])
    #    gridGraphConfig('TimeHarp', [graphConfig('TimeHarp', isHist=True, max_datasets=4), 0, 0])
    #    gridGraphConfig('Raman_411_Linescan',
    #                    [graphConfig('Raman_411_Linescan'),
    #                     0, 0]),
    #  gridGraphConfig('Metastable Microwave Linescan',
    #                  [graphConfig('Metastable Microwave Linescan'),
    #                   0, 0]),
]
