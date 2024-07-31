class Point:
    _temp: float
    _speed: float

    def __init__(self, *, temp: float, speed: float):
        self._temp = temp
        self._speed = max(0.0, min(1.0, speed))

    def get_temp(self) -> float:
        return self._temp

    def get_speed(self) -> float:
        return self._speed


class Curve:
    _points: list[Point]

    def __init__(self, *, points: list[Point]):
        if len(points) == 0:
            raise ValueError("No points defined in curve")

        # Ensure that the list of points does not contain duplicate
        # temperature values.
        seen = set()
        for point in points:
            if point.get_temp() in seen:
                raise ValueError("Curve contains duplicate temperature points")
            seen.add(point.get_temp())

        points.sort(key=lambda p: p.get_temp())
        self._points = points

    def get_speed(self, *, temp: float) -> float:
        if len(self._points) == 1:
            return self._points[0]

        # If the temperature is below the first point, return the speed of the
        # first point.
        if temp <= self._points[0].get_temp():
            return self._points[0].get_speed()

        # If the temperature is above the last point, return the speed of the
        # last point.
        if temp >= self._points[-1].get_temp():
            return self._points[-1].get_speed()

        # Find the interval that the temperature falls within.
        intv: tuple[Point, Point] | None = None
        for cp, np in zip(self._points, self._points[1:]):
            if cp.get_temp() <= temp <= np.get_temp():
                intv = (cp, np)
                break

        if intv is None:
            raise RuntimeError("Failed to find interval for temperature")

        # Linear interpolation between the two points.
        lt, ls = intv[0].get_temp(), intv[0].get_speed()
        rt, rs = intv[1].get_temp(), intv[1].get_speed()
        return ls + (rs - ls) * ((temp - lt) / (rt - lt))
