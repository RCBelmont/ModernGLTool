#version 440

layout (local_size_x = 16, local_size_y = 16) in;
layout(location=0) uniform sampler2D texture0;
layout(location=1) uniform sampler2D texture1;
layout(location=2) uniform sampler2D texture2;
layout(binding=0, rgba32f) uniform image2D destTex;
layout(binding=1, rgba32f) uniform image2D destTex1;


// void main()
// {
//   ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
//   ivec2 size = imageSize(destTex);
//   vec4 color = imageLoad(destTex, texelPos);
//   //imageStore(destTex, texelPos, color);
//   float gray = dot(color.rgb,vec3(0.0, 0.59, 0.0));
//   vec2 uv = vec2(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y);
//   vec4 c = texture(texture0, uv);
//   imageStore(destTex, texelPos, vec4(c.rgb,1));
//   //imageStore(destTex, texelPos, vec4(size, 0, 1));
//   //imageStore(destTex, texelPos, vec4(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y, 0, 1));
// }

//  void main()
//  {
//    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
//    ivec2 size = imageSize(destTex);
//    vec2 uv = vec2(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y);
//    vec2 cood = (uv - 0.5) * 2;
//    vec4 color = texture(texture0, uv);
//    float l = length(cood) * length(cood);
//    float v = sqrt(0.8 - l*l);
//    float b_alpha = 1-color.a;
//    vec4 out_color = vec4(color.r*color.a + b_alpha, color.g*color.a + b_alpha, color.b*color.a + b_alpha, 1);
//    imageStore(destTex, texelPos, out_color);
//  }

void main()
{
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = imageSize(destTex);
    vec2 uv = vec2(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y);
    vec4 color = imageLoad(destTex1, texelPos);
    vec4 color1 = texture(texture1, uv);
    vec4 color2 = texture(texture2, uv);
    double g = color.r*0.3 + color.g*0.59+color.b*0.11;
    double the = 0.92;
    if (g>=the){
       color = vec4(the,the,the,1);
    }

    vec4 out_color = vec4(color.rgb, 1);
    imageStore(destTex, texelPos, out_color);
}