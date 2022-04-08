package cs5004.animator;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.HashMap;

import javax.swing.JOptionPane;

import cs5004.animator.controller.IAnimatorController;
import cs5004.animator.controller.TextAnimatorController;
import cs5004.animator.controller.VisualAnimatorController;
import cs5004.animator.model.AnimationModelImpl;
import cs5004.animator.model.IModel;
import cs5004.animator.util.AnimationBuilder;
import cs5004.animator.util.AnimationReader;
import cs5004.animator.view.IView;
import cs5004.animator.view.TextView;
import cs5004.animator.view.ViewFactory;
import cs5004.animator.view.VisualView;

/**
 * This class is the main class.
 */
public final class EasyAnimator {

  /**
   * This method acts as a helper method to create frame for Visual view.
   *
   * @return New VisualView frame.
   */
  public static VisualView createFrame() {
    return new VisualView(AnimationModelImpl.SCREEN.getX(),
            AnimationModelImpl.SCREEN.getY(), AnimationModelImpl.SCREEN.getWidth(),
            AnimationModelImpl.SCREEN.getHeight());
  }

  /**
   * This is the main method.
   *
   * @param args Command Line arguments.
   */
  public static void main(String[] args) {

    String inputFile = null;
    String typeOfView = null;
    int speed = 1;
    String output = "System.out";

    HashMap<String, String> cmdArgs = new HashMap<>();

    //Parse through command line arguments and save the arguments in an hashmap
    try {
      for (int i = 0; i < args.length - 1; i++) {
        if (args[i].equalsIgnoreCase("-in")) {
          inputFile = args[i + 1];
          cmdArgs.put(args[i], args[i + 1]);
        } else if (args[i].equalsIgnoreCase("-view")) {
          typeOfView = args[i + 1];
          cmdArgs.put(args[i], args[i + 1]);
        } else if (args[i].equalsIgnoreCase("-speed")) {
          speed = Integer.parseInt(args[i + 1]);
          cmdArgs.put(args[i], args[i + 1]);
        } else if (args[i].equalsIgnoreCase("-out")) {
          output = args[i + 1];
          cmdArgs.put(args[i], args[i + 1]);
        }
      }
    } catch (NumberFormatException e) {
      throw new IllegalStateException("speed provided is not an integer");
    }

    AnimationBuilder<IModel> builder = new AnimationModelImpl.Builder();
    Readable readable = null;

    try {
      readable = new FileReader(inputFile);
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    }

    //Build the model from input file provided by user
    IModel model = AnimationReader.parseFile(readable, builder);


    if (cmdArgs.containsKey("-in") && cmdArgs.containsKey("-view")) {

      if (cmdArgs.keySet().size() == 3 && !(cmdArgs.containsKey("-out") ||
              cmdArgs.containsKey("-speed"))
              && typeOfView.equalsIgnoreCase("visual")) {
        VisualView frame = createFrame();
        JOptionPane.showMessageDialog(frame,
                "Invalid arguments",
                "Error",
                JOptionPane.ERROR_MESSAGE);

      } else if (cmdArgs.keySet().size() == 4 && !cmdArgs.containsKey("-out") &&
              !cmdArgs.containsKey("-speed")
              && typeOfView.equalsIgnoreCase("visual")) {
        VisualView frame = createFrame();
        JOptionPane.showMessageDialog(frame,
                "Invalid arguments",
                "Error",
                JOptionPane.ERROR_MESSAGE);

      } else if (cmdArgs.containsKey("-speed") && Integer.parseInt(cmdArgs.get("-speed")) <= 0) {
        VisualView frame = createFrame();
        JOptionPane.showMessageDialog(frame,
                "Invalid Speed Value",
                "Error",
                JOptionPane.ERROR_MESSAGE);
      } else {

        IView view = ViewFactory.makeView(typeOfView, AnimationModelImpl.SCREEN.getX(),
                AnimationModelImpl.SCREEN.getY(), AnimationModelImpl.SCREEN.getWidth(),
                AnimationModelImpl.SCREEN.getHeight());

        //Run VisualView or TextualView as specified by user
        if (view instanceof VisualView) {
          IAnimatorController controller = new VisualAnimatorController(model, (VisualView) view,
                  speed);
          controller.animate();
        } else if (view instanceof TextView) {
          IAnimatorController controllerText = new TextAnimatorController(model,
                  (TextView) view, speed, output, System.out);
          controllerText.animate();
        }
      }
    } else {
      VisualView frame = createFrame();
      JOptionPane.showMessageDialog(frame,
              "Invalid arguments",
              "Error",
              JOptionPane.ERROR_MESSAGE);
    }
  }
}



