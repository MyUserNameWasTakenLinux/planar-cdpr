cmake_minimum_required(VERSION 3.10)

# Project name
project(MyOpenCVProject)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)

# Add the executable
add_executable(vision_server main.cpp controller.cpp)

# Specify the include directories
include_directories(/usr/local/include/opencv4/)

# Specify the link directories
link_directories(/usr/lib/ /usr/local/lib/)

# Link OpenCV libraries
target_link_libraries(vision_server opencv_highgui opencv_core opencv_imgcodecs)
