*****************
THE EASY ANIMATOR
******************

Changes to the Model from Assignment9
**************************************


- IModel interface updated to remove unnecessary method definitions
  Some new methods like  getShapesAtFrame to give list of shapes at each tick
  to controller were added.
- In AnimationModelImpl, addShape method was updated to add a shape with default values,
  since the txt files only declare shapes initially. Shape dimensions are to be found
  only when there is an animation performed on it or there is an instruction for it 
  to just appear on the animation screen for particular time interval. 
  So when shape is initially added to the model, its default values are mapped and 
  through setter methods its real values are updated when we encounter an animation for it
  in the text file

- In AnimationModelImpl, addAction method signature was updated to have all from and to parameters.
  During Assignment9, it was assumed that motion type would specified while trying to add motion
  for a shape. But the text file gives from and to values for all parameters. And from their difference
  motion type that needs to be added to animation list needs to be determined. So, addAction method
  signature was amended to accept all from and to parameters for the shape
- In addition to Move, Scale and Colorchange animation classes that were constructed in Assignment9,
  an addtional Appear animatino was added. In the text files provided, there are frequent instances
  that shape appears on the screen and there is no change in from and to parameters besides start and end time.
  Such instances have been categorized under Appear animation class.
- createShapesAtTickTable method was added to AnimationModelImpl class which supports creation of 
  hashmap which contains a list of shapes that are active/have attributes for each tick of the animation.
- ShapeAnimate class was created in A9 to support setting up
  shapes' appearance and disappearnce time.
  That class has been eliminated, and now shapes disappearance time
  and appearnce time setter and getter methods are added to IShape interface.
- IShape interface was updated to have setter and getter methods for 
  x, y , color, param1 (width or outer radius), param2 (height or inner radius)
  attributes of the shape.

**************
* Controller *
**************

IAnimatorController
*******************
This interface has one method definition: animate()

VisualAnimatorController
*************************
This class implements IAnimatorController interface
and has a IModel, VisualView and timer object
Constructor takes in IModel, VisualView and speed parameters

Animate method starts a timer, which activates a actionlistener 
event which retrieves list of shapes from model to be drawn
for a partcular tick. After giving this list of shapes to view
to draw, value of tick is advanced by one and action listener 
event is executed again after delay (speed) specified/given 
to the timer.


TextAnimatorController
***********************
This class implements IAnimatorController
Constructor takes in IModel, TextView, speed and String output (text file name or System.out)
parameters.

If output specified is System.out then TextView's textView method is called
which would save the return string value to the appendable object

If output specified is a txt file, then the string value returned bye
TextView's textView method is written to the specified file



*********
* View *
*********

IView
******
IView Interface supports draw method which taken in list (of shapes) parameter

IViewShape
**********
IViewShape interface supports draw method which taken in graphics type object

AbstractViewShape
******************
This class implements IViewShape interface


MyOval & MyRectangle
*********************
Both classes extend AbstractViewShape and offer support for
drawing rectangle and oval objects respectively 

CanvasPanel
************
This class extends JPanel class and offers support to 
create panel of required dimension and drawing shapes

ViewFactory
************
Takes in string viewtype, canvas dimension parameters and
returns the appropriate view type (visualview or text view)

VisualView
***********
Visual View extends JFrame  and implements IView
VisualView constructor creates panel and scroll pane

Draw method takes in list of shapes, determines it type (rectangle or oval)
creates the shape object, and calls panel.drawShape method to draw the shape.
Before next list of shapes are drawn, the current shapes drawn on the panel
are cleared.

TextView
*********
TextView implements IView interface

textView method takes in speed, list of shapes and animations
and produces textual view of the animation in string format.



*********
* Model *
*********

IModel now supports 7 methods
addShape, addAction, getShapesAtFrame, createShapesAtTickTable, getShapes & getAnimations

AnimationModelImpl
******************
Implements IModel. Has static builder class with its method implementation
Implements following methods:
addShape 		This method takes in unique String identifier, String ShapeType to create a 
			IShape object (and adds to shapes hashmap).
addAction  		This method takes in unique String identifier, from and to attributes of the shape
			before and after animation.
	    		Animation creation is delegated through transformFactory object and animation
            		is added to a linkedhashmap.
getState  		This method return the state of the model (shapes and animations added) in string format
getShapesAtFrame	This method takes in an integer tick. And return list of all shapes that are active or have
			attributes during that tick
createShapesAtTickTable This method populates a hashmap (shapesAtFrame) with key being all the ticks 
			of the model and value being the list of shapes that are active/have attributes
			for that tick.
getShapes               This method returns hashmap of all shapes added to model.
getAnimations		This method returns hashmap of all animations added to model.


Transformations 
****************
Transformations is an enum class currently describing 4 different animations (SCALE, MOVE, COLORCHANGE & APPEAR);

ShapeFactory 
*************
This class has a IShape object.
This class has a createShape method which has a parameter String type
Based on what type of shape is passed, this method creates a shape object and returns
the shape created to the caller.
For example if "rectangle" is passed in the parameter, createShape method will 
create a new Rectangle shape object based on parameters passed and return this shape object
to its caller (animation model class)


IShape 
*******
This interfaces offers methods avaialble to all shape objects 
a) getX & getY 	 methods to get x & y coordinates of shape's reference location
b) getParam1 	 Param1 can represent width of rectangle, or inner radius of oval 
c) getparam2     Param2 can represent height of rectangle, or outer radius of oval
d) getColor  	 This returns color code object of the shape
e) getShapeType  This return shapes string description of shape type
f) getStartTime  Gets the appearing time of the shape
g) getEndTime    Gets the disappearing time of the shape
h) setX  	 This sets the shapes X coordinate to some integer 
i) setY		 This sets the shapes Y coordinate to some integer 
j) setWidth	 This sets the shapes width or outer radiius to some integer
k) setHeight	 This sets the shapes height or inner radius to some integer.
i) setColor      This sets the shapes color
j) setStartTime  This sets the shapes appearance time
k) setEndTime    This sets the shapes disappearance time.



AbstractShape 
*************
This abstract shape implements IShape
This class has a Color object within it.


Rectangle, Oval
****************
Both the two classes extend Abstract Shape class and construct
respective shapes based on required parameters passed (x & y coordinates, param1, param2, color object)
Both classes also have constructor to create shapes with default values.
Each of these 4 classes return string description of its shape type and string description of its
dimensions, refernece location and its color code



IAnimation
***********
This interface provides following methods available to all animation classes implementing it.
a) getTransformType  	This method returns the animation type (enum) of the animation.
b) getActionStartTime   This method returns the start-time of the animation.
c) getActionEndTime  	This method returns the end-time of the animation.
d) getToColor  		This method return the new color object of the animation after
			color change animation is performed on the shape.
e) getToWidhth  	Return the new width/outer radius set to the shape after scale animation 
			is performed on the shape.
f) getToHeight  	Return the new height/inner radius set to the shape after scale animation
			is performed on the shape
g) getToX 		Return the new X coordinate of the shape after move animation is
	    		performed on the shape
h) getToY 		Returns the new Y coordinate of the shape after move animation is
	    		performed  on the shape.
i) toString  		Returns string description of the animation.
j) getFromColor 	Returns current Color object of the shape before animation is performed on it
k) getFromX		Returns the current X of the shape before animation is performed.
i) getFromY		Returns the current Y of the shape before animation is performed.
j) getFromWidth		Return the current width/outer radius set to the shape before animation 
			is performed on the shape.
k) getFromHeight	Return the current height/inner radius set to the shape before scale animation
			is performed on the shape.

TransformationFactory
*********************
This class has a IAnimation object.
This class constructs an animation object based on from and to attributes of the shape
passed in the parameters
Also adds the new animation to an hashmap


Animation
**********
This abstract class implements IAnimation interface


Scale & Color Change & Move & Appear
*************************************
All these 4 classes extends abstract class animation.






