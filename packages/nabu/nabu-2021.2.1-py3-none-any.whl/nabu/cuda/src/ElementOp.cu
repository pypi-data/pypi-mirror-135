#include <pycuda-complex.hpp>

typedef pycuda::complex<float> complex;

// arr2D *= arr1D (line by line, i.e along fast dim)
__global__ void inplace_complex_mul_2Dby1D(complex* arr2D, complex* arr1D, int width, int height) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= width) || (y >= height)) return;
    // This does not seem to work
    // Use cuCmulf of cuComplex.h ?
    //~ arr2D[y*width + x] *= arr1D[x];
    int i = y*width + x;
    complex a = arr2D[i];
    complex b = arr1D[x];
    arr2D[i]._M_re = a._M_re * b._M_re - a._M_im * b._M_im;
    arr2D[i]._M_im = a._M_im * b._M_re + a._M_re * b._M_im;
}


// arr3D *= arr1D (along fast dim)
__global__ void inplace_complex_mul_3Dby1D(complex* arr3D, complex* arr1D, int width, int height, int depth) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    int z = blockDim.z * blockIdx.z + threadIdx.z;
    if ((x >= width) || (y >= height) || (z >= depth)) return;
    // This does not seem to work
    // Use cuCmulf of cuComplex.h ?
    //~ arr3D[(z*height + y)*width + x] *= arr1D[x];
    int i = (z*height + y)*width + x;
    complex a = arr3D[i];
    complex b = arr1D[x];
    arr3D[i]._M_re = a._M_re * b._M_re - a._M_im * b._M_im;
    arr3D[i]._M_im = a._M_im * b._M_re + a._M_re * b._M_im;
}



// arr2D *= arr2D
__global__ void inplace_complex_mul_2Dby2D(complex* arr2D_out, complex* arr2D_other, int width, int height) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= width) || (y >= height)) return;
    int i = y*width + x;
    complex a = arr2D_out[i];
    complex b = arr2D_other[i];
    arr2D_out[i]._M_re = a._M_re * b._M_re - a._M_im * b._M_im;
    arr2D_out[i]._M_im = a._M_im * b._M_re + a._M_re * b._M_im;
}


// arr2D *= arr2D
__global__ void inplace_complexreal_mul_2Dby2D(complex* arr2D_out, float* arr2D_other, int width, int height) {
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= width) || (y >= height)) return;
    int i = y*width + x;
    complex a = arr2D_out[i];
    float b = arr2D_other[i];
    arr2D_out[i]._M_re *= b;
    arr2D_out[i]._M_im *= b;
}


/*
  Kernel used for CTF phase retrieval

    img_f = img_f * filter_num
    img_f[0, 0] -= mean_scale_factor * filter_num[0,0]
    img_f = img_f * filter_denom

    where mean_scale_factor = Nx*Ny
*/
__global__ void CTF_kernel(
    complex* image,
    float* filter_num,
    float* filter_denom,
    float mean_scale_factor,
    int Nx,
    int Ny
) {
    uint x = blockDim.x * blockIdx.x + threadIdx.x;
    uint y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= Nx) || (y >= Ny)) return;
    uint idx = y*Nx + x;

    image[idx] *= filter_num[idx];
    if (idx == 0) image[idx] -= mean_scale_factor;
    image[idx] *= filter_denom[idx];
}



#ifndef DO_CLIP_MIN
    #define DO_CLIP_MIN 0
#endif

#ifndef DO_CLIP_MAX
    #define DO_CLIP_MAX 0
#endif

// arr = -log(arr)
__global__ void nlog(float* array, int Nx, int Ny, int Nz, float clip_min, float clip_max) {
    uint x = blockDim.x * blockIdx.x + threadIdx.x;
    uint y = blockDim.y * blockIdx.y + threadIdx.y;
    uint z = blockDim.z * blockIdx.z + threadIdx.z;
    if ((x >= Nx) || (y >= Ny) || (z >= Nz)) return;
    uint pos = (z*Ny + y)*Nx + x;
    float val = array[pos];
    #if DO_CLIP_MIN
        val = fmaxf(val, clip_min);
    #endif
    #if DO_CLIP_MAX
        val = fminf(val, clip_max);
    #endif
    array[pos] = -logf(val);
}



// Reverse elements of a 2D array along "x", i.e:
// arr = arr[:, ::-1]
// launched with grid (Nx/2, Ny)
__global__ void reverse2D_x(float* array, int Nx, int Ny) {
    uint x = blockDim.x * blockIdx.x + threadIdx.x;
    uint y = blockDim.y * blockIdx.y + threadIdx.y;
    if ((x >= Nx/2) || (y >= Ny)) return;
    uint pos = y*Nx + x;
    uint pos2 = y*Nx + (Nx - 1 - x);
    float tmp = array[pos];
    array[pos] = array[pos2];
    array[pos2] = tmp;
}

