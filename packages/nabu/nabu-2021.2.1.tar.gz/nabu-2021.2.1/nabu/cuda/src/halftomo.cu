/*
    Perform a "half tomography" sinogram conversion.
    A 360 degrees sinogram is converted to a 180 degrees sinogram with a
    field of view extended (at most) twice".
    *
    Parameters:
    * sinogram: the 360 degrees sinogram, shape (n_angles, n_x)
    * output: the 160 degrees sinogram, shape (n_angles/2, rotation_axis_position * 2)
    * weights: an array of weight, size n_x - rotation_axis_position
*/
__global__ void halftomo_kernel(
    float* sinogram,
    float* output,
    float* weights,
    int n_angles,
    int n_x,
    int rotation_axis_position
) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;

    int n_a2 = (n_angles + 1) / 2;
    int d = n_x - rotation_axis_position;
    int n_x2  = 2 * rotation_axis_position;
    int r = rotation_axis_position;

    if ((x >= n_x2) || (y >= n_a2)) return;

    // output[:, :r - d] = sino[:n_a2, :r - d]
    if (x < r - d) {
        output[y * n_x2 + x] = sinogram[y * n_x + x];
    }

    // output[:, r-d:r+d] = (1 - weights) * sino[:n_a2, r-d:]
    else if (x < r+d) {
        float w = weights[x - (r - d)];
        output[y * n_x2 + x] = (1.0f - w) * sinogram[y*n_x + x] \
                                   + w * sinogram[(n_a2 + y)*n_x + (n_x2 - 1 - x)];
    }

    // output[:, nx:] = sino[n_a2:, ::-1][:, 2 * d :] = sino[n_a2:, -2*d-1:-n_x-1:-1]
    else {
        output[y * n_x2 + x] = sinogram[(n_a2 + y)*n_x + (n_x2 - 1 - x)];
    }

}
