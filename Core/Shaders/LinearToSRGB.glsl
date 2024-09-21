#version 440

layout (local_size_x = 16, local_size_y = 16) in;
//layout(location=0) uniform sampler2D srcTex;
layout(binding=0, rgba32f) uniform image2D srcTex;
layout(binding=1, rgba32f) uniform image2D dstTex;
layout(binding=2, rgba32f) uniform image2D srcTex1;


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

float LinearToSrgbBranchingChannel(float lin)
{
	if(lin < 0.00313067) return lin * 12.92;
	return pow(lin, (1.0/2.4)) * 1.055 - 0.055;
}

vec3 LinearToSrgbBranching(vec3 lin)
{
	return vec3(
		LinearToSrgbBranchingChannel(lin.r),
		LinearToSrgbBranchingChannel(lin.g),
		LinearToSrgbBranchingChannel(lin.b));
}

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
    ivec2 size = imageSize(dstTex);
    vec4 srcColor = imageLoad(srcTex, texelPos);
    //vec4 srcColor1 = imageLoad(srcTex1, texelPos);
    //srcColor = pow(srcColor, vec4(1/2.2, 1/2.2, 1/2.2, 1));
    //vec4 out_color = vec4(LinearToSrgbBranching(srcColor.rgb), srcColor.a);
	vec3 linear_color = sRGBToLinear(srcColor.rgb);
    vec4 out_color = vec4(1-linear_color.g, 0.5, linear_color.r, linear_color.b);
    imageStore(dstTex, texelPos, out_color);
}