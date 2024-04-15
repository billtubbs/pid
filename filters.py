import math


def zoh_Fy(TfTs, Tx=1.0):
    """Zero-order-hold (ZOH) discretization of measurement 
    filter.

    Arguments
    ---------
    TfTs : float
        Number of filter time constants per nominal 
        sampling period: Tf/Ts.
    Tx: float
        Scale factor that relates nominal update period 
        Tx to actual: Tx*Ts.

    Returns
    -------
    a11, a12, a21, a22, b1, b2 : tuple of floats
        Discrete-time measurement filter system matrix elements.
    """

    # Help variables
    h1 = Tx / TfTs
    h2 = math.exp(-h1)
    h3 = h1 * h2
    h4 = h3 / TfTs

    # Filter parameters
    a11 = h2 + h3
    a12 = h2
    a21 = -h4
    a22 = h2 - h3
    b1 = 1 - h2 - h3
    b2 = h4

    return a11, a12, a21, a22, b1, b2


class Fy:

    def __init__(self, TfTs=10.0, Tx=1.0):
        """Discrete-time measurement filter

        Arguments
        ---------
        TfTs : float
            Number of filter time constants per nominal 
            sampling period: Tf/Ts.
        Tx: float
            Scale factor that relates nominal update period 
            Tx to actual: Tx*Ts.
        """

        # Params
        self.TfTs = TfTs  # Tf per nominal Ts
        self.discretize(Tx)

        # Filter state
        self.yf = None
        self.dyf = None
        self.Tx_old = None

    def discretize(self, Tx):
        self.a11, self.a12, self.a21, self.a22, self.b1, self.b2 = zoh_Fy(self.TfTs, Tx)

    def __call__(self, y, Tx=1.0):

        if Tx != self.Tx_old:
            # Rediscretize to match execution period
            self.discretize(Tx)

        # State update
        self.Tx_old = Tx
        self.yf, self.dyf = (self.a11 * self.yf + self.a12 * self.dyf + self.b1 * y,
                             self.a21 * self.yf + self.a22 * self.dyf + self.b2 * y)

        return self.yf, self.dyf
