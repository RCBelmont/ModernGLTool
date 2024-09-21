#version 440
layout (local_size_x = 16, local_size_y = 16) in;
layout(binding=0, rgba32f) uniform image2D srcTex;
layout(binding=1, rgba32f) uniform image2D dstTex;
uniform bool LinToSRGB;

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
	vec3 ret_Color = srcColor.rgb;
	if (LinToSRGB){
		ret_Color = LinearToSrgbBranching(srcColor.rgb);
	}else {
		ret_Color = sRGBToLinear(srcColor.rgb);
	}

    vec4 out_color = vec4(ret_Color.rgb, srcColor.a);
    imageStore(dstTex, texelPos, out_color);
}