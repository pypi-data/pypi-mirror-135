import numpy as np

import py2dmat
import py2dmat.solver.function


def quadratics(xs: np.ndarray) -> float:
    """quadratic (sphear) function

    It has one global miminum f(xs)=0 at xs = [0,0,...,0].
    """
    return np.sum(xs * xs)


def quartics(xs: np.ndarray) -> float:
    """quartic function with two minimum

    It has two global minimum f(xs)=0 at xs = [1,1,...,1] and [0,0,...,0].
    It has one suddle point f(0,0,...,0) = 1.0.
    """

    return np.mean((xs - 1.0) ** 2) * np.mean((xs + 1.0) ** 2)


def ackley(xs: np.ndarray) -> float:
    """Ackley's function in arbitrary dimension

    It has one global minimum f(xs)=0 at xs=[0,0,...,0].
    It has many local minima.
    """
    a = np.mean(xs ** 2)
    a = 20 * np.exp(-0.2 * np.sqrt(a))
    b = np.cos(2.0 * np.pi * xs)
    b = np.exp(0.5 * np.sum(b))
    return 20.0 + np.exp(1.0) - a - b


def rosenbrock(xs: np.ndarray) -> float:
    """Rosenbrock's function

    It has one global minimum f(xs) = 0 at xs=[1,1,...,1].
    """
    return np.sum(100.0 * (xs[1:] - xs[:-1] ** 2) ** 2 + (1.0 - xs[:-1]) ** 2)


def himmelblau(xs: np.ndarray) -> float:
    """Himmelblau's function

    It has four global minima f(xs) = 0 at
    xs=[3,2], [-2.805118..., 3.131312...], [-3.779310..., -3.2831860], and [3.584428..., -1.848126...].
    """
    if xs.shape[0] != 2:
        raise RuntimeError(
            f"ERROR: himmelblau expects d=2 input, but receives d={xs.shape[0]} one"
        )
    return (xs[0] ** 2 + xs[1] - 11.0) ** 2 + (xs[0] + xs[1] ** 2 - 7.0) ** 2


def linear_regression_test(xs: np.ndarray) -> float:
    """ Negative log likelihood of linear regression with Gaussian noise N(0,sigma)

    y = ax + b

    trained by xdata = [1, 2, 3, 4, 5, 6] and ydata = [1, 3, 2, 4, 3, 5].

    Model parameters (a, b, sigma) are corresponding to xs as the following,
    a = xs[0], b = xs[1], log(sigma**2) = xs[2]

    It has a global minimum f(xs) = 1.005071.. at
    xs = [0.628571..., 0.8, -0.664976...].    
    """
    if xs.shape[0] != 3:
        raise RuntimeError(
            f"ERROR: regression expects d=3 input, but receives d={xs.shape[0]} one"
        )

    xdata = np.array([1, 2, 3, 4, 5, 6])
    ydata = np.array([1, 3, 2, 4, 3, 5])
    n = len(ydata)

    return 0.5 * (
        n * xs[2] + np.sum((xs[0] * xdata + xs[1] - ydata) ** 2) / np.exp(xs[2])
    )


class Solver(py2dmat.solver.function.Solver):
    """Function Solver with pre-defined benchmark functions"""

    x: np.ndarray
    fx: float

    def __init__(self, info: py2dmat.Info) -> None:
        """
        Initialize the solver.

        Parameters
        ----------
        info: Info
        """
        super().__init__(info)
        self._name = "analytical"
        function_name = info.solver.get("function_name", "quadratics")

        if function_name == "quadratics":
            self.set_function(quadratics)
        elif function_name == "quartics":
            self.set_function(quartics)
        elif function_name == "ackley":
            self.set_function(ackley)
        elif function_name == "rosenbrock":
            self.set_function(rosenbrock)
        elif function_name == "himmelblau":
            dimension = self.dimension
            if int(dimension) != 2:
                raise RuntimeError(
                    f"ERROR: himmelblau works only with dimension=2 but input is dimension={dimension}"
                )
            self.set_function(himmelblau)
        elif function_name == "linear_regression_test":
            dimension = self.dimension
            if int(dimension) != 3:
                raise RuntimeError(
                    f"ERROR: regression works only with dimension=2 but input is dimension={dimension}"
                )
            self.set_function(linear_regression_test)
        else:
            raise RuntimeError(f"ERROR: Unknown function, {function_name}")
