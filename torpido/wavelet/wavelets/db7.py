""" Daubechies 7 wavelet """


class Daubechies7:
    """
    Properties
    ----------
    asymmetric, orthogonal, bi-orthogonal

    All values are from http://wavelets.pybytes.com/wavelet/db7/
    """
    __name__ = "Daubechies Wavelet 7"
    __motherWaveletLength__ = 14  # length of the mother wavelet
    __transformWaveletLength__ = 2  # minimum wavelength of input signal

    # decomposition filter
    # low-pass
    decompositionLowFilter = [
        0.0003537138000010399,
        - 0.0018016407039998328,
        0.00042957797300470274,
        0.012550998556013784,
        - 0.01657454163101562,
        - 0.03802993693503463,
        0.0806126091510659,
        0.07130921926705004,
        - 0.22403618499416572,
        - 0.14390600392910627,
        0.4697822874053586,
        0.7291320908465551,
        0.39653931948230575,
        0.07785205408506236,
    ]

    # high-pass
    decompositionHighFilter = [
        -0.07785205408506236,
        0.39653931948230575,
        - 0.7291320908465551,
        0.4697822874053586,
        0.14390600392910627,
        - 0.22403618499416572,
        - 0.07130921926705004,
        0.0806126091510659,
        0.03802993693503463,
        - 0.01657454163101562,
        - 0.012550998556013784,
        0.00042957797300470274,
        0.0018016407039998328,
        0.0003537138000010399
    ]

    # reconstruction filters
    # low pass
    reconstructionLowFilter = [
        0.07785205408506236,
        0.39653931948230575,
        0.7291320908465551,
        0.4697822874053586,
        - 0.14390600392910627,
        - 0.22403618499416572,
        0.07130921926705004,
        0.0806126091510659,
        - 0.03802993693503463,
        - 0.01657454163101562,
        0.012550998556013784,
        0.00042957797300470274,
        - 0.0018016407039998328,
        0.0003537138000010399
    ]

    # high-pass
    reconstructionHighFilter = [
        0.0003537138000010399,
        0.0018016407039998328,
        0.00042957797300470274,
        - 0.012550998556013784,
        - 0.01657454163101562,
        0.03802993693503463,
        0.0806126091510659,
        - 0.07130921926705004,
        - 0.22403618499416572,
        0.14390600392910627,
        0.4697822874053586,
        - 0.7291320908465551,
        0.39653931948230575,
        - 0.07785205408506236
    ]
