#include <iostream>
#include <fstream>

int main(int argc, char* argv[]) {
    std::ifstream inp;
    inp.open(argv[1]);
    int in;
    inp >> in;

    std::ifstream outp;
    outp.open(argv[2]);
    int out;
    outp >> out;
    std::cout << (2 * in == out);
}