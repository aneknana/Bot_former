import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def __columns_lenth__(table : pd.DataFrame, margin: float) -> list:
    ''' calculate columns lenth of dataframe '''
    head_as_row = np.concatenate(([table.columns.values], table.values))
    arr_str_len = np.vectorize(lambda x: margin + len(str(x))/5) #1 ~ 5 letters 
    return arr_str_len(head_as_row).max(axis=0)

def df_to_table(data: pd.DataFrame,
                row_height : float = 0.625,
                col_margin : float = 0.1,
                font_size : float = 14,
                header_color : str = '#40466e',
                header_txt_color : str = '#ffffff',
                header_txt_weight : str = 'bold',
                row_colors : list = None,
                data_txt_color : str = '#333333',
                data_txt_weight : str = 'bold',
                edge_color = 'w',
                ax = None):
    ''' dataframe to plot object '''
    if row_colors is None:
        row_colors = ['#cccccc', '#ffffff']

    cols_len = __columns_lenth__(data, col_margin)
    if ax is None:
        fig, ax = plt.subplots(dpi=400, figsize = (sum(cols_len),
                                                   row_height * (len(data) + 1)))
    ax.axis('off')
    cell_colours = list(map(lambda i: data.shape[1] * [row_colors[i[0] % len(row_colors)]],
                            enumerate(data.values)))

    mpl_table = ax.table(cellText = data.values,
                         cellColours = cell_colours,
                         cellLoc='center',
                         bbox = [0, 0, 1, 1],
                         colLabels = data.columns,
                         edges='BRTL',
                         colWidths=cols_len)
    mpl_table.set_fontsize(font_size)
    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0:
            cell.set_facecolor(header_color) 
            cell.set_text_props(weight=header_txt_weight,
                                color=header_txt_color)
        else:
            cell.set_text_props(weight=data_txt_weight,
                                color=data_txt_color)
    return ax.get_figure()
