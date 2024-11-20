#include "controller.h"
#include <cmath>
#include <iostream>

Controller::Controller(vec2D start_pos, float w, float h, vec2D A1, vec2D A2, vec2D A3, vec2D A4, float theta,
bool o1, bool o2, bool o3, bool o4, float pr) {
    current_pos = start_pos;
    width = w;
    height = h;
    this->A1 = A1;
    this->A2 = A2;
    this->A3 = A3;
    this->A4 = A4;
    this->theta = theta;
    this->o1 = o1;
    this->o2 = o2;
    this->o3 = o3;
    this->o4 = o4;
    this->pr = pr;
}   

Controller::~Controller() {

}

float Controller::get_L1() {
    auto x = A1.first - (current_pos.first - (width / 2)) * cos(theta) - (current_pos.second - (height / 2)) * sin(theta);
    x = pow(x, 2);
    auto y = A1.second - (current_pos.first - (width / 2)) * sin(theta) - (current_pos.second - (height / 2)) * cos(theta);
    y = pow(y, 2);

    return sqrt(x + y);
}

float Controller::get_L2() {
    auto x = A2.first - (current_pos.first + (width / 2)) * cos(theta) - (current_pos.second - (height / 2)) * sin(theta);
    x = pow(x, 2);
    auto y = A2.second - (current_pos.first + (width / 2)) * sin(theta) - (current_pos.second - (height / 2)) * cos(theta);
    y = pow(y, 2);

    return sqrt(x + y);
}

float Controller::get_L3() {
    auto x = A3.first - (current_pos.first + (width / 2)) * cos(theta) - (current_pos.second + (height / 2)) * sin(theta);
    x = pow(x, 2);
    auto y = A3.second - (current_pos.first + (width / 2)) * sin(theta) - (current_pos.second + (height / 2)) * cos(theta);
    y = pow(y, 2);

    return sqrt(x + y);
}

float Controller::get_L4() {
    auto x = A4.first - (current_pos.first - (width / 2)) * cos(theta) - (current_pos.second + (height / 2)) * sin(theta);
    x = pow(x, 2);
    auto y = A4.second - (current_pos.first - (width / 2)) * sin(theta) - (current_pos.second + (height / 2)) * cos(theta);
    y = pow(y, 2);

    return sqrt(x + y);
}

std::tuple<float, float, float, float> Controller::move_and_get_lengths(vec2D displacement) {
    current_pos.first += displacement.first;
    current_pos.second += displacement.second;
    return std::make_tuple(get_L1(), get_L2(), get_L3(), get_L4());
}

std::tuple<float, float, float, float> Controller::move_and_get_difference(vec2D displacement) {
    auto [l1, l2, l3, l4] = std::make_tuple(get_L1(), get_L2(), get_L3(), get_L4());
    auto [n1, n2, n3, n4] = move_and_get_lengths(displacement);
    return std::make_tuple(n1 - l1, n2 - l2, n3 - l3, n4 - l4);
}

std::tuple<float, float, float, float> Controller::get_angles_from_difference(float l1, float l2, float l3, float l4) {
    float c = o1 ? 1.0 : -1.0; // Coefficient of orientation
    float a1 = c * (l1 / pr);
    c = o2 ? 1.0 : -1.0;
    float a2 = c * (l2 / pr);
    c = o3 ? 1.0 : -1.0;
    float a3 = c * (l3 / pr);
    c = o4 ? 1.0 : -1.0;
    float a4 = c * (l4 / pr);
    
    return std::make_tuple(a1, a2, a3, a4);
}
