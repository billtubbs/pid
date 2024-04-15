from filters import Fy


def anti_windup(Dui, windup):
    # Prevent increase, decrease, or both
    if windup == 'both' or windup == 'lower':
        Dui = max(Dui, 0)
    if windup == 'both' or windup == 'upper':
        Dui = min(Dui, 0)
    return Dui


class PID:

    def __init__(self, kp, ki, kd, umin, umax, u0, b=1):

        # Initialize parameter states
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.umin = umin
        self.umax = umax
        self.u0 = u0
        self.b = b

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
                self.u_old = utrack
                self.up_old = 0
                self.ud_old = 0
                self.uff_old = 0

            # Control signal increments
            Dup = self.kp * (self.b * r - yf) - self.up_old
            Dui = self.ki * (r - yf) * Tx
            Dui = anti_windup(Dui, windup)
            Dud = (-self.kd * dyf - self.ud_old) / Tx
            Duff = uff - self.uff_old

            # Add control signal increment
            Du = Dup + Dui + Dud + Duff
            u = self.u_old + Du

        else:
            u = uman # Manual control signal

        # Saturate and send control signal
        self.u = max(min(u, self.umax), self.umin)

        # Update old signal states
        self.u_old = u
        self.up_old = self.kp * (self.b * r - yf)
        self.ud_old =  -self.kd * dyf
        self.uff_old = uff
