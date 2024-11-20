#include <opencv2/opencv.hpp> //Include file for every supported OpenCV function
#include "controller.h"
#include <cmath>

int main( int argc, char** argv ) {
    vec2D A1 = {0.0, 0.0};
    vec2D A2 = {50.0, 0.0};
    vec2D A3 = {50.0, 50.0};
    vec2D A4 = {0.0, 50.0};

    auto width = 4.0f;
    auto height = 3.0f;
    auto theta = 0.0f;
    bool o1 = true;
    bool o2 = true;
    bool o3 = true;
    bool o4 = true;
    auto pulley_radius = 2.0f;

    Controller C({25.0, 25.0}, width, height, A1, A2, A3, A4, theta, o1, o2, o3, o4, pulley_radius);
    std::cout << "L1: " << C.get_L1() << " L2: " << C.get_L2() << " L3: " << C.get_L3() << " L4: " << C.get_L4() << "\n";
    auto [l1, l2, l3, l4] = C.move_and_get_lengths({2, 2});
    std::cout << l1 << " " << l2 << " " << " " << l3 << " " << l4 << "\n";
    auto [d1, d2, d3, d4] = C.move_and_get_difference({-2, -2});
    std::cout << d1 << " " << d2 << " " << " " << d3 << " " << d4 << "\n";
    return 0;
}