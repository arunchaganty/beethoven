# Defines evaluators used for higher musical cognition

from mingus.containers import *
from mingus.core import *
import evaluators

BARS_PER_GENE = 5

def rhythmicContinuity(track):
    val = 0
    for i in xrange(4,len(track),BARS_PER_GENE):
        bar_ = track[i-1]
        bar = track[i]

        tmp_track = Track()
        tmp_track.add_bar(bar)
        noteDensity = evaluators.noteDensity(tmp_track)

        tmp_track = Track()
        tmp_track.add_bar(bar_)
        noteDensity_ = evaluators.noteDensity(tmp_track)

        variation = [0.0, 0.015, 0.05]

        # make sure the relative note density is in reasonable bounds
        val += evaluators.rangeCompare(abs(noteDensity_ - noteDensity), variation)
    return float(val)*BARS_PER_GENE/len(track)

def getRhythmicContour(track):
    contour_ = []
    for i in xrange(0,len(track),BARS_PER_GENE):
        tmp_track = Track()
        for j in xrange(BARS_PER_GENE):
            if i+j < len(track):
                tmp_track.add_bar(track[i+j])
        contour_.append(evaluators.noteDensity(tmp_track))

    min_elem = min(contour_)
    # Normalise the contours
    contour_ = [elem/min_elem for elem in contour_]
    # Shifted so that you can actually see some thing
    contour_ = [(100**(i-1) for i in contour_]

    return contour_


def rhythmicContour(track, contour):
    contour_ = getRhythmicContour(track)
    assert(len(contour) == len(contour_))
    val = 0
    var = [-0.01, 0, 0.01]
    for i in xrange(len(contour)):
        val += evaluators.rangeCompare((contour[i] - contour_[i]), var)

    return val

