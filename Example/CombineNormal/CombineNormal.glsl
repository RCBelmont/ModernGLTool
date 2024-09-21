#version 440
layout (local_size_x = 16, local_size_y = 16) in;
layout(location=0) uniform sampler2D normal1;
layout(location=1) uniform sampler2D normal2;
layout(binding=2, rgba32f) uniform image2D OutImg;


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
    ivec2 size = imageSize(OutImg);
    vec2 uv = vec2(texelPos.x*1.0 / size.x, texelPos.y*1.0 / size.y);
    vec4 baseNormalCol = texture(normal1, uv);
    baseNormalCol.g = baseNormalCol.g;
    vec4 topNormalCol = texture(normal2, uv*20.0);
    topNormalCol.g = 1-topNormalCol.g;

    vec3 baseNormal =vec3(baseNormalCol.rg * 2 - 1, 1);
    baseNormal.z = sqrt(1 - dot(baseNormal.xy, baseNormal.xy));
    baseNormal = normalize(baseNormal);
    vec3 topNormal =vec3(topNormalCol.rg * 2 - 1, 1);
    topNormal.z = sqrt(1 - dot(topNormal.xy, topNormal.xy));
    topNormal = normalize(topNormal);
    topNormal = mix(vec3(0,0,1), topNormal, 1);
    topNormal = normalize(topNormal);

    vec3 mixNormal = vec3(baseNormal.rg + topNormal.rg, baseNormal.z * topNormal.z);
    //mixNormal = mix(baseNormal, topNormal, 1);
    mixNormal = normalize(mixNormal);


    //vec4 newMainColor = vec4(max(mianColor.rgb, specGloss.rgb), mianColor.a);

    vec4 newMainColor = vec4((mixNormal.rg) * 0.5 + 0.5, baseNormalCol.b, baseNormalCol.a);

    imageStore(OutImg, texelPos, newMainColor);

}