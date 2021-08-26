import matplotlib.pyplot as plt
import seaborn as sns

def plot_bar(data, x, y, title, label_x_axis='', label_y_axis='', with_annotation=True, save_as=''):
    sns.set_style('whitegrid')
    bar,ax = plt.subplots(figsize=(10,6))
    ax = sns.barplot(x=x, y=y, data=data, ci=None, palette='muted',orient='v', )
    ax.set_title(title, fontsize=18)
    ax.set_xlabel (label_x_axis)
    ax.set_ylabel (label_y_axis)

    if with_annotation:
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points')

    if not (save_as == ''):
        bar.savefig(save_as);