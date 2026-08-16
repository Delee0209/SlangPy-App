[shader("compute")]
[numthreads(32, 32, 1)]
void main(uint3 thread_id: SV_DispatchThreadID, uniform float time, RWTexture2D<float4> frame)
{
    // get current dimension and pixel location
    uint2 pixel = thread_id.xy;
    uint2 dimension;
    frame.GetDimensions(dimension.x, dimension.y);
    if (any(pixel >= dimension))
    {
        return;
    }

    // shadertoy default shader
    float2 uv = (float2)pixel / (float2)dimension;
    float3 color = 0.5f + 0.5f * cos(time + uv.xyx + float3(0.f, 2.f, 4.f));

    frame[pixel] = float4(color, 1.f);
}