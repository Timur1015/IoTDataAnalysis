import os
import re
from typing import List

import matplotlib.pyplot as plt


class IoTStandardPlotter:

    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_xlabel('Date')
        self.ax.grid(True)
        self.elements = []
        self.bar_heights = []

    def add_scatter(self, element, color):
        scatter = self.ax.scatter(element.index, element, label=element.name.replace('_', ' ').capitalize(),
                                  color=color)
        self.elements.append(scatter)
        self.ax.legend(loc='lower right')

    def add_hline(self, element, color, name: str):
        label = name.capitalize()
        if hasattr(element, 'name'):
            label += element.name.replace('_', ' ')
        line = self.ax.axhline(y=element, linestyle='-',
                               label=label,
                               color=color)
        self.elements.append(line)
        self.ax.legend(loc='lower right')

    def add_plot(self, element, color):
        plot = self.ax.plot(element.index, element, label=element.name.replace('_', ' ').capitalize(), color=color,
                            linestyle='-', alpha=0.6)
        self.elements.append(plot)
        self.ax.legend(loc='lower right')

    def add_bar(self, elements: List, categories, color, label_name, bottom=None):
        if bottom is not None:
            bar = self.ax.bar(categories, elements, bottom=self.bar_heights, color=color, label=label_name)
            for i, category in enumerate(categories):
                self.bar_heights[i] += elements[i]
                self.ax.text(category, self.bar_heights[i] - (elements[i] / 2), str(elements[i]), ha='center',
                             va='center')
            self.elements.append(bar)
        else:
            bar = self.ax.bar(categories, elements, color=color, label=label_name)
            self.bar_heights = elements
            for i, category in enumerate(categories):
                self.ax.text(category, elements[i] / 2, str(elements[i]), ha='center', va='center')
            self.elements.append(bar)
        self.ax.legend(loc='lower right')

    def remove_element_by_label(self, label: str):
        for element in self.elements:
            if element.get_label() == label:
                element.remove()
                self.elements.remove(element)
                self.ax.legend(loc='lower right')
                return True
        return False

    def clear_plot(self):
        self.ax.cla()
        self.elements.clear()
        self.ax.set_xlabel('Date')
        self.ax.grid(True)

    def get_element_labels(self):
        element_names = []
        for element in self.elements:
            element_names.append(element.get_label)

    def save_plot(self, use_case_num, solution_path):
        filename = str(use_case_num) + '_'
        title = self.ax.get_title()
        title = re.sub(r'[<>:"/\\|?*]', '', title)
        words = title.split()
        for word in words:
            filename += word.capitalize()
        path = os.path.join(solution_path, filename)
        self.fig.savefig(path)

    def show(self):
        self.fig.show()

    def set_title(self, title: str):
        self.ax.set_title(title)

    def set_ylabel(self, ylabel: str):
        self.ax.set_ylabel(ylabel)
