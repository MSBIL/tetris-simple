"""
Shape Class
"""
from dataclasses import dataclass, field
import json
with open('./conf/conf.json', 'r') as file:
    game_config = json.load(file)

@dataclass(init=False)
class Shape:
    """
        Shape represents possible shapes in tetris games
        Valid shapes are (Q,Z,S,T,I,L,J)
        valid shapes controlled in configuration file of the project (conf/conf.json)
        A Shape contains its code (e.g. Q,I) and width and height
        Coordinates of a shape are relative, (0,0) denotes the upper left corner of a shape
        Blueprint is string representation of shape, (e.g. L="1111")
        shape_coords is the relative coordinates of non-empty parts of a shape
        e.g. in L, relative coordinates starting from upper left part of blueprint
        would be (0,0), (1,0), (2,0), (2,1)
    """
    code: str
    width: int = 0
    height: int = 0
    shape_coords: list[(int, int)] = field(default_factory=list)

    def __init__(self, code):
        self.code = code
        self.config_shape_str = 'shape_' + self.code.lower()
        try:
            self.blueprint = game_config['valid_shapes'][self.config_shape_str]
        except KeyError as exc:
            raise Exception(f"Shape {self.code} is not created in configuration. Error {exc}") from exc
        self.width = len(self.blueprint[0])
        self.height = len(self.blueprint)
        self.shape_coords = set(list(self._create_shape_coords()))

    def _get_blueprint(self) -> list[str]:
        """

        :return:
        """
        """Returns string representation that defines how the shape looks like."""
        return self.blueprint

    def get_shape_coords(self) -> list[(int, int)]:
        """Returns relative coordinates that make up the shape."""
        return self.shape_coords

    def _create_shape_coords(self):
        """Creates relative coordinate representation of shape from blueprint"""
        blueprint = self._get_blueprint()
        width = len(blueprint[0])
        height = len(blueprint)
        for offset_y in range(height):
            for offset_x in range(width):
                if blueprint[offset_y][offset_x] != '0':
                    yield offset_y, offset_x

    def __str__(self):
        return f"Blueprint and coordinate representation of shape " \
               f"{self.code} is {self.blueprint} and {self.get_shape_coords()}"
