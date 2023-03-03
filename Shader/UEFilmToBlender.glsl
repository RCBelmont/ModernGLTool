#version 430 core

struct ToneData{
    vec3 coord;
    vec3 color;
    vec3 logColor;
};

layout (local_size_x = 256) in ;
layout(std430, binding=1) buffer balls_out
{
    ToneData data[];
} Out;




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

void main()
{
    int id = int(gl_GlobalInvocationID.x);
    int z = id % 64;
    int y = (id / 64) % 64;
    int x = id / (64 * 64);
    ivec3 coord = ivec3(x, y, z);
    ToneData data;
    data.coord = vec3(0);
    data.color = vec3(0);
    data.logColor = vec3(0);
    vec3 natureColor = vec3(coord.x / 63.0, coord.y / 63.0, coord.z / 63.0);
    data.color = natureColor;
    Out.data[id] = data;
}