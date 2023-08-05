import ROOT
import numpy as np


def sample(source, nExpected, output_name):
    '''Draws a subset of a RooDataSet.
    
    Returns:
        A RooDataSet sampled from source. The number of events is
        determined by Poisson(nExpected).

    Note:
        An event may be drawn more than once.
    '''
    nEntries = source.numEntries()
    entries_to_draw = np.random.randint(0, nEntries, size=ROOT.gRandom.Poisson(nExpected))
    drawn_dataset = ROOT.RooDataSet(output_name, '', source.get(0))
    for entry in entries_to_draw:
        drawn_dataset.add(source.get(int(entry)))
    return drawn_dataset

