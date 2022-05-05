int main() {
    int* leak = new int[1'000'000'000];
    for (int i = 0; i < 1'000'000'000; ++i) {
	leak[i] = i;
    }
}
