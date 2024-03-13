# ==================================================================================================
#                                           GLOBAL IMPORTS
# ==================================================================================================

import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from logger import *

# ==================================================================================================
#                                             MAIN CLASS
# ==================================================================================================

class plotter:

    def __init__(self, type, length_inch, width_inch):

        # Parameters
        # ------------------------------------------------------------------------------------------
        self.type = type  # LINE, SCATTER, SURFACE, BAR

        # Initializing plot
        # ------------------------------------------------------------------------------------------
        if (self.type == 'LINE') or (self.type == 'SCATTER'):

            self.axes = []
            self.axes.append(None)
            self.plot , self.axes[0] = plt.subplots(figsize=(length_inch,width_inch))
            self.front_axis = self.axes[0]

            self.axes_cnt = []
            self.axes_cnt.append(0)

            self.axis_id = 1
            self.axis_position = 0

            self.resolution = 480

    def set_resolution(self,resolution):

        self.resolution = resolution

    def add_axis(self,axis_type=None):

        if (self.type == 'LINE') or (self.type == 'SCATTER'):

            # Creating the new axis
            self.axes.append(None)
            self.axes[self.axis_id] = self.axes[0].twinx()

            # Updating axis count
            self.axes_cnt.append(None)
            self.axes_cnt[self.axis_id] = 0

            # Setting the axis position
            self.axes[self.axis_id].spines["left"].set_position(("axes", self.axis_position))
            self.axis_position += 1.2

            # Showing the spine (the vertical line) of the axis
            self.axes[self.axis_id].set_frame_on(True)
            self.axes[self.axis_id].patch.set_visible(False)
            for sp in self.axes[self.axis_id].spines.values():
                sp.set_visible(False)
            self.axes[self.axis_id].spines["left"].set_visible(True)

            # Incrementing the axis_id
            self.axis_id += 1

    def set_data(self, data, x_signal, y_signals, axes, zorder, kind=None, legends=None, dashes=None, trendlines=None, groupby=False, groupby_type=None):

        self.groupby = groupby
        self.groupby_type = groupby_type

        self.data = data
        self.kind = ['line' for signal in y_signals]

        if (self.type == 'LINE') or (self.type == 'SCATTER'):

            self.num_signals = len(y_signals)
            logger.info("num_signals: {}".format(self.num_signals))
            logger.info("y_signals: {}".format(y_signals))
            self.data_conf = []

            self.generate_color_hiearchy()

            for index in range(0,self.num_signals):

                signal_config = dict()
                signal_config['x_signal'] = x_signal
                signal_config['y_signal'] = y_signals[index]
                signal_config['legend'] = legends[index]
                signal_config['axis'] = self.axes[axes[index]]
                signal_config['axis_num'] = axes[index]
                self.axes_cnt[axes[index]] += 1
                signal_config['color'] = self.color_hierarchy[index]
                signal_config['zorder'] = float(zorder[index])

                if kind != None:
                    signal_config['kind'] = kind[index]
                else:
                    signal_config['kind'] = self.kind[index]

                # Updating the z-order of the axis
                # if float(self.axes[axes[index]].zorder) < signal_config['zorder']:
                #     self.axes[axes[index]].zorder = signal_config['zorder']

                if (self.type == 'LINE'):
                    signal_config['dash'] = dashes[index]

                if (self.type == 'SCATTER'):
                    signal_config['trendline'] = trendlines[index]

                self.data_conf.append(signal_config)

    def enable_gridlines(self,axis=0, gridline='major', color='red'):

        if gridline == 'major':
            self.axes[axis].grid(which='major', linestyle='-', linewidth='0.5', color=color)
        if gridline == 'minor':
            self.axes[axis].minorticks_on()
            self.axes[axis].grid(which='minor', linestyle=':', linewidth='0.5', color=color)

    # Note this must be run after populating
    def enable_legend(self):

        labels = [line.get_label() for line in self.lines]
        self.axes[0].legend(self.lines, labels, loc=0)

    # Note this must be run after populating
    def disable_legend(self):

        for axis in self.axes:
            try:
                axis.get_legend().remove()
            except:
                logger.info("Unable to remove axis...")
                pass

    def position_legend_left(self,axis_num):

        self.axes[axis_num].legend(bbox_to_anchor=(1.05, 1.0))

    def set_title(self,title):

        self.axes[0].set_title('{}\n'.format(title))

    # Note this must be run after populating
    def set_axis_label(self, axis_id, type, label, color):

        if (self.type == 'LINE') or (self.type == 'SCATTER'):

            if type == 'x':
                self.axes[axis_id].set_xlabel('\n{}\n\n'.format(label))
            elif type == 'y':
                self.axes[axis_id].set_ylabel('\n{}\n'.format(label))
                self.axes[axis_id].yaxis.label.set_color(color)

    def populate(self, colors=[],labels=[]):

        logger.info("Populating plot...")

        if self.type == 'LINE':

            self.lines = []
            self.legends = []
            index = 0

            for row in self.data_conf:
                logger.info("Populating {}...(axis: {}, legend: {}, color: {}, dash: {}, z: {})".format(row['y_signal'],
                                                                                                        row['axis_num'],
                                                                                                        row['legend'],
                                                                                                        row['color'],
                                                                                                        row['dash'],
                                                                                                        row['zorder']))
                self.lines.append(None)
                if row['kind'] == 'line':
                    self.lines[index]  = self.data.plot(x=row['x_signal'],
                                                        y=row['y_signal'],
                                                        color=row['color'],
                                                        dashes=row['dash'],
                                                        ax=row['axis'],
                                                        label=row['legend'],
                                                        zorder=row['zorder'],
                                                        kind=row['kind'])
                elif row['kind'] == 'bar':
                    self.lines[index] = self.data.plot(x=row['x_signal'],
                                                       y=row['y_signal'],
                                                       color=row['color'],
                                                       ax=row['axis'],
                                                       label=row['legend'],
                                                       zorder=row['zorder'],
                                                       kind=row['kind'])

                index += 1

        elif self.type == 'SCATTER':

            self.lines = []
            self.legends = []
            index = 0

            if self.groupby == False:
                for row in self.data_conf:
                    logger.info("Populating {}...(axis: {}, legend: {}, color: {}, z: {})".format(row['y_signal'],
                                                                                                  row['axis_num'],
                                                                                                  row['legend'],
                                                                                                  row['color'],
                                                                                                  row['zorder']))
                    self.lines.append(None)
                    self.lines[index] = self.data.plot.scatter(x=row['x_signal'],
                                                               y=row['y_signal'],
                                                               color=row['color'],
                                                               ax=row['axis'],
                                                               label=row['legend'],
                                                               zorder=row['zorder'])

                    if row['trendline'] == True:

                        polynomial = np.polyfit(self.data[row['x_signal']].values.tolist(),
                                                self.data[row['y_signal']].values.tolist(), 1)

                        x_poly = np.linspace(self.data[row['x_signal']].iloc[0], self.data[row['y_signal']].iloc[-1], 5,
                                             endpoint=True)

                        y_poly = np.poly1d(polynomial)(x_poly)

                        row['axis'].plot(x_poly, y_poly, linewidth=3, alpha=1, zorder=2)

                    index += 1

            elif self.groupby == True:

                if len(colors) > 0:
                    color_index = 0
                if len(labels) > 0:
                    label_index = 0

                for groupby_column , subset_data in self.data.groupby(self.groupby_type):

                    logger.info("Groupby_column: {}".format(groupby_column))
                    logger.info("Subset data: {}".format(subset_data))

                    logger.info(self.data_conf)
                    for row in self.data_conf:

                        if len(colors) > 0:
                            color = colors[color_index]
                            color_index+=1
                        else:
                            color = row['color']

                        if len(labels) > 0:
                            label = labels[label_index]
                            label_index+=1
                        else:
                            label = row['legend']

                        logger.info("Populating {}...(axis: {}, legend: {}, color: {}, z: {})".format(row['y_signal'],
                                                                                                      row['axis_num'],
                                                                                                      label,
                                                                                                      color,
                                                                                                      row['zorder']))

                        self.lines.append(None)
                        self.lines[index] = subset_data.plot.scatter(x=row['x_signal'],
                                                                     y=row['y_signal'],
                                                                     color=color,
                                                                     ax=row['axis'],
                                                                     label=label,
                                                                     zorder=row['zorder'])

                        if row['trendline'] == True:
                            polynomial = np.polyfit(subset_data[row['x_signal']].values.tolist(),
                                                    subset_data[row['y_signal']].values.tolist(), 1)

                            x_poly = np.linspace(subset_data[row['x_signal']].iloc[0],
                                                 subset_data[row['y_signal']].iloc[-1], 5,
                                                 endpoint=True)

                            y_poly = np.poly1d(polynomial)(x_poly)

                            row['axis'].plot(x_poly, y_poly, linewidth=1, alpha=2, zorder=row['zorder'])


        logger.info("Completed populating plot.")

    def show_plot(self):

        self.plot.show()
        logger.info("Please press enter to close plot and continue")
        input()

    def save_plot(self, dir, file_name):

        if dir == None:
            logger.critical('OUTPUT DIRECTORY WAS NOT SPECIFIED: Will not save plot')
        elif file_name == None:
            logger.critical('FILE NAME WAS NOT SPECIFIED: Will not save plot')
        elif os.path.isdir(dir) == True:
            self.plot.savefig(os.path.join(dir, '{}.png'.format(file_name)), dpi=self.resolution, bbox_inches='tight')
            logger.info('Created plot {}\{}.png'.format(dir,file_name))
        else:
            os.makedirs(dir)
            logger.info('Created directory {}'.format(dir))
            self.plot.savefig(os.path.join(dir, '{}.png'.format(file_name)), dpi=self.resolution, bbox_inches='tight')
            logger.info('Created plot {}\{}.png'.format(dir, file_name))

        self.close_plot()

    def close_plot(self):

        plt.close(self.plot)

    # ----------------------------------------------------------------------------------------------
    #                                   Color Generation Functions
    # ----------------------------------------------------------------------------------------------

    # TODO: THIS NEEDS TO BE FIXED THERE ARE REPEATING COLORS
    def generate_color_hiearchy(self):

        # Initializing parameters
        # ==============================================================================================================
        color_intensity = 0
        self.color_hierarchy = []
        color_hex = []
        for i in range(0,3):
            color_hex.append("")

        # Generating colors
        # ==============================================================================================================
        for color_intensity in range(0, self.num_signals):

            # Changing intensity
            inv_color_intensity = 255 - color_intensity

            # Changing which color to increment
            for i in range(0,3):

                color_hex[0] = self.get_hex(inv_color_intensity)
                color_hex[1] = self.get_hex(inv_color_intensity)
                color_hex[2] = self.get_hex(inv_color_intensity)

                color_hex[i] = self.get_hex(color_intensity)

                color_rgb = "#" + color_hex[0] + color_hex[1] + color_hex[2]
                self.color_hierarchy.append(color_rgb)

            color_intensity += 1

        # Removing extra colors
        # ==============================================================================================================
        if len(self.color_hierarchy) > self.num_signals:
            self.color_hierarchy = self.color_hierarchy[0: self.num_signals]

        # Setting first and last color (this is specifically for RPT
        # ==============================================================================================================
        logger.info(len(self.color_hierarchy))

        self.color_hierarchy[len(self.color_hierarchy)-2] = 'blue'  # Setting last color to red (this is current)
        self.color_hierarchy[len(self.color_hierarchy)-1] = 'red' # Setting last color to red (this is voltage)

        logger.debug("Colors being used in plot: {}".format(self.color_hierarchy))

    def get_hex(self,int_num):

        hex_str = hex(int_num)[2:]
        if len(hex_str) == 1:
            hex_str = hex(int_num)[2:] + hex(int_num)[2:]

        return hex_str

    # ----------------------------------------------------------------------------------------------
    #                                          3D-Plotting
    # ----------------------------------------------------------------------------------------------

    # 3D Plotting
    def plot_3d(self,X,Y,Z,z_lim_min,z_lim_max,title,x_label,y_label,z_label,file_name,directory):

        plt.rcParams["axes.labelweight"] = "bold"

        fig = plt.figure(figsize=(18,12))
        ax = fig.gca(projection='3d')

        X, Y = np.meshgrid(X, Y)
        Z = np.array(Z)
        Z = np.transpose(Z)

        # Plot the surface.
        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)

        # Customize the z axis.
        ax.set_zlim(z_lim_min, z_lim_max)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        # fig.colorbar(surf, shrink=0.5, aspect=5)

        fig.suptitle('{}'.format(title) + '\n\n', fontsize=18, fontweight='bold')
        logger.debug("X_label: {}".format(x_label))
        ax.set_xlabel('\n\n\n{}\n'.format(x_label),fontsize=18)

        logger.debug("Y_label: {}".format(y_label))
        ax.set_ylabel('\n\n\n{}\n'.format(y_label),fontsize=18)

        logger.debug("Z_label: {}".format(z_label))
        ax.set_zlabel('\n\n\n{}\n'.format(z_label),fontsize=18)

        fig.tight_layout()
        fig.savefig(os.path.join(directory, '{}.png'.format(file_name)))
        logger.info('Created plot {}\{}.png'.format(directory, file_name))


# ==================================================================================================
#                                            SAMPLE CODE
# ==================================================================================================

if __name__ == '__main__':

    # Creating a sample DF
    # ----------------------------------------------------------------------------------------------
    list = []
    list.append([1, 2, 3])
    list.append([2, 10, 5])
    list.append([3, 7, 1])
    list.append([4, 5, 2])
    list.append([5, 11, 1])
    df = pd.DataFrame(list,columns=['x','y','z'])

    # Plotting
    # ----------------------------------------------------------------------------------------------
    plot_obj = plotter(type='SCATTER', length_inch=5, width_inch=5)

    plot_obj.set_resolution(resolution=480)

    plot_obj.add_axis()

    plot_obj.set_data(data = df,
                      x_signal='x',
                      y_signals=['y','z'],
                      axes=[0,1],
                      legends=['this is y','this is z'],
                      dashes=['',''],
                      trendlines=[True,False])


    plot_obj.populate()

    plot_obj.set_axis_label(0, 'x', 'time','black')
    plot_obj.set_axis_label(0, 'y', 'distance', 'black')
    plot_obj.set_axis_label(1, 'y', 'velocity', 'black')

    plot_obj.enable_legend()

    # plot_obj.disable_legend()

    plot_obj.show_plot()

    plot_obj.save_plot(dir=r'C:\Users\anagarwal\Desktop', file_name='test')
