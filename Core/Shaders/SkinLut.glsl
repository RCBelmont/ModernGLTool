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


void main()
{
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
    ivec2 size = imageSize(dstTex);

    float nol = (1.0*texelPos.x/size.x -0.5) * 2;
    float nol_clamp = clamp(nol, 0, 1);
    nol_clamp = pow(nol_clamp,1.0);

    float opacity = 1.0*texelPos.y/size.y;
    float trans = mix(0.2, 0.95, pow(opacity,1.3));

    vec3 diff_acc = vec3(0);
//    for (int i=-255; i <= 255; i++) {
//
//        float cpos = loop_pos(texelPos.x + i);
//        float delta = 2.0/255.0;
//        float nol_cpos = (1.0*cpos.x/size.x -0.5) * 2;
//        float nol_clamp_cpos = clamp(nol_cpos, 0, 1);
//        vec3 factor = vec3(0.2, 0.2, 0.2)*0.5;
//        vec3 en = vec3(1.0,1.0,1.0);
//
//        float t = i/255.0;
//        factor = kernel(vec3(1.0),factor,vec3(t));
//        en = factor * abs(i/254.0);
//
//        //nol_clamp_cpos = pow(nol_clamp_cpos,3);
//        diff_acc += nol_clamp_cpos*en;
//    }
    float pos = (1.0-1.0*texelPos.x/(size.x-1)) - 0.0;
    pos = max(pos, 0);
    diff_acc = kernel(vec3(1,0.98,0.95)*0.95, vec3(0.82,0.75,0.78)*0.80, vec3(pos))*trans;
    vec4 out_color = vec4(diff_acc + nol_clamp * (1-trans), 1);
    out_color = pow(out_color, mix(vec4(1.5),vec4(2.2), pow(opacity, 1)));
    //out_color = vec4(nol_clamp.xxx, 1);
    imageStore(dstTex, texelPos, out_color);
}