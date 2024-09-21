#version 440

layout (local_size_x = 16, local_size_y = 16) in;
layout(location=0) uniform sampler2D srcTex;
//layout(binding=0, rgba32f) uniform image2D srcTex;
layout(binding=1, rgba32f) uniform image2D dstTex;


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
    vec2 uv = vec2((texelPos.x*1.0 + 0.5) / size.x, (texelPos.y*1.0 + 0.5) / size.y);
	//uv = 1-uv;
    float angle = atan(uv.y, uv.x)/3.1415926535897932384626433832795;
    float ll = length(uv);

    vec4 srcColor = texture(srcTex, uv);
	//vec3 linear_color = sRGBToLinear(srcColor.rgb);
    vec4 out_color = srcColor;
//	if (length > 1){
//		out_color = vec4(0,0,0,0);
//
//	}
//	out_color = vec4(length);
//    out_color.a = 1;

	//float a = length((uv - vec2(0.5, 0.5)) * vec2(2.0, 2.0));
	float a = length((uv - vec2(0.5, 0.5)));
	vec2 uv1 = (uv - vec2(0.5, 0.5))* 1 + vec2(0.5, 0.5);
	a = max(1-smoothstep(0.48, 0.49, a), 0.0);
	srcColor = texture(srcTex, uv1);
	
    imageStore(dstTex, texelPos, vec4(srcColor.rgb, a));
}