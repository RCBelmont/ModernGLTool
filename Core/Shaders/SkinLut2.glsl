#version 440
layout (local_size_x = 16, local_size_y = 16) in;
layout(binding=0, rgba32f) uniform image2D dstTex;


vec3 kernel(vec3 a, vec3 c, vec3 x){
    return a* exp((-x*x) /(c*c));
}

float loop_pos(int pos){
    if (pos < 0){
        return abs(pos);
    }
    if (pos>255){
        return 255*2-pos;
    }
    return pos;
}
const float diffusionSigmas[] = { 0.080f, 0.220f, 0.432f, 0.753f, 1.411f, 2.722f };
const float diffusionWeightsR[] = { 0.233f, 0.100f, 0.118f, 0.113f, 0.358f, 0.078f };
const float diffusionWeightsG[] = { 0.455f, 0.336f, 0.198f, 0.007f, 0.004f, 0.000f };
const float diffusionWeightsB[] = { 0.649f, 0.344f, 0.000f, 0.007f, 0.000f, 0.000f };
vec3 EvaluateDiffusionProfile(float x)// x in millimeters
{
    vec3 color = vec3(0);

    for (int i = 0; i < 6; ++i)
    {
        const float rsqrtTwoPi = 0.39894228f;
        float sigma = diffusionSigmas[i];
        float gaussian = (rsqrtTwoPi / sigma) * exp(-0.5f * (x*x) / (sigma*sigma));

        color.x += diffusionWeightsR[i] * gaussian;
        color.y += diffusionWeightsG[i] * gaussian;
        color.z += diffusionWeightsB[i] * gaussian;
    }
    return color;
}


void main()
{
      ivec2 size = imageSize(dstTex);

    float m_diffusionRadius = 2.7;
    float m_shadowSharpening = 10.0;
    float m_shadowWidthMax = 100.0;
    float m_shadowWidthMin = 8.0;

    float diffusionRadiusFactor = m_diffusionRadius / 2.7f;

	float shadowRcpWidthMin = diffusionRadiusFactor / m_shadowWidthMax;
	float shadowRcpWidthMax = diffusionRadiusFactor / m_shadowWidthMin;
	float shadowScale = (shadowRcpWidthMax - shadowRcpWidthMin) / float(size.y);
	float shadowBias = shadowRcpWidthMin + 0.5f * shadowScale;



    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);

    float u = (texelPos.x + 0.5f)/float(size.x);
    float inputPos = (sqrt(u) - sqrt(1-u)) * 0.5 + 0.5;
    float rcpWidth = float(texelPos.y) * shadowScale + shadowBias;
    const int cIter = 200;
    vec3 out_color = vec3(0, 0, 0);
    float iterScale = 20.0f / float(cIter);
    float iterBias = -10.0f + 0.5f * iterScale;

    for (int iIter = 0; iIter < cIter; ++iIter)
    {
        float delta = float(iIter) * iterScale + iterBias;
        vec3 rgbDiffusion;
        rgbDiffusion = EvaluateDiffusionProfile(delta);

        // Use smoothstep as an approximation of the transfer function of a
        // disc or Gaussian filter.
        float newPos = (inputPos + delta * rcpWidth) * m_shadowSharpening +
        (-0.5f * m_shadowSharpening + 0.5f);
        float newPosClamped = min(max(newPos, 0.0f), 1.0f);
        float newShadow = (3.0f - 2.0f * newPosClamped) * newPosClamped * newPosClamped;

        out_color.x += newShadow * rgbDiffusion.x;
        out_color.y += newShadow * rgbDiffusion.y;
        out_color.z += newShadow * rgbDiffusion.z;
    }

    // Scale sum of samples to get value of integral.  Also hack in a
    // fade to ensure the left edge of the image goes strictly to zero.
    float scale = 20.0f / float(cIter);
    if (texelPos.x * 25 < size.x)
    {
       // scale *= min(25.0f * float(texelPos.x) / float(size.x), 1.0f);
    }
    out_color.x *= scale;
    out_color.y *= scale;
    out_color.z *= scale;

    // Clamp to [0, 1]
    out_color.x = min(max(out_color.x, 0.0f), 1.0f);
    out_color.y = min(max(out_color.y, 0.0f), 1.0f);
    out_color.z = min(max(out_color.z, 0.0f), 1.0f);
    //out_color = vec4(nol_clamp.xxx, 1);
    imageStore(dstTex, texelPos, vec4(out_color,1));
}