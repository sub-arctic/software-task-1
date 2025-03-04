from body import Bodies


class PhysicsEngine:
    def __init__(self) -> None:
        self._bodies: Bodies = Bodies()
        self._gravity = None

    @property
    def bodies(self) -> Bodies:
        return self._bodies

    def update(self, delta_time: float, canvas_width: int, canvas_height: int) -> None:
        pass
