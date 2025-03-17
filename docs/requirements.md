## Brief
I intend to develop an application for high school and primary school students to learn concepts about physics. These concepts can be as basic as newton's laws of motion, or as complicated as collison resolution. It will feature a lesson panel and a simulation where arbitrary convex polygons can be moved, collided and spawned to demonstrate semi-realistic physics laws. The lessons and the intial state of the canvas will be defined using parsed markdown files, which will allow for declarative code logic with imperative lesson building.

Physics is a complicated topic, with large amounts of prerequisite knowledge and equations. This can be overwhelming for some people, and for others who understand more complicated elements of physics, but don't fully grasp the fundamentals. However, as physics is such a universal topic, covering all topics and concepts in one application is infeasable.

Instead, my application will focus on basic physics principles, including the law of conservation of energy, newtons laws of motion and gravity. It will seperate each concept into a seperate "lesson", which will contain simple dot points on each topic; the aim of this application is to learn by example, not by rote. The lesson will define the principle, and provide relevant equations for calculating this.

The main feature of any given lesson will be the "simulation". The simulation will be next to the lesson, and take up approximately 2/3 of the total application width. Each simulation will be able to have two dimensional polygons placed within it, and they will collide with each other and the bounds of the simulation. This will be updated in real time to simulate natural motion, but disregarding complicated variables such as air resistance and friction. Each body will be considered "rigid", which simply means that it cannot be "broken" as a soft body would. This decreases the complication of implementing and handling collison by a *massive* amount.

Objects will be able to be pinned in place, and dragged around. Their velocity will change relative to the movement to allow "throwing". This is useful for demonstrating concepts such as the law of conservation of energy and newton's laws of motion.

Scene based variables such as gravity, which will be assumed to be relative to the y axis, can be varied using sliders to demonstrate the effects of gravity on bodies. When an object is pressed, a properties panel next to the simulation will display useful information such as velocity, mass, weight, restitution (elasticity) and other relevant information. Other informational toggles such as velocity component arrows will be provided for demonstratory purposes.

Having the scene information defined in a markdown file reduces the amount of formatting required to be done in a python file, which reduces the need for long, cumbersome strings. It also enables individuals to write their own lessons without needing knowledge of python; just markdown.


## Requirements
My application should:
- Have a graphical user interface (gui)
- Display an introductory screen, with information on how to navigate lessons and use the simulations
- Allow switching between lessons
    - A lesson is comprised of an information panel, and re-useable simulation canvas
- Simulate the motion of rigid bodies in real time with variable gravity and other parameters
- Update smoothly
- Handle user inputs such as pausing, playing, resetting, creating new shapes, and changing gravity
- Allow dragging shapes
- Detect and resolve collisions
- Read in lesson "instructions" from a markdown file
    - Render objects on the canvas from the metadata of the file
    - Create labels, images and equations using the main markdown text
- Allow visualising force components

## Design
### Abstract
#### Aesthetics/Quality
- Code will be written according to python [pep8](https://peps.python.org/pep-0008/) standards
    - Consistent formatting
    - snake_case variable naming
    - CamelCase classes
- Follow the object oriented paradigm where possible
- Use type annotation for both variables and function returns
- Avoid redundant code
- Minimize use of libraries
- Avoid redundant comments; focus on readable code

#### Function
- Each function accomplishes one thing
- Related functions grouped in one module
- Avoid dictionary returns; use named classes or tuples
- Modular; use interfaces to allow swapping of algorithms
- Use pythonic code principles
- Re-use code where possible
- Generic classes

### Specific
#### General
- Use tkinter for the interface
    - Use dynamic tkinter ttk where applicable
- Create classes for application elements
- Create vector classes with applicable calculatory methods
#### Parser
- Recursively open all markdown files in a directory for reading
- Iterate through each file
- Iterate through each line in the file
- Process and check for defined markdown elements such as headings and bullet points
    - Use regular expressions to simplify code and improve performance
    - Detect LaTeX maths expressions and render them as images using matplotlib
- Define cases for markdown elements to be different text sizes and styles
- Parse properties denoted by a `---` block and read in yaml-style inline object properties for rendering on the canvas
    - Ensure sanitzation
- Render discovered text and elements in a tkinter frame
- Use os.path.join for cross-platform compatability
#### Interface
- Display lesson frame next to canvas
- Allow resizing the canvas based on window size; update bounds
- Create buttons that pause the simulation
- Allow resetting canvas on switching lessons

#### Simulation
- Choose a collision algorithm; sat/gjk
    - Performance testing
- Create a function to draw polygons as a set of vertices
- Store individual object data in a rigidbody class
- Store objects in an engine class
- Step the simulation based on a time delta
- Calculate the new position of objects given properties and velocity over the time step
- Check for collisions between objects
- Resolve bad collisions by updating velocity and position
- Enforce bounds by defining "object" walls
    - Resize bounds based on canvas dimensions
- Draw non-existent shapes found in engine
- Change coordinates of existing shapes by calling their method to return vertices
- Setup handlers using tkinter event handlers for dragging and mouse movement

## Specifications
- Developed on and for linux, needs to run on windows, not going to be tested for macos
- Target python versions 3.12 and above for type annotation
- tkinter library required
- matplotlib library required
- Should work across various screen sizes
markdown.