import Database
import StatCache
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def stat_figure(stat_name):

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    axis.plot(StatCache.circular_all(Database.connect_redis(), stat_name)[::-1])


    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    return output
