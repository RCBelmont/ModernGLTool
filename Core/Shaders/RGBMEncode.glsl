#version 440

layout (local_size_x = 16, local_size_y = 16) in;
//layout(location=0) uniform sampler2D srcTex;
layout(binding=0, rgba32f) uniform image2D srcTex;
layout(binding=1, rgba32f) uniform image2D dstTex;



void main()
{
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = imageSize(dstTex);
    vec4 srcColor = imageLoad(srcTex, texelPos);

    float maxRange = 16.0;
    float maxComponent = max(max(srcColor.r, srcColor.g), srcColor.b);
    float M = clamp(ceil(maxComponent / maxRange), 0.00001, 1.0);
    vec3 RGB = srcColor.rgb / (M * maxRange);


    vec4 out_color = vec4(RGB, M);
    imageStore(dstTex, texelPos, out_color);
}