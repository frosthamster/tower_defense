from Event import Event
from model.Direction import Direction
from model.GameObject import GameObject


class MovableGameObject(GameObject):
    def __init__(self, location, road, **kwargs):
        super().__init__(location, **kwargs)
        if len(road) < 1:
            raise ValueError
        self._velocity = 2
        self._max_velocity = 2
        self._road = road
        self._destination_node_number = 0
        self.on_end = Event()

    @property
    def curr_destination(self):
        return self._road[self._destination_node_number]

    @property
    def destination(self):
        return self._road[-1]

    def _get_next_step(self):
        if not self.destination or self._destination_node_number == \
                        len(self._road) - 1 and \
                        (self._location - self.destination).length() < 1:
            self._remove()
            self.on_end.fire()
            return self._location

        direction = self.curr_destination - self._location
        length_to_destination = direction.length()
        transition = direction.normalize() * self._velocity

        if transition.length() < length_to_destination:
            return self._location + transition

        destination = self.curr_destination
        if self._destination_node_number < len(self._road) - 1:
            self._destination_node_number += 1
        return destination

    def tick(self):
        super().tick()
        next_location = self._get_next_step()
        dir_sign = 1 if next_location[0] - self._location[0] > 0 else -1
        self._direction = Direction(dir_sign)
        self._location = next_location
