#version 440
layout (local_size_x = 16, local_size_y = 16) in;
layout(location=0) uniform sampler2D mainTex;
layout(location=1) uniform sampler2D specTex;
layout(binding=2, rgba32f) uniform image2D mainTexNew;
layout(binding=3, rgba32f) uniform image2D mixTex;
uniform bool LinToSRGB;

float LinearToSrgbBranchingChannel(float lin)
{
    if (lin < 0.00313067) return lin * 12.92;
    return pow(lin, (1.0/2.4)) * 1.055 - 0.055;
}

vec3 LinearToSrgbBranching(vec3 lin)
{

    return vec3(
    LinearToSrgbBranchingChannel(lin.r),
    LinearToSrgbBranchingChannel(lin.g),
    LinearToSrgbBranchingChannel(lin.b));
}


vec3 sRGBToLinear(vec3 Color)
{
    Color = max(vec3(6.10352e-5), Color);// minimum positive non-denormal (fixes black problem on DX11 AMD and NV)
    vec3 ret = vec3(0.0);
    ret.r = Color.r <= 0.04045 ? Color.r / 12.92 : pow((Color.r + 0.055) / 1.055, 2.4);
    ret.g = Color.g <= 0.04045 ? Color.g / 12.92 : pow((Color.g + 0.055) / 1.055, 2.4);
    ret.b = Color.b <= 0.04045 ? Color.b / 12.92 : pow((Color.b + 0.055) / 1.055, 2.4);
    return ret;
}

void main()
{
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = imageSize(mixTex);
    vec2 uv = vec2(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y);
    vec4 mianColor = texture(mainTex, uv);
    vec4 specGloss = texture(specTex, uv);

    //vec4 newMainColor = vec4(max(mianColor.rgb, specGloss.rgb), mianColor.a);


    float max_spc = max(specGloss.r, max(specGloss.g, specGloss.b));
    float meta = 0;
    meta = mix(0, 1, clamp(max_spc/0.5, 0, 1));
    vec4 mixColor = vec4(meta, 1-specGloss.a, 0, 1);
    imageStore(mixTex, texelPos, mixColor);

    //vec4 newMainColor = vec4(mix(mianColor.rgb, specGloss.rgb, mixColor.r), mianColor.a);
    vec4 newMainColor = vec4(max(mianColor.rgb, specGloss.rgb), mianColor.a);
    //vec4 newMainColor = vec4(specGloss.rgb, mianColor.a);
    imageStore(mainTexNew, texelPos, newMainColor);

}