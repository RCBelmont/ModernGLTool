#version 440

layout (local_size_x = 16, local_size_y = 16) in;
layout(location=0) uniform sampler2D srcTex;
layout(location=1) uniform sampler2D maskTex;
layout(binding=1, rgba32f) uniform image2D dstTex;
uniform int Radius;

void main()
{
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = imageSize(dstTex);
    vec2 uv = vec2((texelPos.x*1.0 + 0.5) / size.x, (texelPos.y*1.0 + 0.5) / size.y);

    vec4 srcColor = texture(srcTex, uv);
    vec4 maskColor = texture(maskTex, uv);

    float out_a = (1-maskColor.a);
    vec4 out_color = vec4(srcColor.rgb, out_a);
    //out_color = vec4(1, 0, 0, 1);
    imageStore(dstTex, texelPos, out_color);
}