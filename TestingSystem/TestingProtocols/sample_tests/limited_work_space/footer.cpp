int main() {
    bool passed = true;
    for (int test = 1; test <= 3; ++test) {
        passed &= (f(test) == 2 * test);
        if (!passed) break;
    }
    std::cout << passed;
}