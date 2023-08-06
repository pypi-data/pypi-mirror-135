texture<float, 2, cudaReadModeElementType> texProj;
//~ cudaChannelFormatDesc floatTex = cudaCreateChannelDesc<float>();

__global__ void backproj(
    int num_proj,
    int num_bins,
    float axis_position,
    float *d_SLICE,
    float gpu_offset_x,
    float gpu_offset_y,
    float * d_cos_s,
    float * d_sin_s,
    float *  d_axis_s)
{
    const int tidx = threadIdx.x;
    const int bidx = blockIdx.x;
    const int tidy = threadIdx.y;
    const int bidy = blockIdx.y;

    __shared__  float   shared[768];
    float  * sh_sin  = shared;
    float  * sh_cos  = shared+256;
    float  * sh_axis = sh_cos+256;

    float pcos, psin;
    float h0, h1, h2, h3;

    const float apos_off_x = gpu_offset_x - axis_position ;
    const float apos_off_y = gpu_offset_y - axis_position ;
    float acorr05;
    float res0 = 0, res1 = 0, res2 = 0, res3 = 0;
    const float bx00 = (32 * bidx + 2 * tidx + apos_off_x);
    const float by00 = (32 * bidy + 2 * tidy + apos_off_y);

    int read=0;
    for (int proj=0; proj<num_proj; proj++) {
        if(proj>=read) {
            __syncthreads();
            int ip = tidy*16+tidx;
            if( read+ip < num_proj) {
                sh_cos [ip] = d_cos_s[read+ip];
                sh_sin [ip] = d_sin_s[read+ip];
                sh_axis[ip] = d_axis_s[read+ip];
            }
            read = read + 256; // 256=16*16 block size
            __syncthreads();
        }
        pcos = sh_cos[256 - read + proj] ;
        psin = sh_sin[256 - read + proj] ;
        acorr05 = sh_axis[256 - read + proj];

        h0 =  acorr05 + bx00*pcos - by00*psin;
        h1 =  acorr05 + bx00*pcos - (by00+1)*psin;
        h2 =  acorr05 + (bx00+1)*pcos - by00*psin;
        h3 =  acorr05 + (bx00+1)*pcos - (by00+1)*psin;

        if(h0 >= 0 && h0 < num_bins) res0 += tex2D(texProj, h0 + 0.5f, proj + 0.5f);
        if(h1>=0 && h1<num_bins) res1 += tex2D(texProj, h1 +0.5f, proj + 0.5f);
        if(h2>=0 && h2<num_bins) res2 += tex2D(texProj, h2 +0.5f, proj + 0.5f);
        if(h3>=0 && h3<num_bins) res3 += tex2D(texProj, h3 +0.5f, proj + 0.5f);
    }
    d_SLICE[32*gridDim.x * (bidy*32+tidy*2+0) + bidx*32 + tidx*2 + 0] = res0;
    d_SLICE[32*gridDim.x * (bidy*32+tidy*2+1) + bidx*32 + tidx*2 + 0] = res1;
    d_SLICE[32*gridDim.x * (bidy*32+tidy*2+0) + bidx*32 + tidx*2 + 1] = res2;
    d_SLICE[32*gridDim.x * (bidy*32+tidy*2+1) + bidx*32 + tidx*2 + 1] = res3;
}



