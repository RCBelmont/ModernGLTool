#version 440

layout (local_size_x = 16, local_size_y = 16) in;
struct Vector4 {
    vec4 color;
};

layout(std430, binding=0) buffer ColorBuffer {
    Vector4 colorData[];
} colorBuffer;

layout(binding=0, rgba32f) uniform image2D dstTex;


//vec3 GetSHDiffuse(vec3 Normal)
//{
//    vec4 NormalVector = vec4(Normal, 1.0f);
//
//    vec3 Intermediate0, Intermediate1, Intermediate2;
//    Intermediate0.x = dot(shBuffer.shData[0].sh, NormalVector);
//    Intermediate0.y = dot(shBuffer.shData[1].sh, NormalVector);
//    Intermediate0.z = dot(shBuffer.shData[2].sh, NormalVector);
//
//    vec4 vB = NormalVector.xyzz * NormalVector.yzzx;
//    Intermediate1.x = dot(shBuffer.shData[3].sh, vB);
//    Intermediate1.y = dot(shBuffer.shData[4].sh, vB);
//    Intermediate1.z = dot(shBuffer.shData[5].sh, vB);
//
//    float vC = NormalVector.x * NormalVector.x - NormalVector.y * NormalVector.y;
//    Intermediate2 = shBuffer.shData[6].sh.xyz * vC;
//
//    // max to not get negative colors
//    return max(vec3(0, 0, 0), Intermediate0 + Intermediate1 + Intermediate2);
//}


void main()
{
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    int x = int(texelPos.x*1.0 / 64);
    int y = int(texelPos.y*1.0 / 64);
    vec3 out_color = colorBuffer.colorData[x + y*6].color.rgb;
    ivec2 size = imageSize(dstTex);
    vec2 uv = vec2(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y);
    imageStore(dstTex, texelPos, vec4(out_color, 1));
}