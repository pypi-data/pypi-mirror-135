
#define READ_AND_MAP(i) (make_float2(x[i], x[i]))
#define REDUCE(a, b) (make_float2(min(a.x, b.x), max(a.y, b.y)))



__global__ void max_min_reduction_stage1( global const float *data,
                                      global float2 *out,
                                      int size,
                                      local  float2 *l_data)// local storage 2 float per thread
{
    int group_size =  get_local_size(0);
    int lid = get_local_id(0);
    float2 acc;
    int big_block = group_size * get_num_groups(0);
    int i =  lid + group_size * get_group_id(0);

    if (lid<size)
        acc = read_and_map(lid, data);
    else
        acc = read_and_map(0, data);

    // Linear pre-reduction stage 0

    while (i<size){
      acc = REDUCE(acc, read_and_map(i, data));
      i += big_block;
    }

    // parallel reduction stage 1

    l_data[lid] = acc;
    barrier(CLK_LOCAL_MEM_FENCE);
    for (int block=group_size/2; block>1; block/=2)
        {
            if ((lid < block) && ((lid + block)<group_size)){
                l_data[lid] = REDUCE(l_data[lid], l_data[lid + block]);
            }
            barrier(CLK_LOCAL_MEM_FENCE);
        }
    if (lid == 0)
    {
        if (group_size > 1)
        {
            acc = REDUCE(l_data[0], l_data[1]);
        }
        else
        {
            acc = l_data[0];
        }
        out[get_group_id(0)] = acc;
    }
}


__global__ void max_min_reduction_stage2(
        global const float2 *data2,
        global float2 *maxmin,
        local  float2 *l_data)// local storage 2 float per thread
{
    int lid = get_local_id(0);
    int group_size =  get_local_size(0);
    float2 acc = (float2)(-1.0f, -1.0f);
    if (lid<=group_size)
    {
        l_data[lid] = data2[lid];
    }
    else
    {
        l_data[lid] = acc;
    }

    // parallel reduction stage 2


    barrier(CLK_LOCAL_MEM_FENCE);
    for (int block=group_size/2; block>1; block/=2)
    {
        if ((lid < block) && ((lid + block)<group_size))
        {
            l_data[lid] = REDUCE(l_data[lid], l_data[lid + block]);
        }
        barrier(CLK_LOCAL_MEM_FENCE);

    }

    if (lid == 0 )
    {
        if ( group_size > 1)
        {
            acc = REDUCE(l_data[0], l_data[1]);
        }
        else
        {
            acc = l_data[0];
        }
        maxmin[0] = acc;
    }
}
