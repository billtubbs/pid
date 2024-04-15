import math


def zoh_Fy(TfTs, Tx=1.0):

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


def anti_windup(Dui, windup):
    # Prevent increase, decrease, or both
    if windup == 'both' or windup == 'lower':
        Dui = max(Dui, 0)
    if windup == 'both' or windup == 'upper':
        Dui = min(Dui, 0)
    return Dui


class Fy:

    def __init__(self, TfTs=10.0, Tx=1.0):

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
        yf1 = self.yf
        self.Tx_old = Tx
        self.yf = self.a11 * yf1 + self.a12 * self.dyf + self.b1 * y
        self.dyf = self.a21 * yf1 + self.a22 * self.dyf + self.b2 * y

        return self.yf, self.dyf


class PID:

    def __init__(self):

        # Initialize parameter states
        self.kp = None
        self.kp = None
        self.ki = None
        self.kd = None
        self.umin = None
        self.umax = None
        self.u0 = None
        self.b = 1

        # Initialize signal states
        self.u_old = None
        self.up_old = None
        self.ud_old = None
        self.uff_old = None

    def __call__(self, r, y, uff, uman, utrack, Tx=1.0,
                 track=False, auto=True, windup=None):

        # Filter updates
        yf, dyf = Fy(y, Tx)

        if auto:
            if self.ki == 0:
                self.u_old = self.u0  # Bias term if P or PD control
                self.up_old = 0
                self.ud_old = 0
                self.uff_old = 0
                self.b = 1

            if track:  # Tracking mode
                u_old = utrack
                up_old = 0
                ud_old = 0
                uff_old = 0

            # Control signal increments
            Dup = self.kp * (self.b * r - yf) - up_old
            Dui = self.ki * (r - yf) * Tx
            Dui = anti_windup(Dui, windup)
            Dud = (-self.kd * dyf - ud_old) / Tx
            Duff = uff - uff_old

            # Add control signal increment
            Du = Dup + Dui + Dud + Duff
            u = u_old + Du

        else:
            u = uman # Manual control signal

        # Saturate and send control signal
        self.u = max(min(u, self.umax), self.umin)

        # Update old signal states
        self.u_old = u
        self.up_old = self.kp * (self.b * r - yf)
        self.ud_old =  -self.kd * dyf
        self.uff_old = uff
