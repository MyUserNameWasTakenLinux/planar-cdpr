#include <opencv2/opencv.hpp> //Include file for every supported OpenCV function
#include "controller.h"
#include <cmath>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>


struct Server {
    Server(int port) {
        server_sock = socket(AF_INET, SOCK_STREAM, 0);
        if(server_sock == -1) {
            std::cerr << "Failed to create a socket\n";
        }

        sockaddr_in server_addr {};
        server_addr.sin_family = AF_INET;
        server_addr.sin_addr.s_addr = INADDR_ANY;
        server_addr.sin_port = htons(port);

        if(bind(server_sock, (struct sockaddr *) &server_addr, sizeof(server_addr)) == -1) {
            std::cerr << "Failed to bind socket";
        }

        if (listen(server_sock, 3) == -1) {
            std::cerr << "Listen failed\n";
        }
        std::cout << "Listening on port " << port << "...\n";


        sockaddr_in client_addr {};
        socklen_t client_addr_len = sizeof(client_addr);
        int client_sock = accept(server_sock, (struct sockaddr *) &client_addr, &client_addr_len);
        if (client_sock == -1) {
            std::cerr << "Failed to accept connection\n";
        }
        std::cout << "Client connected\n";
        
    }

    ~Server() {
        close(client_sock);
        close(server_sock);
    }

    void send_angles(float a1, float a2, float a3, float a4) {
        float data[4] = {a1, a2, a3, a4};
        char buffer[sizeof(data)];

        std::memcpy(buffer, data, sizeof(buffer));

        send(client_sock, buffer, sizeof(buffer), 0);

        char read_buffer[16];
        auto valread = read(client_sock, read_buffer, 16);
        for(int i = 0; valread <= 0 && i < 50; ++i) {
            valread = read(client_sock, read_buffer, 16);
        }

    }

    int server_sock;
    int client_sock;

};


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
    std::cout << l1 << " " << l2 << " " << l3 << " " << l4 << "\n";
    auto [d1, d2, d3, d4] = C.move_and_get_difference({-2, -2});
    std::cout << d1 << " " << d2 << " " << d3 << " " << d4 << "\n";
    auto [a1, a2, a3, a4] = C.get_angles_from_difference(d1, d2, d3, d4);
    std::cout << a1 << " " << a2 << " " << a3 << " " << a4 << "\n";

    Server s(9999);
    s.send_angles(a1, a2, a3, a4);
    sleep(10);

    return 0;
}