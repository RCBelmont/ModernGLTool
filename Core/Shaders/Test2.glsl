#version 440

layout (local_size_x = 16, local_size_y = 16) in;
layout(location=0) uniform sampler2D texture0;
layout(binding=0, rgba32f) uniform image2D destTex;


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
    int idx = int(texelPos.y/64);
     float x = uv.x*uv.x;
    if (uv.x <= 0.3){
        x = mix(0,1, uv.x / 0.3)/20.0;
    } else {
        x = mix(1, 20, (uv.x-0.3)/0.7)/20.0;
    }
    float a = x * 20;
    vec4 color1 = vec4(a, a, a, 1);
    if (idx == 0){
        color1 = vec4(a, 0, 0, 1);
    } else if (idx==1){
        color1 = vec4(0, a, 0, 1);
    } else if (idx==2){
        color1 = vec4(0, 0, a, 1);
    }

    //    vec4 color1 = texture(texture0, uv);
    //    int rp = texelPos.x%16;
    //    int gp = texelPos.y;
    //    float bp = (texelPos.x/16);
    //    int bp1 = int(floor(bp));
    //    int bp2 = int(ceil(bp));
    //    float time = fract(bp);
    //    uv = vec2((bp1*64 + rp*2)/1024.0 + 0.5/1024.0,1-gp/16.0 - 0.5/32.0);
    //    color1 = texture(texture0, uv);


    vec4 out_color = color1;
    imageStore(destTex, texelPos, out_color);
}