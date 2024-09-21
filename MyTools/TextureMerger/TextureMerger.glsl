#version 440

layout (local_size_x = 16, local_size_y = 16) in;
layout(binding=0) uniform sampler2D tex0;
layout(binding=1) uniform sampler2D tex1;
layout(binding=2) uniform sampler2D tex2;
layout(binding=3, rgba32f) uniform image2D dstTex;
layout(binding=4, rgba32f) uniform image2D dstTex1;
layout(location = 10) uniform float Radius = 3.5;

void main()
{
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = imageSize(dstTex);
    vec2 uv = vec2((texelPos.x*1.0 + 0.5) / size.x, (texelPos.y*1.0 + 0.5) / size.y);

    vec4 col0 = texture(tex0, uv*2);
    vec4 col1 = texture(tex1, uv);
    vec4 col2 = texture(tex2, uv*1);


    vec4 out_color = vec4(col1.rg, dot(col0.rgb, vec3(0.26, 0.6, 0.14)), col2.r * col2.r);
    //out_color = vec4(1, 0, 0, 1);
    imageStore(dstTex, texelPos, out_color);

}