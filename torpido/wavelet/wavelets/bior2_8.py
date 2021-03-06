""" Biorthogonal 2.8 wavelet """


class Biorthogonal28:
    """
    Properties
    ----------
     near symmetric, not orthogonal, biorthogonal

    All values are from http://wavelets.pybytes.com/wavelet/bior2.8/
    """
    __name__ = "Biorthogonal Wavelet 2.8"
    __motherWaveletLength__ = 18  # length of the mother wavelet
    __transformWaveletLength__ = 2  # minimum wavelength of input signal

    # decomposition filter
    # low-pass
    decompositionLowFilter = [
        0.0,
        0.0015105430506304422,
        -0.0030210861012608843,
        -0.012947511862546647,
        0.02891610982635418,
        0.052998481890690945,
        -0.13491307360773608,
        -0.16382918343409025,
        0.4625714404759166,
        0.9516421218971786,
        0.4625714404759166,
        -0.16382918343409025,
        -0.13491307360773608,
        0.052998481890690945,
        0.02891610982635418,
        -0.012947511862546647,
        -0.0030210861012608843,
        0.0015105430506304422,
    ]

    # high-pass
    decompositionHighFilter = [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.3535533905932738,
        -0.7071067811865476,
        0.3535533905932738,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ]

    # reconstruction filters
    # low pass
    reconstructionLowFilter = [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.3535533905932738,
        0.7071067811865476,
        0.3535533905932738,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ]

    # high-pass
    reconstructionHighFilter = [
        0.0,
        -0.0015105430506304422,
        -0.0030210861012608843,
        0.012947511862546647,
        0.02891610982635418,
        -0.052998481890690945,
        -0.13491307360773608,
        0.16382918343409025,
        0.4625714404759166,
        -0.9516421218971786,
        0.4625714404759166,
        0.16382918343409025,
        -0.13491307360773608,
        -0.052998481890690945,
        0.02891610982635418,
        0.012947511862546647,
        -0.0030210861012608843,
        -0.0015105430506304422,
    ]
