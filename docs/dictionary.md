| **Variable**            | **Data type**           | **Format (display)**   | **Description**                               | **Example**           | **Validation**                         |
|-------------------------|-------------------------|------------------------|-----------------------------------------------|-----------------------|----------------------------------------|
| `acceleration`           | `Vec2`                  | `(x, y)`               | Represents acceleration in 2D space           | `(0.0, 9.8)`          | Tuple of floats                        |
| `angle`                 | `Real` (or `float`)     | `decimal`              | The angle of rotation in radians              | `1.57`                | Non-negative, in radians              |
| `angular_acc`           | `float`                 | `decimal`              | Angular acceleration                          | `0.1`                 | Non-negative                           |
| `angular_velocity`      | `float`                 | `decimal`              | Angular velocity                              | `5.0`                 | Non-negative                           |
| `annotations`           | `list`                  | `[annotation1, ...]`    | List of annotations for physics objects       | `[note1, note2]`      | List of `str`                           |
| `app`                   | `Application`           | `Application`          | Main application instance                     | `app = Application(root)` | Instance of `Application` |
| `bodies`                | `list`                  | `[object1, object2]`    | List of body objects in the simulation        | `[body_a, body_b]`    | List of `RigidBody` objects            |
| `canvas`                | `tkinter.Canvas`        | `Canvas`               | Canvas for rendering in Tkinter               | `canvas = Canvas(root)` | Must be a `tk.Canvas` instance       |
| `force`                 | `Vec2`                  | `(x, y)`               | Force applied to a body in vector form        | `(10.0, -5.0)`        | Tuple of floats                        |
| `gravity`               | `Real` (or `float`)     | `decimal`              | Gravitational constant used in the simulation | `9.8`                 | Positive value                         |
| `velocity`              | `Vec2`                  | `(x, y)`               | The velocity of an object in 2D space         | `(1.0, 0.0)`          | Tuple of floats                        |
| `time_step`             | `float`                 | `decimal`              | The time step in the simulation              | `0.016`               | Non-negative, small value             |
| `objects`               | `dict`                  | `key-value pairs`      | Dictionary holding objects and their properties | `{1: body1, 2: body2}` | Keys are integers, values are objects |
| `root`                  | `Tk`                    | `Tk()`                 | The main Tkinter window object               | `root = Tk()`         | Instance of `tk.Tk`                   |
| `scalar`                | `float`                 | `decimal`              | A scalar value, often used for scalar fields or physics quantities | `1.0`  | Non-negative                          |
| `Vec2`                  | `class`                 | `Vec2(x, y)`           | Represents a 2D vector object                 | `Vec2(1.0, 2.0)`      | Tuple of two floats                    |
| `velocity_x`            | `float`                 | `decimal`              | X-component of velocity                      | `2.0`                 | Float                                 |
| `velocity_y`            | `float`                 | `decimal`              | Y-component of velocity                      | `3.0`                 | Float                                 |
| `body_a`                | `RigidBody`             | `RigidBody`            | Represents a rigid body object               | `body_a = RigidBody()` | Instance of `RigidBody`               |
| `mass`                  | `Real` (or `float`)     | `decimal`              | Mass of an object                            | `2.5`                 | Positive number                        |
| `position`              | `Vec2`                  | `(x, y)`               | Position of the object in 2D space           | `(5.0, 6.0)`          | Tuple of floats                        |
| `button`                | `tkinter.Button`        | `Button`               | Button widget in Tkinter for user input       | `Button(root)`        | Must be an instance of `tk.Button`    |
| `apply_force`           | `function`              | `function`             | Function that applies force to an object      | `apply_force(force)`  | Callable function                      |
| `clear_button`          | `tkinter.Button`        | `Button`               | Button for clearing objects                  | `clear_button = Button(root)` | Instance of `tk.Button` |
| `body_renderer`         | `BodyRenderer`          | `BodyRenderer`         | Renders bodies in the simulation              | `body_renderer = BodyRenderer()` | Instance of `BodyRenderer` |
| `collision`             | `CollisionResult`       | `CollisionResult`      | Result object holding collision information  | `collision = CollisionResult()` | Instance of `CollisionResult` |
| `clear`                 | `function`              | `function`             | Function to clear elements in the simulation  | `clear()`             | Callable function                      |
| `draw_polygon`          | `function`              | `function`             | Function to draw polygons on canvas           | `draw_polygon()`      | Callable function                      |
| `draw_velocity_arrows`  | `function`              | `function`             | Function to draw velocity arrows              | `draw_velocity_arrows()` | Callable function                   |
| `columnconfigure`       | `method`                | `method`               | Method to configure columns in a grid layout | `root.columnconfigure(0, weight=1)` | Method of `Tk`                     |
| `grid`                  | `method`                | `method`               | Method to place widgets in a grid layout      | `widget.grid(row=0, column=1)` | Method of `Tk`                        |
| `font`                  | `str`                   | `font-name`            | Font name for rendering text in Tkinter       | `"Arial"`             | String                                 |
| `btn`                   | `tkinter.Button`        | `Button`               | Button instance in Tkinter                    | `btn = Button(root)`  | Instance of `tk.Button`               |
| `latex_expr`            | `str`                   | `string`               | LaTeX string to render in Tkinter             | `latex_expr = "$\\vec{v}$"` | LaTeX formatted string             |
| `latex_images`          | `dict`                  | `{expr: image}`        | Mapping of LaTeX expressions to image objects | `latex_images["$\\vec{v}$"]` | Dict of LaTeX expressions to images  |
| `interaction_manager`   | `InteractionManager`    | `InteractionManager`   | Manages interactions in the physics simulation | `interaction_manager = InteractionManager()` | Instance of `InteractionManager` |
| `step`                  | `function`              | `function`             | Function for simulating one time step        | `step()`              | Callable function                      |
| `objects_map`           | `dict`                  | `key-value pairs`      | Mapping of object IDs to `RigidBody` objects | `{1: body1, 2: body2}` | Keys are integers, values are `RigidBody` |
| `sides`                 | `int`                   | `integer`              | Number of sides of a polygon                 | `4`                   | Integer between 3 and 10              |
| `result`                | `dict`                  | `key-value pairs`      | Dictionary holding results of the simulation | `{ "collision": True }` | Key-value pairs                      |
| `output_dir`            | `str`                   | `directory path`       | Directory for saving outputs                 | `"/path/to/dir"`      | String path                            |
| `moment_of_inertia`     | `float`                 | `decimal`              | Moment of inertia of the body                | `10.0`                | Non-negative                           |
| `collision_result`      | `CollisionResult`       | `CollisionResult`      | Result of a collision detection              | `collision_result = CollisionResult()` | Instance of `CollisionResult` |

