#!/usr/bin/env python3
import Show_class
import FigMaker
import webbrowser


def main(url):
    serie = Show_class.Show(url)
    figs = FigMaker.FigureMaker(serie)

    with open('p_graph.html', 'w') as f:
        f.write(figs.fig1().to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(figs.fig2().to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(figs.fig3().to_html(full_html=False, include_plotlyjs='cdn'))

    webbrowser.open_new_tab('p_graph.html')


if __name__ == "__main__":
    imdb_url = input("Give imdb url of a serie: ")
    main(imdb_url)
