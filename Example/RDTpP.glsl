#version 430 core

layout (local_size_x = 16, local_size_y = 16) in;
layout(location=0) uniform samplerCube texture0;
layout(binding=1, rgba32f) uniform image2D destTex;
#define PI 3.1415926

vec3 sRGBToLinear(vec3 Color )
{
	Color = max(vec3(6.10352e-5), Color); // minimum positive non-denormal (fixes black problem on DX11 AMD and NV)
	vec3 ret = vec3(0.0);
	ret.r = Color.r <= 0.04045 ? Color.r / 12.92 : pow((Color.r + 0.055) / 1.055, 2.4);
	ret.g = Color.g <= 0.04045 ? Color.g / 12.92 : pow((Color.g + 0.055) / 1.055, 2.4);
	ret.b = Color.b <= 0.04045 ? Color.b / 12.92 : pow((Color.b + 0.055) / 1.055, 2.4);
	return ret;
}

void main()
{
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = imageSize(destTex);
    //vec4 color = imageLoad(destTex, texelPos);
    //imageStore(destTex, texelPos, color);
    //float gray = dot(color.rgb, vec3(0.3, 0.59, 0.11));
    vec2 uv = vec2(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y);
    float phi = uv.x * 2 * PI;
    float theta = uv.y * PI;
    vec3 cube_uv = vec3(sin(theta)*cos(phi), cos(theta), sin(theta)*sin(phi));
    vec4 c = texture(texture0, (cube_uv));
    imageStore(destTex, texelPos, vec4(sRGBToLinear(c.rgb), 1));
    //imageStore(destTex, texelPos, vec4(1,0,0,1));
    //imageStore(destTex, texelPos, vec4(size, 0, 1));
    //imageStore(destTex, texelPos, vec4(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y, 0, 1));
}