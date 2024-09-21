#version 430 core

layout (local_size_x = 16, local_size_y = 16) in;
layout(location=0) uniform sampler2D texture0;
layout(binding=1, rgba32f) uniform image2D destTex;
#define PI 3.1415926


void main()
{
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = imageSize(destTex);
    vec2 uv = vec2((texelPos.x * 1.0 + 0.5) / size.x, (texelPos.y * 1.0 + 0.5) / size.y);
    vec4 color = texture(texture0, uv);
    imageStore(destTex, texelPos, color);
}