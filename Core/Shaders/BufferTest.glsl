#version 440
layout (local_size_x = 9, local_size_y = 1) in;
struct MyData {
    vec4 position;
    vec4 normal;
};

layout(std430, binding = 0) buffer MyBuffer {
    MyData data[];
} myBuffer;




void main()
{
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    myBuffer.data[texelPos.x].position = vec4(1, 2, 3, 5);
    myBuffer.data[texelPos.x].normal = vec4(7, 8, 9, 5);
}