#include <random>
#include <iostream>

int main() {
    int x = rand() % 1024;
    std::cout << x;
}