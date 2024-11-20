#ifndef CONTROLLER_H
#define CONTROLLER_H

#include <utility>

using vec2D = std::pair<float, float>;

class Controller {
private:
vec2D current_pos; // (x,y) the position of the center of the end-effector
float width, height; // Width and height of the end-effector, from the paper a width b height
vec2D A1, A2, A3, A4; // A1 is the winch at the bottom left, anti-clockwise for the rest
float theta; // Orientation
float o1, o2, o3, o4, pr;

public:
    // Pulley orientation, true means clockwise to release, pr is pulley radius
    Controller(vec2D start_pos, float w, float h, vec2D A1, vec2D A2, vec2D A3, vec2D A4, float theta,
    bool o1, bool o2, bool o3, bool o4, float pr);
    ~Controller();

    float get_L1();
    float get_L2();
    float get_L3();
    float get_L4();

    // Move by displacement and get the length of the cables after the movement
    std::tuple<float, float, float, float> move_and_get_lengths(vec2D displacement);
    // Move by displacement and get the difference in cable lengths
    std::tuple <float, float, float, float> move_and_get_difference(vec2D displacement);
    // Get angles(radians) from the difference in cable lengths
    std::tuple<float, float, float, float> get_angles_from_difference(float l1, float l2, float l3, float l4);
};


#endif