class ColorblindSafeColormaps:
    """
     A collection of colorblind-safe colormaps
    """
    def __init__(self):
        self.names = ["Vibrant", "Bright", "Muted", "Medium-Contrast", "Grayscale"]
        self.colors = [
            ["#0077BB", "#CC3311", "#33BBEE", "#EE7733", "#009988", "#EE3377", "#BBBBBB"],
            ["#4477AA", "#AA3377", "#66CCEE", "#EE6677", "#CCBB44", "#228833", "#BBBBBB"],
            ["#332288", "#882255", "#88CCEE", "#CC6677", "#44AA99", "#AA4499", "#117733",
            "#DDCC77", "#999933", "#DDDDDD"],
            ["#004488", "#994455", "#997700", "#6699CC", "#EE99AA", "#EECC66"],
            ["#444444", "#999999", "#666666", "#DDDDDD"],
        ]
    def get_names(self):
        """
        get_names returns a list of colormap names

        Returns:
            list of str: returns a list of colormap names
        """
        return self.names
    def get_count(self):
        """
        get_count returns the number of colormaps available

        Returns:
            int: the number of colormaps available
        """
        return len(self.names)
    def get_colors_by_index(self, index):
        """
        get_colors_by_index returns the colormap associated with index

        Args:
            index (int): the index of the colormap

        Returns:
            list of str: the list of colors in the colormap
        """
        return self.colors[index]
    def get_colors_by_name(self, name):
        """
        get_colors_by_name returns the colormap associated with name

        Args:
            name (str): the name of the colormap

        Returns:
            list of str: the list of colors in the colormap
        """
        return self.colors[self.names.index(name)]
    def get_colors(self, colors):
        """
        get_colors returns the colormap associated with name or index

        Args:
            name (str or int): the name or index of the colormap

        Returns:
            list of str: the list of colors in the colormap
        """
        if isinstance(colors, int):
            return self.get_colors_by_index(colors)
        return self.get_colors_by_name(colors)

if __name__ == "__main__":
   colormaps = ColorblindSafeColormaps()
   print("Number of colormaps: ", colormaps.get_count())
   print("Names of colormaps: ", colormaps.get_names())
   print(colormaps.get_colors_by_index(0))
   print(colormaps.get_colors_by_name("Vibrant"))
   print(colormaps.get_colors_by_index(-1))
   print(colormaps.get_colors_by_name("Grayscale"))
   print(colormaps.get_colors(0))
   print(colormaps.get_colors("Vibrant"))

