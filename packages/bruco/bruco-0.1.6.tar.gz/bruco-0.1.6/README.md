Brute force coherence (Gabriele Vajente, 2021-01-20 vajente@caltech.edu)

Command line arguments (with default values)

--ifo                                     interferometer prefix [H1, L1, V1] 
                                          (no default, must specify)

--channel=OAF-CAL_DARM_DQ                 name of the main channel

--excluded=bruco_excluded_channels.txt    file containing the list of channels excluded 
                                          from the coherence computation

--gpsb=1087975458                         starting time

--length=180                              amount of data to use (in seconds)

--outfs=8192                              sampling frequency of the output results 
                                          (coherence will be computed up to outfs/2 
                                          if possible)

--minfs=512                               skip all channels with samplig frequency 
                                          smaller than this

--naver=100                               number of averages to compute the coherence

--dir=bruco                               output directory

--top=100                                 for each frequency, save to cohtab.txt and 
                                          idxtab.txt this maximum number of coherence 
                                          channels

--webtop=20                               show this number of coherence channels per 
                                          frequency, in the web page summary

--plot=png                                plot format (png, pdf, none)

--nproc                                   number of processes to use (if not specified,
                                          use all CPUs)

--calib                                   name of a text file containing the calibration 
                                          transfer function to be applied to the target 
                                          channel spectrum, in a two column format 
                                          (frequency, absolute value)

--xlim                                    limits for the frequency axis in plots, in the 
                                          format fmin:fmax

--ylim                                    limits for the y axis in PSD plots, in the 
                                          format ymin:ymax

--tmp=~/tmp                               temporary file directory where cache files 
                                          will be saved if needed

Example:
./bruco.py --ifo=H1 --channel=CAL-DELTAL_EXTERNAL_DQ 
           --calib=share/lho_cal_deltal_calibration.txt 
           --gpsb=1111224016 --length=600 --outfs=4096 --naver=100 
           --dir=./bruco_1111224016 --top=100 --webtop=20 --xlim=1:1000 
           --ylim=1e-20:1e-14 --excluded=share/bruco_excluded_channels.txt

