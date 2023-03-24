void filter_green(unsigned char*** rgb_matrix, int m, int n) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            float h, s, v;
            rgb_to_hsv(rgb_matrix[i][j][0], rgb_matrix[i][j][1], rgb_matrix[i][j][2], &h, &s, &v);
            if (h >= 60 && h <= 180) {
                // Keep the color as is (it's green)
            } else {
                // Set the color to black (it's not green)
                rgb_matrix[i][j][0] = 0;
                rgb_matrix[i][j][1] = 0;
                rgb_matrix[i][j][2] = 0;
            }
        }
    }
}