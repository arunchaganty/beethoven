set term png;

set output 'pitchVariety.png';
set title 'pitchVariety.png';
plot "features.dat" using 2;

set output 'pitchRange.png';
set title 'pitchRange.png';
plot "features.dat" using 3;

set output 'keyCentric.png';
set title 'keyCentric.png';
plot "features.dat" using 4;

set output 'nonScaleCount.png';
set title 'nonScaleCount.png';
plot "features.dat" using 5;

set output 'dissonance.png';
set title 'dissonance.png';
plot "features.dat" using 6;

set output 'noteDensity.png';
set title 'noteDensity.png';
plot "features.dat" using 7;

set output 'restDensity.png';
set title 'restDensity.png';
plot "features.dat" using 8;

set output 'rhythmicVariety.png';
set title 'rhythmicVariety.png';
plot "features.dat" using 9;

set output 'rhythmicRange.png';
set title 'rhythmicRange.png';
plot "features.dat" using 10;

set output 'syncopation.png';
set title 'syncopation.png';
plot "features.dat" using 11;


